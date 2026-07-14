---
name: adaptive-model-routing
description: >-
  Choose and revise Codex model and reasoning effort for multi-stage engineering work. Use when
  deciding between Sol, Terra, and Luna; balancing judgment, cost, and latency; delegating bounded
  implementation or research to subagents; planning a model handoff; or escalating work after
  uncertainty, risk, or failed attempts increase. Apply at the start of substantial coding tasks
  that have independently executable work, not to trivial tasks where delegation overhead exceeds
  the work.
---

# Adaptive Model Routing

Keep the strongest necessary model in the judgment loop. Delegate bounded execution to the least
expensive model that can complete it reliably. Reassess at every handoff; model selection is a
risk decision, not a one-way countdown.

This skill governs model choice and handoffs. It does not broaden the user's authorization, permit
unrequested external actions, or override repository instructions. The parent agent retains
ownership of scope, architecture, integration, verification, and the final answer.

Read [references/codex-models.md](references/codex-models.md) for the current Codex-specific model
and reasoning-effort mapping.

## Core Workflow

### 1. Start with Judgment

Use Sol at `high` for the initial pass on substantial work:

- Read repository instructions and the exact user request.
- Establish scope, constraints, risks, existing contracts, and verification authority.
- Decide whether the work is separable enough to delegate.
- Produce bounded tasks with explicit ownership and acceptance criteria.

Increase Sol to `xhigh`, `max`, or `ultra` only when the decision itself warrants it. Examples
include cross-system architecture, high-stakes security or data integrity, ambiguous incident
diagnosis, large migrations, conflicting evidence, or repeated failed approaches.

Do not use a high-effort Sol pass for a self-evident one-file edit merely to satisfy a ritual.

### 2. Build a Judgment Packet

Downshift only after the parent can give the worker a self-contained packet:

1. Objective and user-visible outcome.
2. Owned files, modules, or read-only question.
3. Relevant repository rules and established patterns.
4. Constraints and actions that are out of scope.
5. Acceptance criteria and exact verification commands.
6. Known risks, assumptions, and unresolved questions.
7. Escalation conditions that require returning to the parent.

If the packet still asks the worker to discover the architecture, redefine scope, or choose among
high-impact alternatives, keep that work with Sol first.

### 3. Route the Execution

| Work shape | Default route |
|------------|---------------|
| Mechanical edits, formatting, renames, fixtures, repetitive tests, focused read-only lookup | Luna `medium` |
| Narrow implementation with exact files, established pattern, and strong tests | Luna `high` |
| Bounded multi-file implementation, nontrivial refactor, or hypothesis-led debugging | Terra `medium` or `high` |
| Cross-cutting design, unclear ownership, public contract change, or complex integration | Sol `high` or `xhigh` |
| High-stakes security, destructive migration, concurrency, auth, financial correctness, or repeated failure | Sol `xhigh`, `max`, or `ultra` |

Prefer Luna when success is cheaply and objectively testable. Prefer Terra when the task still
requires local design judgment. Keep Sol when a wrong local choice would reshape the system or
create expensive rework.

Delegation must save more context, latency, or cost than it adds in briefing and review overhead.
Keep tiny, tightly coupled, or inherently serial work in the parent.

### 4. Review at the Right Level

The parent reviews every delegated result before integration.

- Check the diff or evidence against the judgment packet, not merely the worker's summary.
- Run proportionate project-native verification.
- Use Terra for an independent routine review when the contract is clear and risk is moderate.
- Use Sol for architecture, security, compatibility, destructive changes, or whole-branch review.
- Return a failed review to a bounded worker only when the correction is clear. Otherwise escalate
  the diagnosis and decision to Sol.

Never let the implementing worker be the sole authority that its work is complete.

### 5. Escalate Dynamically

Stop and move up a tier when any of these appear:

- The task must broaden beyond its owned files or acceptance criteria.
- Repository behavior contradicts the judgment packet.
- A public API, schema, migration, permission, or compatibility decision is newly exposed.
- The same verification failure survives two evidence-based attempts.
- The worker cannot explain the failure or is guessing at hidden state.
- The change touches authentication, authorization, secrets, destructive operations, financial
  correctness, concurrency, deployment control, or irreversible data changes.
- Integration reveals conflicting edits or a cross-task architectural decision.

Escalation can mean Luna to Terra, Terra to Sol, or higher Sol reasoning effort. It does not always
mean `ultra`; choose the smallest increase that addresses the uncertainty.

## Parent and Worker Contract

The parent must:

- Retain the full user and repository context.
- Assign non-overlapping ownership.
- Keep architecture and integration decisions centralized.
- Inspect results directly and own final validation.
- Continue locally if delegation is unavailable or costs more than it saves.

The worker must:

- Stay within the judgment packet.
- Preserve unrelated work and accommodate concurrent edits.
- Report evidence, changed files, verification, and unresolved risks.
- Escalate instead of silently making a high-impact decision.

## Anti-Patterns

- Starting every task at Sol `ultra` regardless of ambiguity or risk.
- Delegating an open-ended architecture question to Luna.
- Choosing models solely by line count; a one-line auth change can be high risk.
- Downshifting before the task has explicit acceptance criteria.
- Creating many subagents for serial or overlapping work.
- Accepting a worker's confidence statement instead of inspecting evidence.
- Leaving Sol to perform every mechanical edit after the decisions are settled.
- Treating escalation as failure; it is the intended response to newly discovered uncertainty.

## Completion Check

- Did the strongest necessary model own the important judgment?
- Was each delegated task bounded enough for its assigned model?
- Did the handoff include files, constraints, acceptance criteria, and verification?
- Were model choices based on uncertainty and blast radius rather than prestige?
- Did the parent inspect, integrate, and validate the result?
- Were escalation triggers acted on when the task changed shape?
- Would delegation still look worthwhile after counting briefing and review overhead?
