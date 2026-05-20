# .claude/skills

このディレクトリは、本プロジェクトの Claude Code 用 skill 定義を置く場所です。
skill は AI が **特定の文書を書く / 更新する** ときの方法論をまとめたものです。
チーム全員が同じ規約で文書を書けるよう、`.claude/skills/` は **git 管理対象** とし、`.gitignore` に入れません。

## 一覧

| skill | 用途 |
| --- | --- |
| `exec-plan` | 新しい exec-plan を `docs/exec-plans/active/` に起票するとき |
| `product-spec` | 新しい product-spec を `docs/product-specs/` に作るとき |
| `adr` | アーキテクチャ決定を記録するとき |

## ディレクトリ構造

```text
.claude/skills/
├── README.md              # このファイル
└── <skill-name>/
    ├── SKILL.md           # スキル定義（必須）
    └── template.md        # 文書テンプレート（任意）
```

## skill を追加する手順

1. `.claude/skills/<skill-name>/SKILL.md` を作る。
2. frontmatter に `name` と `description` を書く。
   - `name`: kebab-case のスキル名（ディレクトリ名と一致）
   - `description`: いつこの skill が起動すべきかを具体的に書く。trigger 例（「○○を作って」など）を必ず含める
3. SKILL.md 本文には以下を載せる:
   - なぜこの skill があるか
   - やること（手順）
   - 各セクションの書き方ガイド
   - 書く時のチェックリスト
   - アンチパターン
   - 関連リンク
4. 必要に応じて `template.md` を作り、SKILL.md から参照する。
5. この README.md の「一覧」表に追加する。
6. `AGENTS.md` の「文書を書く / 更新するとき」セクションを更新する。

## 設計原則（全 skill 共通）

- **日本語で書く**（テンプレート例含む）。プロジェクト文書の言語と揃え、生成時の語彙ドリフトを防ぐ
- **`description` は trigger 場面を具体的に書く**。Claude Code が正しく load 判断できるように
- **接口 / 型は code block で書き、散文での field 説明を禁止する**
- **代替案には観測可能な事実に基づく却下理由を書く**（「複雑」「微妙」のような曖昧形容詞は不可）
- **書き終えた後の checklist を必ず付ける**
- **アンチパターンを明示する**。よくある悪い書き方を先に列挙して防ぐ

## skill が触る docs

- `docs/exec-plans/active/`: exec-plan の起票先
- `docs/exec-plans/completed/`: 実装完了後の置き場（exec-plan は削除せず必ずここへ移動）
- `docs/product-specs/`: product-spec
- `docs/adr/`: ADR（`adr` skill 導入時に併せて作成）

## 既存テンプレートとの関係

`docs/product-specs/feature-template.md` などには簡略版の旧テンプレートが残っている。
新しい文書は **skill のテンプレートが正本** とし、既存テンプレートは段階的に skill 側へ寄せる。
矛盾が生じた場合は skill を優先する。
