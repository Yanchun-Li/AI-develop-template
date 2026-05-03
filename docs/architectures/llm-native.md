# Architecture: `llm-native`

LLM を中心に、retrieval / tool / agent を組み合わせて応答を生成するシステム向け。
chatbot、agent、copilot、RAG、semantic search が典型例。

> Berkeley AI Research の "Compound AI Systems"（2024）が定着させた語彙。

## 想定するシステムの形

```text
[ User input ]
    │
    ▼
[ Query understanding ]   ── prompt + LLM
    │
    ▼
[ Router / Planner ]
    │
    ├──► [ Retrieval ]    ── BM25 / vector / hybrid
    ├──► [ Tool: SQL ]    ── 構造化データ取得
    └──► [ Tool: API ]    ── 外部 service
    │
    ▼
[ Answer synthesis ]      ── prompt + LLM
    │
    ▼
[ Eval / Guardrail ]      ── hallucination check, citation check
```

## src/ 構成

```text
src/
  contract/        # query / response の schema、tool 定義契約
  retrieval/       # BM25 / vector / SQL retriever（純関数）
  tool/            # LLM が呼べる tool 群（純関数 / 副作用最小）
  prompt/          # prompt template、version 管理、partial
  agent/           # LLM 呼び出し orchestration（state machine）
  eval/            # offline eval、regression test、guardrail
  pipeline/        # query → answer の組み立て
  entrypoint/      # CLI（API は backend が書く想定なら不要）
  providers/
    llm/           # OpenAI / Anthropic / Bedrock adapter
    vector/        # pgvector / Qdrant
    sql/           # 既存 DB へのクエリ
    tracking/      # LangSmith / Langfuse
  shared/
notebooks/         # 探索（src/ を import OK、逆は禁止）
experiments/       # ad-hoc な prompt 実験
```

## Layer Responsibilities

### `contract/`
- query / response の Pydantic / dataclass schema
- tool 引数 / 戻り値の型定義
- prompt 入出力契約

依存: 無し（最下層）

### `retrieval/`
- BM25 / vector / hybrid retriever
- reranker
- 純関数として書く（IO は `providers/` 経由）

依存: `contract`、`providers`

### `tool/`
- LLM の function calling から呼べる tool
- SQL query 実行、API 呼び出し、計算 helper
- 副作用を最小化、決定論的に書く

依存: `contract`、`providers`

### `prompt/`
- prompt template 文字列
- partial / few-shot example
- version 管理（ファイル名 / git で）

依存: `contract` のみ（IO 禁止）

### `agent/`
- LLM 呼び出しの state machine（LangGraph 流 or 自前）
- routing / planning logic
- tool / retrieval を組み合わせる

依存: `contract`、`prompt`、`retrieval`、`tool`、`providers/llm`

### `eval/`
- offline eval（質問セット → 期待応答のチェック）
- guardrail（hallucination、citation、PII）
- regression test 用の fixture

依存: `contract`、`retrieval`、`tool`、`agent`

### `pipeline/`
- query → answer の合成
- streaming / non-streaming の組み立て
- agent と eval を組み合わせる

依存: 上記すべて

### `entrypoint/`
- CLI（`python -m ...`）
- API handler を自分で書くなら追加

依存: `pipeline`

### `providers/`
- 横断 IO 具象（LLM SDK、vector DB、SQL DB、tracking）
- vendor SDK の直接 import はここに閉じ込める

## 機械的に守るルール

`pyproject.toml` の `[tool.repo-arch]` に貼るスニペット：

```toml
[tool.repo-arch]
kind = "llm-native"
src = "src"

[tool.repo-arch.layers]
contract = []
retrieval = ["contract"]
tool = ["contract"]
prompt = ["contract"]
agent = ["contract", "prompt", "retrieval", "tool"]
eval = ["contract", "retrieval", "tool", "agent"]
pipeline = ["contract", "retrieval", "tool", "prompt", "agent", "eval"]
entrypoint = ["contract", "pipeline"]

[tool.repo-arch.provider_only]
libraries = ["openai", "anthropic", "boto3", "psycopg", "sqlalchemy", "qdrant_client"]
```

## このアーキテクチャでやらないこと

- 業務 entity の Aggregate / Repository pattern（過剰）
- 大きな単一 prompt にロジックを詰め込む（agent layer で state machine に分解する）
- LLM 呼び出しを `pipeline` 以外から直接行う（必ず `agent` 経由）
- `prompt/` から外部 IO（LLM 呼び出しは `agent` の役目）

## やる必要があること

- prompt の version 管理（git のファイル単位で十分）
- eval の自動回帰（CI で daily / per-PR）
- LLM の出力を schema validation する（`contract/` の型に通す）
- tracking（LangSmith / Langfuse / 自前）でリクエスト全件を残す
