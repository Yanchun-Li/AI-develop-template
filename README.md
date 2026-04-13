# AI-development-template

Harness engineering template for agent-first development.

## Included

- `AGENTS.md` as the top-level map for agents
- `ARCHITECTURE.md` for layer and provider rules
- `docs/` as the repository knowledge base
- `scripts/lint_repo_rules.py` for mechanical architecture checks

## Run The Linter

```bash
python3 scripts/lint_repo_rules.py
```

## Prompt

ログイン機能を追加したい。

要件:
- 既存ユーザーがメールアドレスとパスワードでログインできること
- 成功時はセッションを発行すること
- 失敗時は理由をユーザーに過剰に漏らさないこと
- 一定回数以上失敗したら一時的に制限すること

非要件:
- SNSログインは今回やらない
- パスワード再設定は今回やらない

制約:
- ARCHITECTURE.md の layer rule を守ること
- cross-cutting concern は src/providers/ 経由にすること

作業手順:
- まず AGENTS.md と ARCHITECTURE.md を読む
- docs/exec-plans/active/ に plan を作る
- 必要なら docs/PRODUCT_SENSE.md と docs/SECURITY.md を更新する
- 最後に linter を実行する
