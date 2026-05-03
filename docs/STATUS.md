# STATUS.md

この文書は、AI が着手前に確認するための軽量な進捗メモです。

## 現在のアーキテクチャ

- `kind`: `tbd`
- 正本: `pyproject.toml` の `[tool.repo-arch].kind`
- 選択肢一覧: `docs/architectures/index.md`

`tbd` のうちは、AI は実装に着手せず、利用者にアーキテクチャ選択を促すこと。

## 現在の目的

- AI-driven development template として、アーキテクチャを選んで使えるスケルトンを提供する

## 現在の状態

- アーキテクチャ選択メカニズム（`pyproject.toml` + `docs/architectures/`）を導入済み
- 共通ルール（`ARCHITECTURE.md`）と architecture 別 layer 構成が分離済み
- 検証は `make lint` / `make test`、CI は `.github/workflows/ci.yml`
- プロダクト固有の内容（`docs/PRODUCT_SENSE.md`、`docs/product-specs/`）は利用開始時に埋める

## 次に AI がやるとよいこと

- 利用者にアーキテクチャ選択を確認する（`llm-native` / `ml-backend` / `ml-pipeline` / `web-app` / `mobile-app`）
- 選択後に `[tool.repo-arch]` と本ファイルの「現在のアーキテクチャ」を更新する
- `docs/PRODUCT_SENSE.md` をプロジェクト固有内容で埋める
- `docs/product-specs/` に最初の機能仕様を書く
