# 成果物カタログ（工程別）

各工程の標準成果物と完了条件の一覧。/delivery-package はこの表と実ファイルを突合する。
契約上の納品物リストがある場合はそちらを正とし、この表を上書きテーラリングすること。

凡例 — ◎: 必須（検収対象になりうる） / ○: 推奨 / △: 案件により

## docs/ ディレクトリ標準（工程順ナンバリング）

案件の docs/ は**工程順に番号をつけたディレクトリ**で構成する。ビューア・GitHub・IDE・成果物一覧のどこで見ても工程順に並び、「どれから見るか」を人間が並べ替えなくて済む。

```
docs/
├── 01-requirements/     要件定義（機能一覧・AC・非機能・業務フロー。現行調査は legacy/）
├── 02-design/           設計（basic/=基本設計・detail/=詳細設計・erd/・security-architecture.md）
├── 03-test/             テスト（計画・仕様書兼成績書・エビデンス・pre-uat/・ui-check/）
├── 04-reports/          階層レポート（overall/・phase/・agent/）とQCD週次（qcd/）・週次診断（llm-friendly/）
├── 05-decisions/        ADR
├── 06-context-history/  引き継ぎ（LATEST.md・archive/・health-YYYYMMDD.md）
├── 07-standards/        開発規約12種（/dev-standards の出力）
├── 08-operations/       運用設計・手順書
├── 09-migration/        移行計画・手順・リハーサル記録
├── 10-management/       運営台帳（estimation/・minutes/・incidents/・ai-standards/・ai-dev-security.md・effort/・customer-standard/）
├── 90-pack/             パック由来の標準（読み取り専用。standards/・本カタログ・tailoring-guide 等。案件で編集しない）
└── 直下: project-phase.md / open-questions.md / issues.md / glossary.md /
        deliverables-ledger.md（成果物台帳・正本）/ deliverables-index.html（一覧ビュー）/ project-plan.html（計画ビュー）
```

- 番号は「工程の順序」であって網羅ではない。間に挟む場合は `15-` のような中間番号を許容する（採番の理由をテーラリング記録に1行残す）
- パック由来の標準は `90-pack/` に置き、末尾に沈める。**案件側で 90-pack/ を編集しない**（パック更新時に上書きされる前提。変更が必要ならテーラリングとして CLAUDE.md・案件正本側に記録する）
- 正本の1枚もの台帳（project-phase.md 等）はルート直下のまま置く

## 成果物台帳と一覧ビュー（在庫と確認状態を1画面で見る）

**「この案件で実際に何が生まれ、どれを人間が確認済みか」**の実績一覧。カタログ（本表 = あるべき）と台帳（実績）を突合すれば「作られていない◎成果物」も検出できる。

- **正本**: `docs/deliverables-ledger.md`（機械可読な表。テンプレート: project-init `templates/deliverables-ledger.md`）。列 = キー / 表示名（日本語） / ファイルパス / 工程 / 区分（案件成果物 / パック標準） / 更新日 / 人間確認（未確認 / 確認済み / 条件付きOK） / OK日付 / 確認者（**ロールIDで記載。実名を書かない**） / 備考
- **一覧ビュー**: `docs/deliverables-index.html`。台帳からの一方向生成（テンプレート: project-init `templates/deliverables-index-template.html`）。ファイル名は英数のまま、一覧の表示名は日本語で管理する（表示名⇔パスの対応は台帳が持つ）
- **鮮度切れ検出**: 「確認済みなのに更新日がOK日付より新しい」行は鮮度切れとして強調表示する（確認後の変更を人間が見落とさない）
- **運用**: 成果物の新規作成・更新時に documentation-specialist が台帳を更新し、ビューを再生成する。leader は工程ゲート判定時に「当該工程の成果物の人間確認が全件『確認済み』か」を突合条件にする（未確認残ありは条件付き通過の条件に明記）

## 人間承認ビジュアル（ゲート別の標準ビュー — 人間のレビュー速度を上げる）

品質ループのブレーキ役は人間であり、人間の承認スループットが全体の律速になる。各工程ゲートの承認は「文書の通読」ではなく「ビジュアルの確認」でできる状態を標準とする。

- **正本/ビュー分離の原則**: 正本は機械可読なMarkdown/Mermaid（git管理・audit_pack.py対象。AIはこちらを読む）。ビジュアルは正本からの**一方向生成ビュー**（人間はこちらを見る）であり、直接編集禁止・常に再生成可能に保つ（二重正本化の禁止）。承認記録は正本側（各文書の承認欄・project-phase.md・成果物台帳）に残す
- **再承認は差分ベース**: 差し戻し後・変更後の再承認では、前回承認時点からの変更点をビジュアル上で明示する（docs/project-plan.html の再承認運用と同じ。全量を再説明して人間の確認コストを膨らませない）
- 閲覧は `tools/docs_viewer.py`（Markdown内Mermaid・`.mmd`・HTMLモックをそのまま描画できる）

