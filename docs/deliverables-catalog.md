# 成果物カタログ（工程別）

各工程の標準成果物と完了条件の一覧。/delivery-package はこの表と実ファイルを突合する。
契約上の納品物リストがある場合はそちらを正とし、この表を上書きテーラリングすること。

凡例 — ◎: 必須（検収対象になりうる） / ○: 推奨 / △: 案件により

## 人間承認ビジュアル（ゲート別の標準ビュー — 人間のレビュー速度を上げる）

品質ループのブレーキ役は人間であり、人間の承認スループットが全体の律速になる。各工程ゲートの承認は「文書の通読」ではなく「ビジュアルの確認」でできる状態を標準とする。

- **正本/ビュー分離の原則**: 正本は機械可読なMarkdown/Mermaid（git管理・audit_pack.py対象。AIはこちらを読む）。ビジュアルは正本からの**一方向生成ビュー**（人間はこちらを見る）であり、直接編集禁止・常に再生成可能に保つ（二重正本化の禁止）。承認記録は正本側（各文書の承認欄・project-phase.md）に残す
- **再承認は差分ベース**: 差し戻し後・変更後の再承認では、前回承認時点からの変更点をビジュアル上で明示する（docs/project-plan.html の再承認運用と同じ。全量を再説明して人間の確認コストを膨らませない）
- 閲覧は `tools/docs_viewer.py`（Markdown内Mermaid・`.mmd`・HTMLモックをそのまま描画できる）

| 工程ゲート | 承認の入力にするビジュアル | 正本（生成元） | 担い手 |
|---|---|---|---|
| テーラリング承認（開始時・変更時） | プロジェクト計画HTML（docs/project-plan.html） | CLAUDE.md・project-phase.md・本カタログ | project-init / ai-dev-standardizer |
| 要件定義 | 業務フロー図・DFD・機能関連図（Mermaid） | docs/requirements/ | business-process-analyst / requirements-analyst |
| 基本設計 | 画面遷移図（Mermaid）・HTMLモック・ERD図・アーキテクチャ構成図・インフラ（サービス）構成図 | docs/basic-design/・docs/erd/ | basic-design / ui-ux-designer / data-model-specialist / architecture-guardian / infra-coder |
| テスト計画（W字の各ドラフト） | テスト構成図（テストレベル×環境×データの対応図） | docs/test/test-plan.md | test-planning / test-engineer |
| 各テスト完了 | テスト報告サマリ（計画/実施/合否件数・不具合密度の表） | docs/test/<レベル>/ | test-engineer |
| 工程共通（随時） | 課題トレンド（起票数vs解決数の推移） | docs/issues.md | leader（「品質ループの停止判断」の入力） |

ビジュアル自体の必須度は◎ではなく**ゲート運用の標準**（納品物になるのは正本文書。必須度は下の各工程の表に従う）。例外はUIあり案件のHTMLモックで、従来どおり基本設計の◎。

## 要件定義

| 成果物 | 必須度 | 正本の場所 | 完了条件 |
|---|---|---|---|
| 機能一覧 | ◎ | docs/requirements/functional-list.md | 全機能にID・優先度・状態 |
| 受入基準（AC）一式 | ◎ | docs/requirements/acceptance-criteria/ | 全ThenがObservable、異常系1件以上 |
| 非機能要件定義書 | ◎ | docs/requirements/non-functional.md | 6大項目に未記入なし（仮置き可） |
| 業務フロー図 | ○ | docs/requirements/business-flow.md | As-Is/To-Beの別が明記 |
| 用語集 | ○ | docs/glossary.md | — |
| オープン課題一覧 | ◎ | docs/open-questions.md | Must機能の未解決ゼロ or 顧客確認中 |
| テスト計画書 | ◎ | docs/test/test-plan.md | 対象範囲・完了条件・データ方針あり（W字: 要件定義完了前に初版） |
| 総合テスト仕様書ドラフト | ◎ | docs/test/system/ | 全Must機能のACがトレースされている |

## 基本設計（外部設計）

