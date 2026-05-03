# リポジトリ構成

このテンプレートは、**プロジェクトごとに 1 つのアーキテクチャを選んで使う** 形を取ります。
具体的な layer 構成は `docs/architectures/<kind>.md` に書いてあり、ここでは **どの architecture でも共通の骨格** だけを定義します。

## ルートの骨格（architecture 非依存）

```text
.
├── AGENTS.md                  # 入口（目次）
├── ARCHITECTURE.md            # 共通ルール（layer 非依存）
├── RULES.md                   # 実務ルール
├── README.md
├── Makefile
├── pyproject.toml             # [tool.repo-arch] でアーキテクチャを宣言
├── uv.lock
├── docs/
│   ├── architectures/         # アーキテクチャ選択肢
│   ├── design-docs/
│   ├── product-specs/
│   ├── exec-plans/
│   ├── STATUS.md
│   ├── PRODUCT_SENSE.md
│   ├── WORKFLOW.md
│   ├── CI.md
│   ├── DESIGN.md
│   ├── RELIABILITY.md
│   ├── SECURITY.md
│   └── QUALITY_SCORE.md
├── scripts/
│   └── lint_repo_rules.py     # [tool.repo-arch] を読んで layer 違反を検査
├── src/                       # architecture 選択後に layer を作る
├── tests/
└── .github/workflows/ci.yml
```

## src/ の中身は architecture 依存

`src/` 配下は、`pyproject.toml` の `[tool.repo-arch].kind` に応じて構造が変わります。
詳細は対応する architecture doc を参照してください。

| kind | src/ の主な layer | 詳細 |
| --- | --- | --- |
| `tbd` | （未選択） | `docs/architectures/index.md` |
| `llm-native` | `contract / retrieval / tool / prompt / agent / eval / pipeline / entrypoint / providers` | `docs/architectures/llm-native.md` |
| `ml-backend` | `domain / usecase / handler / infra / providers` | `docs/architectures/ml-backend.md` |
| `ml-pipeline` | `schema / feature / model / evaluation / pipeline / entrypoint / providers` | `docs/architectures/ml-pipeline.md` |

## 構成を決める原則

- AI が担当境界を構造から理解できること
- 人間が変更範囲をレビューしやすいこと
- 仕様、実装、テスト、運用知識の距離が遠すぎないこと
- 境界変更が `ARCHITECTURE.md`、`docs/architectures/<kind>.md`、`pyproject.toml` の 3 か所で揃うこと

## エージェントの基本フロー

1. ルート `AGENTS.md` を読む
2. `pyproject.toml` の `[tool.repo-arch].kind` を読む
3. `docs/architectures/<kind>.md` を読む（`tbd` なら `index.md` を読む）
4. `ARCHITECTURE.md`（共通ルール）と `RULES.md` を読む
5. 関連するコード近傍の README、test を読む
6. 複数 layer にまたがる前提があれば、対応する `docs/architectures/<kind>.md` を更新する
