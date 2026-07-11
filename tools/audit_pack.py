#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""パック整合性監査（CI用）。

検査項目:
  1. 数量整合   — READMEの記載数（エージェント/スキル）と実ファイル数の一致
  2. 参照整合   — docs/90-pack/standards/*.md への参照・スキル参照・エージェント名参照の実在
  3. 混入検査   — ローカルパス（先頭スラッシュなしの Users/... 形式も対象）・メールアドレス・
                  シークレットらしき文字列・任意キーワード。エビデンス類（*.log / *.txt）も対象

使い方:
  python3 tools/audit_pack.py            # リポジトリルートで実行（exit 1 = 問題あり）
  AUDIT_KEYWORDS="社名,個人名" python3 tools/audit_pack.py   # 追加の混入検査ワード（カンマ区切り）
  AUDIT_ALLOWLIST="CT-masato-hino" ...   # キーワード検査から除外する公開情報（GitHubアカウント名等の
                                         # false positive 回避。カンマ区切り）

導入先の運用: /project-init フェーズ4で AUDIT_KEYWORDS に開発者名・OSユーザー名を必ず登録する
（成果物の人物表記はロールIDが正。実名・ローカルパスの混入は本監査で検出する）。
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
issues = []

# 実行時に生成される（パックには同梱されない）ことが仕様のファイル参照
# （案件生成物は v2.0.0 で docs/90-pack/standards/ の外へ移動したため現在は空）
RUNTIME_ARTIFACTS = set()
# 環境が提供する外部スキル・名前空間（パック外だが参照してよいもの）
# project-pack はプラグイン導入時のスキル名前空間（.claude-plugin/plugin.json の name）
EXTERNAL_SKILLS = {"design-sync", "design-login", "code-review", "update-config", "loop", "project-pack"}

agents = sorted((ROOT / ".claude/agents").glob("*.md"))
skills = sorted((ROOT / ".claude/skills").glob("*/SKILL.md"))
standards = sorted((ROOT / "docs/90-pack/standards").glob("*.md"))
agent_names = {a.stem for a in agents}
skill_names = {s.parent.name for s in skills}
std_names = {s.name for s in standards}

texts = {}
for f in list(ROOT.rglob("*.md")) + [ROOT / ".mcp.json.template", ROOT / "CLAUDE.md.template"]:
    if f.is_file() and ".git" not in f.parts and "node_modules" not in f.parts and f.name != "CLAUDE.local.md":
        texts[f] = f.read_text(encoding="utf-8")

# ---- 1. 数量整合 ----
readme = texts.get(ROOT / "README.md", "")
for pat, actual, label in [
    (r"サブエージェント(\d+)体", len(agents), "エージェント数"),
    (r"スキル(\d+)個", len(skills), "スキル数"),
]:
    for m in re.finditer(pat, readme):
        if int(m.group(1)) != actual:
            issues.append("README %s不一致: 記載=%s 実際=%d" % (label, m.group(1), actual))

# ---- 1b. 版数整合（README ↔ CHANGELOG） ----
changelog = texts.get(ROOT / "CHANGELOG.md", "")
m_readme = re.search(r"現在のバージョン: \*\*([\d.]+)\*\*", readme)
m_cl = re.search(r"^## \[([\d.]+)\]", changelog, re.M)
if m_readme and m_cl and m_readme.group(1) != m_cl.group(1):
    issues.append("版数不一致: README=%s CHANGELOG最新=%s" % (m_readme.group(1), m_cl.group(1)))
elif not (m_readme and m_cl):
    issues.append("版数表記が見つからない: README=%s CHANGELOG=%s" % (bool(m_readme), bool(m_cl)))

# ---- 1c. 版数・数量整合（プラグインマニフェスト） ----
pj_path = ROOT / ".claude-plugin/plugin.json"
if pj_path.is_file():
    pdata = json.loads(pj_path.read_text(encoding="utf-8"))
    pv = pdata.get("version")
    if m_readme and pv != m_readme.group(1):
        issues.append("版数不一致: plugin.json=%s README=%s" % (pv, m_readme.group(1)))
    # agents はファイル列挙が必要な仕様のため、実ファイルとの同期を検査する
    listed = {Path(p).name for p in pdata.get("agents", [])}
    actual = {a.name for a in agents}
    for n in sorted(actual - listed):
        issues.append("plugin.json agents に未掲載: %s" % n)
    for n in sorted(listed - actual):
        issues.append("plugin.json agents に実在しないファイル: %s" % n)
