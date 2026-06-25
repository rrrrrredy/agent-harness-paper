# Related Work Notes

- **Deli AutoResearch** contributes the long-horizon operating discipline: progress is persisted to files; stale loops are detected externally; fresh sessions reduce context accumulation; verification can be delegated to independent subagents.
- **ToolSandbox** motivates stateful, conversational, interactive evaluation rather than single-turn stateless tool benchmarks.
- **AgentDojo** shows that tool-using agents must be evaluated under untrusted data and prompt-injection attacks, not just task completion.
- **SWE-agent / ACI** shows that interfaces built for agents change performance and behavior, especially for software engineering tasks.
- **SkillOps** is closest first-party precedent: it treats skills as operational artifacts with trigger contracts, memory interfaces, constraints, tests, and security checks.

Gap: these lines cover benchmark environments, agent-computer interfaces, skill engineering, or security evaluation. The present paper focuses on the production harness layer that binds runtime, evaluation, permission, replay, state diff, audit, and human review into one engineering object.
