# QUALITY_SCORE.md

品質は見える化し、時間とともに追跡できる状態にします。

## スコア基準

- `Q0`: 未定義、または未検証
- `Q1`: happy path のみ成立
- `Q2`: 基本的な検証がある
- `Q3`: 通常利用で信頼できる
- `Q4`: 強い自動検証と観測性がある

## 領域ごとの記録

各業務領域、各アーキテクチャ層ごとに品質を記録します。

例:

| Area | Score | Notes | Next action |
| --- | --- | --- | --- |
| identity/application | Q1 | 成功経路のみ想定 | 失敗系と権限不足を追加する |
| billing/interface | Q2 | 基本テストあり | webhook retry を検証する |
| recommendation/evaluation | Q0 | 評価指標未定義 | offline metric を決める |

## 更新タイミング

- MVP scope を変更したとき
- production に影響する障害や regression が起きたとき
- CI / E2E / monitoring を追加したとき
- AI agent に大きな実装を任せる前後
