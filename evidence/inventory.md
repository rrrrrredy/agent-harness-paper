# Evidence Inventory

This inventory separates first-party artifacts, upstream PR evidence, formative background notes, and external related work. Background notes informed terminology and framing; they are not the reproducible evidence layer for artifact claims.

Generated GitHub metadata snapshots are stored in `evidence/github_evidence.json` and `evidence/github_snapshots.md`. Source-level signal snapshots are stored in `evidence/source_audit.json` and `evidence/source_audit.md`. These files are the reproducible evidence layer for repository metadata, PR metadata, and path-level source signals used by the manuscript.

## Formative Background Notes

- Essay note: `路由契约，才是 Skill 的灵魂`: argues that skill quality depends on routing contracts, not prose.
- Essay note: `一个 Skill 是怎么“看起来很强”却“用起来不稳”的`: identifies pseudo-engineering patterns and production failures in skills.
- Essay note: `如何写好 Skill：不是一段漂亮的 Prompt`: defines workflow decomposition, routing, deterministic scripts, fallback paths, and eval sets.
- Essay note: `把 Skill 当 API 写，而不是当作文写`: frames skills as input/output/error-boundary interfaces.
- Document note: `如何写好 Skills`: expanded version with spreadsheet/data-cleaning eval methodology.
- Conversation note: agent harness as runtime, evaluation, observability, replay, and safety control.
- Conversation note: thin vs thick harness argument.

## First-Party GitHub Artifacts

- `rrrrrredy/skillops-paper`: paper, benchmark inputs, experiment runners, results, and tests for modular skills.
- `rrrrrredy/skill-design-guide`: skill design/testing methodology, routing contracts, linting, testing guide.
- `rrrrrredy/skill-security-guard`: static skill security scanner with deterministic risk dimensions and CI tests.
- `rrrrrredy/persistent-memory`: three-layer memory distillation skill with local state, health checks, and safety rules.
- `rrrrrredy/agent-self-audit`: agent health and self-audit checks for skills, memory, cron, config, and workspace state.
- `rrrrrredy/ai-radar-web`: production workflow case: dry-run ingestion, source review, report candidates, admin audit, write gates.
- `rrrrrredy/ai-radar-skill`: portable public-information skill with routing contract, schemas, examples, and source evidence rules.
- Non-fork OpenClaw skill repositories: `all-net-search-read`, `ai-info-radar`, `ai-talent-graph`, `ai-talent-radar`, `agent-job-monitor`, `book-hunter`, `wechat-reader`, `weibo-scraper`, `x-twitter-scraper`, `xiaoyuzhou-podcast`, `bilibili-video`, `lobster-guard`.

## Upstream PR Evidence

- OpenClaw PR `openclaw/openclaw#93149`: `cron add --dry-run` preview. Evidence for preview-before-side-effect, JSON params preview, and no gateway mutation.
- OpenClaw PR `openclaw/openclaw#69975`: timezone help text clarification. Evidence for CLI contract clarity.
- OpenClaw PRs `#59444`, `#70046`: time-only cron scheduling and timezone interpretation. Evidence for stateful scheduler semantics.
- OpenClaw PRs `#59488`, `#59637`, `#69199`: memory error guidance. Evidence for recoverable failure messages in memory/runtime boundaries.
- Hermes PR `NousResearch/hermes-agent#47094`: reusable cron sessions. Evidence for state continuity in scheduled agent work.
- Hermes PR `NousResearch/hermes-agent#47589`: session recall scoped to chat threads. Evidence for memory isolation and context pollution control.

## External Related Work

- Deli AutoResearch framework: long-horizon agent protocol with state files, stall detection, fresh sessions, heartbeat, and subagent verification. <https://victorchen96.github.io/auto_research/framework.html>
- ToolSandbox: stateful conversational interactive evaluation for tool-use agents. <https://aclanthology.org/2025.findings-naacl.65/>
- AgentDojo: dynamic framework for prompt injection attacks and defenses in tool-using agents. <https://arxiv.org/abs/2406.13352>
- SWE-agent and Agent-Computer Interface: interface design for coding agents. <https://arxiv.org/abs/2405.15793>
- DeepSeek API docs: OpenAI-compatible API and model references. <https://api-docs.deepseek.com/>
- Kimi API docs: OpenAI-compatible API, `kimi-k2.7-code`, and model parameter references. <https://platform.kimi.ai/docs/api/overview>
