# .claude/agents

このディレクトリは、本テンプレート（および本テンプレートから作る新規プロジェクト）向けの
**Claude Code subagent 定義（`.md`）** を置く場所です。`agency-agents` 由来の AIDD（AI 駆動開発）
関連エージェントを、Claude Code がそのまま `.md` + YAML frontmatter 形式で読めるよう配置しています。

Codex 用の同一セット（`.toml`）は [`.codex/agents/`](../../.codex/agents/) にあり、
**slug（ファイル名）は両者で完全一致** します。追加・削除するときは両方を揃えてください。

## agents と skills の使い分け

- **agents**（このディレクトリ）= 役割ベースの subagent 定義。「誰に任せるか」。
  - Claude Code: `.claude/agents/<slug>.md` / Codex: `.codex/agents/<slug>.toml`
- **skills**（[`.claude/skills/`](../skills/)）= 特定文書を書く/手順を踏む方法論。「どう進めるか」。
  - Claude Code: `.claude/skills/<name>/SKILL.md` / Codex: `.codex/skills/<name>/SKILL.md`（`.claude/skills` の同期コピー）

## スコープ（重要）

- ここはルート雛形（新規プロジェクト用）に同梱する agents です。本テンプレートから作る
  プロジェクトはこの 28 体を最初から使えます。
- 既存リポジトリ向けの **AIDD overlay 配布物（`templates/aidd-overlay/`）には agents/skills を
  含めません**（`docs/exec-plans/active/2026-05-31-aidd-overlay-installer-plan.md` の Non-Goal）。

## 一覧（計 28 体）

| 区分 | エージェント |
| --- | --- |
| Product / PM | `product-manager`, `senior-project-manager` |
| UX / Design | `ux-researcher`, `ux-architect`, `ui-designer` |
| Architecture | `software-architect`, `backend-architect` |
| Implementation | `frontend-developer`, `ai-engineer`, `data-engineer`, `database-optimizer`, `rapid-prototyper`, `minimal-change-engineer` |
| Code 理解 / VCS | `codebase-onboarding-engineer`, `git-workflow-master` |
| Quality / Review | `code-reviewer`, `evidence-collector`, `reality-checker`, `test-results-analyzer` |
| Testing | `api-tester`, `accessibility-auditor`, `performance-benchmarker` |
| Release / Ops | `devops-automator`, `sre`, `security-engineer` |
| Docs / Tooling | `technical-writer`, `tool-evaluator` |
| Orchestration | `agents-orchestrator` |

> 補足: `senior-developer`（Laravel/Livewire/Three.js などフレームワーク特化）は汎用テンプレートに
> 不向きなため除外しています。プロジェクトのスタックが固まった後、必要なら `agency-agents` から追加してください。

## 使い方（Claude Code）

```
Use the Code Reviewer agent to review this diff.
Activate Backend Architect and design the API for X.
```

`1 subagent = 1 primary 定義` を原則とします（複数観点が必要なときは subagent を分ける）。
詳細は [`AGENTS.md`](../../AGENTS.md) の「Agents と Skills」を参照。

## 追加・更新の手順

1. `agency-agents`（`/Users/s30000/Projects/agency-agents`）から対象を選ぶ。
2. Claude Code 用: `.md` を `.claude/agents/<slug>.md` にコピー（clean slug にリネーム）。
3. Codex 用: `integrations/codex/agents/<name>.toml` を `.codex/agents/<slug>.toml` にコピー。
4. 両ディレクトリで slug が一致していることを確認する。
5. この README と `.codex/agents/README.md` の一覧を更新する。
6. Claude Code / Codex を再起動して再読み込みする。

## ソースとライセンス

`agency-agents` 由来で、同リポジトリの MIT ライセンス下にあります。
このディレクトリの [`LICENSE.agency-agents`](./LICENSE.agency-agents) を参照してください。
