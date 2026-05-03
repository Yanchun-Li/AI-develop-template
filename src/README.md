# src

このディレクトリの中身は、選択したアーキテクチャに応じて変わります。

`pyproject.toml` の `[tool.repo-arch].kind` を見て、対応する `docs/architectures/<kind>.md` の `src/` 構成に従ってディレクトリを作成してください。

| kind | 主な layer |
| --- | --- |
| `tbd` | （未選択。`docs/architectures/index.md` を参照） |
| `llm-native` | `contract / retrieval / tool / prompt / agent / eval / pipeline / entrypoint / providers / shared` |
| `ml-backend` | `domain / usecase / handler / infra / providers / shared` |
| `ml-pipeline` | `schema / feature / model / evaluation / pipeline / entrypoint / providers / shared` |

## 共通ルール

- 上位 layer は下位 layer のみを import できる（許可関係は `pyproject.toml` の `[tool.repo-arch.layers]`）
- vendor SDK / 外部ライブラリの直接 import は `providers/` か `infra/` に閉じ込める（`[tool.repo-arch.provider_only].libraries`）
- `notebooks/` と `experiments/` から `src/` の import は OK、逆は禁止

機械的検査は `make lint`（`scripts/lint_repo_rules.py` + `ruff check`）で実行されます。
