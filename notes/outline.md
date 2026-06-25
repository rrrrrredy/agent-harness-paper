# Paper Outline

1. Introduction: agents change world state; final answers are not enough.
2. Definition: production-oriented agent harness as runtime + eval + observability + permission + replay.
3. Taxonomy: capability patches vs system boundaries.
4. Design principles: thin harness, strong contracts; stateful acceptance; trajectory logs; permission gates; memory scoping; review queues.
5. Case studies: SkillOps, AI Radar, OpenClaw, Hermes, security guard, persistent memory.
6. Pilot evaluation: 24 cases across routing, stateful tools, security, memory, replay.
7. Results: no harness vs thick checklist vs thin contract; Codex reference and live DeepSeek/Kimi results where available.
8. Discussion: model improvement, technical debt, feedback loops, model-lab advantage.
9. Limitations: author artifact base, small benchmark, model API instability, synthetic tasks.
10. Conclusion: harnesses that encode temporary cognitive patches should stay thin; harnesses that encode trust boundaries are core infrastructure.