mp_path = ROOT / ".claude-plugin/marketplace.json"
if mp_path.is_file():
    mp_text = mp_path.read_text(encoding="utf-8")
    for pat, actual, label in [
        (r"サブエージェント(\d+)体", len(agents), "エージェント数"),
        (r"スキル(\d+)個", len(skills), "スキル数"),
    ]:
        for m in re.finditer(pat, mp_text):
            if int(m.group(1)) != actual:
                issues.append("marketplace.json %s不一致: 記載=%s 実際=%d" % (label, m.group(1), actual))

# ---- 2. 参照整合 ----
for f, text in texts.items():
    rel = f.relative_to(ROOT)
    for m in re.finditer(r"docs/90-pack/standards/([\w-]+\.md)", text):
        name = m.group(1)
        if name not in std_names and name not in RUNTIME_ARTIFACTS:
            issues.append("実在しない標準への参照: %s (in %s)" % (name, rel))
    for m in re.finditer(r"[`（(/ ]/([a-z][a-z]+(?:-[a-z]+)+)\b", text):
        s = m.group(1)
        if s not in skill_names and s not in EXTERNAL_SKILLS:
            issues.append("未定義スキル参照?: /%s (in %s)" % (s, rel))
    for m in re.finditer(r"\b([a-z]+(?:-[a-z]+)+)\b", text):
        name = m.group(1)
        if name.endswith(("-coder", "-specialist", "-analyst", "-reviewer", "-guardian",
                          "-compliance", "-performance", "-engineer", "-responder",
                          "-modernizer", "-designer", "-standardizer")) \
                and name not in agent_names \
                and not name.startswith(("backend-coder-", "frontend-coder-")):
            issues.append("実在しないエージェント参照?: %s (in %s)" % (name, rel))

# ---- 3. 混入検査 ----
# ローカルパスは先頭スラッシュなし（スタックトレースの "(Users/xxx/..." 形式）も検出する
leak_patterns = [
    (r"\bUsers/[a-zA-Z0-9_.-]+/", "ローカルパス"),
    (r"\bhome/[a-zA-Z0-9_.-]+/", "ローカルパス"),
    (r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+", "メールアドレス"),
    (r"\b(AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20,}|sk-ant-[A-Za-z0-9-]{20,})\b", "シークレットらしき文字列"),
]


def is_package_version(match: str) -> bool:
    """npm等の package@version 表記（marked@12, pkg@^1.2.3 等）をメール検知から除外する。"""
    domain = match.rsplit("@", 1)[-1]
    return re.fullmatch(r"[\d.^~x*-]+", domain) is not None


extra_keywords = [k.strip() for k in os.environ.get("AUDIT_KEYWORDS", "").split(",") if k.strip()]
# 公開情報（GitHubアカウント名等）はキーワード検査から除外して false positive を防ぐ
allow_terms = [a.strip() for a in os.environ.get("AUDIT_ALLOWLIST", "").split(",") if a.strip()]
scan_targets = dict(texts)
# エビデンス類（*.log / *.txt）・HTMLも混入検査の対象にする（テスト実行ログへのパス混入が実例）
for pattern in ("*.html", "*.log", "*.txt"):
    for f in ROOT.rglob(pattern):
        if f.is_file() and ".git" not in f.parts and "node_modules" not in f.parts:
            scan_targets[f] = f.read_text(encoding="utf-8", errors="replace")
for f, text in scan_targets.items():
    rel = f.relative_to(ROOT)
    for pat, label in leak_patterns:
        for m in re.finditer(pat, text):
            if label == "メールアドレス" and is_package_version(m.group(0)):
                continue
            issues.append("混入検査 %s: '%s' (in %s)" % (label, m.group(0)[:40], rel))
    if extra_keywords:
        scan_text = text
        for allow in allow_terms:
            scan_text = scan_text.replace(allow, "")
        for kw in extra_keywords:
            if kw.lower() in scan_text.lower():
                issues.append("混入検査 キーワード '%s' (in %s)" % (kw, rel))

# ---- 結果 ----
print("agents=%d skills=%d standards=%d 検査ファイル=%d" % (
    len(agents), len(skills), len(standards), len(scan_targets)))
uniq = sorted(set(issues))
if uniq:
    print("\n検出事項 %d件:" % len(uniq))
    for i in uniq:
        print(" - " + i)
    sys.exit(1)
print("検出事項: なし")
