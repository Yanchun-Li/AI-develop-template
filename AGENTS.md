# AGENTS.md

このファイルは AI が最初に読む短い目次です。詳細は `docs/` と `RULES.md` に置きます。

## 最初に読む順番

1. `pyproject.toml` の `[tool.repo-arch]` を読み、`kind` の値を確認する
2. `kind` に対応する `docs/architectures/<kind>.md` を読む
   - `kind = "tbd"` の場合は `docs/architectures/index.md`（選び方）を読み、利用者に選択を促す
3. `ARCHITECTURE.md`（共通ルール）
4. `RULES.md`
5. `docs/STATUS.md`
6. `docs/PRODUCT_SENSE.md`
7. 関連する `docs/product-specs/` と `docs/exec-plans/active/`

## アーキテクチャ選択の扱い

- リポジトリの aрхитектура は `[tool.repo-arch].kind` が正本
- `kind = "tbd"` の間は実装に着手せず、まず利用者に選択を確認する
- AI が独断で `kind` を変更しない
- 一度選んだら、`docs/architectures/<kind>.md` の layer 構造と禁止事項を厳密に守る

## 編集範囲

- 依頼で指定されたファイル / ディレクトリを優先する
- 編集範囲が曖昧な場合は、関連 docs と `src/` 配下の選択済み layer から最小範囲を選ぶ
- layer 境界を変更する場合は、先に `docs/architectures/<kind>.md` を更新する
- 共通ルールを変更する場合は `ARCHITECTURE.md` と `RULES.md` を更新する

## 共有 docs の役割

- `docs/architectures/`: アーキテクチャ選択肢（1 つ選んで使う）
- `docs/PRODUCT_SENSE.md`: プロダクト意図
- `docs/product-specs/`: 機能仕様
- `docs/STATUS.md`: 現在の進捗とアーキテクチャ選択
- `docs/exec-plans/active/`: 進行中の作業計画
- `docs/WORKFLOW.md`: AI 運用手順
- `docs/CI.md`: CI とローカル検証の運用

## 重要ルール

- 会話よりリポジトリ内 markdown とコードを正とする
- `AGENTS.md` に詳細を書きすぎず、知識は `docs/` に残す
- 期待した参照先が見つからなければ、不整合として報告する
- 大きい変更の前には `docs/exec-plans/active/` を更新する
- 未確定の仕様や技術選定（特に `[tool.repo-arch].kind`）を AI が勝手に固定しない
- `docs/PRODUCT_SENSE.md` が `TBD` のままの間は、プロダクト前提を AI が推測しない
