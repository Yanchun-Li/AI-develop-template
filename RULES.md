# RULES.md

このファイルは、リポジトリ全体の実務ルールです。`AGENTS.md` は入口、`RULES.md` は変更時の判断基準、`docs/` は長期知識として扱います。

## 1. Source of Truth

- 会話よりリポジトリ内 markdown とコードを正とする
- 仕様、契約、設計判断、既知負債は prompt だけに残さず docs に戻す
- 不整合を見つけたら、黙って補完せず、修正するか報告する
- AI が未確定事項を勝手に決定しない。決めた場合は decision log に残す

## 2. Change Scope

- 依頼で指定された編集範囲を優先する
- 編集範囲が曖昧な場合は、関連 docs とコード構造から最小範囲を選ぶ
- 他コンポーネントの変更が必要な場合は、まず docs に依存関係として記録する
- 共有契約、横断ルール、CI 運用、品質基準を変える場合はルート `docs/` と `RULES.md` を更新する
- 大きい変更や複数コンポーネント変更の前には `docs/exec-plans/active/` を追加または更新する

## 3. Architecture

- リポジトリのアーキテクチャは `pyproject.toml` の `[tool.repo-arch].kind` が正本
- `kind` 選択前（`tbd`）は実装に着手せず、利用者に選択を確認する
- 選択後は `docs/architectures/<kind>.md` の layer 構成と禁止事項を厳密に守る
- コンポーネント間は documented contract で接続する
- 業務ロジックを framework、vendor SDK、transport schema に閉じ込めない
- 外部 SDK や横断ライブラリは provider 経由で扱う（`[tool.repo-arch.provider_only].libraries` で強制）
- layer 境界 / 共通ルールを変える場合は `ARCHITECTURE.md` と関連 docs を更新する

## 4. CI-driven Validation

- GitHub 連携は CI までを標準範囲にする
- Issue や Pull Request の起票運用はテンプレートに含めない
- CI failure はログを確認して原因を特定してから修正する
- ローカルの `make lint` / `make test` と CI の検証内容を揃える

## 5. Quality

- MVP でも「とりあえず動く」だけのコードで終わらせない
- happy path だけでなく、失敗、空状態、再試行、権限不足、タイムアウトを扱う
- 重要な挙動はテスト、lint、型検査、architecture check のいずれかで検証可能にする
- テストのためだけに production domain を歪めない。必要ならテスト側で正規化する
- dead branch を削除する場合は、primary path を別テストで pin できているか確認する

## 6. Dependency / Supply Chain

- 新規依存は目的、代替案、運用リスクを docs に記録する
- バージョンは lock file と整合させる
- secret、token、private endpoint、個人情報をコミットしない
- install script を実行する依存や実行時に外部コードを取得する依存は慎重に扱う

## 7. Observability

- 重要な user journey、API、job、inference はログやメトリクスで状態を追えるようにする
- ログは安定した event name と、人間が読める原因情報を持たせる
- 機微情報や payload 全量をログに出さない
- fallback、degraded mode、retry は docs と観測ポイントをセットで設計する

## 8. Documentation Hygiene

- `AGENTS.md` に詳細を書きすぎない
- 長期知識は `docs/` に残す
- 機能仕様は `docs/product-specs/` に置く
- 実行計画は `docs/exec-plans/active/`、完了後は `docs/exec-plans/completed/` に移す
- 古くなった文書は削除するか obsolete を明示する

## 9. Validation

変更後は、可能な範囲で次を実行します。

```bash
make lint
make test
```

`make lint` は `scripts/lint_repo_rules.py`（architecture rule）と `ruff check` を回します。
プロジェクト固有の追加コマンドは `README.md` または `docs/WORKFLOW.md` に記録します。
