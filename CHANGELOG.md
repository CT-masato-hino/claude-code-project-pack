# Changelog

本パックの変更履歴。形式は [Keep a Changelog](https://keepachangelog.com/ja/1.1.0/)、バージョニングは [Semantic Versioning](https://semver.org/lang/ja/) に従います。

このパックにおける互換性の解釈:

- **MAJOR** — 導入済み案件のテーラリングを壊す変更。エージェント・スキルの削除や改名、QCD基準IDの変更・削除、正本ドキュメントのパス変更
- **MINOR** — 後方互換のある追加。エージェント・スキル・標準ドキュメントの追加、既存定義へのチェック項目追加
- **PATCH** — 文言の修正、誤りの訂正、テンプレートやスクリプトのバグ修正

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

[1.0.1]: https://github.com/CT-masato-hino/claude-code-project-pack/releases/tag/v1.0.1
[1.0.0]: https://github.com/CT-masato-hino/claude-code-project-pack/releases/tag/v1.0.0
