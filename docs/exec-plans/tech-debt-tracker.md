# 技術負債トラッカー

会話履歴の中に消えてほしくない既知の負債をここで追跡します。

| Date | Area | Debt | Impact | Planned fix |
| --- | --- | --- | --- | --- |
| 2026-04-12 | template | 初期テンプレート由来の placeholder が多い | AI が前提を誤解する可能性がある | 利用開始時に `docs/PRODUCT_SENSE.md` と `docs/product-specs/` を埋める |
| 2026-05-03 | automation | deploy / release workflow は未配置 | CI 以外の自動化は利用先プロジェクトで追加が必要 | 必要になった時点で `docs/GITHUB_AUTOMATION.md` と workflow を更新する |
