# Project-Scoped Codex Agents

このディレクトリは、本テンプレート（および本テンプレートから作る新規プロジェクト）向けの
**Codex subagent 定義（`.toml`）** を置く場所です。`agency-agents`
（`/Users/s30000/Projects/agency-agents/integrations/codex/agents`）由来の AIDD 関連エージェントを配置しています。

Claude Code 用の同一セット（`.md`）は [`.claude/agents/`](../../.claude/agents/) にあり、
**slug（ファイル名）は両者で完全一致** します。追加・削除するときは両方を揃えてください。

## スコープ（重要）

- ここはルート雛形（新規プロジェクト用）に同梱する agents。
- 既存リポジトリ向けの AIDD overlay 配布物（`templates/aidd-overlay/`）には agents/skills を
  **含めません**（overlay installer プランの Non-Goal）。

## 選定（計 28 体）

汎用テンプレート向けに、AIDD ワーク（計画→設計→実装→レビュー→テスト→リリース→運用→文書）で
広く使う役割を選定。

- Product / PM: `product-manager`, `senior-project-manager`
- UX / Design: `ux-researcher`, `ux-architect`, `ui-designer`
- Architecture: `software-architect`, `backend-architect`
- Implementation: `frontend-developer`, `ai-engineer`, `data-engineer`, `database-optimizer`, `rapid-prototyper`, `minimal-change-engineer`
- Code 理解 / VCS: `codebase-onboarding-engineer`, `git-workflow-master`
- Quality / Review: `code-reviewer`, `evidence-collector`, `reality-checker`, `test-results-analyzer`
- Testing: `api-tester`, `accessibility-auditor`, `performance-benchmarker`
- Release / Ops: `devops-automator`, `sre`, `security-engineer`
- Docs / Tooling: `technical-writer`, `tool-evaluator`
- Orchestration: `agents-orchestrator`

> `sre.toml` は `agency-agents` の `sre-site-reliability-engineer.toml`、
> `senior-project-manager.toml` は同 `senior-project-manager.toml` を slug 統一のためリネームして配置。
> `senior-developer`（フレームワーク特化）は汎用テンプレートに不向きなため除外。

## agents と skills

- agents（このディレクトリ）= 役割定義。Codex は `.codex/agents/*.toml` を読む。
- skills = 手順ワークフロー。Codex はプロジェクトローカルの `.codex/skills/<name>/SKILL.md` を読む。
  正本は [`.claude/skills/`](../../.claude/skills/) で、`make skills-sync` で同期する。

エージェント定義を変更したら、このリポジトリ root から Codex を再起動して再読み込みしてください。

## ソースとライセンス

`agency-agents` 由来で、同リポジトリの MIT ライセンス下にあります。
このディレクトリの `LICENSE.agency-agents` を参照してください。
