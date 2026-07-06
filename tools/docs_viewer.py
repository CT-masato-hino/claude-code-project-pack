#!/usr/bin/env python3
"""docs/ 配下をブラウズする人間レビュー用ローカルWebビューア。

ファイル管理アプリ風UI（左: ツリー / 右: プレビュー）で、Markdownはレンダリング表示
（Mermaid対応）、HTML成果物（モック・計画図・スライド）はそのままレンダリングする。
ビューアは読み取り専用。正本はあくまで docs/ 配下の Markdown / HTML（二重正本を作らない）。

使い方:
  ローカル起動（デフォルト: ./docs を 127.0.0.1:8765 で配信）
    python3 tools/docs_viewer.py
    python3 tools/docs_viewer.py --root docs --port 8765

  GitHub Pages 向け静的ビルド（allowlist 必須・デフォルト非公開）
    python3 tools/docs_viewer.py --build --allowlist docs/publish-allowlist.txt --out site

  allowlist の書式: 1行1パターン（root からの相対グロブ）。# はコメント。
    例)
      # 顧客レビュー用に公開してよいものだけを明示する
      basic-design/mockups/*.html
      requirements/functional-list.md

公開統制（重要）: docs/ には個人情報・顧客情報・秘密情報が含まれうる。
静的ビルドは allowlist に明示されたファイルだけを含める（allowlist なしではビルド不可）。
Markdown / Mermaid のレンダリングに CDN（jsdelivr の marked / mermaid）を使うため、
プレビューにはネットワーク接続が必要（文書内容自体が外部送信されることはない）。
"""

import argparse
import fnmatch
import json
import mimetypes
import shutil
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote, urlparse

VIEW_EXTS = {
    ".md", ".markdown", ".html", ".htm", ".svg", ".png", ".jpg", ".jpeg",
    ".gif", ".webp", ".pdf", ".csv", ".txt", ".mmd",
}

