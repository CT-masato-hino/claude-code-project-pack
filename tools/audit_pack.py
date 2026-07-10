#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""パック整合性監査（CI用）。

検査項目:
  1. 数量整合   — READMEの記載数（エージェント/スキル）と実ファイル数の一致
  2. 参照整合   — docs/standards/*.md への参照・スキル参照・エージェント名参照の実在
  3. 混入検査   — 絶対ローカルパス・メールアドレス・シークレットらしき文字列・任意キーワード

使い方:
  python3 tools/audit_pack.py            # リポジトリルートで実行（exit 1 = 問題あり）
  AUDIT_KEYWORDS="社名,個人名" python3 tools/audit_pack.py   # 追加の混入検査ワード（カンマ区切り）
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
issues = []

# 実行時に生成される（パックには同梱されない）ことが仕様のファイル参照
RUNTIME_ARTIFACTS = {"effort-map.md"}
# 環境が提供する外部スキル・名前空間（パック外だが参照してよいもの）
# project-pack はプラグイン導入時のスキル名前空間（.claude-plugin/plugin.json の name）
EXTERNAL_SKILLS = {"design-sync", "design-login", "code-review", "update-config", "loop", "project-pack"}

agents = sorted((ROOT / ".claude/agents").glob("*.md"))
skills = sorted((ROOT / ".claude/skills").glob("*/SKILL.md"))
standards = sorted((ROOT / "docs/standards").glob("*.md"))
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
    for m in re.finditer(r"docs/standards/([\w-]+\.md)", text):
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
leak_patterns = [
    (r"/Users/[a-zA-Z0-9_.-]+/", "ローカル絶対パス"),
    (r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+", "メールアドレス"),
    (r"\b(AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20,}|sk-ant-[A-Za-z0-9-]{20,})\b", "シークレットらしき文字列"),
]
extra_keywords = [k.strip() for k in os.environ.get("AUDIT_KEYWORDS", "").split(",") if k.strip()]
scan_targets = dict(texts)
for f in ROOT.rglob("*.html"):
    if ".git" not in f.parts:
        scan_targets[f] = f.read_text(encoding="utf-8")
for f, text in scan_targets.items():
    rel = f.relative_to(ROOT)
    for pat, label in leak_patterns:
        for m in re.finditer(pat, text):
            issues.append("混入検査 %s: '%s' (in %s)" % (label, m.group(0)[:40], rel))
    for kw in extra_keywords:
        if kw.lower() in text.lower():
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
