---
plan_id: YYYY-MM-DD-<short-topic>
status: active
review_status: pending
created: YYYY-MM-DD
last_verified: YYYY-MM-DD
owner: <name or role>
related_specs:
  - docs/product-specs/<file>.md
affected_modules:
  - src/<path>
superseded_by:
---

# <Topic> Plan

## Goal

技術的に何を変えるかを 3 行以内で書く。ビジネス価値は書かない。

## Non-Goals

最低 2 項目。今回やらないことを具体的に書く。

- ...
- ...

## 影響範囲

### files_to_modify

- `path/to/file.py` — なぜ修正するか

### files_to_create

- `path/to/new_file.py` — 何を担う新ファイルか

### files_to_delete

- `path/to/obsolete.py` — なぜ削除可能か（代替先を必ず添える）

## 実装ステップ

### Step 1: <action verb で始める>

- 内容:
- 完了条件:
- 検証方法:

### Step 2:

- 内容:
- 完了条件:
- 検証方法:

### Step 3:

- 内容:
- 完了条件:
- 検証方法:

## 接口定義

新規 / 変更される型・関数・API・data schema をコードブロックで書く。散文での field 説明は禁止。

```python
# 例: Python の class / 関数 signature
```

```text
POST /v1/<endpoint>
Authorization: Bearer <token>
Request:  <TypeName> (JSON)
Response: <TypeName> (JSON)
Errors:   400 invalid_input / 401 unauthorized / 503 provider_unavailable
```

## 検討した代替案

最低 2 案。各案の却下理由には観測可能な事実 / 測定可能な値 / 参照リンクを含める。曖昧形容詞は禁止。

### 案 A: <方針名>

- 概要:
- 却下理由:

### 案 B: <方針名>

- 概要:
- 却下理由:

## Open Questions

- [OPEN] ... — 誰がいつ決めるか:
- [OPEN] ... — 誰がいつ決めるか:

## Review Notes

- Reviewer:
- Result: pending / approved / request_changes
- Notes:

## Completion

実装完了後に埋める。埋めずに `completed/` へ移動しない。

- Completed: YYYY-MM-DD
- Validation: 実行したコマンド・テスト・確認手順
- Related PR / commit:
- Remaining follow-up:
