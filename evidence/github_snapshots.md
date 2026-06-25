# GitHub Evidence Snapshots

Generated at: `2026-06-25T09:43:50.881851+00:00`

## First-Party Repositories

| Repository | Private | Fork | Language | Updated | Description |
| --- | --- | --- | --- | --- | --- |
| [rrrrrredy/skillops-paper](https://github.com/rrrrrredy/skillops-paper) | False | False | Python | 2026-06-25T09:10:36Z | Paper and supporting artifacts for SkillOps: A Practical Framework for Designing, Testing, and Operating Modular Skills in Personal AI Agents. |
| [rrrrrredy/skill-design-guide](https://github.com/rrrrrredy/skill-design-guide) | False | False | Python | 2026-06-23T02:32:08Z | Skill design, testing & QA methodology — distilled from 16+ production skills |
| [rrrrrredy/skill-security-guard](https://github.com/rrrrrredy/skill-security-guard) | False | False | Python | 2026-06-23T02:32:16Z | Static security scanner for agent skills: A-F risk rating, safe zip scanning, CI-tested rules |
| [rrrrrredy/persistent-memory](https://github.com/rrrrrredy/persistent-memory) | False | False | Python | 2026-06-23T02:32:03Z | Agent persistent memory system — 3-layer distillation: daily logs → facts.yaml → MEMORY.md |
| [rrrrrredy/agent-self-audit](https://github.com/rrrrrredy/agent-self-audit) | False | False | Python | 2026-06-23T07:13:07Z | OpenClaw agent health check & self-audit — memory, skills, cron, config diagnostics |
| rrrrrredy/ai-radar-web | True | False | TypeScript | 2026-06-23T02:31:02Z | Bilingual AI industry radar website for source ingestion, ranking, clustering, Q&A, and reports |
| rrrrrredy/ai-radar-skill | True | False | Python | 2026-06-23T02:30:56Z | Cross-agent skill for AI industry radar, source evaluation, news analysis, and report generation |
| [rrrrrredy/lobster-guard](https://github.com/rrrrrredy/lobster-guard) | False | False |  | 2026-06-23T07:13:58Z | AI agent identity security guard — prevents impersonation & data leaks in group chats |
| [rrrrrredy/all-net-search-read](https://github.com/rrrrrredy/all-net-search-read) | False | False | Python | 2026-06-23T07:13:33Z | Social media search & extraction — WeChat, Xiaohongshu, Twitter/X, YouTube, Reddit, Bilibili, Weibo |
| [rrrrrredy/ai-talent-graph](https://github.com/rrrrrredy/ai-talent-graph) | False | False | Python | 2026-06-23T07:13:23Z | Academic AI scholar profiling — OpenAlex, arXiv, Semantic Scholar, ORCID integration |
| [rrrrrredy/ai-info-radar](https://github.com/rrrrrredy/ai-info-radar) | False | False | Python | 2026-06-23T07:13:19Z | AI news & resource discovery with subscription push — 50+ sources across podcasts, books, media |
| [rrrrrredy/book-hunter](https://github.com/rrrrrredy/book-hunter) | False | False | Python | 2026-06-23T06:45:46Z | Ebook search on Z-Library & Anna's Archive — title/author/ISBN with 4-layer fallback |
| [rrrrrredy/x-twitter-scraper](https://github.com/rrrrrredy/x-twitter-scraper) | False | False | Python | 2026-06-23T03:01:49Z | X/Twitter public data scraper — profile, timeline, full tweets without login |
| [rrrrrredy/xiaoyuzhou-podcast](https://github.com/rrrrrredy/xiaoyuzhou-podcast) | False | False | Shell | 2026-06-23T02:32:44Z | Xiaoyuzhou podcast fetcher & transcriber — download, transcribe with faster-whisper, summarize |
| [rrrrrredy/weibo-scraper](https://github.com/rrrrrredy/weibo-scraper) | False | False | Shell | 2026-06-23T02:32:31Z | Weibo public content scraper — no login required, visitor cookie mode |
| [rrrrrredy/wechat-reader](https://github.com/rrrrrredy/wechat-reader) | False | False | Python | 2026-06-23T02:32:25Z | Read WeChat Official Account articles as Markdown — no login required |
| [rrrrrredy/bilibili-video](https://github.com/rrrrrredy/bilibili-video) | False | False | Shell | 2026-06-23T02:31:37Z | Bilibili video download & transcription — no cookie required, faster-whisper powered |
| [rrrrrredy/ai-talent-radar](https://github.com/rrrrrredy/ai-talent-radar) | False | False | Python | 2026-06-23T02:31:25Z | Recruitment-oriented AI talent search — Semantic Scholar, GitHub, Zhihu, Weibo integration |
| [rrrrrredy/agent-job-monitor](https://github.com/rrrrrredy/agent-job-monitor) | False | False | Python | 2026-06-23T02:30:31Z | AI company Agent/LLM job monitoring — auto-collects from ByteDance, Tencent, Alibaba, Zhipu AI, Kimi, MiniMax daily |

## Upstream Pull Requests

| PR | State | Additions | Deletions | Files | Evidence relevance |
| --- | --- | --- | --- | --- | --- |
| [openclaw/openclaw#93149](https://github.com/openclaw/openclaw/pull/93149) | OPEN | 82 | 0 | docs/cli/cron.md, src/cli/cron-cli.test.ts, src/cli/cron-cli/register.cron-add.ts | Preview before side effect; mutation boundary evidence. |
| [openclaw/openclaw#69975](https://github.com/openclaw/openclaw/pull/69975) | MERGED | 5 | 1 | src/cli/cron-cli.test.ts, src/cli/cron-cli/register.cron-edit.ts | Scheduler contract and temporal semantics evidence. |
| [openclaw/openclaw#70046](https://github.com/openclaw/openclaw/pull/70046) | OPEN | 96 | 13 | docs/automation/cron-jobs.md, docs/cli/cron.md, src/cli/cron-cli.test.ts, src/cli/cron-cli/register.cron-add.ts, src/cli/cron-cli/register.cron-edit.ts | Scheduler contract and temporal semantics evidence. |
| [openclaw/openclaw#59488](https://github.com/openclaw/openclaw/pull/59488) | CLOSED | 27 | 2 | extensions/memory-core/src/tools.shared.ts, extensions/memory-core/src/tools.test.ts | Recoverable memory/runtime boundary evidence. |
| [openclaw/openclaw#59637](https://github.com/openclaw/openclaw/pull/59637) | CLOSED | 75 | 770 | .github/actions/setup-node-env/action.yml, .github/actions/setup-pnpm-store-cache/action.yml, .github/labeler.yml, .github/pr-assets/compaction-checkpoints/sessions-checkpoints-inline.png, .github/pr-assets/compaction-checkpoints/sessions-overview-inline.png | Recoverable memory/runtime boundary evidence. |
| [openclaw/openclaw#69199](https://github.com/openclaw/openclaw/pull/69199) | CLOSED | 68 | 12 | extensions/memory-core/src/tools.shared.ts, extensions/memory-core/src/tools.test.ts | State continuity or scoped memory recall evidence. |
| [NousResearch/hermes-agent#47094](https://github.com/NousResearch/hermes-agent/pull/47094) | OPEN | 398 | 42 | cron/jobs.py, cron/scheduler.py, hermes_cli/cron.py, hermes_cli/subcommands/cron.py, tests/cron/test_cronjob_schema.py | State continuity or scoped memory recall evidence. |
| [NousResearch/hermes-agent#47589](https://github.com/NousResearch/hermes-agent/pull/47589) | OPEN | 469 | 17 | agent/agent_runtime_helpers.py, agent/conversation_compression.py, agent/tool_executor.py, gateway/session.py, gateway/slash_commands.py | State continuity or scoped memory recall evidence. |
