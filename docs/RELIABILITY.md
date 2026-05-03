# RELIABILITY.md

信頼性要件は、AI が検証できる具体さで書く必要があります。

## 指針

- 性能目標は測定可能な閾値にする
- 起動、停止、復旧の期待値を定義する
- 可能な限り、ログ、メトリクス、トレースで検証できる形にする
- retry、timeout、fallback、degraded mode は仕様として扱う
- background job や async workflow は失敗状態を観測できるようにする

## 設計時に決めること

- どの操作が失敗してもよいか
- どの操作は必ず一貫性を保つべきか
- retry してよい操作と、重複実行が危険な操作はどれか
- ユーザーに見せる失敗と、内部で回復する失敗をどう分けるか
- GitHub Actions や runtime monitoring で何を検知するか

## 例

- service startup completes under a fixed threshold
- key user journeys stay under latency budgets
- no critical background job fails silently
- inference fallback is recorded with stable event names
