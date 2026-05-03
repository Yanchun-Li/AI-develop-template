# Architecture: `ml-backend`

事前学習済みモデル（自前 fine-tune を含む）を **API として serve する** backend 向け。
顔認証、画像分類 API、推薦 serving、embedding lookup が典型例。

> 中心は backend 設計。ML は 1 つの adapter に過ぎない。
> Hexagonal / Clean Architecture が素直にフィットする領域。

## 想定するシステムの形

```text
[ Client ]
    │
    ▼
[ HTTP / gRPC Handler ]      (interface)
    │
    ▼
[ UseCase: Verify / Predict ] (application)
    │
    ├──► [ Domain rules ]      (domain)  ── しきい値、再試行、ロックアウト
    ├──► [ Model adapter ]     (infra)   ── face embedding / classifier
    ├──► [ Vector store ]      (infra)   ── pgvector / Qdrant
    └──► [ Audit log ]         (infra)
```

## src/ 構成

```text
src/
  domain/          # 業務ルール（しきい値、状態遷移、不変条件）
  usecase/         # register / verify / predict など、ユースケース単位
  handler/         # HTTP / gRPC / CLI handler（薄い層）
  infra/           # model adapter、vector store、DB、外部 API
  providers/       # logging、metrics、tracing、secret manager
  shared/          # Result / Error 型、汎用 helper
tests/
```

複数 ML problem を 1 リポジトリで扱う場合は、`src/domains/<context>/{domain,usecase,handler,infra}` のように bounded context を 1 階層挟みます。

## Layer Responsibilities

### `domain/`
- 業務ルール（顔認証なら：類似度しきい値、N 回失敗で lock、生体情報の保管期間）
- value object（embedding vector の型、score の単位）
- repository / model port（抽象 interface）

依存: 無し（framework / SDK 直接 import 禁止）

### `usecase/`
- 1 use case = 1 module（`register_user_face.py`、`verify_user_face.py`）
- domain と port を組み合わせる orchestration
- transaction 境界の宣言

依存: `domain`

### `infra/`
- model adapter（InsightFace / Rekognition / Bedrock の wrapper）
- vector store adapter（pgvector / Qdrant client）
- DB / cache / audit log の具象実装
- 外部 SDK の直接 import はここに閉じ込める

依存: `domain`、`usecase`（インターフェース実装）

### `handler/`
- HTTP（FastAPI など）/ gRPC / CLI handler
- request schema → usecase 入力 への変換
- usecase 出力 → response schema への変換

依存: `domain`、`usecase`

### `providers/`
- 横断的なインフラ関心事（logging、metrics、tracing、secret manager）
- 業務ルールは置かない

## 機械的に守るルール

`pyproject.toml` の `[tool.repo-arch]` に貼るスニペット：

```toml
[tool.repo-arch]
kind = "ml-backend"
src = "src"

[tool.repo-arch.layers]
domain = []
usecase = ["domain"]
infra = ["domain", "usecase"]
handler = ["domain", "usecase"]

[tool.repo-arch.provider_only]
libraries = [
    "fastapi",
    "starlette",
    "grpc",
    "sqlalchemy",
    "psycopg",
    "redis",
    "boto3",
    "qdrant_client",
    "openai",
    "anthropic",
]
```

## このアーキテクチャでやらないこと

- model 呼び出しを `usecase` 以下から直接（必ず `infra` の port 経由）
- `domain` で framework / DB / SDK を import
- `handler` から `infra` を直接呼ぶ（必ず `usecase` 経由）
- 業務ルールを HTTP schema や ORM model に閉じ込める

## やる必要があること

- model の version / hash を audit log に残す
- 監査ログ（誰が何を verify したか）を必ず取る
- 生体情報 / PII の保管ポリシーを `domain/` の中に明文化
- model 推論の latency / accuracy を metrics で監視
- model 差し替え時の互換性チェック（embedding 次元、score 分布）
