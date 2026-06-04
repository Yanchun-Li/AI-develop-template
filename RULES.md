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

### 変更レベル（適応型ワークフロー: 柔軟な深さ）

変更の影響範囲に応じて、必要な「準備の深さ」を 3 段階で使い分ける。固定プロセスで小変更を窒息させない / 大変更を素通しさせない、ためのバランス。

| レベル | 対象 | 必要な準備 | 例 |
| --- | --- | --- | --- |
| **L0** | 挙動と設計判断を変えない 1 行修正 | そのまま実装 → commit | typo、表記揺れ、import 並べ替え、コメント修正、明白なローカル変数 rename |
| **L1** | 単一 layer 内の挙動変更 / バグ修正 / 小機能追加 | commit message または PR 説明に **意図 1 行 + 検証コマンド 1 行** | 1 関数のロジック修正、新規 unit test 追加、 1 fixture 拡張、 layer 内 helper 追加 |
| **L2** | 複数 layer をまたぐ / 仕様 / 設計 / 契約 / CI / RULES に影響する変更、新機能 | `docs/exec-plans/active/YYYY-MM-DD-<topic>-plan.md` を起票し承認を得る | 新 endpoint、provider boundary 追加、`[tool.repo-arch]` 変更、新 schema、認証フロー変更、 新規依存追加 |

判断に迷ったら **一段上を選ぶ**。L1 と L2 の境界が読み取れない場合は L2 として扱い、plan を起票して人間に確認する。

### レベル別ルール

- **L0**: 直接編集してよい。検証は `make lint` 1 回で十分。
- **L1**: commit / PR 本文に「なぜこの変更が必要か」「どのコマンドで検証したか」を必ず書く。test の追加が必要なら同じ commit に含める。
- **L2**: 必ず `docs/exec-plans/active/` に plan を起票し、`Review status: approved` になるまで実装に着手しない。実装中に L2 と判明した場合は、その時点で着手を止め plan を起票してから再開する。

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
- 実行計画は `docs/exec-plans/active/`、完了後は同じ計画ファイルを `docs/exec-plans/completed/` に移す
- 古くなった文書は削除するか obsolete を明示する

### Execution Plan Lifecycle

新機能、少し複雑な変更、複数ファイル / 複数コンポーネント変更、仕様 / 設計 / 契約に影響する変更では、次の順番を必ず守る。

1. `docs/exec-plans/active/YYYY-MM-DD-short-topic-plan.md` に実行計画を作る
2. 計画に Objective、Scope、Constraints、Open questions、Implementation steps、Validation steps、Decision log、Follow-up work を書く
3. 計画レビューまたは利用者との合意を得てから実装する
4. 実装中に前提や手順が変わったら、会話だけでなく計画ファイルも更新する
5. 検証後、結果と残リスクを計画に残し、同じファイルを `docs/exec-plans/completed/` に移す

## 9. Validation

変更後は、可能な範囲で次を実行します。

```bash
make lint
make test
```

`make lint` は `scripts/lint_repo_rules.py`（architecture rule）と `ruff check` を回します。
プロジェクト固有の追加コマンドは `README.md` または `docs/WORKFLOW.md` に記録します。

## 10. Human in the Loop

すべての変更に人間レビューを要求すると、AI の速度が活きずレビュアーがボトルネックになる。逆に何もチェックしないと、設計判断が AI に流れて再現性が失われる。**変更の種類ごとに介入の強度を変える** ことで両立する。

### 3 つの介入パターン

| パターン | 何をするか | 適用対象 |
| --- | --- | --- |
| **全件レビュー** | 人間が必ず読んで承認する | `docs/architectures/<kind>.md`、ADR、`docs/exec-plans/completed/` への移動、`[tool.repo-arch]` の変更、`AGENTS.md` / `RULES.md` / `ARCHITECTURE.md` の変更 |
| **スコアベース** | 自動チェック（`make lint` + `make test` + coverage 閾値 + architecture rule）がすべて pass したら人間レビューを 軽量化（diff 確認のみ）または skip | L1 変更（単一 layer 内のバグ修正・小機能・test 追加） |
| **エスカレーション** | AI が自動チェックを実行し、特定の trigger が出たときだけ人間に escalate する | provider boundary 違反、layer 単方向依存違反、新規依存追加、secret らしき文字列の混入、CI runner image 変更 |

### 強制ポイント（trigger 一覧）

次のいずれかに該当した時点で、自動進行を止め人間に確認する。**plan の `Review status: approved` は前提条件であり代替ではない**。

- `[tool.repo-arch].kind` を変更する
- `provider_only.libraries` の値を追加 / 削除する
- `docs/architectures/<kind>.md` の layer 構成 / 禁止事項を変更する
- 新規依存パッケージを追加する（`pyproject.toml` 直接編集 / `uv add` どちらも対象）
- `scripts/lint_repo_rules.py` の検査内容を緩める
- `make lint` / `make test` を skip / `--no-verify` で回避する
- secret / token / private endpoint らしき値を含む変更
- `RULES.md` / `AGENTS.md` / `ARCHITECTURE.md` を変更する

### 適用ルール

- どのパターンが適用されるかは **変更レベル**（§2 の L0 / L1 / L2）と **trigger 該当の有無** で決まる
- L0 + trigger 非該当 → スコアベース（自動チェック pass で進行）
- L1 + trigger 非該当 → スコアベース（PR の diff 確認は推奨）
- L2 または trigger 該当 → 全件レビュー（plan 承認 + 実装後 diff レビュー）
- AI が「これは trigger ではない」と独断で判定しない。判定が曖昧なら一段上のパターンを取る
