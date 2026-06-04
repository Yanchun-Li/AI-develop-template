# AGENTS.md

このファイルは AI が最初に読む短い目次です。詳細は `docs/` と `RULES.md` に置きます。

## 最初に読む順番

1. `pyproject.toml` の `[tool.repo-arch]` を読み、`kind` の値を確認する
2. `kind` に対応する `docs/architectures/<kind>.md` を読む
   - `kind = "tbd"` の場合は `docs/architectures/index.md`（選び方）を読み、利用者に選択を促す
   - また、kickoff 時は `grill-with-docs` skill を起動し、現在のフェーズ（探索 / 意思決定 / 本番化 / 運用）と使うアプローチ（Vibe Coding / SDD / AIDD）を利用者と擦り合わせる。AI 単独で判断しない
3. `ARCHITECTURE.md`（共通ルール）
4. `RULES.md`
5. `docs/STATUS.md`
6. `docs/PRODUCT_SENSE.md`
7. 関連する `docs/product-specs/` と `docs/exec-plans/active/`

## フェーズ / アプローチを使い分ける

新規プロジェクトと既存プロジェクトのフェーズ移行時に、AI は静的設定を読むのではなく `grill-with-docs` で利用者と対話して確定する。

| フェーズ | 使うアプローチ | 主な出力 |
| --- | --- | --- |
| 探索（`kind = "tbd"` 含む） | Vibe Coding | スパイク、PRODUCT_SENSE 初稿 |
| 意思決定 | SDD（Spec-Driven） | architectures / ADR / product-specs |
| 本番化 | AIDD（plan → 質問 → 承認 → 実装） | layer 実装 + test |
| 運用 | AIDD + L1 はスコアベース HITL（`RULES.md §10`） | バグ修正 / 機能追加 |

擦り合わせるべき質問の典型:

- このプロジェクト（または今回の作業）は捨てる前提のスパイクか、続ける前提か
- 現時点で確定している契約 / スキーマはあるか
- 最初の deploy 想定はいつか（= 本番化フェーズに入る時期）
- 人間が承認する変更の範囲はどこまでか（`RULES.md §10` の HITL trigger に追加すべき項目）

grill の結果は会話に残さず、必要に応じて ADR / `docs/PRODUCT_SENSE.md` / `docs/exec-plans/active/` に書き戻す。

## アーキテクチャ選択の扱い

- リポジトリの aрхитектура は `[tool.repo-arch].kind` が正本
- `kind = "tbd"` の間は実装に着手せず、まず利用者に選択を確認する
- AI が独断で `kind` を変更しない
- 一度選んだら、`docs/architectures/<kind>.md` の layer 構造と禁止事項を厳密に守る

## 編集範囲

- 依頼で指定されたファイル / ディレクトリを優先する
- 編集範囲が曖昧な場合は、関連 docs と `src/` 配下の選択済み layer から最小範囲を選ぶ
- layer 境界を変更する場合は、先に `docs/architectures/<kind>.md` を更新する
- 共通ルールを変更する場合は `ARCHITECTURE.md` と `RULES.md` を更新する

## 共有 docs の役割

- `docs/architectures/`: アーキテクチャ選択肢（1 つ選んで使う）
- `docs/PRODUCT_SENSE.md`: プロダクト意図
- `docs/product-specs/`: 機能仕様
- `docs/STATUS.md`: 現在の進捗とアーキテクチャ選択
- `docs/exec-plans/active/`: 進行中の作業計画
- `docs/exec-plans/completed/`: 完了済みの作業計画
- `docs/WORKFLOW.md`: AI 運用手順
- `docs/CI.md`: CI とローカル検証の運用

## Agents と Skills（2 軸で整理）

AI 設定は **agents（誰に任せるか）** と **skills（どう進めるか）** の 2 軸で置く。
Claude Code / Codex の両方が同じものを使えるよう、配置を対称にしている。

| 軸 | 中身 | Claude Code | Codex |
| --- | --- | --- | --- |
| **agents** | 役割ベースの subagent 定義（`agency-agents` 由来） | `.claude/agents/<slug>.md` | `.codex/agents/<slug>.toml` |
| **skills** | 文書を書く / 手順を踏む方法論 | `.claude/skills/<name>/SKILL.md` | `.codex/skills/<name>/SKILL.md` |

- **agents**: 計 28 体。slug（ファイル名）は `.claude/agents/` と `.codex/agents/` で完全一致させる。
  選定理由と一覧は各ディレクトリの `README.md` を参照。これらはルート雛形（新規プロジェクト用）に同梱する。
- **skills**: 正本は `.claude/skills/`。`.codex/skills/` はその同期コピーで、`make skills-sync` で反映する
  （`.codex/skills/` の skill を直接編集しない）。
- **スコープ**: 既存リポジトリ向けの AIDD overlay 配布物（`templates/aidd-overlay/`）には agents/skills を
  含めない（`docs/exec-plans/completed/2026-05-31-aidd-overlay-installer-plan.md` の Non-Goal）。
- **subagent ルール**: 原則 `1 subagent = 1 primary 定義`（Claude Code は `.md`、Codex は `.toml`）。
  複数観点が必要なら subagent を分ける（例: `ui-designer` -> `accessibility-auditor` -> `code-reviewer`）。
  agent / skill 定義を変更したら、各ツールを再起動して再読み込みする。

## 重要ルール

- 会話よりリポジトリ内 markdown とコードを正とする
- `AGENTS.md` に詳細を書きすぎず、知識は `docs/` に残す
- 期待した参照先が見つからなければ、不整合として報告する
- 新機能、少し複雑な変更、複数ファイル / 複数コンポーネント変更では、必ず `docs/exec-plans/active/` に実行計画を置く
- 実行順序は active plan 作成 -> レビュー / 合意 -> 実装 / 検証 -> `docs/exec-plans/completed/` へ移動
- 未確定の仕様や技術選定（特に `[tool.repo-arch].kind`）を AI が勝手に固定しない
- `docs/PRODUCT_SENSE.md` が `TBD` のままの間は、プロダクト前提を AI が推測しない

## 文書を書く / 更新するとき

新規 markdown 文書を作るときは、対応する skill を使う。skill 定義の正本は `.claude/skills/<name>/SKILL.md`
に置き、Codex 用に `.codex/skills/<name>/SKILL.md` へ同期する（`make skills-sync`）。

- 新しい exec-plan を作る → `.claude/skills/exec-plan/`
- 新しい product-spec を作る → `.claude/skills/product-spec/`
- アーキテクチャ決定を記録する（ADR） → `.claude/skills/adr/`
- 既存 docs の更新 → 対象ファイルの frontmatter と既存構造に従う

更新ポリシー:

- **Immutable**（書いた後は基本変更しない）: `docs/architectures/`, `docs/exec-plans/completed/`, ADR
  - 修正が必要な場合は新ファイルを作り、旧ファイルの frontmatter を `status: superseded` に変更し、`superseded_by` で新ファイルへリンクする
- **Living**（継続更新する）: `docs/STATUS.md`, `docs/PRODUCT_SENSE.md`, `docs/product-specs/`, `docs/exec-plans/active/`
  - 直接更新可。更新時に `last_verified` を当日日付に更新する
