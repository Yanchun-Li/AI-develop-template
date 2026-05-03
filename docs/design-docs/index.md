# 設計ドキュメント一覧

このディレクトリには、人間と AI の両方にとって長期的に意味を持つ設計知識を置きます。

## 文書一覧

- `core-beliefs.md`: agent-first 開発の基本思想
- `repo-topology.md`: アーキテクチャ選択型のリポジトリ構造（meta）
- `../architectures/`: アーキテクチャ選択肢ごとの構造と layer
- `../WORKFLOW.md`: AI 駆動開発の基本ワークフロー
- `../CI.md`: GitHub Actions / CI 運用

## ルール

- 複数領域に影響する判断は design docs に残す
- 文書は簡潔に保ち、関連コードや計画にリンクできる状態にする
- 古くなった文書は、黙って放置せず obsolete を明示する
