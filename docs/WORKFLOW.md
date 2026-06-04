# WORKFLOW.md

この文書は、AI-driven development を安定運用するための基本ワークフローを定義します。

## 基本方針

- 人間が方針を決め、AI が実行する
- 長い指示を一度に渡すより、短い入口とリポジトリ内知識で進める
- 会話で決まったことは、必要なら docs に戻す
- `AGENTS.md` は百科事典ではなく目次として使う
- GitHub Actions を検証の共有面として使う

## コアメンタルモデル: 計画 → 質問 → 承認 → 実装

AI 駆動開発の基本サイクルは 4 ステップ。1 ステップでも飛ばすと plan の質が落ちる。

```text
[人間: 意図を伝える]
       ↓
[AI: 計画を起草する]              ← docs/exec-plans/active/ に書く
       ↓
[AI: 前提・曖昧さ・選択肢を能動的に質問する]  ← Open Questions / 代替案として明示
       ↓
[人間: 質問に答えて plan を承認する]
       ↓
[AI: 承認された plan のみに従って実装する]
       ↓
[人間: 検証結果を確認する] → 必要なら 計画 に戻る
```

### 各ステップの責務

| ステップ | 担当 | 出力 | 飛ばすと起きること |
| --- | --- | --- | --- |
| **計画** | AI | `docs/exec-plans/active/<...>-plan.md` | 思いつきベースの実装、後戻り |
| **質問** | AI | plan 内の `[OPEN]` ラベル、代替案、Non-Goals | 前提のズレが実装後に発覚する、無駄な書き直し |
| **承認** | 人間 | plan の `Review status: approved` | AI の独断、設計判断の漏れ |
| **実装** | AI | コード + 検証ログ | （承認なしの実装は禁止） |

### 「質問」フェーズの重要性

このテンプレートで最も省略されやすいのが **質問** フェーズ。AI が plan を書いたあと、すぐ承認に進まず、**先に AI から能動的に質問を投げさせる**。

質問する典型ポイント:

- 仕様の境界（「ここまで実装するで合っているか」「Non-Goals の認識合わせ」）
- 代替案の選択（「A 案 / B 案のどちらを取るか」+ 各案の trade-off）
- 既存契約への影響（「この変更は既存 API の互換性を壊すが許容するか」）
- 実装順序（「先にスキーマを切るか、先に provider boundary を引くか」）

`.claude/skills/exec-plan/` の Open Questions / 代替案 / Non-Goals セクションは、すべてこの質問フェーズのための器。空欄のまま実装に進まない。

### 自動化への階段

この 4 ステップは、最終的に **「質問」と「承認」を Slack 等の最小操作に圧縮する** ことで自動化に向かう。今のフェーズではまず 4 ステップを愚直に回し、回数を重ねてから自動化の対象を決める。

## AI にタスクを渡す前に確認すること

1. `pyproject.toml` の `[tool.repo-arch].kind` が選択済みか確認する（`tbd` なら先に選ばせる）
2. タスクの編集範囲を、選択された architecture の layer に当てはめる
3. 仕様が曖昧なら、まず `docs/product-specs/` または関連 docs に前提を書く
4. 新機能、少し複雑な変更、複数ファイル / 複数コンポーネント変更なら `docs/exec-plans/active/` に計画を書く
5. 計画レビューまたは利用者との合意が終わるまで実装に進まない

## Execution Plan Lifecycle

新機能、少し複雑な変更、複数ファイル / 複数コンポーネント変更、仕様 / 設計 / 契約に影響する変更では、次の順番を守ります。

1. `docs/exec-plans/active/YYYY-MM-DD-short-topic-plan.md` に実行計画を作る
2. 計画レビューまたは利用者との合意を得る
3. 実装と検証を進め、前提が変わったら計画を更新する
4. 完了時に検証結果と残リスクを記録し、同じファイルを `docs/exec-plans/completed/` に移す

## 長時間エージェント向けの入口

長く動く AI は、毎回次の順で文脈を回収する想定です。

1. 現在の作業ディレクトリを確認する
2. ルート `AGENTS.md` を読む
3. `pyproject.toml` の `[tool.repo-arch]` を読み、`docs/architectures/<kind>.md` を読む
4. `ARCHITECTURE.md`（共通ルール）、`RULES.md` を読む
5. `docs/STATUS.md` を読む
6. `docs/product-specs/` と `docs/exec-plans/active/` を読む
7. 関連するコード近傍の README、test を読む
8. CI failure がある場合は、ログと再現コマンドを確認する

## 推奨する repository artifact

- `docs/architectures/`: アーキテクチャ選択肢
- `docs/product-specs/`: 機能仕様
- `docs/exec-plans/active/`: 進行中の実行計画
- `docs/exec-plans/completed/`: 完了済み計画
- `docs/exec-plans/tech-debt-tracker.md`: 既知負債
- `docs/STATUS.md`: 現在の進捗とアーキテクチャ選択
- `docs/CI.md`: CI / ローカル検証の運用

## 変更後チェック

- 変更範囲が依頼された領域に収まっているか
- 仕様や契約を変えた場合に docs が更新されているか
- 実行した検証コマンドを説明できるか
- CI failure がある場合に原因と次 action を説明できるか

## 避けるべきこと

- `AGENTS.md` にすべての背景知識を書くこと
- 他領域の挙動を prompt の中だけで決めること
- リポジトリに残っていない合意を前提に実装を進めること
- CI failure を原因不明のまま放置すること
