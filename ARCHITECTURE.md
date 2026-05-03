# ARCHITECTURE.md

このリポジトリは、**プロジェクトごとに 1 つのアーキテクチャを選んで使う** テンプレートです。
このファイル自体はアーキテクチャ非依存の **共通ルール** を定義し、選択肢の中身は `docs/architectures/` に置きます。

## 選択メカニズム

1. 利用者は `docs/architectures/` から 1 つを選ぶ
2. `pyproject.toml` の `[tool.repo-arch]` に値を書き込む（`kind`、`layers`、`provider_only.libraries`）
3. `docs/STATUS.md` の「現在のアーキテクチャ」を更新する
4. `src/` 配下に該当 architecture の layer ディレクトリを作る
5. AI / lint は `[tool.repo-arch]` を読み、選ばれた architecture の制約を適用する

選択前は `kind = "tbd"`。この間は layer の機械検査は skip されますが、後述の **共通ルール** はすべて適用されます。

## 選択肢

| kind | 用途 | 詳細 |
| --- | --- | --- |
| `llm-native` | chatbot / agent / RAG / copilot | `docs/architectures/llm-native.md` |
| `ml-backend` | 顔認証、画像分類 API、推薦 serving | `docs/architectures/ml-backend.md` |
| `ml-pipeline` | 自分でモデルを学習する batch / training | `docs/architectures/ml-pipeline.md` |
| `web-app` | SaaS dashboard / admin / CRUD / full-stack web app | `docs/architectures/web-app.md` |
| `mobile-app` | スマホアプリ / 端末機能 / offline / push | `docs/architectures/mobile-app.md` |

選び方の判断基準は `docs/architectures/index.md` を参照してください。

## 共通ルール（全 architecture に適用）

### 1. Schema-first / Contract-first

`schema/` または `contract/` に相当する layer を最下層に置き、データ・API・prompt の契約を最初に固定します。
**コードより先に契約を書く**。これがどの architecture でも崩せない出発点です。

### 2. Layer は単方向依存

```text
最下層（schema / domain / contract）
  ↑
中間層（feature / model / usecase / agent ...）
  ↑
最上層（pipeline / handler / entrypoint）
```

- 上位 layer は下位 layer を import できる
- 下位 layer は上位 layer を import **できない**
- 実際の許可関係は `pyproject.toml` の `[tool.repo-arch.layers]` で宣言する
- `scripts/lint_repo_rules.py` がこの関係を機械的に検査する

### 3. Provider Boundary

vendor SDK や外部ライブラリ（`openai`、`sqlalchemy`、`boto3` など）は、`providers/` または `infra/` 内のモジュールに **import を閉じ込める**。

- 業務 layer から vendor SDK を直接 import しない
- 必要なら provider 側で port / adapter を提供し、業務 layer はそれだけを参照する
- 該当ライブラリは `[tool.repo-arch.provider_only].libraries` に列挙し、lint で強制する

### 4. Pure / Side-effect の分離

- 計算ロジック（feature / model / retrieval / tool / domain rule）は **純関数寄り** に書く
- IO（DB、API、LLM、ファイル）は `pipeline/` か `entrypoint/` か `infra/` から行う
- 純関数 layer から IO を呼ぶことを禁止する（lint では検査しない、レビュー観点）

### 5. Research / Experiment の片方向 import

`notebooks/` と `experiments/` は `src/` を import してよい。
逆（`src/` が `notebooks/` を import する）は **絶対に禁止**。
これを破ると本番コードが notebook 依存になり、再現性が壊れる。

### 6. 機械的検証

```bash
make lint
make test
```

`make lint` は `scripts/lint_repo_rules.py` と `ruff check` を回す。
CI（`.github/workflows/ci.yml`）でも同じコマンドを回すので、ローカルと CI で結果が揃う。

## 共通の禁止事項

- `domain` / `schema` / `contract` 相当の最下層から framework / DB / vendor SDK を import
- 同じ vendor library が複数の非 provider ファイルで直接 import されている
- prompt / 業務ルール / モデルしきい値を、コミットされていないノート上に置く
- `src/` 内のファイルから `notebooks/` または `experiments/` への import

## アーキテクチャを切り替える / 増やす場合

1. 新しい architecture を `docs/architectures/<new-kind>.md` として書く（既存 3 ファイルがテンプレート）
2. 切り替える場合は `[tool.repo-arch]` を書き換え、`docs/STATUS.md` を更新
3. `src/` 配下を新 layer 構成に移植
4. `make lint` で違反が無いか確認
