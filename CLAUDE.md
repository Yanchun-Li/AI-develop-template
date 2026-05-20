# CLAUDE.md

このプロジェクトのルール・規約・skill インデックスは `AGENTS.md` に集約しています。
Claude Code と Codex の両方が **同じ正本（AGENTS.md）** を読むことで、ツール間の規約ドリフトを防ぎます。
本ファイルは Claude Code がプロジェクト起動時に自動ロードするエントリーポイントで、下記の `@AGENTS.md` import によって AGENTS.md の内容を context に取り込みます。

**規約・ルールの変更は AGENTS.md に対して行ってください。本ファイルにはルール本文を書きません。**

Claude Code 固有の挙動（特定 hook、permission 設定、Claude Code 専用ワークアラウンド）が必要になった場合のみ、下記 import の後ろに追記してください。

@AGENTS.md
