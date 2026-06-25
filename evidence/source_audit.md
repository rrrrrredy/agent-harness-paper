# Source Evidence Audit

Generated at: `2026-06-25T10:17:36.173987+00:00`

Path and keyword-signal audit using GitHub API. Source file bodies are not stored.

This audit supports bounded artifact claims. It records repository paths and signal categories, not source excerpts.

| Repository | Private | Fork | Signal files | Top signals | Representative paths |
| --- | --- | --- | --- | --- | --- |
| rrrrrredy/skillops-paper | False | False | 55 | testing=38, memory_scope=13, observability=5, routing_contract=5 | benchmark/README.md, benchmark/.gitkeep, benchmark/external_artifact_corpus_sources.csv, benchmark/risk_cases.csv, benchmark/skill_samples.csv |
| rrrrrredy/skill-design-guide | False | False | 1 | testing=1 | references/testing-guide.md |
| rrrrrredy/skill-security-guard | False | False | 5 | testing=5 | tests/fixtures/high-risk-skill/SKILL.md, tests/fixtures/nonstandard-frontmatter/SKILL.md, tests/fixtures/safe-skill/SKILL.md, tests/fixtures/high-risk-skill/scripts/run.sh, tests/test_scan.py |
| rrrrrredy/persistent-memory | False | False | 2 | memory_scope=2 | MEMORY.md.template, scripts/memory_manager.py |
| rrrrrredy/agent-self-audit | False | False | 1 | observability=1 | references/audit-criteria.md |
| rrrrrredy/ai-radar-web | True | False | 29 | testing=13, observability=10, review_gate=7, memory_scope=5, state_diff=1 | data/ingestion/latest/.gitkeep, data/scheduled/latest/.gitkeep, data/understanding/latest/.gitkeep, lib/retrieval/citations.ts, lib/retrieval/load-radar-items.ts |
| rrrrrredy/ai-radar-skill | True | False | 4 | testing=3, routing_contract=2 | docs/source-evaluation.md, examples/source-evaluation-example.md, tests/routing-cases.md, docs/routing-contract.md |
| rrrrrredy/lobster-guard | False | False | 0 |  |  |
| rrrrrredy/all-net-search-read | False | False | 0 |  |  |
| rrrrrredy/ai-talent-graph | False | False | 1 | testing=1 | scripts/orcid_api.py |
| rrrrrredy/ai-info-radar | False | False | 0 |  |  |
| rrrrrredy/book-hunter | False | False | 1 | observability=1 | scripts/public_catalog_search.py |
| rrrrrredy/x-twitter-scraper | False | False | 0 |  |  |
| rrrrrredy/xiaoyuzhou-podcast | False | False | 0 |  |  |
| rrrrrredy/weibo-scraper | False | False | 0 |  |  |
| rrrrrredy/wechat-reader | False | False | 0 |  |  |
| rrrrrredy/bilibili-video | False | False | 0 |  |  |
| rrrrrredy/ai-talent-radar | False | False | 0 |  |  |
| rrrrrredy/agent-job-monitor | False | False | 2 | state_diff=1, testing=1 | scripts/daily_diff.py, scripts/push_citadel.py |
