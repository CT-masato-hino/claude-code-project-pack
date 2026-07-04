# Claude Code Project Pack for 日本のSI事業者

日本のSIer / 受託開発向けに設計した Claude Code のサブエージェント・スキル・運用ルール一式です。
IPA 共通フレーム2013（SLCP-JCF2013）の工程構造と、日本のSI現場で一般的なV字モデル
（要件定義 → 基本設計 → 詳細設計 → 製造 → 単体テスト → 結合テスト → 総合テスト → 受入 → 納品）
に対応し、**案件ごとにテーラリングして使う**ことを前提にしています。

**構成: サブエージェント23体 / スキル21個 / 標準ドキュメント8点（QCD基準・仮定管理・フィーチャーチーム・AIセキュリティ・大規模SIer統制含む） / CLAUDE.mdテンプレート / MCP接続テンプレート**

全体像は [docs/flow-map.md](docs/flow-map.md)（Mermaid 4枚: 工程×エージェント / ドキュメント正本フロー / 運用ループ / 仮定ライフサイクル）から掴むのが最短。

各エージェントは「起動時シーケンス → ドメイン別チェックリスト → ワークフローフェーズ → 連携マップ → 報告形式 → 品質基準」の統一構造で記述されており、汎用エージェント集（VoltAgent等）にない日本SI固有領域（帳票・バッチ・移行・障害報告・見積り・レガシー解析）をカバーします。

## 4層モデル — このパックが何であるかの見取り図

AI駆動開発の重心は「プロンプト → コンテキスト → ハーネス → ループ」と進化してきた。本パックは4層すべてを工程つき受託開発向けに配置したものであり、**下の層を飛ばして上の層を使うことを統制で禁じている**（ハーネスなしのループ運転は禁止、など）。

| 層 | 重心の時期 | 何のことか | 本パックでの実装 |
|---|---|---|---|
| プロンプト | 〜2024 | 1回の指示・聞き方の最適化 | 各エージェント定義（起動時シーケンス・チェックリスト・報告形式の統一構造） |
| コンテキスト | 2025 | 何を見せるかの情報設計 | CLAUDE.md / docs正本主義 / コンテキストヒストリー / 仮定マーカー / 要約のみ報告・汚染防止ルール |
| ハーネス | 2026初頭〜 | 許可設定・hooks・ガードレールで1回の実行を安全に動かす装備 | permissions deny / MCP許可リスト / QCDゲート / ERD独占管轄 / 破壊防止3層防御（enterprise-controls） |
| ループ | 2026年6月〜 | ハーネス済みエージェントを自動で回し続ける仕組み | 週次QCD・ヘルスチェックの定期運転 / pm-sync同期 / ループ統制（kill switch・上限・人間チェックポイント） |

成熟度診断にも使う: 自組織がどの層まで整備できているかを ai-dev-standardizer が点検し、**整備できていない層の一つ上に手を出さない**のが事故防止の原則。

## 設計思想

1. **多次元分割** — レイヤー（Infra/FE/BE）× 役割（Leader/Coder/Reviewer）× 工程（要件定義〜納品）でサブエージェントを分割
2. **横断サブエージェント** — セキュリティ、アーキテクチャ、データモデル（ERD）、ドキュメント、品質・性能は工程をまたぐため専用サブを常設
3. **コンテキスト汚染防止を最優先** — サブエージェント多用・要約中心の報告・知識の外部ドキュメント化・定期リセット
4. **テスト可能性重視** — 要件は Acceptance Criteria 中心。曖昧さはAIに4分類（未定義/多義/暗黙/矛盾）で指摘させ、顧客に投げられる質問文まで作らせる
5. **知識の外部化** — Documentation Specialist と「コンテキストヒストリー」でセッションを超えて決定・制約を引き継ぐ
6. **トレーサビリティ** — 機能ID → AC → 設計書項番 → テストNo を全成果物で連結し、断絶を機械検出する

