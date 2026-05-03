# Architecture: `mobile-app`

スマホアプリ向け。Flutter、React Native、Kotlin Multiplatform、Swift / Kotlin native などで、画面遷移、端末機能、オフライン状態、権限状態が重要なプロダクトに使う。

> 中心は screen state と use case。端末 API や backend API は `data` / `platform` / `providers` に閉じ込める。

## 想定するシステムの形

```text
[ Screen / Component ]       (presentation)
    │
    ▼
[ UseCase ]                  (usecase)
    │
    ├──► [ Domain rules ]     (domain)
    ├──► [ API repository ]   (data)
    └──► [ Device adapter ]   (platform)
```

## src/ 構成

```text
src/
  contract/        # API DTO, local storage schema, route args, error contract
  domain/          # entity, value object, policy, repository port
  usecase/         # screen-independent application action
  data/            # API client, repository impl, local storage adapter
  presentation/    # screen, component, controller, state machine
  navigation/      # route graph, deep link, tab/shell navigation
  platform/        # camera, biometric auth, push notification, location
  providers/       # DI, logging, analytics, config
  shared/          # generic helper, result/error type
tests/
```

## Layer Responsibilities

### `contract/`
- backend API DTO
- local storage schema
- route argument
- error code / permission state contract

依存: 無し

### `domain/`
- entity / value object
- user-visible business rule
- repository port
- permission / policy model

依存: `contract`

### `usecase/`
- app action
- domain と repository port の orchestration
- retry / timeout / offline fallback の方針

依存: `contract`, `domain`

### `data/`
- API client
- repository implementation
- local storage
- cache
- serialization

依存: `contract`, `domain`, `usecase`

### `presentation/`
- screen
- component
- controller / state holder
- loading / empty / error / retry / permission denied state

依存: `contract`, `domain`, `usecase`

### `navigation/`
- route graph
- deep link
- tab / shell navigation
- auth gate

依存: `contract`, `domain`, `usecase`, `presentation`

### `platform/`
- camera
- biometric auth
- location
- push notification
- file picker
- OS permission adapter

依存: `contract`, `domain`, `usecase`

### `providers/`
- DI
- config
- logging
- analytics
- feature flag

業務ルールは置かない。

## 機械的に守るルール

`pyproject.toml` の `[tool.repo-arch]` に貼るスニペット：

```toml
[tool.repo-arch]
kind = "mobile-app"
src = "src"
provider_dirs = ["providers", "data", "platform"]

[tool.repo-arch.layers]
contract = []
domain = ["contract"]
usecase = ["contract", "domain"]
data = ["contract", "domain", "usecase"]
presentation = ["contract", "domain", "usecase"]
navigation = ["contract", "domain", "usecase", "presentation"]
platform = ["contract", "domain", "usecase"]

[tool.repo-arch.provider_only]
libraries = [
    "requests",
    "httpx",
    "boto3",
    "openai",
    "anthropic",
]
```

## このアーキテクチャでやらないこと

- screen から API client / SDK を直接呼ぶ
- navigation に business rule を置く
- permission state を UI だけの一時条件として扱う
- backend の undocumented response に依存する

## やる必要があること

- screen ごとの state machine を docs に残す
- 初回、再訪、offline、permission denied、retry を設計する
- 端末 API は `platform/` に閉じ込め、usecase から port 経由で呼ぶ
- crash / analytics / performance の観測点を定義する
