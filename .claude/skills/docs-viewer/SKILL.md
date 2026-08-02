---
name: docs-viewer
description: docs/レビュー用ローカルWebビューア（tools/docs_viewer.py）の起動・停止・静的ビルド。「ビューアを開いて」「docsを見たい」「モック/図を確認したい」で使う。一度閉じた後の再起動もこのスキル一発でよい（起動コマンドを覚える必要はない）。
---

# docs-viewer スキル

`tools/docs_viewer.py`（docs/ レビュー用ローカルWebビューア）の起動・停止・静的ビルドを代行する。
人間がコマンドを覚えていなくても「ビューアを開いて」で開ける状態にするのが目的。

## 起動（デフォルト動作）

1. 既に起動していないか確認する: `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8765/`
   - `200` が返れば起動済み。URLだけ案内して終了する
2. 起動していなければバックグラウンドで起動する:
   ```bash
   python3 tools/docs_viewer.py          # ./docs を 127.0.0.1:8765 で配信
   ```
   （Claude Code からは Bash の run_in_background で起動し、curl で 200 を確認してから案内する）
3. ユーザーへの案内は必ず次の3点をセットで返す:
   - 閲覧URL: **http://127.0.0.1:8765/**
   - 再起動のしかた: 「`/docs-viewer` と打つだけ」（コマンドを覚えなくてよいことを明示）
   - 停止のしかた: 「ビューアを止めて」と依頼するか、起動したターミナルで Ctrl+C

## 停止

`lsof -ti :8765 | xargs kill` で停止する（ポートを変えて起動した場合はそのポートで）。

## トラブル時

- ポート衝突（8765 が別プロセス）: `python3 tools/docs_viewer.py --port 8766` のように空きポートで起動し、案内URLも合わせて変える
- 「root が見つかりません」: リポジトリ直下（`docs/` がある場所）で実行しているか確認する
- Markdown/Mermaid のレンダリングには CDN（jsdelivr）への接続が必要（文書内容は外部送信されない）

## 静的ビルド（GitHub Pages 向け・任意）

公開は allowlist 必須のデフォルト非公開（公開統制は `tools/docs_viewer.py` の docstring を正とする）:

```bash
python3 tools/docs_viewer.py --build --allowlist docs/publish-allowlist.txt --out site
```

ビルド前に allowlist の中身（個人情報・顧客情報・秘密情報が含まれないこと）を人間に目視確認させる。
