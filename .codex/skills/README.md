# .codex/skills

このディレクトリは、本テンプレートの **Codex 用 skill 定義** を置く場所です。
Codex はプロジェクトローカルの `.codex/skills/<name>/SKILL.md` を読み込みます。

## ⚠️ 正本は `.claude/skills/`

ここは [`.claude/skills/`](../../.claude/skills/) の **同期コピー（mirror）** です。
skill の SKILL.md / template.md は Claude Code と Codex で同一形式のため、`.claude/skills/` を
唯一の正本（source of truth）とし、ここへはコピーで反映します。**このディレクトリの skill を直接編集しないでください。**

```bash
# .claude/skills/ の skill ディレクトリを .codex/skills/ へ同期する
make skills-sync
```

skill の追加・編集手順、設計原則、対象 docs は `.claude/skills/README.md` を参照してください。

## 一覧

| skill | 用途 |
| --- | --- |
| `exec-plan` | 新しい exec-plan を `docs/exec-plans/active/` に起票するとき |
| `product-spec` | 新しい product-spec を `docs/product-specs/` に作るとき |
| `adr` | アーキテクチャ決定を記録するとき |
