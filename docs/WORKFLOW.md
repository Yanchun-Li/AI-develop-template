# WORKFLOW.md

この文書は、AI-driven development を安定運用するための基本ワークフローを定義します。

## 基本方針

- 人間が方針を決め、AI が実行する
- 長い指示を一度に渡すより、短い入口とリポジトリ内知識で進める
- 会話で決まったことは、必要なら docs に戻す
- `AGENTS.md` は百科事典ではなく目次として使う
- GitHub Actions を検証の共有面として使う

## AI にタスクを渡す前に確認すること

1. `pyproject.toml` の `[tool.repo-arch].kind` が選択済みか確認する（`tbd` なら先に選ばせる）
2. タスクの編集範囲を、選択された architecture の layer に当てはめる
3. 仕様が曖昧なら、まず `docs/product-specs/` または関連 docs に前提を書く
4. 大きい変更なら `docs/exec-plans/active/` に計画を書く

## 長時間エージェント向けの入口

長く動く AI は、毎回次の順で文脈を回収する想定です。

1. 現在の作業ディレクトリを確認する
2. ルート `AGENTS.md` を読む
3. `pyproject.toml` の `[tool.repo-arch]` を読み、`docs/architectures/<kind>.md` を読む
4. `ARCHITECTURE.md`（共通ルール）、`RULES.md` を読む
5. `docs/STATUS.md` を読む
6. `docs/product-specs/` と `docs/exec-plans/active/` を読む
7. 関連するコード近傍の README、test を読む
8. CI failure がある場合は、ログと再現コマンドを確認する

## 推奨する repository artifact

- `docs/architectures/`: アーキテクチャ選択肢
- `docs/product-specs/`: 機能仕様
- `docs/exec-plans/active/`: 進行中の実行計画
- `docs/exec-plans/completed/`: 完了済み計画
- `docs/exec-plans/tech-debt-tracker.md`: 既知負債
- `docs/STATUS.md`: 現在の進捗とアーキテクチャ選択
- `docs/CI.md`: CI / ローカル検証の運用

## 変更後チェック

- 変更範囲が依頼された領域に収まっているか
- 仕様や契約を変えた場合に docs が更新されているか
- 実行した検証コマンドを説明できるか
- CI failure がある場合に原因と次 action を説明できるか

## 避けるべきこと

- `AGENTS.md` にすべての背景知識を書くこと
- 他領域の挙動を prompt の中だけで決めること
- リポジトリに残っていない合意を前提に実装を進めること
- CI failure を原因不明のまま放置すること