| 工程ゲート | 承認の入力にするビジュアル | 正本（生成元） | 担い手 |
|---|---|---|---|
| テーラリング承認（開始時・変更時） | プロジェクト計画HTML（docs/project-plan.html） | CLAUDE.md・project-phase.md・本カタログ | project-init / ai-dev-standardizer |
| 工程共通（常時） | 成果物一覧HTML（docs/deliverables-index.html） | docs/deliverables-ledger.md | documentation-specialist |
| 要件定義 | 業務フロー図・DFD・機能関連図（下記「図の正本/ビュー基準」に従う） | docs/01-requirements/ | business-process-analyst / requirements-analyst |
| 要件定義 | AC一覧・トレーサビリティ表のHTMLビュー | docs/01-requirements/ | requirements-analyst / documentation-specialist |
| 基本設計 | 画面遷移図・HTMLモック・ERD図・アーキテクチャ構成図・インフラ（サービス）構成図・**セキュリティ構成図** | docs/02-design/ | basic-design / ui-ux-designer / data-model-specialist / architecture-guardian / infra-coder / security-compliance |
| 製造・単体完了（UIあり案件） | ローカルUI目視チェック（スクリーンショット一式＋チェックリスト） | docs/03-test/ui-check/ | frontend-coder（撮る）/ 人間（見る） |
| テスト計画（W字の各ドラフト） | テスト構成図（テストレベル×環境×データの対応図） | docs/03-test/test-plan.md | test-planning / test-engineer |
| 各テスト完了 | テスト報告サマリ（数値サマリー表: 計画/実施/合否件数・消化率・不具合密度） | docs/03-test/<レベル>/ | test-engineer |
| 各工程完了 | フェーズ報告書（docs/04-reports/phase/） | ゲート判定記録・成績書・台帳 | documentation-specialist / leader |
| 工程共通（随時） | 課題トレンド（起票数vs解決数の推移） | docs/issues.md | leader（「品質ループの停止判断」の入力） |

ビジュアル自体の必須度は◎ではなく**ゲート運用の標準**（納品物になるのは正本文書。必須度は下の各工程の表に従う）。例外はUIあり案件のHTMLモック（基本設計の◎）とローカルUI目視チェック（UIあり案件の製造・単体完了ゲート条件）。

## 図の正本/ビュー基準（図種別マトリクス）

Mermaidは万能ではない。**構造が線形・表形式に近い図は自動レイアウトで足りるが、エッジが交差する図・ノードの多い図はレイアウトを手動制御できず「読み順」を作れない**。図種ごとに正本とビューを使い分ける:

| 図種 | 正本 | 人間承認ビジュアル |
|---|---|---|
| シーケンス図・ER図・状態遷移図 | Mermaid | Mermaidのまま（レンダリングで十分） |
| 業務フロー図・DFD・機能関連図 | Mermaid（構造の正） | **HTML生成ビュー必須**（project-plan.html流の手組みレイアウト） |
| アーキテクチャ / インフラ / セキュリティ構成図 | Mermaid or 構成の箇条書き | 同上（HTML生成ビュー必須） |
| 画面遷移図 | Mermaid | 画面数が多ければHTMLビュー |

- **機械的な閾値**: ノード10超、またはエッジ交差が避けられない図はHTMLビューを作る（判断を人に委ねない）
- **HTMLビューの生成規約**: 正本（Mermaid/Markdown）からの一方向生成・直接編集禁止・再生成可能。デザインは project-plan.html の言語（チップ・カード・モノクロSVG・**絵文字禁止**）を踏襲。置き場所は正本と同ディレクトリ
- **代替ツールを標準にしない理由（再議論の防止）**: draw.io / D2 / PlantUML / Excalidraw は「git管理でdiffが取れる × AIが確実に生成・更新できる × 人間に見やすい」を同時に満たさない（バイナリ/独自形式は必ず陳腐化し、実装との乖離をgrepで検出できない）。よって正本は常にMermaid/Markdown、見やすさはHTMLビュー側で解決する

## レビュアー向けサマリ（主要成果物テンプレの共通規約）

人間のレビュー速度がMarkdownの物量に追いつかない問題への対策。**主要成果物（要件定義書・設計書・テスト計画/成績書・各報告書）の冒頭に次の欄を必須とする**:

```markdown
## レビュアー向けサマリ
- 前版からの差分: （初版なら「初版」）
- 人間が判断すべきポイント（3〜5点）:
- 影響するQ-ID・基準ID:
- 承認に必要な最小読解セット: （このファイルのこの節だけ読めば承認判断できる、の指定）
```

