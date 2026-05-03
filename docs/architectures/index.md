# Architectures

このディレクトリには、本テンプレートが選択肢として持つアーキテクチャを 1 つ 1 ファイルで置きます。
プロジェクトはこの中から **1 つだけ** を選び、`pyproject.toml` の `[tool.repo-arch].kind` に書き込みます。

## 選択肢


| kind          | 用途の典型                                         | 主な動詞                                          | HTTP     |
| ------------- | --------------------------------------------- | --------------------------------------------- | -------- |
| `tbd`         | 未選択（テンプレ初期値）                                  | —                                             | —        |
| `llm-native`  | chatbot / agent / RAG / copilot               | `retrieve` / `plan` / `generate` / `eval`     | あってもなくても |
| `ml-backend`  | 顔認証、画像分類 API、推薦 serving など、事前学習モデルを使う backend | `register` / `verify` / `predict`             | 必須寄り     |
| `ml-pipeline` | 自分でモデルを学習する batch / training                  | `train` / `evaluate` / `predict` / `backfill` | 不要       |


## 選び方

タスクが何かではなく **「主要動詞」と「データの流れ」** で選びます。

1. **対話 / 文書生成 / 検索 / agent が中心** なら `llm-native`
2. **HTTP API として model を提供** し、業務ルール（試行制限・監査など）が無視できないなら `ml-backend`
3. **自分でモデルを学習** し batch / scheduled job が中心なら `ml-pipeline`
4. 複数該当する場合は **メインの動詞** で選ぶ。サブ機能は provider / 別 module として吸収する

## 切り替え手順

1. `pyproject.toml` の `[tool.repo-arch]` で `kind` と `[tool.repo-arch.layers]` を選んだ architecture のものに置き換える
2. `docs/STATUS.md` の「現在のアーキテクチャ」を更新する
3. 対応する architecture doc に従って `src/` 配下の layer ディレクトリを作成する
4. `make lint` を回し、layer 違反が無いことを確認する

## 参考

- `index.md`（このファイル）: 選び方
- `llm-native.md`: Compound AI System / RAG / Agent
- `ml-backend.md`: Hexagonal backend with ML adapter
- `ml-pipeline.md`: Layered ML pipeline

