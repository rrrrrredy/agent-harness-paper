# Argument Map

## Thesis

Capability-patch harnesses become technical debt as models improve, but system-boundary harnesses become durable infrastructure.

## Definitions

- Agent harness: a controlled environment for running, observing, evaluating, replaying, and constraining agent behavior.
- Capability-patch harness: orchestration that compensates for temporary model weaknesses, such as brittle planners, role-chains, parser repair loops, or hand-coded routing.
- System-boundary harness: external contracts that define what an agent may access, change, record, replay, escalate, or publish.

## Claims

1. Final-answer evaluation is insufficient for agents because action trajectories can violate permissions, leak data, or mutate state while producing a plausible final answer.
2. Stateful acceptance criteria are the natural unit for production agent evaluation: git diffs, file contents, database rows, report statuses, audit events, and review queues.
3. Skills are a tractable microcosm of agent harness design: routing contracts, fixed I/O, failure paths, tool permissions, memory policy, and eval cases.
4. Thin contracts are preferable to thick choreography: the harness should not over-specify cognition, but it must harden boundaries and evidence.
5. Model companies are structurally advantaged in harness work because they see model failure modes, tool-use traces, and post-training feedback loops earlier.

## Case-Study Mapping

- SkillOps: modular skill contracts and eval flywheel.
- AI Radar: workflow harness with source ingestion, dry-run writes, report candidate review, audit, public-safe views.
- OpenClaw PRs: dry-run preview, scheduler semantics, memory error recovery.
- Hermes PRs: reusable sessions and session-recall scoping.
- skill-security-guard: static preflight harness for package safety.
- persistent-memory: stateful memory as local bounded context rather than global capability.
