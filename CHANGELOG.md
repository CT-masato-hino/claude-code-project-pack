# Changelog

本パックの変更履歴。形式は [Keep a Changelog](https://keepachangelog.com/ja/1.1.0/)、バージョニングは [Semantic Versioning](https://semver.org/lang/ja/) に従います。

このパックにおける互換性の解釈:

- **MAJOR** — 導入済み案件のテーラリングを壊す変更。エージェント・スキルの削除や改名、QCD基準IDの変更・削除、正本ドキュメントのパス変更
- **MINOR** — 後方互換のある追加。エージェント・スキル・標準ドキュメントの追加、既存定義へのチェック項目追加
- **PATCH** — 文言の修正、誤りの訂正、テンプレートやスクリプトのバグ修正

## [1.0.5] - 2026-07-07

1.0.4のUI刷新で使用した絵文字アイコンを撤去（ユーザーフィードバック対応）。UIアイコンはモノクロのインラインSVGに統一し、HTMLを生成する各スキルに絵文字禁止ルールを明記。

### Fixed
- **project-plan-template.html**: タイトルの📋を削除、現在地バナーの📍をアクセント色のSVGピンに置き換え
- **tools/docs_viewer.py**: ヘッダーの📁・空表示の🗂・ファイル種別の絵文字アイコン8種を、フェザー系モノクロSVG（stroke=currentColor、選択時はアクセント色に連動）に置き換え

### Added
- HTML成果物を生成する3スキルに「絵文字をアイコン・装飾に使わない（必要ならモノクロSVG/CSS図形）」ルールを明記: slide-deck（検品チェックリスト）・basic-design（モック生成）・project-init（計画HTML）

## [1.0.4] - 2026-07-07

報告・レビュー用HTMLの見た目を全面刷新（Backlog/Notion風のソフトなモダンUI: 白ベース・ソフトカラーのステータスチップ・角丸カード・縦罫線なしテーブル）。機能・クラス名・プレースホルダ・生成手順は不変（後方互換）。

### Changed
- **project-plan-template.html**: 工程フローを等幅グリッドのカード＋ステータスチップ（完了=緑/進行中=青/未着手=灰）に、現在地バナーをコールアウトブロックに、表を縦罫線なしの角丸カードに刷新。ゲート表記の絵文字🚧をチップ表示に変更
- **tools/docs_viewer.py**: サイドバーツリーにファイル種別アイコン・ホバー/選択状態・開閉アニメーションを追加し、Markdown表示のタイポグラフィ（見出し・表・コード・引用）をNotion風に調整。配信ロジック・API・公開統制は不変
- **slide-deck theme.css v1.1**: 表を紺ベタ塗りヘッダー＋全罫線からソフトヘッダー＋行区切りのみに、バッジを白抜きからソフトカラーチップに、カード・スケジュールバーを角丸化、表紙タイトルにアクセントバー追加。カラートークン名・クラス名は不変（既存デッキ・ブランド差し替え手順に影響なし）。`examples/sample-phase-completion.html` へ再インライン済み（`templates/previews/*.html` はインライン前のプレースホルダ形式のため変更不要）

## [1.0.3] - 2026-07-07

1.0.1/1.0.2 の変更にパック内の他文書が追従していなかった矛盾を、横断チェックで検出し修正。

### Fixed
- 日次セルフチェックの5問化（1.0.1）に未追従だった箇所を統一: llm-friendly-check の日次軽量版・flow-map 運用ループ図・README見出しが「3問」のままだった
- test-engineer がW字化（1.0.2 #6）に未追従: description と原則に「対応する定義・設計工程の完了前にドラフト作成→テスト工程開始時に確定版へ更新」を追記
- llm-friendly-check の CLAUDE.md 鮮度チェックが「現在の工程」を CLAUDE.md 側で見る前提のままだった → 工程正本 `docs/project-phase.md` の鮮度チェック（宣言工程と実作業の乖離＝黙った越境のサイン）に変更
- context-history の LATEST.md テンプレートが工程を転記させる書式で、工程正本との二重正本化リスクがあった → project-phase.md 参照に変更

### Added
- context-health-check の文書間矛盾チェックに「宣言工程と実作業の乖離検知」（黙った越境のAI側検出。#5の週次バックストップ）
- ai-dev-standardizer のテーラリング管理に「テーラリング変更時は `docs/project-plan.html` を再生成し変更後の絵で再承認を得る」（#9の更新運用の担い手を明確化）

## [1.0.2] - 2026-07-07

Formmit案件フィードバックの残件（Issue #3, #5, #6, #7, #8, #9, #10）を全対応。内容的には後方互換の追加（本来のsemver解釈ではMINOR相当）だが、1.0.1に続く実運用フィードバック一括対応としてPATCH番号でリリース。

### Added
- **工程状態の正本ファイル `docs/project-phase.md`**（#5）: 現在工程・ゲート判定記録・越境記録を機械可読に持つ。project-init が `templates/project-phase.md` から生成。CLAUDE.md.template の「現在の工程」はここへの参照に変更（転記の陳腐化防止）
- **越境アラート規約**（#5）: 宣言工程外の作業は作業前に確認＋越境記録への理由1行記載を義務化（「越えるのは可、黙って越えるのが不可」）。CLAUDE.md.template・leader に明文化
- **成果物トレーサビリティ突合ゲート**（#3）: leader の実装工程完了判定に画面・IF一覧×（詳細設計/実装ルート/UI/テスト）のマトリクス突合を必須化。code-reviewer に「設計書が明記する成果物の実在確認」（欠落検出）観点を追加。detail-design にスコープ除外宣言と操作記述の矛盾チェックを追加。deliverables-catalog に突合記録を必須成果物として追加
- **テスト計画のシフトレフト（W字化）**（#6）: 要件定義完了前にテスト計画書＋総合テスト仕様書ドラフト、基本設計完了前に結合テスト仕様書ドラフト、詳細設計完了前に単体テスト観点を必須化。test-planning / requirements-definition / basic-design / detail-design / leader / deliverables-catalog / flow-map に反映
- **構成デフォルト逸脱チェック**（#8）: tech-stack-selection にステップ5として追加（DB/Git/環境面数の観点例つき、ADR必須セクション化、非機能要件書からの委任項目の消し込み義務）。requirements-definition の非機能テンプレに環境面数・主要ミドルウェア構成方針の明示行を追加（「デフォルトを使うのは可、無意識に使うのが不可」）
- **UIあり案件のHTMLモックゲート**（#10）: basic-design に画面設計書と対になるHTMLモック生成→人間承認を基本設計完了条件として追加（正本は画面設計書、モックはレビュー用ビューの一方向生成）。project-init の構成決定表に発動条件を追加
- **案件別プロジェクト計画HTML**（#9）: project-init が工程フロー・ゲート位置・成果物マップ・採用エージェント・現在地を1枚のHTML（`docs/project-plan.html`）に生成し、テーラリング承認をこの絵の上で行う。テンプレート `templates/project-plan-template.html` を同梱
- **docsレビュー用ローカルWebビューア `tools/docs_viewer.py`**（#7）: ファイル管理風ツリー＋Markdown（Mermaid対応）/HTMLモックのレンダリング表示。Python標準ライブラリのみ・ワンコマンド起動。GitHub Pages向け静的ビルドは allowlist 必須のデフォルト非公開（公開統制）

## [1.0.1] - 2026-07-07

Formmit案件での実運用フィードバック（Issue #1〜#10）のうち、実際に事故を起こした定義・規約の欠陥3件を修正。プロセス追加系（#3, #5, #6, #8）と新機能系（#7, #9, #10）は1.1.0以降で対応予定。

### Fixed
- 実装系サブエージェント8体（backend-coder / frontend-coder / batch-specialist / infra-coder / migration-specialist / data-model-specialist / report-specialist / test-engineer）から Agent tool を除外（`tools:` を明示指定）。サブエージェントが再帰的に委譲して偽の完了報告を返す事故（#1）の再発防止。委譲判断はメインセッション（Leader）専任
- CLAUDE.md.template のオーケストレーション原則に適用範囲を明記: サブエージェントとして起動された場合は再帰委譲禁止（#1）
- 並行セッションでのID二重採番の防止規約を追加（#2）: Q-ID / I-ID / ADR の採番前に main 側台帳と突合する（CLAUDE.md.template・documentation-specialist）。ADRファイル名は英字サフィックス・連番でなくスラッグで一意化する
- worktree/ブランチ衛生の規約を追加（#4): CLAUDE.md.template の日次セルフチェックにgit衛生2問を追加（未コミット残骸・マージ済みブランチからの離脱）。dev-standards の git-workflow.md 必須項目に worktree ライフサイクルを追加。project-init が案件のテストランナー設定に `.claude/worktrees/**` 除外を含めるよう明記

## [1.0.0] - 2026-07-04

初版公開。

### 含まれるもの
- サブエージェント23体（統括・要件4 / 実装3 / 専門ドメイン5 / 品質・検証3 / 横断7 / メタ1）
- スキル21個（工程8 / 横断・随時13）
- 標準ドキュメント8点（QCD 21基準、仮定・未確定管理、フィーチャーチーム、AIセキュリティベースライン、大規模組織統制、成果物カタログ、テーラリングガイド、IPA共通フレーム2013対応表）
- 全体地図（Mermaid 4枚）、CLAUDE.md・MCP接続テンプレート
- 実行可能ツール: Excel変換（往復）、スライドテーマ一式、整合性監査
- CI 2本: push/PRごとの整合性検査、四半期棚卸しissueの自動起票

[1.0.3]: https://github.com/CT-masato-hino/claude-code-project-pack/releases/tag/v1.0.3
[1.0.2]: https://github.com/CT-masato-hino/claude-code-project-pack/releases/tag/v1.0.2
[1.0.1]: https://github.com/CT-masato-hino/claude-code-project-pack/releases/tag/v1.0.1
[1.0.0]: https://github.com/CT-masato-hino/claude-code-project-pack/releases/tag/v1.0.0
