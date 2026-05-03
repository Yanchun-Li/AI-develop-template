# Architecture: `web-app`

Web application 向け。SaaS dashboard、admin tool、CRUD app、認証付き業務画面、軽量な full-stack app が典型例。

> 中心は user journey と use case。UI は `usecase` を呼び、DB / external SDK は `data` / `providers` に閉じ込める。
> Next.js / Remix / FastAPI + frontend / Django など、具体 framework は利用先で選ぶ。

## 想定するシステムの形

```text
[ Browser ]
    │
    ▼
[ Route / Server Action ]    (route)
    │
    ├──► [ UI composition ]   (ui)
    │
    ▼
[ UseCase ]                  (usecase)
    │
    ├──► [ Domain rules ]     (domain)
    └──► [ Repository impl ]  (data / providers)
```

## src/ 構成

```text
src/
  contract/        # API schema, form schema, shared DTO, error contract
  domain/          # business rules, entity, value object, policy
  usecase/         # user-facing actions and application orchestration
  data/            # repository implementation, DB mapper, cache adapter
  ui/              # component, view model, form state, client-side state
  route/           # page route, server action, API route, controller
  providers/       # auth, DB client, logging, metrics, external SDK factory
  shared/          # generic helper, result/error type
tests/
```

## Layer Responsibilities

### `contract/`
- request / response schema
- form validation schema
- public error code
- route parameter contract

依存: 無し

### `domain/`
- entity / value object
- business invariant
- policy
- repository port

依存: `contract`

### `usecase/`
- 1 user action = 1 use case
- transaction boundary
- permission check の orchestration
- domain と repository port の合成

依存: `contract`, `domain`

### `data/`
- repository implementation
- ORM / SQL mapper
- cache adapter
- external API adapter

依存: `contract`, `domain`, `usecase`

### `ui/`
- component
- view model
- form state
- loading / empty / error / retry state
- client-side interaction

依存: `contract`, `domain`, `usecase`

### `route/`
- page route
- server action
- API route / controller
- request parsing と response mapping

依存: `contract`, `domain`, `usecase`, `ui`

### `providers/`
- DB client factory
- auth provider
- logging / metrics
- external SDK factory

業務ルールは置かない。

## 機械的に守るルール

`pyproject.toml` の `[tool.repo-arch]` に貼るスニペット：

```toml
[tool.repo-arch]
kind = "web-app"
src = "src"
provider_dirs = ["providers", "data"]

[tool.repo-arch.layers]
contract = []
domain = ["contract"]
usecase = ["contract", "domain"]
data = ["contract", "domain", "usecase"]
ui = ["contract", "domain", "usecase"]
route = ["contract", "domain", "usecase", "ui"]

[tool.repo-arch.provider_only]
libraries = [
    "sqlalchemy",
    "psycopg",
    "redis",
    "boto3",
    "requests",
    "httpx",
    "openai",
    "anthropic",
]
```

## このアーキテクチャでやらないこと

- UI component から DB / external SDK を直接呼ぶ
- route handler に business rule を置く
- form schema と API schema を別々に暗黙管理する
- `data/` の ORM model を domain entity として使う

## やる必要があること

- 壊れてはいけない user journey を `docs/product-specs/` に書く
- loading / empty / error / retry を UI state として定義する
- auth / permission boundary を usecase で明示する
- browser E2E が必要な画面は stable selector を用意する