INDEX_HTML = r"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>docs viewer</title>
<style>
  :root { --line:#d8dde8; --bg:#f4f6fa; --ink:#1a2233; --sub:#5a6478; --accent:#2456a6; --sel:#e8f0fe; }
  * { box-sizing:border-box; }
  body { margin:0; height:100vh; display:flex; flex-direction:column; color:var(--ink);
         font-family:"Hiragino Sans","Noto Sans JP","Yu Gothic",sans-serif; }
  header { padding:10px 16px; border-bottom:1px solid var(--line); background:#fff;
           display:flex; align-items:baseline; gap:12px; }
  header h1 { font-size:15px; margin:0; }
  header .sub { font-size:12px; color:var(--sub); }
  main { flex:1; display:flex; min-height:0; }
  #tree { width:300px; min-width:200px; overflow:auto; border-right:1px solid var(--line);
          background:var(--bg); padding:8px 0; font-size:13px; }
  #view { flex:1; overflow:auto; background:#fff; }
  .dir > .label { font-weight:600; color:var(--sub); cursor:pointer; }
  .dir > .label::before { content:"▸ "; }
  .dir.open > .label::before { content:"▾ "; }
  .dir > .children { display:none; }
  .dir.open > .children { display:block; }
  .node { padding:3px 8px 3px 0; }
  .indent { padding-left:16px; }
  .file { cursor:pointer; border-radius:4px; padding:3px 8px; }
  .file:hover { background:#e9edf5; }
  .file.selected { background:var(--sel); color:var(--accent); font-weight:600; }
  .file .ext { color:var(--sub); font-size:11px; margin-left:4px; }
  #content { max-width:900px; margin:0 auto; padding:32px 40px; line-height:1.75; }
  #content h1,#content h2,#content h3 { line-height:1.4; }
  #content h1 { border-bottom:1px solid var(--line); padding-bottom:6px; }
  #content table { border-collapse:collapse; font-size:14px; }
  #content th,#content td { border:1px solid var(--line); padding:6px 10px; }
  #content th { background:#eef1f7; }
  #content pre { background:#f0f2f7; padding:12px; border-radius:6px; overflow:auto; font-size:13px; }
  #content code { background:#f0f2f7; padding:1px 4px; border-radius:3px; font-size:0.9em; }
  #content pre code { background:none; padding:0; }
  #content img { max-width:100%; }
  #content blockquote { border-left:4px solid var(--line); margin-left:0; padding-left:14px; color:var(--sub); }
  iframe.htmlview { width:100%; height:100%; border:0; }
  .placeholder { color:var(--sub); padding:40px; text-align:center; }
  .crumb { font-size:12px; color:var(--sub); padding:8px 16px; border-bottom:1px solid var(--line);
           background:#fafbfd; position:sticky; top:0; }
</style>
</head>
<body>
<header>
  <h1>📁 docs viewer</h1>
  <span class="sub">レビュー用ビューア（読み取り専用・正本は docs/ 配下のファイル）</span>
</header>
<main>
  <nav id="tree"></nav>
  <section id="view"><div class="placeholder">左のツリーからファイルを選択してください</div></section>
</main>
<script src="https://cdn.jsdelivr.net/npm/marked@12/marked.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
const CONFIG = __CONFIG__;
mermaid.initialize({ startOnLoad: false, securityLevel: "strict" });

function el(tag, cls, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text) e.textContent = text;
  return e;
}

function buildTree(node, container, depth) {
  (node.dirs || []).forEach(d => {
    const wrap = el("div", "dir node indent" + (depth < 1 ? " open" : ""));
    const label = el("div", "label", d.name);
    label.onclick = () => wrap.classList.toggle("open");
    wrap.appendChild(label);
    const children = el("div", "children");
    wrap.appendChild(children);
    buildTree(d, children, depth + 1);
    container.appendChild(wrap);
  });
  (node.files || []).forEach(f => {
    const item = el("div", "file node indent", f.name);
    item.dataset.path = f.path;
    item.onclick = () => select(item, f.path);
    container.appendChild(item);
  });
}

function select(item, path) {
  document.querySelectorAll(".file.selected").forEach(x => x.classList.remove("selected"));
  if (item) item.classList.add("selected");
  render(path);
}

async function render(path) {
  const view = document.getElementById("view");
  const url = CONFIG.rawBase + path.split("/").map(encodeURIComponent).join("/");
  const ext = path.slice(path.lastIndexOf(".")).toLowerCase();
  view.innerHTML = "";
  view.appendChild(Object.assign(el("div", "crumb"), { textContent: path }));
  if (ext === ".html" || ext === ".htm" || ext === ".pdf") {
    const frame = el("iframe", "htmlview");
    frame.src = url;
    view.appendChild(frame);
    view.style.overflow = "hidden";
    return;
  }
  view.style.overflow = "auto";
  const content = el("div");
  content.id = "content";
  view.appendChild(content);
  if ([".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp"].includes(ext)) {
    const img = el("img");
    img.src = url;
    content.appendChild(img);
    return;
  }
  const res = await fetch(url);
  if (!res.ok) { content.textContent = "読み込みに失敗しました: " + res.status; return; }
  const text = await res.text();
  if (ext === ".md" || ext === ".markdown" || ext === ".mmd" || ext === ".txt" || ext === ".csv") {
    if (ext === ".txt" || ext === ".csv") {
      const pre = el("pre", null, text);
      content.appendChild(pre);
      return;
    }
    const src = ext === ".mmd" ? "```mermaid\n" + text + "\n```" : text;
    content.innerHTML = marked.parse(src);
    const blocks = content.querySelectorAll("pre code.language-mermaid");
    let i = 0;
    for (const code of blocks) {
      const div = el("div", "mermaid");
      div.id = "mmd-" + (i++);
      div.textContent = code.textContent;
      code.closest("pre").replaceWith(div);
    }
    if (i > 0) { try { await mermaid.run({ querySelector: ".mermaid" }); } catch (e) { console.warn(e); } }
  }
}

fetch(CONFIG.treeUrl).then(r => r.json()).then(tree => {
  const nav = document.getElementById("tree");
  buildTree(tree, nav, 0);
  // 計画図があればトップページとして開く
  const plan = document.querySelector('.file[data-path="project-plan.html"]');
  if (plan) select(plan, "project-plan.html");
});
</script>
</body>
</html>
"""


def build_tree(root: Path, allow=None):
    """root 配下の表示対象ファイルをツリー（dict）にする。allow は相対パスの許可判定関数。"""

    def walk(d: Path):
        node = {"name": d.name, "dirs": [], "files": []}
        try:
            entries = sorted(d.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        except PermissionError:
            return node
        for p in entries:
            if p.name.startswith("."):
                continue
            if p.is_dir():
                child = walk(p)
                if child["dirs"] or child["files"]:
                    node["dirs"].append(child)
            elif p.suffix.lower() in VIEW_EXTS:
                rel = p.relative_to(root).as_posix()
                if allow is None or allow(rel):
                    node["files"].append({"name": p.name, "path": rel})
        return node

    return walk(root)


def safe_resolve(root: Path, rel: str):
    """パストラバーサルを防いで root 配下の実ファイルを返す。範囲外は None。"""
    target = (root / rel).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        return None
    return target if target.is_file() else None


def make_handler(root: Path):
    index = INDEX_HTML.replace("__CONFIG__", json.dumps({"treeUrl": "/api/tree", "rawBase": "/raw/"}))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802 (http.server の規約)
            path = unquote(urlparse(self.path).path)
            if path in ("/", "/index.html"):
                self._send(200, "text/html; charset=utf-8", index.encode("utf-8"))
            elif path == "/api/tree":
                body = json.dumps(build_tree(root), ensure_ascii=False).encode("utf-8")
                self._send(200, "application/json; charset=utf-8", body)
            elif path.startswith("/raw/"):
                target = safe_resolve(root, path[len("/raw/"):])
                if target is None:
                    self._send(404, "text/plain; charset=utf-8", b"not found")
                    return
                ctype = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
                if ctype.startswith("text/") or ctype in ("application/json",):
                    ctype += "; charset=utf-8"
                self._send(200, ctype, target.read_bytes())
            else:
                self._send(404, "text/plain; charset=utf-8", b"not found")

        def _send(self, code, ctype, body):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            # ローカルレビュー用。キャッシュで古い成果物を見せない
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, fmt, *args):
            sys.stderr.write("[docs-viewer] %s\n" % (fmt % args))

    return Handler


def serve(root: Path, host: str, port: int):
    httpd = HTTPServer((host, port), make_handler(root))
    print(f"docs viewer: http://{host}:{port}/  (root: {root})")
    print("停止は Ctrl+C")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


def load_allowlist(path: Path):
    patterns = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            patterns.append(line)
    return patterns


def build_site(root: Path, out: Path, allowlist: Path):
    """GitHub Pages 向け静的サイトを生成する。allowlist に一致するファイルのみ含める。"""
    patterns = load_allowlist(allowlist)
    if not patterns:
        print("エラー: allowlist が空です。公開してよい成果物を明示してください（デフォルト非公開）。", file=sys.stderr)
        return 1

    def allow(rel: str):
        return any(fnmatch.fnmatch(rel, pat) for pat in patterns)

    tree = build_tree(root, allow=allow)

    def collect(node, acc):
        for f in node["files"]:
            acc.append(f["path"])
        for d in node["dirs"]:
            collect(d, acc)
        return acc

    files = collect(tree, [])
    if not files:
        print("エラー: allowlist に一致するファイルがありません。ビルドを中止します。", file=sys.stderr)
        return 1

    out.mkdir(parents=True, exist_ok=True)
    for rel in files:
        dst = out / "files" / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / rel, dst)
    (out / "tree.json").write_text(json.dumps(tree, ensure_ascii=False), encoding="utf-8")
    index = INDEX_HTML.replace("__CONFIG__", json.dumps({"treeUrl": "tree.json", "rawBase": "files/"}))
    (out / "index.html").write_text(index, encoding="utf-8")

    print(f"静的サイトを生成しました: {out}（{len(files)}ファイル）")
    print("含めたファイル:")
    for rel in files:
        print(f"  - {rel}")
    print("\n公開前チェック: 上記に個人情報・顧客情報・秘密情報が含まれていないか必ず目視確認すること。")
    print("private リポジトリの Pages 可視性設定（公開範囲）にも注意。")
    return 0


def main():
    ap = argparse.ArgumentParser(description="docs/ レビュー用ローカルWebビューア")
    ap.add_argument("--root", default="docs", help="表示対象ディレクトリ（デフォルト: docs）")
    ap.add_argument("--host", default="127.0.0.1", help="バインド先（デフォルト: 127.0.0.1）")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--build", action="store_true", help="GitHub Pages 向け静的ビルド")
    ap.add_argument("--out", default="site", help="ビルド出力先（デフォルト: site）")
    ap.add_argument("--allowlist", help="公開ファイルのallowlist（--build 時は必須）")
    args = ap.parse_args()

    root = Path(args.root)
    if not root.is_dir():
        print(f"エラー: root が見つかりません: {root}", file=sys.stderr)
        return 1

    if args.build:
        if not args.allowlist:
            print("エラー: --build には --allowlist が必須です（公開してよい成果物の明示。デフォルト非公開）。", file=sys.stderr)
            return 1
        allowlist = Path(args.allowlist)
        if not allowlist.is_file():
            print(f"エラー: allowlist が見つかりません: {allowlist}", file=sys.stderr)
            return 1
        return build_site(root, Path(args.out), allowlist)

    serve(root, args.host, args.port)
    return 0


if __name__ == "__main__":
    sys.exit(main())
