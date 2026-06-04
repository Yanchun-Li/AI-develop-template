# AI-driven development template

このリポジトリは、AI エージェントと人間が同じ前提で開発を進めるための個人用 template repository です。

会話履歴ではなくリポジトリ内 markdown、コード構造、CI 結果を一次情報として使い、AI が安全に開発へ参加できる状態を最初から用意します。

## このテンプレートの特徴

- **アーキテクチャを選んで使う**: ML / LLM / Web / mobile から 1 つ選択
- **選択は `pyproject.toml` の `[tool.repo-arch]` が正本**: AI も lint も同じ場所を見る
- **layer 違反を機械的に検査**: `scripts/lint_repo_rules.py` が選択された architecture の制約を CI で強制
- **GitHub 連携は CI まで**: Issue / PR 起票運用は標準化しない

## トップレベル構成

```text
.
├── AGENTS.md                  # AI の入口（目次）
├── ARCHITECTURE.md            # 共通ルール（layer 非依存）
├── RULES.md                   # 実務ルール
├── README.md
├── Makefile
├── pyproject.toml             # [tool.repo-arch] でアーキテクチャ宣言
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
├── src/                       # architecture 選択後に layer を作る
├── tests/
└── .github/workflows/ci.yml
```

## まず読むもの

1. `AGENTS.md`
2. `pyproject.toml` の `[tool.repo-arch]`
3. 選択した `docs/architectures/<kind>.md`（`tbd` なら `index.md`）
4. `ARCHITECTURE.md` と `RULES.md`
5. `docs/STATUS.md`
6. `docs/PRODUCT_SENSE.md`
7. 関連する `docs/product-specs/` と `docs/exec-plans/active/`

## 新しいプロジェクトで最初にやること

1. アーキテクチャを選ぶ — `docs/architectures/index.md` の判断基準で 1 つ決める
2. `pyproject.toml` の `[tool.repo-arch]` を更新（`kind` と `layers` と `provider_only.libraries`）
3. `docs/STATUS.md` の「現在のアーキテクチャ」を更新
4. `src/` 配下に該当 architecture の layer ディレクトリを作成
5. `docs/PRODUCT_SENSE.md` をプロジェクト固有内容で埋める
6. `docs/product-specs/` に最初の機能仕様を書く

## 初期セットアップ

```bash
make init
```

`make init` は `uv sync` で依存を入れ、git hooks を設定します。

## 既存 repo に AIDD overlay を入れる

既にコード構造がある repo には、root template を丸ごと適用せず、local-only overlay を入れます。

```bash
./scripts/aidd-init.sh /path/to/target-repo
```

script を shell の `PATH` に置いた場合は、target repo 直下で引数を省略できます。

```bash
aidd-init.sh
```

作成される構成:

```text
<target-repo>/
├── AGENTS.md
├── CLAUDE.md
└── .aidd/
    ├── RULES.md
    └── docs/
        ├── CI.md
        ├── DESIGN.md
        ├── PLANS.md
        ├── PRODUCT_SENSE.md
        ├── QUALITY_SCORE.md
        ├── RELIABILITY.md
        ├── SECURITY.md
        ├── STATUS.md
        ├── WORKFLOW.md
        ├── adr/
        ├── design-docs/
        ├── exec-plans/
        ├── product-specs/
        └── tasks/
```

`templates/aidd-overlay/` が配布元です。overlay には `docs/architectures/`、hooks、skills、agents、CI workflow は含めません。
`scripts/aidd-init.sh` は既存の `.aidd/` / `AGENTS.md` / `CLAUDE.md` を上書きせず、git repo では `.git/info/exclude` に local overlay path を追加します。
`.aidd/` を template から再同期したい場合だけ `./scripts/aidd-init.sh --force` を使います。

## 検証

```bash
make lint    # architecture rule + ruff
make test    # pytest
```

CI は `.github/workflows/ci.yml` で同じコマンドを回します。詳細は `docs/CI.md`。

## アーキテクチャ選択肢

| kind | 用途 |
| --- | --- |
| `llm-native` | chatbot / agent / RAG / copilot |
| `ml-backend` | 顔認証、画像分類 API、推薦 serving |
| `ml-pipeline` | 自分でモデルを学習する batch / training |
| `web-app` | SaaS dashboard、admin、CRUD、full-stack web app |
| `mobile-app` | スマホアプリ、端末機能、offline、push、位置情報 |

選び方の詳細は `docs/architectures/index.md`。


```text
.
├── .rulesync/
│   └── rules/
│       └── overview.md
├── AGENTS.md
├── CLAUDE.md
├── GEMINI.md
├── ARCHITECTURE.md
├── Makefile
├── README.md
├── docs/                             
│   ├── DESIGN.md                   
│   ├── SECURITY.md
│   ├── RELIABILITY.md
│   ├── WORKFLOW.md                  
│   ├── STATUS.md
│   ├── PRODUCT_SENSE.md
│   ├── PLANS.md
│   ├── FRONTEND.md
│   ├── QUALITY_SCORE.md
│   └── exec-plans/                 
│       ├── active/
│       ├── completed/
│       └── tech-debt-tracker.md
├── mobile/
│   ├── AGENTS.md
│   ├── ARCHITECTURE.md
│   ├── docs/
│   └── src/
├── backend/
│   ├── AGENTS.md
│   ├── ARCHITECTURE.md
│   ├── docs/
│   └── src/
├── ml/
│   ├── docs/
│   ├── match-maker/
│   └── destination-recommender/
├── proto/
└── scripts/
```
