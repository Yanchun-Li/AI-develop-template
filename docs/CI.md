# CI.md

このテンプレートで標準化する GitHub 連携は CI までです。Issue や Pull Request の起票、運用テンプレート、レビューコメント管理は標準範囲に含めません。

## 基本方針

- GitHub Actions を検証の正本にする
- clone 直後に `make init` でローカル環境を作れるようにする
- CI とローカルで同じコマンドを使う
- workflow は最小構成に留め、プロジェクト固有の deploy や release は利用先で追加する

## 標準 CI

`.github/workflows/ci.yml` は次を実行します。

1. Python を `.python-version` に合わせてセットアップする
2. `uv` を固定バージョンでインストールする
3. `uv lock --check` で `pyproject.toml` と `uv.lock` の整合を確認する
4. `uv sync --frozen --all-groups` で依存関係を再現する
5. `make lint` を実行する
6. `make test` を実行する

## ローカルと CI の対応

- 初期化: `make init`
- lock 確認: `make lock-check`
- lint: `make lint`
- test: `make test`

pre-commit hook も `make lint` を呼び、ローカル commit 前と CI の lint 内容を揃えます。

## 追加してよいもの

プロジェクト開始後に必要になった場合だけ追加します。

- deploy workflow
- release workflow
- container build
- secret scan
- coverage upload
- package publish

追加した場合は、この文書と `README.md` の検証手順を更新してください。
