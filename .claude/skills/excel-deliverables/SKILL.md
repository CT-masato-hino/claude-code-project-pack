---
name: excel-deliverables
description: Excel成果物変換。Markdown正本（設計書・テスト仕様書・課題管理表等）を納品用Excel体裁（表紙・変更履歴シート・罫線つき表・A4横印刷設定）に変換する。逆方向（顧客から戻ったExcelのMarkdown取り込み・差分確認）にも対応。納品前、顧客レビュー往復時に使う。
---

# Excel成果物変換スキル

正本は常にMarkdown（`docs/` 配下）で管理し、**Excelは「出力形式」として都度生成する**。このスキルは同梱スクリプトでその変換を行う。

## 大原則（二重管理の禁止）

- 正本はMarkdown。Excelを直接編集して正本と乖離させない
- 顧客がExcel上で修正・コメントした場合は、**逆変換→差分確認→正本(Markdown)へ反映→Excel再生成** のループを回す
- 生成したExcelは `deliverables/` 配下に置き、`docs/` には置かない（正本と納品物の分離）

## 同梱スクリプト

| スクリプト | 役割 |
|---|---|
| `scripts/md_to_excel.py` | Markdown → Excel納品体裁（表紙・変更履歴・シート分割・罫線・印刷設定） |
| `scripts/excel_to_md.py` | Excel → Markdown（顧客戻りの取り込み・差分確認用） |

前提: Python 3.9+ と openpyxl。openpyxlがない場合は `python3 -m pip install --user openpyxl`（PATHのpython3で入らなければ `/usr/bin/python3` を試す）。

## 手順1: 納品用Excelの生成（Markdown → Excel）

```bash
python3 .claude/skills/excel-deliverables/scripts/md_to_excel.py \
  docs/basic-design/screens/SCR-001.md \
  -o deliverables/YYYYMMDD/SCR-001_画面設計書.xlsx \
  --project "{{案件名}}" --author "{{作成者}}" --approver "{{承認者}}" \
  --doc-version "1.0" --font "游ゴシック"
```

- 複数ファイル一括: 入力を並べて `-o deliverables/YYYYMMDD/`（ディレクトリ指定）
- 変換ルール: H1=文書名 / H2=シート分割 / 表=罫線＋ヘッダー装飾 / `変更履歴` セクション=専用シート
- 1シートにまとめたい文書（議事録等）は `--single-sheet`
- フォント・版数・作成日はCLAUDE.mdの顧客標準に合わせて指定する

### 生成後の検品チェックリスト（必須）

- [ ] 表紙: 文書名・案件名・版数・作成日・作成者・承認欄が正しい
- [ ] 変更履歴シートが存在し、今回の版の行がある
- [ ] 表の列ズレ・文字切れがない（列幅上限で折返しになっているだけかを確認）
- [ ] 内部メモ・【要確認】マーカー・AI痕跡が残っていない（残っていたら正本側を先に直す）
- [ ] シート名が文字化け・連番化（`_2`）していない
- [ ] 印刷プレビュー相当の確認: A4横・1ページ幅に収まる設定になっている

## 手順2: 顧客戻りExcelの取り込み（Excel → Markdown）

```bash
# 1. 逆変換
python3 .claude/skills/excel-deliverables/scripts/excel_to_md.py \
  受領物/SCR-001_画面設計書_顧客修正.xlsx -o /tmp/scr-001-returned.md

# 2. 正本との差分確認（変更点の洗い出し）
diff docs/basic-design/screens/SCR-001.md /tmp/scr-001-returned.md
```

- 差分は機械的に正本へ上書きせず、1件ずつ判定する:
  - 誤字修正・表現修正 → そのまま正本へ反映
  - **仕様変更に相当する修正** → requirements-analyst の影響分析（AC・テストへの波及）を経てから反映。契約影響があれば leader → 人間へ
  - コメント・質問 → `docs/open-questions.md` に起票
- 反映後は変更履歴を更新し、Excelを再生成して次版として提出する

## 顧客標準の様式が指定されている場合

顧客Excelテンプレート（会社ロゴ・独自ヘッダー等）に完全一致が求められる場合、汎用スクリプトでは体裁が合わないことがある:

1. 顧客テンプレートを `docs/customer-standard/templates/` に保存する
2. `md_to_excel.py` をコピーして案件用に改造する（`build_cover` と体裁定数の差し替えが中心）
3. 改造版は `.claude/skills/excel-deliverables/scripts/md_to_excel_<顧客名>.py` として保存し、テーラリング記録に残す
4. セル単位の完全一致が必要な帳票的様式は、無理に自動化せず「表データ部分のみ自動・枠は手動」の分担を提案する

## エージェント連携

| 状況 | 連携先 |
|---|---|
| 変換前の正本の体裁整備（版数・変更履歴） | documentation-specialist |
| 納品一式としての突合 | /delivery-package のフローに組み込む |
| 顧客戻りが仕様変更を含む | requirements-analyst → leader |
| 秘密情報の混入チェック | security-compliance（生成後のExcelも検査対象） |

## 完了条件

- 生成Excelが検品チェックリストを全件通過している
- 顧客戻り取り込みの場合: 全差分に判定（反映/影響分析行き/起票）が付いている
- 正本とExcelの版数が一致している
