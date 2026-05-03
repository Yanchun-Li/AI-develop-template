# Architecture: `ml-pipeline`

自分でモデルを学習し、batch / scheduled job で予測を生成する系。
レコメンデーション、需要予測、ranking、credit scoring、scoring 系 ML プロダクトが典型例。

> Layered ML Architecture（Google "Hidden Technical Debt in ML Systems" 系の系譜）。
> 純関数の Hexagonal core + Pipeline 層 + IO Adapters。

## 想定するシステムの形

```text
[ raw data ]
    │
    ▼
[ feature engineering ]     ── 純関数
    │
    ▼
[ model train / predict ]   ── 純関数（fit / predict）
    │
    ▼
[ evaluation ]              ── metric、誤差分析
    │
    ▼
[ artifact / output ]       ── model registry、prediction store
```

orchestrator（Airflow / Prefect / Dagster / 自前 CLI）から `entrypoint/` の関数が呼ばれる。

## src/ 構成

```text
src/
  schema/          # 特徴量、ラベル、出力スキーマの契約
  feature/         # 特徴量エンジニアリング（純関数 / 決定的）
  model/           # モデル定義、fit / predict、ハイパラ
  evaluation/      # metric、CV split、誤差分析
  pipeline/        # train / predict / eval を組み合わせる orchestration
  entrypoint/      # CLI / job entrypoint（orchestrator から呼ばれる）
  providers/
    data/          # parquet / BQ / S3 / feature store adapter
    registry/      # MLflow / W&B / 自前 artifact store
    tracking/      # experiment tracking adapter
    logging/
  shared/
notebooks/         # 探索（src/ を import OK、逆は禁止）
experiments/       # ad-hoc 実験 script
```

## Layer Responsibilities

### `schema/`
- 特徴量名・型・単位の契約
- ラベル定義、target spec
- prediction の出力契約

依存: 無し

### `feature/`
- 特徴量計算（純関数、決定的）
- IO は持たない（読み込みは `pipeline/` の役目）

依存: `schema`

### `model/`
- モデル定義（sklearn / lightgbm / pytorch wrapper）
- `fit` / `predict` ラッパ
- ハイパラ定義

依存: `schema`

### `evaluation/`
- metric 計算
- CV split / train-test split logic
- 誤差分析、segment analysis

依存: `schema`、`model`

### `pipeline/`
- 「読む → 特徴量 → 学習 → 評価 → 保存」の組み立て
- IO はここで `providers/` 経由で行う
- 業務判断は持たない（feature / model / evaluation の合成のみ）

依存: `schema`、`feature`、`model`、`evaluation`、`providers`

### `entrypoint/`
- CLI（`python -m ...`）
- orchestrator から呼ばれる関数（task として登録される）
- `pipeline/` を呼ぶだけの薄い層

依存: `pipeline`

### `providers/`
- データ IO（parquet、BQ、S3、feature store）
- model registry（MLflow、W&B）
- experiment tracking
- vendor SDK の直接 import はここに閉じ込める

## 機械的に守るルール

`pyproject.toml` の `[tool.repo-arch]` に貼るスニペット：

```toml
[tool.repo-arch]
kind = "ml-pipeline"
src = "src"

[tool.repo-arch.layers]
schema = []
feature = ["schema"]
model = ["schema"]
evaluation = ["schema", "model"]
pipeline = ["schema", "feature", "model", "evaluation"]
entrypoint = ["schema", "pipeline"]

[tool.repo-arch.provider_only]
libraries = [
    "boto3",
    "google.cloud",
    "snowflake",
    "psycopg",
    "sqlalchemy",
    "mlflow",
    "wandb",
    "feast",
]
```

## このアーキテクチャでやらないこと

- `feature/` / `model/` で IO（純関数を保つ）
- `notebooks/` / `experiments/` を `src/` から import（禁止）
- 業務判断を `pipeline/` に持ち込む（feature / model / evaluation 側に移す）
- experiment の手作業実行（必ず `entrypoint/` 経由で再現可能に）

## やる必要があること

- すべての run に config + git commit + 入力 data hash を紐付ける（traceability）
- offline metric の閾値を `evaluation/` で定義し、CI で regression 検出
- artifact 名に config hash / commit を焼き込む
- `notebooks/` の更新は research → production への昇格手順を docs に残す
