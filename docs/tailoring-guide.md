# テーラリングガイド

共通フレームの思想通り、**本パックはそのまま使わずに案件ごとに削る・足す**ことを前提とする。
テーラリングの結果は CLAUDE.md に記録し、「なぜ削ったか」を残すこと（監査・引き継ぎ対応）。

> **通常は `/project-init` スキルを実行すれば本ガイドの内容は対話フローで適用される。**
> 本ガイドはその決定表の背景説明と、手動テーラリング時のリファレンス。

## 1. 案件規模別の推奨構成

### 小規模（〜3人月、画面数〜10）
- **コア（残す）**: leader / backend-coder / frontend-coder / code-reviewer / data-model-specialist / documentation-specialist
- **統合する**: requirements-analyst と test-engineer の役割はメインセッション＋スキルで代替可
  （/requirements-definition と /test-planning は残す。スキルは軽いので削らない）
- **削る**: infra-coder（インフラが定型なら）、quality-performance（性能要件が緩ければ。
  **削る場合はQ-04/Q-08の担保先をcode-reviewerへ付け替える** — 担保者が空席の基準を作らない）、
  estimation-specialist / business-process-analyst（メインセッション＋leaderで代替）、
  ai-dev-standardizer（初案件はleaderに統合可。ただしAI駆動開発を組織展開するなら2案件目から必須）
- **QCD運用の軽量化**: 小規模ではQCD週次レポートを「工程末＋隔週」に減らしてよい（基準そのものは削らない。
  計測頻度のテーラリングとして qcd-standards の記録表に残す）
- **案件特性で選ぶ**: batch-specialist（バッチがあるなら残す）/ report-specialist（帳票があるなら残す）/
  migration-specialist・legacy-modernizer（リプレースなら必須、新規開発なら削除）/
  ui-ux-designer（UIを持ち専任デザイナーがいるなら残す。専任デザイナー不在ならfrontend-coder＋basic-designの原則チェックリスト直接適用に統合して削る）
- **絶対に削らない**: /context-history（小規模でも引き継ぎは発生する）、data-model-specialist（DBがあるなら）

### 中規模（3〜20人月、複数ドメイン）
- 全構成をそのまま使う。これが本パックの基準サイズ
- 案件特性に無い領域だけ削る（帳票なし→report-specialist、移行なし→migration-specialist/legacy-modernizer、
  保守フェーズ未受託→incident-responderは総合テスト以降まで保留）
- 機能ドメインが多い場合、coder系を複製してドメイン専任化してよい
  （例: `backend-coder-auth.md` を作り「認証ドメイン専任。docs/basic-design/auth/ を熟知」と追記）

### 大規模（20人月〜、複数チーム）
- チーム（会社）境界ごとに本パックを複製し、リポジトリ分割する
- 横断エージェント（security / architecture / data-model / documentation / operations / incident）は
  **全チーム共通の定義を親リポジトリで一元管理**し、差分が出ないようにする
- api-designer をチーム間IFの正本管理者として常設する（IF紛争の予防）
- UIを持つ複数チーム構成では ui-ux-designer を全チーム共通のデザイン判断者として一元管理する
  （チームごとに複製しない。判断基準を一箇所に足せば全チームに同時に効くレバレッジを優先する）
- /context-history の頻度を週次→日次に上げる

## 2. 契約形態別の調整

| 項目 | 請負 | 準委任・ラボ |
|---|---|---|
| スコープ変更 | leader が必ず「契約影響あり」でエスカレーション | 記録して続行可 |
| 成果物の体裁 | deliverables-catalog を契約書の納品物リストに完全一致させる | 顧客と合意した最小セットに削る |
| 工程の完了条件 | 顧客承認記録を必須にする | チーム内レビューで可とできる |
| 曖昧要件の扱い | 実装前に必ず文書で確認（open-questions経由） | 仮実装→デモ確認のループも可 |

## 3. 顧客標準がある場合

1. 顧客の開発標準（工程名・成果物様式・レビュー規程）を `docs/customer-standard/` に配置する
2. 各スキルのテンプレート部分を顧客様式に差し替える（スキルの手順・完了条件は残す）
3. 工程名の読み替え表を CLAUDE.md に追記する（例: 顧客標準「外部設計」= 本パック「基本設計」）
4. 成果物カタログ（deliverables-catalog.md）を顧客の納品物リストで上書きする

## 4. 削ってはいけないもの（全案件共通）

- **コンテキスト汚染防止ルール一式**（CLAUDE.mdの該当節、/context-history、/context-health-check）
  — 削った瞬間から品質が劣化し、劣化に気づけなくなる
- **ERD変更のdata-model-specialist独占ルール** — データ不整合は後工程で最も高くつく
- **AC中心の要件定義** — テスト可能性が検収可能性に直結する
- **サブエージェントの「要約のみ報告」ルール** — 各エージェント定義の報告形式節を消さない

## 5. 足すことが多いもの

- 業種別のコンプライアンス観点（金融: FISC安全対策基準 / 医療: 3省2ガイドライン / 官公庁: 政府統一基準）
  → security-compliance の「法令・規程」節に追記する
- 顧客固有の用語集（`docs/glossary.md` を作り、requirements-analyst と documentation-specialist に参照させる）
- 帳票が多い案件: 帳票専門の設計テンプレート・帳票テスト観点
- 外部連携が多い案件: IF疎通試験の専用スキル

## 6. テーラリング記録テンプレート（CLAUDE.mdに追記）

```markdown
## テーラリング記録
| 日付 | 変更(追加/削除/変更) | 対象 | 理由 |
|---|---|---|---|
```