| 成果物 | 必須度 | 正本の場所 | 完了条件 |
|---|---|---|---|
| 画面設計書 | ◎ | docs/basic-design/screens/ | 項目定義完備・エラー時挙動あり |
| 画面HTMLモック | ◎（UIあり案件） | docs/basic-design/mockups/ | 全画面分あり・人間がモックを見て承認した記録（正本は画面設計書。モックはレビュー用ビュー）。ui-ux-designer採用時は複数案比較と推奨理由の記録も伴う |
| 外部IF・API設計書 | ◎ | docs/basic-design/interfaces/ | エラーコード・冪等性・リトライ定義あり |
| 帳票設計書 | △ | docs/basic-design/reports/ | — |
| システム方式設計書 | ◎ | docs/basic-design/architecture.md | 非機能要件との対応が明記 |
| ERD・テーブル定義書 | ◎ | docs/erd/ | data-model-specialist承認・CHANGELOG更新 |
| コード定義書 | ◎ | docs/erd/codes.md | 実装との同期確認済み |
| バッチ処理一覧・設計 | △ | docs/basic-design/batch/ | リラン可否・異常時運用あり |
| 結合テスト仕様書ドラフト | ◎ | docs/test/integration/ | 基本設計（画面・IF）トレース済みのドラフト（W字対応） |
| 顧客承認記録 | ◎ | 各文書内の承認欄 | 承認日・承認者 |

## 詳細設計（内部設計）

| 成果物 | 必須度 | 正本の場所 | 完了条件 |
|---|---|---|---|
| 詳細設計書 | ◎ | docs/detail-design/<機能ID>/ | 異常系分岐・Tx境界・単体テスト観点あり |
| ADR（設計判断記録） | ○ | docs/decisions/ | 却下案と理由を含む |

## 製造・単体テスト

| 成果物 | 必須度 | 正本の場所 | 完了条件 |
|---|---|---|---|
| ソースコード | ◎ | リポジトリ | code-reviewerのMust指摘ゼロ |
| 単体テスト仕様書兼成績書 | ◎ | docs/test/unit/ | 根拠項番トレース済み・全件実施記録 |
| マイグレーション | ◎ | リポジトリ | data-model-specialistレビュー済み |
| 成果物トレーサビリティ突合記録 | ◎ | docs/project-phase.md（ゲート判定記録） | 画面・IF一覧×（詳細設計/実装ルート/UI/テスト）の突合で欠落ゼロ、または欠落の理由記録 |

## 結合テスト

| 成果物 | 必須度 | 正本の場所 | 完了条件 |
|---|---|---|---|
| 結合テスト仕様書兼成績書 | ◎ | docs/test/integration/ | 基本設計トレース・不合格は起票済み |
| 不具合管理表 | ◎ | docs/issues.md | Critical未解決ゼロ |

## 総合テスト

| 成果物 | 必須度 | 正本の場所 | 完了条件 |
|---|---|---|---|
| 総合テスト仕様書兼成績書 | ◎ | docs/test/system/ | ACトレース済み |
| 性能テスト結果 | ◎(性能要件があれば) | docs/test/system/performance/ | 要件値vs実測(p95等)の表 |
| 運用手順書 | ◎ | docs/operations/ | 運用者リテラシーに合わせた粒度 |

## 受入・納品・移行

| 成果物 | 必須度 | 正本の場所 | 完了条件 |
|---|---|---|---|
| 受入テスト支援資料 | ○ | docs/test/uat-support/ | シナリオ・データ準備済み |
| 移行計画書・手順書 | △ | docs/migration/ | 切り戻し手順あり・リハーサル記録 |
| 納品物一覧 | ◎ | deliverables/<納品日>/ | 全◎成果物の突合OK |
| コンテキストヒストリー（引き継ぎ） | ◎ | docs/context-history/LATEST.md | 保守フェーズが読んで再開できる |

## 品質基準（納品前ゲート・全案件共通の最低ライン）

数値基準の正本は `docs/standards/qcd-standards.md`（基準ID・担保エージェント・判定者つき）。以下はその納品前サマリ:

- Q-02: code-reviewer の Must 指摘 残ゼロ
- Q-09: security-compliance の Critical/High 残ゼロ（リスク受容は顧客合意の記録必須）
- Q-03: トレーサビリティ断絶ゼロ（または理由記録済み）
- Q-10: ERD三者一致監査 合格
- Q-04/Q-07/Q-08: カバレッジ・性能p95・静的解析がテーラリング後の確定値を充足
- 全◎成果物: 版数・変更履歴・承認記録あり
