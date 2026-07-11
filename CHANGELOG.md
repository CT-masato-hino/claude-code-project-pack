# Changelog

本パックの変更履歴。形式は [Keep a Changelog](https://keepachangelog.com/ja/1.1.0/)、バージョニングは [Semantic Versioning](https://semver.org/lang/ja/) に従います。

このパックにおける互換性の解釈:

- **MAJOR** — 導入済み案件のテーラリングを壊す変更。エージェント・スキルの削除や改名、QCD基準IDの変更・削除、正本ドキュメントのパス変更
- **MINOR** — 後方互換のある追加。エージェント・スキル・標準ドキュメントの追加、既存定義へのチェック項目追加
- **PATCH** — 文言の修正、誤りの訂正、テンプレートやスクリプトのバグ修正

## [2.0.0] - 2026-07-11

導入実走フィードバック（ec-module 導入 Issue #22〜#29, #31〜#34 / Formmit導入 Issue #30）の一括対応。docs/ 配置の再設計（正本パスの変更）を含むため**MAJOR**。テーマは3つ — ①人間レビューの律速対策（生成は速いのにレビューが追いつかない問題への、台帳・サマリ・レポート・作図基準の体系化）②工程ゲートの実効性強化（数値必須・UI目視・プレUAT）③セキュリティの可視化と混入防止。

### Changed（互換性に影響 — MAJOR の理由）
- **docs/ ディレクトリ標準の再設計**（#26, #28）: パック由来ドキュメントを `docs/90-pack/`（読み取り専用）に分離し、案件成果物は工程順ナンバリング（`01-requirements/` `02-design/` `03-test/` `04-reports/` `05-decisions/` `06-context-history/` `07-standards/` `08-operations/` `09-migration/` `10-management/`）で配置する標準に変更。どのツリー表示でも工程順に並び、パック標準が案件レビューの邪魔をしない。旧配置の案件生成物（docs/standards/ 配下にあった dev-standards・qcd-report・effort 系）も案件側名前空間へ移動。エージェント・スキル・テンプレート・ツールの全パス参照（55ファイル）を更新し、番号は「順序であって網羅ではない」（中間番号 15- 等を許容）をカタログに明記。**v1.x 導入済み案件の移行は /project-init フェーズ0の配置検査が案内する**（git mv＋参照一括置換。移行しない選択も可）
- **audit_pack.py の混入検査を強化**（#34）: 検査対象に `*.log` `*.txt`（エビデンス類）を追加、ローカルパス検査を先頭スラッシュなし（スタックトレースの `(Users/...` 形式）にも対応、`package@version` 表記のメール誤検知を除外、`AUDIT_ALLOWLIST`（公開情報の除外）を新設。導入先は AUDIT_KEYWORDS への開発者名・OSユーザー名登録が /project-init フェーズ4の必須ステップに

### Added
- **成果物台帳＋一覧ビュー**（#25）: `docs/deliverables-ledger.md`（正本: 日本語表示名⇔ファイルパス・工程・区分・更新日・人間確認・OK日付・確認者ロールID）から `docs/deliverables-index.html` を一方向生成。「確認済みなのに更新日がOK日付より新しい」行を鮮度切れとして強調。documentation-specialist が管轄し、leader が工程ゲートで「当該工程の成果物が全件確認済みか」を突合。テンプレート2点（deliverables-ledger.md / deliverables-index-template.html）を project-init に同梱
- **階層レポート `docs/04-reports/`**（#27）: 全体（数値サマリ＋下層リンクのみ）→フェーズ（ゲート判定とセットで必須。判定記録の「根拠」列から参照）→エージェント（サブエージェントがチャット要約と同内容を自分の報告書へ追記 — 汚染防止と監査可能性の両立）の3層を標準化。QCD週次・診断レポートも 04-reports/ に集約。テンプレート report-templates.md を同梱
- **数値サマリー必須化**（#22）: 成績書テンプレ冒頭に数値サマリー表（実施/合格/不合格/スキップ/消化率/実行時間/計画値差分）を必須欄として追加。qcd-standards 運用原則に「数値なしの合否宣言は無効（基準ID引用と同格）」を明記し、Q-06等の計測系基準は成績書サマリーから機械転記できる形に統一。leader のゲート判定・test-engineer の成績記録にも配線
- **レビュアー向けサマリ規約**（#23）: 主要成果物テンプレの冒頭に「前版からの差分 / 人間が判断すべきポイント3〜5点 / 影響Q-ID・基準ID / 承認に必要な最小読解セット」欄を規約化（requirements-definition / basic-design / detail-design / test-planning / 各報告書）。documentation-specialist の報告形式に最小読解セットの提示を追加。承認単位の分割（1ゲートで新規正本5本超なら分納）の粒度ガイドと、AC一覧・トレーサビリティ表のHTMLビュー化をカタログに追加
- **ローカルUI目視チェック**（#24）: UIあり案件の製造・単体完了ゲートに「UI確認記録」（`docs/03-test/ui-check/`）を◎成果物として追加。スクリーンショットを撮るのはAI（frontend-coderの完了条件）、チェックリスト（モック乖離/空・エラー・ローディング/主要ブレークポイント）に○×をつけるのは人間（Q-11の生成/検証分離と同型）。leaderのゲート判定で突合。バッチ/API専業は適用しない
- **図の正本/ビュー基準（図種別マトリクス）**（#29）: シーケンス図・ER図・状態遷移図はMermaidのまま、業務フロー図・DFD・機能関連図・構成図はHTML生成ビュー必須（ノード10超 or エッジ交差で機械判定）。HTMLビューの生成規約（一方向生成・project-plan.htmlのデザイン言語・絵文字禁止・正本と同ディレクトリ）と、代替ツール（draw.io/D2/PlantUML/Excalidraw）を標準にしない却下理由を明文化
- **プレUAT工程**（#30）: 総合テスト完了後〜受入テスト前の任意工程として標準化（任意実施・合否記録なし・検収対象外。実環境構築前にユーザー視点の一気通貫でUX不満と取りこぼしを安く回収）。前提タスク（全状態網羅シードデータ・モック連携先の単体起動・実施可否表）と受入テストとの区別の明文化を test-planning に追加。ai-security-baseline に §2-2「安全な穴あけ設計パターン」（ローカル認証迂回の4点セット: 発動範囲の構造的限定・本番混入トリップワイヤー・監査痕跡・securityレビュー必須）を新設
- **セキュリティ構成図**（#32）: `docs/02-design/security-architecture.md` を基本設計の◎成果物に追加（信頼境界図・**未適用の保護の明示**（点線＋チップで「ない」を描く — 受容済みリスクと検討漏れの区別）・攻撃面一覧（エンドポイント×認証×検証×AC/テストのトレース）・秘密情報の置き場）。security-compliance をレビュー専任から「セキュリティ正本の管轄者」へ半歩拡張（tools に Write/Edit を追加）。Q-09 の判定根拠をこの図・攻撃面一覧への突合として qcd-standards に接続
- **AI駆動開発セキュリティ説明資料**（#33): `docs/10-management/ai-dev-security.md`（AIのアクセス範囲・遮断されているもの（deny実態から生成し乖離を防ぐ）・権限3層・データフローと漏洩リスク・残リスクの受容記録欄・プラン別分岐）を標準成果物に追加。/project-init フェーズ4ステップ8の出力として生成、主管は ai-dev-standardizer。ai-security-baseline に §2-3「説明資料との接続」を新設（ルール文書と説明資料の役割分離）
- **実名・ローカルパス混入の再発防止**（#34）: 「成果物・docsの人物表記は役割名/ロールIDを正とし実名を書かない」を CLAUDE.md.template（禁止事項・体制表の担当者欄を呼称に変更）・documentation-specialist・ai-dev-standardizer に規約化。エビデンス保存時の「ローカル絶対パスを `<repo>` に置換」を test-planning / test-engineer / debugger に追加
- **docs_viewer.py の機能追加**（#26, #31): ①ツリーを「案件成果物 / パック標準（読み取り専用バッジ・デフォルト折りたたみ）」の2セクション表示に ②`/raw/` にAcceptコンテンツネゴシエーションを追加 — 生成ビュー内の.mdリンク（ブラウザ通常遷移: Accept: text/html）にはレンダリングページ（marked＋mermaid・トップへの導線つき）を返し、SPAのfetch（Accept: */*）は従来どおり生テキスト。フォールバックも text/plain 化（octet-streamでダウンロードさせない）。静的ビルド側の制約（.mdリンクは遷移先でレンダリングされない）は docstring に既知の制約として明記

### 対応 Issue
#22 #23 #24 #25 #26 #27 #28 #29 #30 #31 #32 #33 #34（すべて導入実走フィードバック）

## [1.2.0] - 2026-07-10

Claude Code のプラグイン機構による配布に対応。ファイル移動なしの追加のみ（plugin.json のカスタムパスで既存の `.claude/` 配置をそのまま参照）のため、本パックのsemver解釈どおりMINOR。

### Added
- **Claude Code プラグイン対応**: `.claude-plugin/plugin.json`（agents/skills を既存パスのまま参照）と `.claude-plugin/marketplace.json` を新設。`claude plugin marketplace add CT-masato-hino/claude-code-project-pack` → `claude plugin install project-pack@claude-code-project-pack` の2コマンドで導入でき、更新は plugin update でバージョン管理される
- **導入手順の2方式化（README）**: 方式A=プラグイン（お試し・個人利用の高速導入路。スキルは `project-pack:` 名前空間つき）/ 方式B=クローン（案件正式導入 — パック一式が案件リポジトリにコミットされ、PRレビュー・audit_pack.py・エージェント単位テーラリングの対象になる）。統制の前提が異なるため用途を明確に分離
- **project-init のプラグイン対応**: フェーズ0の正本コピー元にプラグインインストール先を追加。フェーズ3に「プラグイン導入時はエージェント単位の除外ができないため、テーラリングが必要と判定された時点でクローン導入への切替を人間に案内する」を明記
- **audit_pack.py にプラグインマニフェスト検査を追加**: plugin.json の version が README・CHANGELOG と一致するか、agents のファイル列挙（Claude Codeの仕様上ディレクトリ指定不可のため列挙が必要）が実ファイルと同期しているか、marketplace.json の記載数（エージェント/スキル）が実数と一致するか。ローカルマーケットプレイスからの install → enable → uninstall の往復を実地検証済み

### 採用を見送ったもの（調査記録）
- **msitarzewski/agency-agents（230体・ペルソナ型エージェント集）**: エージェント定義が人格演技型で、QCD基準・ゲート・成果物カタログへの配線を持たない「肩書きコレクション」方式のため不採用。本パックの設計思想（エージェント=仕組みに配線された担保者）・テーラリング原則（削るのが正しい）・コンテキスト汚染防止と正面から矛盾する。外部エージェント定義の無検証取り込みは ai-security-baseline 穴あけ#9 にも該当
- **anthropics/knowledge-work-plugins のロール（営業・マーケ・法務等）**: 受託開発デリバリーのスコープ外。配布機構（marketplace.json / .claude-plugin 構造）のみ参考にした

## [1.1.1] - 2026-07-10

Formmit案件フィードバック（Issue #16, #18）への対応。品質チェックのループ（レビュー→指摘→起票→再検証）に「見つけるのをやめて前に進む基準」がなく自己増殖する問題（#16）と、ブレーキ役である人間の承認スループットを上げる正本/ビュー分離・ゲート別ビジュアル標準（#18）を対で導入。あわせてパック全体の健全性チェック（人間・組織が向き合える立ち上がりになっているか／セキュリティ＝漏洩・破壊が最初に検討されるか／サイズ・SLAのヒアリング品質）で見つかった構造ギャップ2点——破壊防止denyが大規模専用に格納されていた点、規模・SLAを「答えられない質問」（概算人月は？SLAは？）で直接聞く設計だった点——を修正。内容的には後方互換の追加（本来のsemver解釈ではMINOR相当）だが、v1.1.0直後の実運用フィードバック一括対応としてPATCH番号でリリース。

### Added
- **leader に「品質ループの停止判断」チェックリストを新設**（#16）: ①停止基準の適用（Mustブロッカー0件なら工程通過。残Should/Nitsは工程完了の条件にしない）②Should/Nitsの「記録」と「起票」の分離（軽微なものはissue行を作らずコミットメッセージ記録で足りる。禁止は暗黙の握りつぶしのみ）③自己増殖の定量検知（起票数>解決数の継続・同一issue行の「完全解決」2回以上・context-historyアーカイブ週3本超 → 人間へ警告）④進捗はissues.mdの分量ではなくD-01（成果物完了基準・0/100）で測る
- **停止基準のテンプレート項目**（#16）: CLAUDE.md.template のQCD節に確定値記入欄を追加し、project-init のフェーズ3決定表に「納期・顧客検収のない案件（内製・ホビー・R&D）」行を新設。tailoring-guide の小規模構成にも明記（納期のない案件ほど停止基準が必須 — 自然な締め切りが存在しないため）
- **dev-standards の git-workflow.md 必須項目に「レビュー指摘のトリアージ」を追加**（#16）: Should/Nitsの記録と起票の分離を案件規約レベルで確定させる
- **context-history に「発火頻度の基準」を新設**（#16）: 週次＋月1大リセット＋ゲート通過時が基準。高密度開発でもarchiveスナップショットは1日1本まで（同日は上書き）。週3本超ペースは自己増殖のサインとしてleaderの停止判断へ接続
- **正本/ビュー分離原則の明文化**（#18）: 「正本は機械可読なMarkdown/Mermaid（AIが読む）、ビジュアルは正本からの一方向生成ビュー（人間が見る）・直接編集禁止・常に再生成可能」を CLAUDE.md.template 成果物運用節・tailoring-guide 4節（削ってはいけないもの）に追加。1.0.2で個別実装した project-plan.html・HTMLモックゲート・docs_viewer.py の暗黙原則を一般原則に昇格
- **deliverables-catalog に「人間承認ビジュアル（ゲート別の標準ビュー）」節を新設**（#18): 工程ゲートごとに承認の入力とするビジュアル（DFD・機能関連図 / 画面遷移図・ERD図・アーキテクチャ構成図・インフラ構成図・HTMLモック / テスト構成図 / テスト報告サマリ / 課題トレンド）と正本・担い手を対応表化。担い手はすべて既存エージェント/スキルに割り当て（新設なし）。ビジュアルの必須度は◎ではなくゲート運用の標準（HTMLモックのみ従来どおり◎）
- **再承認の差分ベース化**（#18）: leader の工程完了判定に「再判定・再承認では前回承認時点からの差分だけを明示する」を追加し、deliverables-catalog の原則にも記載（project-plan.html の再承認運用を全ビジュアルへ一般化）
- **破壊防止denyの規模非依存化**（健全性チェック）: enterprise-controls §A第1層のdenyセット（rm -rf・force push・git reset --hard origin・DROP/TRUNCATE・terraform/kubectl/クラウドCLIの破壊操作）を ai-security-baseline §2「破壊防止deny（規模非依存）」へ移管し、全規模共通の最低ラインに変更。破壊事故は案件規模と無関係に起きるため、1人・ホビー案件でも省略しない。enterprise-controls §A第1層はベースライン参照＋大規模上乗せ（managed settings強制・本番系CLI白リスト徹底）に書き換え（正本の一元化）。project-init フェーズ4ステップ8にも「漏洩系＋破壊系の2スニペット適用・省略不可」を明記
- **出発資産の機微度確認**（健全性チェック）: project-init ブロックB質問6に「資産に本番データ・個人情報・秘密情報（.env・鍵・接続情報）が含まれるか」を追加。P1現行システム・P2既存コードの初動（棚卸し・資産評価）は**AIが資産を読む作業**なので、この確認とマスキング/除外方針の決定より先に始めない
- **規模ヒアリングの代理指標化**（健全性チェック）: 「概算人月は？」を依頼者に直接答えさせない。画面数・帳票数・連携先数・利用者数・データ量・業務種類数の代理指標で聞き、規模帯（小/中/大）を**パック側が推定して根拠つきで提示**し、依頼者の体感とすり合わせてから次に進む（最初の見立て誤り＝「思ったより重い/軽い」が全工程の期待値に波及するため）。leader の工程完了判定に「規模・期間の見立ての再確認」を追加し、乖離時は再テーラリング→project-plan.html差分承認で工程末ごとに補正する
- **業務影響度ヒアリング＝SLAの入口**（健全性チェック）: project-init ブロックAに質問4-2を新設。「SLAは？」「稼働率は？」と聞かず、業務の言葉（「止まると誰の・どの業務が・どれくらい困るか」「何時間止まったら実害が出るか」「データは手作業で復元できるか」）で聞いて影響度4レベルに変換し、フェーズ3の構成判断（quality-performance・operations-design・incident-responder採用、Q基準の厳格度）と要件定義への入力にする
- **非機能ヒアリング質問集（平易言語版）を requirements-definition に新設**（健全性チェック）: SLA用語→業務の言葉の変換表（稼働率・RTO・RPO・p95・同時接続・データ量成長・バックアップ・監視・機密度の9項目）。回答を要求値にこちらが変換し、根拠列に「ヒアリング回答（誰が・いつ）」として推奨値仮置きと区別して記録。「わからない」は推奨値仮置き＋Q-ID起票とし、**専門用語のまま顧客に宿題として投げない**。requirements-analyst のチェックリスト冒頭にも同原則を追加

### Changed
- **重複記載のポインタ化（最終精度チェック）**: 複数人体制の運用ルール（leader相談・人間専管事項の窓口・ロールID宣言）の全文が project-init 質問18と CLAUDE.md.template 体制表注記にも繰り返されていたのを、正本（tailoring-guide 0-1節／テンプレートのオーケストレーション原則）への参照に置き換え。停止基準の機序説明（品質ループの自己増殖）も leader「品質ループの停止判断」を正本に一本化し、tailoring-guide・project-init 決定表側は参照に短縮

### Fixed
- README の「よくある事故パターン10項目」が1.1.0の穴あけパターン10→11化に未追従だった → 11項目に修正
- ai-security-baseline §4 継続統制の「本標準の1〜10の実地確認」も同じく未追従だった → 1〜11に修正

### 確認のみ（変更なし）
- docs_viewer.py のMermaid描画（Markdown内コードブロック・`.mmd` 単体ファイルとも対応済み）を確認 — #18のビジュアル閲覧手段として拡張不要

## [1.1.0] - 2026-07-08

外部記事（AIを活用したデザイン業務の構造化事例）から要素を取り込み、UI/UXデザインの判断・レビューを担う専門エージェントを新設。あわせて、「案件を操作する依頼者は常に同じ1人のPM像ではない（インフラ・PMO・フロント・バックエンド・QA・ビジネス企画・デザイナー等、様々なロールがあり得る）」という前提に立ち、依頼者の主務ロールとチームの専任者の有無に応じて各エージェントの意思決定範囲（フォーメーション・ミッション）を出し分ける仕組みを `/project-init` に追加。ui-ux-designerの採用可否はその一適用例。

### Added
- **新規サブエージェント `ui-ux-designer`**（横断）: 画面デザインの複数案比較・提案、デザイン原則チェックリスト（一貫性・必須3状態・アクセシビリティ等）の適合判定、HTMLモック承認前レビューを担当。「制作者」ではなく「レビュアー・判断者」として、実装（frontend-coder）と分離する。前例のない「ゼロイチ」画面は複数案の叩き台までに留め、人間判断へ引き渡す限界も明記
- **project-init の体制ギャップヒアリング**（ブロックD-18）: このセッションを操作する依頼者自身の主務ロール（インフラ／PMO・PM／フロントエンド／バックエンド／テスター・QA／ビジネス企画・業務分析／デザイナー／その他）と、各ドメインの専任者の有無を確認。フェーズ3決定表に「体制ギャップ」行を追加し、専任者不在のドメインほど対応エージェントの意思決定代行範囲を広げ、専任者ありのドメインはエージェントを叩き台ツールとして人間が深く監修する運用に出し分ける。ui-ux-designerの採用可否はUIドメインでの適用例として個別記載
- **docs/tailoring-guide.md に0節「利用者ロール・体制ギャップによるテーラリング」を新設**（案件規模別構成と直交する軸として整理）。CLAUDE.md.template にも依頼者の主務ロール記載欄とオーケストレーション原則への「体制ギャップ運用」を追加
- **basic-design のHTMLモック生成フロー拡張**: 調査（既存画面の参照パターン）→複数案実装→提案（理由つき推奨）の流れをui-ux-designer採用時の担い手として明記。保留時はfrontend-coder＋requirements-analystが原則チェックリストを直接適用する代替も明記
- ui-ux-designerをflow-map・ipa-process-mapping・deliverables-catalog・feature-team.md（複製禁止リスト）に反映
- **複数人が同時にセッションを操作する体制への対応**: CLAUDE.md.templateの依頼者ロール欄を、複数担当者×主務ドメイン×主に使うエージェントを記録するチーム体制表に拡張。project-initのブロックD-18を人数・役割の複数人ヒアリングに拡張。tailoring-guide.mdに0-1節「複数人が同時にセッションを操作する場合」を新設し、feature-team.md（機能ドメイン別スクワッド）とは別軸のロール別分割として整理
- **`CLAUDE.local.md`（gitignore対象）を「ロールID宣言1行のみ」に限定して導入**: 役割の中身（担当ドメイン・主に使うエージェント）はロールIDつきで共有CLAUDE.mdのチーム体制表（PRレビュー・audit_pack.py対象）に書き、CLAUDE.local.mdは「私のロールID: X」の宣言だけにする設計とした。これにより「個人のCLAUDE.local.mdでQCD基準・権限・工程ルールを個人セッションだけ迂回する」という穴あけリスクを、運用ルールだけでなく構造（正規の内容がロールID1行のみ）でも塞ぐ。`docs/standards/ai-security-baseline.md` に穴あけパターン#11として追加し、`docs/standards/enterprise-controls.md` の穴あけパターン数表記を10→11に修正、§C監査証跡にCLAUDE.local.mdが対象外である旨を明記。`/context-health-check` の週次診断に「ロールID宣言1行以外を含んでいないか」の自己確認を追加。`tools/audit_pack.py`はCLAUDE.local.mdをスキャン対象から除外し、`.gitignore`にエントリを追加
- **「Leader窓口=特定の人間に集約」という設計を撤回**: `docs/standards/qcd-standards.md`の判定者列は元々ほぼ全項目「leader」（サブエージェント）であり、`leader`は呼ばれるたびに`CLAUDE.md`・`docs/project-phase.md`・`docs/decisions/`という同じ正本を読むため、誰の担当セッションから呼んでも一貫した判断が返る。よって特定の人間を「Leader」に指名する必要はなく、各担当者は自分の主務ドメインを遂行しながら横断判断だけ`leader`サブエージェントに相談する運用に修正。チーム体制表の「Leader窓口」列は廃止し、契約・費用・リスク受容・顧客提出・検収判定などAIが判断できない事項だけを担う「人間専管事項の窓口」に置き換えた。`leader.md`にも複数セッションからの呼び出しで一貫性が保たれる旨を明記

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

[2.0.0]: https://github.com/CT-masato-hino/claude-code-project-pack/releases/tag/v2.0.0
[1.2.0]: https://github.com/CT-masato-hino/claude-code-project-pack/releases/tag/v1.2.0
[1.1.1]: https://github.com/CT-masato-hino/claude-code-project-pack/releases/tag/v1.1.1
[1.1.0]: https://github.com/CT-masato-hino/claude-code-project-pack/releases/tag/v1.1.0
[1.0.5]: https://github.com/CT-masato-hino/claude-code-project-pack/releases/tag/v1.0.5
[1.0.4]: https://github.com/CT-masato-hino/claude-code-project-pack/releases/tag/v1.0.4
[1.0.3]: https://github.com/CT-masato-hino/claude-code-project-pack/releases/tag/v1.0.3
[1.0.2]: https://github.com/CT-masato-hino/claude-code-project-pack/releases/tag/v1.0.2
[1.0.1]: https://github.com/CT-masato-hino/claude-code-project-pack/releases/tag/v1.0.1
[1.0.0]: https://github.com/CT-masato-hino/claude-code-project-pack/releases/tag/v1.0.0
