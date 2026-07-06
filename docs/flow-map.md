# フローマップ（全体地図）

パックの構成要素がどう連なるかをMermaidで図示する。**個々の定義の正本は各ファイルであり、この図は読むための地図**（矛盾したら各ファイルが正）。

## 1. 工程フロー × エージェント × スキル（V字＋シフトレフトのW字運用）

```mermaid
flowchart TD
    INIT["/project-init<br/>出発資産判定・テーラリング・QCD確定<br/>project-phase.md＋project-plan.html生成"] --> BPA

    subgraph LEFT["V字左側（定義・設計）— テスト仕様ドラフトも左側で作る（W字 /test-planning）"]
        BPA["業務分析<br/>business-process-analyst"] --> REQ["要件定義 /requirements-definition<br/>requirements-analyst<br/>＋テスト計画・総合テスト仕様ドラフト"]
        REQ --> BD["基本設計 /basic-design<br/>api-designer・report-specialist<br/>batch-specialist・architecture-guardian<br/>＋HTMLモック承認（UIあり）・結合テスト仕様ドラフト"]
        BD --> DD["詳細設計 /detail-design<br/>＋単体テスト観点"]
    end

    DD --> IMP["製造<br/>frontend-coder・backend-coder・infra-coder<br/>→ code-reviewer（Q-01/Q-02・設計記載成果物の実在確認）"]

    subgraph RIGHT["V字右側（検証）"]
        UT["単体テスト"] --> IT["結合テスト"]
        IT --> ST["総合テスト<br/>quality-performance（Q-07）"]
        ST --> UAT["受入支援・移行<br/>migration-specialist /migration-planning"]
    end

    IMP --> TRC["トレーサビリティ突合<br/>画面・IF×実装（leaderゲート）"] --> UT
    UAT --> DEL["納品 /delivery-package<br/>→ 保守 incident-responder"]

    DD -.検証根拠.-> UT
    BD -.検証根拠.-> IT
    REQ -.検証根拠AC.-> ST

    ERD["data-model-specialist<br/>ERD独占管轄 /erd-update"] -.全工程.- BD
    SEC["security-compliance"] -.全工程ゲート.- DEL
    PH["docs/project-phase.md<br/>工程正本・ゲート判定・越境記録"] -.工程移行ごとにleaderが更新.- TRC
```

## 2. ドキュメント正本フロー（誰が作り、誰が照合するか）

```mermaid
flowchart LR
    subgraph STD["docs/standards/（基準の正本）"]
        QCD["qcd-standards.md<br/>Q/C/D 21基準"]
        ASM["assumption-management.md<br/>仮定・Q-IDマーカー"]
        DEV["dev-standards/<br/>開発規約12種 /dev-standards"]
        SECB["ai-security-baseline.md<br/>enterprise-controls.md"]
    end

    subgraph WORK["docs/（案件の正本）"]
        REQD["requirements/ 機能一覧・AC"]
        DESIGN["basic-design/ detail-design/"]
        ERDD["erd/ テーブル定義・CHANGELOG"]
        OQ["open-questions.md（Q-ID台帳）"]
        ADR["decisions/（ADR）"]
        HIST["context-history/LATEST.md"]
    end

    subgraph OUT["deliverables/（出力形式）"]
        XLS["Excel /excel-deliverables"]
        SLD["スライド /slide-deck"]
    end

    QCD --> |合否の照合先| WORK
    DEV --> |実装の照合先| DESIGN
    REQD --> |機能IDトレース| DESIGN --> |項番トレース| ERDD
    OQ --> |仮定マーカー| DESIGN
    WORK --> |変換・体裁| OUT
    WORK --> |決定を外部化| ADR --> HIST
    HIST --> |新セッションの入口| WORK
```

## 3. 運用ループ（日次・週次・月次・四半期）

```mermaid
flowchart TD
    subgraph DAILY["日次"]
        D1["実績記録 C-01<br/>documentation-specialist"] --> D2["pm-sync 同期<br/>外部ツール⇔issues.md"]
        D3["セッション終了5問<br/>（llm-friendly日次版・git衛生込み）"]
    end

    subgraph WEEKLY["週次"]
        W1["QCD週次レポート<br/>estimation・test・quality が実測"] --> W2["leader判定<br/>基準ID引用必須"]
        W2 --> W3["人間承認 → Slack配信"]
        W4["/context-health-check<br/>矛盾・仮定マーカー突合"]
        W5["/llm-friendly-check<br/>人間側・リポジトリ診断"]
        W6["Q-11監査<br/>ai-dev-standardizer"]
    end

    subgraph MONTHLY["月次"]
        M1["/effort-compression<br/>圧縮率計測 C-06/C-07"]
        M2["/context-history 大リセット<br/>（月1）"]
    end

    subgraph QUARTERLY["四半期"]
        Q1["GitHub Actions 棚卸しissue自動起票<br/>MCP死活・プラン機能・形骸化点検"]
    end

    DAILY --> WEEKLY --> MONTHLY --> QUARTERLY
    W2 -->|黄/赤| ESC["エスカレーション<br/>leader → 人間 →（顧客影響）顧客"]
```

## 4. 仮定（曖昧さ）のライフサイクル

```mermaid
flowchart TD
    A["曖昧さ検出<br/>（全エージェント・全工程）"] --> B["起票: Q-ID＋影響範囲（機能ID）<br/>docs/open-questions.md"]
    B --> C{"進行可否<br/>leader判断"}
    C -->|待てる| D["顧客確認へ<br/>期限管理 D-05"]
    C -->|待てない| E["仮定設定<br/>仮決め内容＋爆風半径<br/>（大きければ人間承認）"]
    E --> F["伝播: 作業時に依存箇所へ<br/>【仮定: Q-xxx】マーカー<br/>coder・設計・テストは着手前に<br/>担当機能IDでフィルタ"]
    F --> G["顧客回答（解決）"]
    D --> G
    G --> H{"仮定と一致?"}
    H -->|一致| I["マーカー除去 → クローズ"]
    H -->|不一致| J["巻き戻し: grep Q-xxx で<br/>影響成果物を全件列挙<br/>→ 修正タスク化（issues）"]
    J --> K["修正完了確認<br/>leaderがクローズ"]
    F -.->|2週間放置| L["催促起票<br/>documentation-specialist"]
    E -.->|仮定の上に仮定<br/>3段目| M["人間エスカレーション<br/>（2段まで）"]
```

## 図の保守ルール

- 構成要素（エージェント・スキル・標準）を追加/削除したら、この図も同じPRで更新する（consistency.yml の数量チェックが崩れたら図も疑う）
- 図と各定義ファイルが矛盾した場合は**定義ファイルが正**。図を直す
