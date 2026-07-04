# フィーチャーチーム運用標準（機能別FE/BEスクワッド）

機能ドメイン単位でFE/BEをペアにした「スクワッド」を組み、並列開発する運用モード。
中規模以上（機能ドメイン3つ以上・並行開発が必要）で発動する。/project-init の決定表から適用。

## 構成

```
スクワッド〈認証〉 : backend-coder-auth ＋ frontend-coder-auth（＋必要なら batch/report専任）
スクワッド〈受注〉 : backend-coder-order ＋ frontend-coder-order
スクワッド〈請求〉 : backend-coder-billing ＋ frontend-coder-billing
─────────────────────────────────────────────
共有（複製禁止）  : leader / code-reviewer / api-designer / data-model-specialist /
                    architecture-guardian / security-compliance / documentation-specialist /
                    quality-performance / ai-dev-standardizer
```

### スクワッド専任エージェントの作り方（複製テンプレ）

`backend-coder.md` をコピーして `backend-coder-<domain>.md` を作り、frontmatter と冒頭に以下だけ追記する（本文は書き換えない — 原本との差分を最小に保つ）:

```markdown
## ドメイン専任設定
- 担当ドメイン: <ドメイン名>（機能ID: F-0XX〜F-0YY）
- 熟知すべき正本: docs/basic-design/<domain>/ / docs/detail-design/<domain>/ / 関連ADR一覧
- 越境禁止: 他ドメインのコード・共通部品の変更は提案のみ（変更は共通部品の所有スクワッドまたはarchitecture-guardian判断）
```

## 複製禁止ルール（フィーチャーチーム化の失敗はここで起きる）

横断エージェントを複製すると一貫性が壊れるため**禁止**:
- **data-model-specialist**: ERDは全ドメイン共有の一枚。スクワッドごとに持つと整合性が死ぬ
- **code-reviewer**: レビュー基準がドメインごとに割れる（規約の方言化）
- **api-designer**: スクワッド間IFの中立な審判。どちらかの所属にしない
- 開発規約（docs/standards/dev-standards/）はチーム間共有の生命線。ドメイン別の追補は「規約への追記」として一元管理し、別ファイルの方言を作らない

## IF契約ファースト（FE/BE並列化の要）

スクワッド内のFE/BEを並列で走らせるための順序:

1. **api-designer がIF定義を先に固定**（項目・型・エラーコードまで。「実装しながら決める」禁止）
2. IF定義からモック/スタブを生成（FE はモックAPIで、BE はIFテストで、互いを待たずに実装）
3. **統合ポイントを機能IDごとに設定**（両者完了時に実IF疎通 → IF定義との突合を code-reviewer が確認）
4. IF変更が必要になったら実装を止めて api-designer 経由で改版（勝手に「実装に合わせてIFを直す」の禁止。改版は両側の作業影響を確認してから）

## 並列実行の運用（Claude Code上）

- スクワッドのFE/BEはAgentの並列呼び出し（またはworktree分離）で同時進行できる
- **直列必須の作業**: ERD/テーブル変更（data-model-specialist独占）・共通部品の変更・規約改訂。並列中にこれらが発生したら該当スクワッドは停止して報告
- 統合の頻度: 最低でも機能ID完了ごと。長期並走での「ビッグバン統合」を禁止

## マネジメント（人間から見える形）

- 進捗はD-01（成果物完了基準）を機能ID単位で集計 → そのまま**スクワッド別進捗**になる（/pm-syncでタスク管理ツールのボードに対応付け可能）
- leader の横断調整はスクワッド間の依存（共通部品・IF・ERD）に集中する。スクワッド内はスクワッドに任せる
- QCD週次レポートにスクワッド別の内訳行を追加（遅いスクワッドの特定→原因分析）
- スクワッドの組み替え（応援）はコンテキスト引き継ぎコストが高い。組み替え前に該当ドメインの /context-history 更新を必須とする

## 解除条件

- ドメイン間依存が想定より強く、調整コストが並列効果を食う場合はスクワッドを統合する（テーラリング記録に残す）
- 保守フェーズ移行時は専任を解除し、原本エージェント構成に戻す（専任定義ファイルは削除せず agents.disabled へ）
