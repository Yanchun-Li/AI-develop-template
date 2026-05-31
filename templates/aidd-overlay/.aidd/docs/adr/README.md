# Architecture Decision Records (ADR)

このディレクトリは本プロジェクトの **アーキテクチャ決定** を時系列で残す場所です。

## 性質

- ADR は **Immutable** — 一度 `accepted` になったものは本文を変更しません
- 決定が覆された場合は、**新しい ADR を作って旧 ADR の status を `superseded` に変えます**
- 理由: 後から読む人（半年後の自分含む）が「なぜそう決めたか」と「検討した代替案」を辿れること

## ファイル名

```text
NNNN-<short-topic>.md
```

- `NNNN` は 4 桁ゼロパディングの連番（`0001`, `0002`, ...）
- slug は kebab-case、ASCII、決定の本質を 2〜5 単語で
- 例:
  - `0001-use-firestore-as-primary-store.md`
  - `0002-adopt-hexagonal-architecture-for-backend.md`
  - `0007-replace-rest-with-graphql.md`

連番は採番した時点で予約します（誰かが先に `accepted` にしても番号は重複させない）。

## Status 遷移

| Status | 意味 |
| --- | --- |
| `proposed` | レビュー中。本文の修正が許される |
| `accepted` | 採用。**以降本文を変更しない** |
| `superseded` | 別の ADR で置き換えられた（`superseded_by` を埋める） |
| `deprecated` | 採用していたが廃止。新しい ADR を立てるほどでもない場合 |

status 変更時は frontmatter の `status` を更新するだけで、本文は変更しません。

## 書き方

`.claude/skills/adr/SKILL.md` を使う。Claude Code は「ADR を書いて」「設計判断を記録」のような依頼から自動 trigger する。Codex の場合は AGENTS.md の指針に従い、`.claude/skills/adr/SKILL.md` を明示的に読んでテンプレを使う。

## いつ ADR を書くか

書く対象（=後から覆すコストが高い判断）:

- 技術選定（DB、auth、LLM provider、major framework）
- layer 境界の変更
- データモデル / 所有権の方向転換
- 外部依存の追加方針
- deploy / runtime 構成
- 横断ルール（ログ規約、エラー規約、命名規約）の変更

書かない対象:

- 日々の実装判断
- バグ修正の方針（exec-plan で扱う）
- 一時的なワークアラウンド

判断に迷ったら: 「この決定を 6 ヶ月後に新規メンバーが疑問に思った場合、本人の説明なしに ADR だけで納得できるべきか？」がイエスなら書く。

## Supersede の手順

1. 新しい ADR を起票（次の連番）
2. 新 ADR の frontmatter に `supersedes: .aidd/docs/adr/NNNN-<old-slug>.md` を書く
3. 旧 ADR の frontmatter:
   - `status: superseded`
   - `superseded_by: .aidd/docs/adr/MMMM-<new-slug>.md`
   - **本文は変更しない**
4. 下記「索引」で旧 ADR の Status 列を更新

## 索引

| ID | タイトル | Status | Date |
| --- | --- | --- | --- |
| _未登録_ | | | |
