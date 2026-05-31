# PLANS.md

計画は、少し複雑な作業を ad hoc に進めないための hard rule として使います。
新機能、少し複雑な変更、複数ファイル / 複数コンポーネント変更、仕様 / 設計 / 契約に影響する変更では、必ず execution plan を作ります。

## 計画の種類

- 小さな変更: 誤字修正、表記揺れ修正、単一行の明白な修正など、挙動と設計判断を変えないもの。会話内の短い計画でよい
- execution plan 必須の変更: 新機能、少し複雑な変更、複数ファイル / 複数コンポーネント変更、仕様 / 設計 / 契約に影響する変更
- 完了後: 同じ plan ファイルを `.aidd/docs/exec-plans/active/` から `.aidd/docs/exec-plans/completed/` に移す

## Lifecycle

1. `.aidd/docs/exec-plans/active/YYYY-MM-DD-short-topic-plan.md` に execution plan を作る
2. 計画レビューまたは利用者との合意を得る
3. 実装と検証を進める
4. 前提、scope、手順が変わったら plan を更新する
5. 完了時に検証結果、残リスク、follow-up を記録する
6. 同じ plan ファイルを `.aidd/docs/exec-plans/completed/` に移す

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
- 完了後は作業用 plan を `.aidd/docs/exec-plans/completed/` に移す
- 長期的に必要な判断履歴は、completed plan だけでなく `.aidd/docs/design-docs/`、`.aidd/RULES.md`、または共有すべき tracked repo docs にも反映する
