---
name: adr
description: アーキテクチャ決定を docs/adr/ に immutable な文書として記録するときに使う。技術選定、layer 境界の変更、データモデルの方向転換、外部依存の追加方針、deploy / runtime 構成、データの所有権境界など、後から覆すコストが高い判断で必須。一度書いたら基本変更しない（推翻された場合は新 ADR で supersede）。「ADR を書いて」「この決定を残して」「設計判断を記録」「アーキテクチャ決定を記録」「technical decision の log を残したい」のような依頼で起動する。日々の実装判断やバグ修正方針には使わない。
---

# adr

アーキテクチャ決定 (Architecture Decision Record) を記録するスキル。
ADR は **Immutable** — 一度 `accepted` になったら本文を書き換えない。決定が覆された場合は、**新しい ADR を立てて旧 ADR の status を `superseded` に変える**。
理由: 後から ADR を読む人（半年後の自分含む）は「なぜそう決めたか」を知りたい。書き換えると意図の履歴が失われ、過去の検討プロセスが消える。

## いつ ADR を書くか

書く対象（=後から覆すコストが高い判断）:

- 技術選定（DB、auth、LLM provider、major framework）
- layer 境界の変更（ARCHITECTURE.md / architectures/ に影響する変更）
- データモデル / 所有権の方向転換
- 外部依存の追加方針（特に provider 経由のルール）
- deploy / runtime 構成（マルチリージョン、IaC 方針）
- 横断ルールの変更（ログ規約、エラー規約、命名規約）

書かない対象:

- 日々の実装判断（変数名、関数分割、CSS の整理）
- バグ修正の方針（exec-plan で扱う）
- 一時的なワークアラウンド（commit message と TODO で十分）

判断に迷ったら: 「この決定を 6 ヶ月後に新規メンバーが疑問に思った場合、本人の説明なしに ADR だけで納得できるべきか？」がイエスなら書く。

## やること

1. `docs/adr/NNNN-<short-topic>.md` を新規作成する。
   - `NNNN` は 4 桁ゼロパディングの連番（`docs/adr/` 配下の最大番号 + 1）
   - slug は kebab-case、ASCII、決定の本質を 2〜5 単語で
   - 例: `0001-use-firestore-as-primary-store.md`, `0007-replace-rest-with-graphql.md`
2. 同ディレクトリの `template.md` の内容をコピーして埋める。
3. `docs/adr/README.md` の索引表に新規エントリを追加する。
4. 初回は `status: proposed` で起票。review 後に `accepted` に変える。
5. 書き終えたら「チェックリスト」を確認してから review に出す。

## セクション別ガイド

### Title

- 形式: `NNNN. <短い決定の要約>`
- 能動態 / 命令形で書く。決定そのものを書く（「採用する」「やめる」「置き換える」など）
- OK 例: `0001. Firestore を primary store として採用する`
- NG 例: `0001. データストアについて`（決定が読み取れない）

### Status

- `proposed` — レビュー中
- `accepted` — 採用。**以降本文を変更しない**
- `superseded` — 別の ADR で置き換えられた（`superseded_by` を埋める）
- `deprecated` — 採用していたが廃止。新しい ADR を立てるほどでもない場合

status 変更時は frontmatter の `status` を更新するだけ（本文は変えない）。`accepted` → `superseded` の場合は `superseded_by: docs/adr/MMMM-<slug>.md` も埋める。

### Context

- **なぜ今この決定が必要か** を書く。
- 現状の制約、関係者、トリガーとなった事象を含める。
- 読み手が「この決定が何を解こうとしているか」を本人の説明なしに理解できること。
- 単なる「現状の説明」で終わらせない — 「だから今決める必要がある」まで書く。

### Decision

- **何を決めたか** を明確に書く。
- 1〜3 段落。能動態。決定そのものを最初の文で書く。
- 「迂回する書き方」（「検討した結果」「いろいろ考えると」）を排除して、結論を先頭に置く。

### Consequences

- 決定の **positive と negative の両方を必ず書く**。片方しか書かないと「やる前提の自己正当化文書」になる。
- できれば `neutral / 未確定` も書く（時間が経てば判明する事項）。
- 観測可能・測定可能な事実を含める。

### Alternatives Considered

- **最低 2 案**。
- 各案に **却下理由** を書く。曖昧形容詞は禁止。
- 却下理由には **観測可能な事実 / 測定可能な値 / 既存 docs への参照** を含める。
- OK 例: 「PostgreSQL JSONB は採用可能だが、対応する managed service を本プロジェクトの infra コストポリシー（月 ¥10,000 上限）に収められない」
- NG 例: 「微妙な気がする」「将来困りそう」

## チェックリスト

書き終えたら自分で確認してから review に出す。

- [ ] Title が能動態で、決定の本質を 1 行で表している
- [ ] Status が `proposed` で起票されている
- [ ] Context が「現状」だけでなく「だから今決める必要がある」まで書いている
- [ ] Decision の最初の文に結論が書かれている（迂回表現がない）
- [ ] Consequences に positive と negative が両方書かれている
- [ ] Alternatives Considered が 2 案以上あり、各却下理由が観測可能な事実を含む
- [ ] frontmatter の `adr_id`, `status`, `date`, `deciders` が埋まっている
- [ ] 連番が `docs/adr/` 内で重複していない
- [ ] `docs/adr/README.md` の索引表に追加した
- [ ] 「将来的に」「いずれ」「多分」「微妙」が本文に存在しない

## アンチパターン

| パターン | 修正方針 |
| --- | --- |
| Title が名詞句で決定が読み取れない | 能動態 / 命令形で書く |
| Decision が長い前置きから始まる | 結論を最初の文に置く |
| Consequences が positive のみ | negative を必ず書く（無い場合は「Negative: 既知の負面は無い（理由）」と明示） |
| Alternatives の却下理由が形容詞のみ | 観測可能な事実 / 数値 / 参照リンクで根拠を示す |
| accepted の ADR を後から書き換える | 新 ADR を立てて旧 ADR を `superseded` にする |
| 日々の実装判断を ADR にする | コミットメッセージ / コードコメント / exec-plan で扱う |
| Context が「現状の説明」だけ | 「だから今決める必要がある」まで書く |

## Supersede の手順（決定を覆すとき）

1. 新しい ADR を起票（次の連番）。
2. 新 ADR の frontmatter に `supersedes: docs/adr/NNNN-<old-slug>.md` を書く。
3. 旧 ADR の frontmatter:
   - `status: superseded`
   - `superseded_by: docs/adr/MMMM-<new-slug>.md`
   - **本文は変更しない**
4. `docs/adr/README.md` の索引表で旧 ADR の Status 列を `superseded` に更新。

## 関連

- `docs/adr/README.md`: ADR 一覧と運用ルール
- `ARCHITECTURE.md`: 共通アーキテクチャルール（ADR で覆す場合はここを参照する）
- `docs/architectures/<kind>.md`: アーキテクチャ選択（kind 変更時は ADR を起票する）
- `AGENTS.md`「文書を書く / 更新するとき」: ADR は Immutable 文書として扱う
- `.claude/skills/exec-plan/`: ADR の決定を実装する plan は別途起票
- `.claude/skills/product-spec/`: 機能の意図は spec、構造の判断は ADR