- 本文は従来どおり正本（サマリは導線であって要約正本ではない。矛盾したら本文が正）
- **粒度ガイド**: 逆生成・ドラフトでは「1ファイルに全部」より**承認単位で分割**する（レビューをインクリメンタルにできる。1回のゲートで人間に読ませる新規正本が5本を超えるなら分割・分納を検討する）

## 要件定義

| 成果物 | 必須度 | 正本の場所 | 完了条件 |
|---|---|---|---|
| 機能一覧 | ◎ | docs/01-requirements/functional-list.md | 全機能にID・優先度・状態 |
| 受入基準（AC）一式 | ◎ | docs/01-requirements/acceptance-criteria/ | 全ThenがObservable、異常系1件以上 |
| 非機能要件定義書 | ◎ | docs/01-requirements/non-functional.md | 6大項目に未記入なし（仮置き可） |
| 業務フロー図 | ○ | docs/01-requirements/business-flow.md | As-Is/To-Beの別が明記 |
| 用語集 | ○ | docs/glossary.md | — |
| オープン課題一覧 | ◎ | docs/open-questions.md | Must機能の未解決ゼロ or 顧客確認中 |
| テスト計画書 | ◎ | docs/03-test/test-plan.md | 対象範囲・完了条件・データ方針あり（W字: 要件定義完了前に初版） |
| 総合テスト仕様書ドラフト | ◎ | docs/03-test/system/ | 全Must機能のACがトレースされている |

## 基本設計（外部設計）

| 成果物 | 必須度 | 正本の場所 | 完了条件 |
|---|---|---|---|
| 画面設計書 | ◎ | docs/02-design/basic/screens/ | 項目定義完備・エラー時挙動あり |
| 画面HTMLモック | ◎（UIあり案件） | docs/02-design/basic/mockups/ | 全画面分あり・人間がモックを見て承認した記録（正本は画面設計書。モックはレビュー用ビュー）。ui-ux-designer採用時は複数案比較と推奨理由の記録も伴う |
| 外部IF・API設計書 | ◎ | docs/02-design/basic/interfaces/ | エラーコード・冪等性・リトライ定義あり |
| 帳票設計書 | △ | docs/02-design/basic/reports/ | — |
| システム方式設計書 | ◎ | docs/02-design/basic/architecture.md | 非機能要件との対応が明記 |
| **セキュリティ構成図** | ◎ | docs/02-design/security-architecture.md | 信頼境界・境界ごとの防御・**未適用の保護の明示**・攻撃面一覧（エンドポイント×認証×検証×AC/テストのトレース）・秘密情報の置き場。security-compliance承認（内容の詳細は security-compliance 定義・/basic-design 参照） |
| ERD・テーブル定義書 | ◎ | docs/02-design/erd/ | data-model-specialist承認・CHANGELOG更新 |
| コード定義書 | ◎ | docs/02-design/erd/codes.md | 実装との同期確認済み |
| バッチ処理一覧・設計 | △ | docs/02-design/basic/batch/ | リラン可否・異常時運用あり |
| 結合テスト仕様書ドラフト | ◎ | docs/03-test/integration/ | 基本設計（画面・IF）トレース済みのドラフト（W字対応） |
| 顧客承認記録 | ◎ | 各文書内の承認欄 | 承認日・承認者（ロールID） |

## 詳細設計（内部設計）

| 成果物 | 必須度 | 正本の場所 | 完了条件 |
|---|---|---|---|
| 詳細設計書 | ◎ | docs/02-design/detail/<機能ID>/ | 異常系分岐・Tx境界・単体テスト観点あり |
| ADR（設計判断記録） | ○ | docs/05-decisions/ | 却下案と理由を含む |

## 製造・単体テスト

| 成果物 | 必須度 | 正本の場所 | 完了条件 |
|---|---|---|---|
| ソースコード | ◎ | リポジトリ | code-reviewerのMust指摘ゼロ |
| 単体テスト仕様書兼成績書 | ◎ | docs/03-test/unit/ | 根拠項番トレース済み・全件実施記録・**冒頭の数値サマリー表**（/test-planning） |
| マイグレーション | ◎ | リポジトリ | data-model-specialistレビュー済み |
| 成果物トレーサビリティ突合記録 | ◎ | docs/project-phase.md（ゲート判定記録） | 画面・IF一覧×（詳細設計/実装ルート/UI/テスト）の突合で欠落ゼロ、または欠落の理由記録 |
| **UI確認記録（ローカルUI目視チェック）** | ◎（UIあり案件） | docs/03-test/ui-check/ | 変更画面のスクリーンショット一式（撮るのはAI）＋UI品質チェックリスト（モック乖離 / 空・エラー・ローディング状態 / 主要ブレークポイント）への人間の○×記録（見るのは人間。Q-11の生成/検証分離と同型）。バッチ/API専業は適用しない（HTMLモックゲートと同じ分岐条件） |

## 結合テスト