## サブエージェント一覧（.claude/agents/ 23体）

### 統括・要件
| エージェント | 役割 |
|---|---|
| leader | 統括PL。工程完了判定・横断調整・トレードオフ裁定・エスカレーション判断 |
| requirements-analyst | AC作成・曖昧さ4分類検出・非機能要件（IPA非機能要求グレード） |
| business-process-analyst | As-Is/To-Be業務フロー・業務ヒアリング設計・デシジョンテーブル化 |
| estimation-specialist | WBS積上げ＋類推のクロスチェック・前提条件/除外事項・リスクバッファ |

### 実装（レイヤー別）
| エージェント | 役割 |
|---|---|
| frontend-coder | 業務システムUI実装（項目定義準拠・3状態・二重送信防止） |
| backend-coder | API・業務ロジック・DBアクセス実装（金額計算・Tx境界・排他制御） |
| infra-coder | IaC・CI/CD・監視設定（本番適用は人間。plan要約と手順書まで） |

### 専門ドメイン（日本SI特化）
| エージェント | 役割 |
|---|---|
| api-designer | API/外部IF設計・ファイル連携仕様・連携先との仕様調整 |
| batch-specialist | ジョブネット・リラン設計・締め処理・突き抜け対策 |
| report-specialist | 帳票設計（改ページ・集計・丸め・現行踏襲差分管理） |
| migration-specialist | データ移行・切替方式・リハーサル・切り戻し設計 |
| legacy-modernizer | 現行システム仕様復元・機能棚卸し・「現行通り」の言語化 |

### 品質・レビュー
| エージェント | 役割 |
|---|---|
| code-reviewer | 差分レビュー（設計書突合が第一観点。Must/Should/Nits） |
| test-engineer | V字対応テスト設計・トレーサビリティ両方向検査・成績書 |
| debugger | 再現手順確立・切り分け・根本原因特定（修正はCoderへ） |

### 横断（工程またぎ）
| エージェント | 役割 |
|---|---|
| security-compliance | OWASP/IPAベースのレビュー・業種別規制・納品前ゲート |
| architecture-guardian | 方式設計レビュー・新規導入審査・一貫性監査・ADR管理 |
| data-model-specialist | ERD/テーブル定義の独占管轄・影響調査・三者一致監査 |
| quality-performance | 性能検証（p95で判定）・品質メトリクス・ボトルネック調査 |
| documentation-specialist | ADR化・顧客資料整形・課題台帳・版数管理 |
| operations-designer | 運用設計・監視設計・手順書・運用引き継ぎ |
| incident-responder | 障害初動（証拠保全→影響→暫定）・恒久対策・水平展開 |

### メタ（AI駆動開発そのものの管理）
| エージェント | 役割 |
|---|---|
| ai-dev-standardizer | AI/人間の責任分界定義・AI成果物の検収基準・テーラリング管理・振り返りとパック改善・AI利用記録（顧客/監査対応） |

## スキル一覧（.claude/skills/ 21個）

### 工程スキル（V字の左から右へ）
| スキル | 内容 |
|---|---|
| /project-init | **最初に実行するスターター**。出発資産の判定（現行/既存コード/モック/類似サービス/RFP/ビジネス目的のみ）→パターン別プレイブック→構成テーラリング→CLAUDE.md生成→QCD基準確定→最初の一手 |
| /requirements-definition | 要件定義書・AC・非機能要件（IPA非機能要求グレード6大項目） |
| /basic-design | 基本設計書（画面・IF・帳票・方式）テンプレートと完了条件 |
| /detail-design | 詳細設計書（処理フロー・DBアクセス・単体テスト観点導出） |
| /test-planning | テスト計画・仕様書兼成績書（V字対応・トレーサビリティ検査） |
| /migration-planning | 移行計画書・マッピング表・当日Runbook・切り戻し計画 |
| /operations-design | 運用設計書・監視設計・手順書・EOL管理表 |
| /delivery-package | 納品物一覧・カタログ突合・品質ゲート・秘密情報混入検査 |

