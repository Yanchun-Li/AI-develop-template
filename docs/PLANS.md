# PLANS.md

計画は、作業中の補助として使います。テンプレート自体には、個別作業の plan を完了後に残しません。

## 計画の種類

- 小さな変更: タスク説明の短い計画でよい
- 中規模以上の変更: 必要に応じて `docs/exec-plans/active/` に一時 markdown を作る
- 完了後: 個別作業の plan は削除し、永続化が必要な判断だけを該当 docs に反映する

## 計画テンプレート

各 execution plan には次を含めます。

1. Objective
2. Scope
3. Constraints
4. Open questions
5. Implementation steps
6. Validation steps
7. Decision log
8. Follow-up work

## ルール

- 計画は具体的で実行可能にする
- 現実が変わったら計画も更新する
- 完了後は作業用 plan を残さない
- 長期的に必要な判断履歴は、plan ではなく `docs/design-docs/`、`ARCHITECTURE.md`、`RULES.md` などの正本へ移す
