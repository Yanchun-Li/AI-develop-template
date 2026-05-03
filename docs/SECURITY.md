# SECURITY.md

セキュリティ要件は、明示的で、リポジトリ内で追跡できる必要があります。

## 基本方針

- secrets をコミットしない
- 外部アクセスはレビューされた provider / infrastructure モジュール経由で行う
- 認証・認可ルールは所有ドメインの近くに記録する
- 危険な操作は、明示的な interface と監査可能性を持たせる
- AI agent に secret や個人情報を含むログを渡さない

## 特に重要な項目

- 認証失敗時に過剰な情報を返さない
- セッション、token、API key の発行・失効ルールを docs に残す
- ユーザーまたは tenant ごとの access control を境界で強制する
- 外部 provider に渡すデータ範囲を明示する
- ML / analytics 用データの匿名化、保持期間、再利用範囲を記録する

## レビュー質問

- どのデータが機微情報か
- どの境界で access control を強制するか
- 外部と通信する provider はどれか
- その制御が効いている根拠は何か
- GitHub Actions、logs、artifacts に secret や機微情報が残らないか