| 成果物 | 必須度 | 正本の場所 | 完了条件 |
|---|---|---|---|
| 結合テスト仕様書兼成績書 | ◎ | docs/03-test/integration/ | 基本設計トレース・不合格は起票済み・数値サマリー表あり |
| 不具合管理表 | ◎ | docs/issues.md | Critical未解決ゼロ |

## 総合テスト

| 成果物 | 必須度 | 正本の場所 | 完了条件 |
|---|---|---|---|
| 総合テスト仕様書兼成績書 | ◎ | docs/03-test/system/ | ACトレース済み・数値サマリー表あり |
| 性能テスト結果 | ◎(性能要件があれば) | docs/03-test/system/performance/ | 要件値vs実測(p95等)の表 |
| 運用手順書 | ◎ | docs/08-operations/ | 運用者リテラシーに合わせた粒度 |

## プレUAT（任意工程 — 総合テスト完了後・受入テスト前）

実環境構築という重い投資の前に、**ユーザー視点の一気通貫操作でUX不満と取りこぼし不具合を安く回収する**任意工程。合否記録なし・検収対象外（気づきは課題起票候補としてメモする）。詳細は /test-planning の「プレUAT」節。

| 成果物 | 必須度 | 正本の場所 | 完了条件 |
|---|---|---|---|
| プレUATガイド | △（実施する場合は◎） | docs/03-test/pre-uat/ | ローカル起動手順・実施可否表・シードデータ手順・受入テストとの差分（位置づけ）が記載 |

- 前提タスク: 全画面・全状態を網羅するシードデータ＋リセット手順（実在情報不使用）。認証があるアプリのローカル認証迂回は ai-security-baseline の「安全な穴あけ設計」パターン必須
- コンプラ停止点（実在サイトへのアクセス禁止・本番データ禁止等）はローカルでも有効

## 受入・納品・移行

| 成果物 | 必須度 | 正本の場所 | 完了条件 |
|---|---|---|---|
| 受入テスト支援資料 | ○ | docs/03-test/uat-support/ | シナリオ・データ準備済み |
| 移行計画書・手順書 | △ | docs/09-migration/ | 切り戻し手順あり・リハーサル記録 |
| 納品物一覧 | ◎ | deliverables/<納品日>/ | 全◎成果物の突合OK |
| コンテキストヒストリー（引き継ぎ） | ◎ | docs/06-context-history/LATEST.md | 保守フェーズが読んで再開できる |

## 工程横断（常設の成果物）

| 成果物 | 必須度 | 正本の場所 | 完了条件 |
|---|---|---|---|
| 成果物台帳 | ◎ | docs/deliverables-ledger.md | 全成果物が登録済み・工程ゲート時に当該工程分が「確認済み」 |
| 成果物一覧ビュー | ○ | docs/deliverables-index.html | 台帳からの一方向生成・鮮度切れ強調あり |
| フェーズ報告書 | ◎ | docs/04-reports/phase/YYYYMMDD-<工程>.md | ゲート判定とセットで作成（目的/実施/成果物/数値/判定/積み残し。テンプレ: project-init templates/report-templates.md） |
| エージェント報告書 | ○ | docs/04-reports/agent/YYYYMMDD-<agent>.md | サブエージェント完了時にチャットへの要約と同内容を追記（監査可能性の確保） |
| 全体報告書 | ○（節目・納品時は◎） | docs/04-reports/overall/YYYYMMDD-overall.md | 数値サマリ＋下層（フェーズ/エージェント報告書）へのリンク集。単層の長文にしない |
| AI駆動開発セキュリティ説明資料 | ○（顧客説明・稟議・監査対応時は◎） | docs/10-management/ai-dev-security.md | AIのアクセス範囲・権限3層・遮断されているもの（deny実態と一致）・残リスクと受容判断の記録（テンプレ: project-init templates/ai-dev-security.md） |

## 品質基準（納品前ゲート・全案件共通の最低ライン）

数値基準の正本は `docs/90-pack/standards/qcd-standards.md`（基準ID・担保エージェント・判定者つき）。以下はその納品前サマリ:

- Q-02: code-reviewer の Must 指摘 残ゼロ
- Q-09: security-compliance の Critical/High 残ゼロ（リスク受容は顧客合意の記録必須。判定根拠はセキュリティ構成図・攻撃面一覧への突合）
- Q-03: トレーサビリティ断絶ゼロ（または理由記録済み）
- Q-10: ERD三者一致監査 合格
- Q-04/Q-07/Q-08: カバレッジ・性能p95・静的解析がテーラリング後の確定値を充足
- 全◎成果物: 版数・変更履歴・承認記録あり・成果物台帳で「確認済み」
- **数値なしの合否宣言は無効**（基準ID引用と同格のルール。「テスト合格」ではなく「67/67合格・消化率100%」のように書く）
