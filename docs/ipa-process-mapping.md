# 共通フレーム2013（SLCP-JCF2013）と本パックの対応表

本パックの工程・エージェント・スキルが、IPA 共通フレーム2013のどのプロセスに対応するかを示す。
顧客・監査対応で「標準準拠」を説明する際の根拠資料としても使える。

> 注: 共通フレーム2013は「何をすべきか」のプロセス参照モデルであり、工程名・成果物名は
> 各社がテーラリングする前提の枠組みである（共通フレーム自体がテーラリングを要求している）。
> 本パックはSI現場で一般的なV字工程名に読み替えて対応付けている。

## プロセス対応表

| 共通フレーム2013 プロセス | 本パックの工程 | 主担当エージェント | 対応スキル |
|---|---|---|---|
| 企画プロセス（システム化構想・計画） | 提案・見積り支援（受注判断は人間） | leader / estimation-specialist / business-process-analyst | /tech-stack-selection, /estimation |
| 要件定義プロセス（利害関係者要件） | 業務分析・要件定義 | business-process-analyst / requirements-analyst | /requirements-definition |
| システム要件定義 | 要件定義（機能一覧・非機能要件） | requirements-analyst（現行調査は legacy-modernizer） | /requirements-definition |
| システム方式設計 | 基本設計（システム構成・方式） | architecture-guardian / infra-coder | /basic-design |
| ソフトウェア要件定義 | 要件定義〜基本設計（AC・画面/IF要件） | requirements-analyst | /requirements-definition, /basic-design |
| ソフトウェア方式設計 | 基本設計（外部設計） | architecture-guardian / api-designer / data-model-specialist / batch-specialist / report-specialist / ui-ux-designer（UIあり案件） | /basic-design, /erd-update |
| ソフトウェア詳細設計 | 詳細設計（内部設計） | backend-coder / frontend-coder（設計） | /detail-design |
| ソフトウェア構築（コーディング・単体） | 製造・単体テスト | frontend-coder / backend-coder / infra-coder / test-engineer（不具合調査は debugger） | /test-planning（単体） |
| ソフトウェア結合・ソフトウェア適格性確認 | 結合テスト | test-engineer / api-designer（対向試験） | /test-planning（結合） |
| システム結合・システム適格性確認 | 総合（システム）テスト | test-engineer / quality-performance | /test-planning（総合） |
| 導入・受入支援 | 受入テスト支援・納品・移行 | test-engineer / migration-specialist / operations-designer / documentation-specialist | /delivery-package, /migration-planning, /operations-design |
| 保守プロセス | 保守（障害対応・変更管理） | incident-responder / debugger / 全エージェント | /incident-report, /context-history, /context-health-check |

## 支援プロセス（工程横断）の対応

| 共通フレーム2013 支援プロセス | 本パックでの実現 |
|---|---|
| 品質保証プロセス | quality-performance ＋ 各工程の完了条件（スキル内に定義） |
| 検証・妥当性確認プロセス | code-reviewer（検証）＋ AC中心の要件定義（妥当性確認の基準化） |
| 構成管理プロセス | Git ＋ 文書の版数・変更履歴ルール（documentation-specialist） |
| 文書化プロセス | documentation-specialist ＋ /context-history |
| 監査プロセス | /context-health-check、/erd-update の整合性監査、/delivery-package の突合 |
| 問題解決プロセス | docs/issues.md ＋ docs/open-questions.md の運用 |

## 関連IPA資料と本パックでの利用箇所

| IPA資料 | 利用箇所 |
|---|---|
| 非機能要求グレード | /requirements-definition の非機能要件6大項目テンプレート |
| 機能要件の合意形成ガイド | requirements-analyst の曖昧さ検出観点（画面・帳票・IF・バッチの定義項目） |
| 安全なウェブサイトの作り方 | security-compliance のレビュー観点のベースライン |

## トレーサビリティの通し方（本パックの背骨）

```
機能ID（機能一覧）
 └→ AC-ID（受入基準）
     └→ 画面ID / IF-ID（基本設計）
         └→ 詳細設計書の項番
             └→ 単体テストNo（根拠=詳細設計）
     └→ 結合テストNo（根拠=基本設計）
 └→ 総合テストNo（根拠=AC）
```

全成果物が機能IDで連結されるため、/context-health-check と /delivery-package で機械的に断絶を検出できる。