### 横断・随時スキル
| スキル | 内容 |
|---|---|
| /estimation | 見積り根拠書（レンジ＋前提条件。金額化は人間） |
| /tech-stack-selection | 技術選定マトリックス（Team Familiarity重視・ADR化） |
| /erd-update | ERD変更フロー（影響調査→承認→正本更新）・整合性監査 |
| /meeting-minutes | 議事録＋決定/宿題の台帳自動反映・過去決定との矛盾検出 |
| /excel-deliverables | Excel成果物変換（Markdown正本→納品Excel体裁、顧客戻りExcelの逆取り込み。実行可能スクリプト同梱） |
| /slide-deck | 顧客向けスライド作成（Claude Design前提・HTML 16:9。SI定番6デッキ型・テーマDS・DesignSync同期対応・完成サンプル同梱） |
| /incident-report | 障害報告書（第一報/中間報/最終報の3段階） |
| /context-history | コンテキストヒストリー（引き継ぎ資料・時系列差分チェック） |
| /context-health-check | 週次コンテキスト自己診断（矛盾・鮮度・外部化漏れ・仮定マーカー突合） |
| /llm-friendly-check | 週次のLLMフレンドリー診断（人間の指示の質・リポジトリの機械診断・運用習慣。改善提案は週1つだけ） |
| /dev-standards | 開発規約12種の生成・作り込み（既存コード抽出 or スタック標準から。lint機械化まで。coder稼働前に実行） |
| /effort-compression | SES工数圧縮の仕組み化（作業棚卸し→AI移管度マップ→ベースライン→月次圧縮率計測。Q悪化の圧縮は無効計上） |
| /pm-sync | Jira/Backlog/Redmine/Notion/Slack連携（MCP接続・正本ルール・課題/宿題/QCDレポートの同期運用） |

## ディレクトリ構成

```
claude-code-project-pack/
├── README.md
├── CLAUDE.md.template         ← 案件リポジトリ用CLAUDE.mdの雛形（運用ルール込み）
├── .claude/
│   ├── agents/                ← 22体（上表）
│   └── skills/                ← 14個（上表）
└── docs/
    ├── flow-map.md              ← 全体地図（Mermaid: 工程・ドキュメント・運用ループ・仮定ライフサイクル）
    ├── ipa-process-mapping.md   ← 共通フレーム2013との対応表
    ├── tailoring-guide.md       ← 規模・契約形態別テーラリングガイド
    ├── deliverables-catalog.md  ← 工程別成果物カタログ（必須度・完了条件）
    └── standards/
        ├── qcd-standards.md           ← QCD基準の正本（基準ID×担保エージェント×判定者。全合否判定の照合先）
        ├── assumption-management.md   ← 仮定・未確定管理標準（Q-ID・影響範囲・仮定マーカー・巻き戻し）
        ├── feature-team.md            ← フィーチャーチーム標準（機能別FE/BEスクワッド・IF契約ファースト・複製禁止則）
        ├── ai-security-baseline.md    ← AI利用セキュリティ（Claudeプラン別統制・穴あけ対策10項目・deny設定スニペット）
        └── enterprise-controls.md     ← 大規模SIer統制（破壊防止3層防御・ループ統制・監査証跡・職務分掌・協力会社統制）

このほかパック直下に `.mcp.json.template`（Jira/Backlog/Redmine/Notion/Slack接続の雛形。/pm-sync 参照）
```

## 導入方法

1. 案件リポジトリにパック一式をコピーする（**`.claude/` だけでは動かない** — エージェントは `docs/standards/` の基準を参照する）
   ```bash
   cp -r .claude/ /path/to/your-project/.claude/
   cp -r docs/ /path/to/your-project/docs/
   cp CLAUDE.md.template .mcp.json.template /path/to/your-project/
   ```
2. **`/project-init` を実行する**（ヒアリング→構成テーラリング→CLAUDE.md生成→QCD基準確定まで一括。標準ドキュメントの配置漏れもここで検査される。手動でやる場合は `docs/tailoring-guide.md` 参照）
3. `/project-init` が提案する「最初の一手」から着手する（新規→業務分析、リプレース→現行棚卸し、既存参画→`/context-history`）

## 運用の要点（詳細は CLAUDE.md.template）

- **メインセッション = オーケストレーター**。Claude Code の制約上サブエージェントはサブエージェントを呼べないため、「Leaderが専門サブを階層的に呼ぶ」構造は *メインセッションが各サブへ委譲し、判断はleaderに壁打ちする* 形で実現する
- **サブエージェントの報告は要約のみ**（全エージェントの「報告形式」節で強制）
- **決定はその日のうちにADR化**（documentation-specialist）
- **週1回 `/context-health-check`、月1回の大リセット＋ `/context-history` 引き継ぎ**
- **人間にしかできないこと**は各エージェントが明示的にエスカレーションする: 契約・金額・本番適用・顧客提出・リスク受容

## メンテナンス — 動かない場合はここを疑え

陳腐化が速い順に:

1. **`.mcp.json.template` の接続先** — MCPサーバーのURL・パッケージ名は変わる。mcp registry で最新を確認して差し替える
2. **`docs/standards/ai-security-baseline.md` のプラン別機能** — Claudeの管理機能（managed settings等）は更新される。最新のAnthropicドキュメントを正とする
3. **README 4層モデルのハーネス/ループ層** — Claude Code本体の機能進化と乖離しうる

該当したら Issue を立ててください（`maintenance` ラベル）。放置されないように、リポジトリ側に自動化を同梱しています:

| 仕組み | 内容 |
|---|---|
| `.github/workflows/consistency.yml` | push/PRごとに `tools/audit_pack.py` を実行（README記載数と実体の一致・参照切れ・ローカルパス/メール/シークレット混入を検査）。社名・個人名の混入検査は Secrets `AUDIT_KEYWORDS` で追加 |
| `.github/workflows/quarterly-review.yml` | 四半期cron（1/4/7/10月1日）で棚卸しissueを自動起票。MCPエンドポイントの死活を機械確認し、上記1〜3のチェックリスト＋整合性監査結果を添付 |

※ cron はGitHubのデフォルトブランチでのみ動作。フォーク運用時は Actions を有効化すること。

## ライセンス・運営

- MIT License / © 2026 [Chapter Tech合同会社](https://github.com/CT-masato-hino)（ITコンサルティング・PMO・DX支援 / 業務自動化・システム開発）
- IPA 共通フレーム2013・非機能要求グレード等の用語体系を参照していますが、本パックはIPA非公式です
- 成果物テンプレートは各社標準・顧客標準に合わせて必ずテーラリングしてください

## 最後に — このパックが自動化しないもの

ここまで23体のエージェントと基準の話をしてきたが、プロジェクトを成功させるのは最後まで**人と組織に向き合うこと**である。

顧客の「大丈夫です」の声色が先週と違うこと。決裁者が資料のどのページで目を止めたか。ベテラン運用者が新画面の説明中に一度も頷かなかったこと。メンバーの「ちょっと詰まってて」が3日続いていること。——プロジェクトを壊すものも救うものも、たいていこういう**構造化できない不確実なインサイト**の中にいる。それを拾い続けることに、テンプレートも基準IDもない。

人と向き合うのは、技術や仕組みに逃げ込めないという意味で最も逃げ場のない仕事であり、だからこそ本質である。このパックが定型を引き受けるのは、あなたがその仕事から逃げないための時間を作るためだ。QCDレポートが緑でも、顧客の表情が曇っていたら、信じるべきは表情のほうである。
