# Codex Model Mapping

Use this reference for Codex model names and reasoning efforts available in the current runtime.
Revalidate the tool metadata when models or effort levels change.

## Model Roles

| Model | Role | Good default work |
|-------|------|-------------------|
| `gpt-5.6-sol` | Frontier judgment and complex integration | Architecture, decomposition, high-risk review, ambiguous debugging, final synthesis |
| `gpt-5.6-terra` | Balanced implementation and reasoning | Bounded multi-file changes, nontrivial refactors, focused diagnosis, routine independent review |
| `gpt-5.6-luna` | Fast, economical execution | Mechanical edits, repetitive changes, focused research, exact-pattern implementation, test expansion |

## Reasoning Efforts

- Sol supports `low`, `medium`, `high`, `xhigh`, `max`, and `ultra`.
- Terra supports `low`, `medium`, `high`, `xhigh`, `max`, and `ultra`.
- Luna supports `low`, `medium`, `high`, `xhigh`, and `max`.

Use effort to tune within a model before jumping multiple tiers:

| Need | Typical choice |
|------|----------------|
| Fast deterministic execution | Luna `medium` |
| Narrow code change with some reasoning | Luna `high` |
| Substantive bounded implementation | Terra `medium` or `high` |
| Initial judgment and final integration | Sol `high` |
| Cross-cutting ambiguity or high risk | Sol `xhigh` or `max` |
| Exceptional, consequential, unresolved judgment | Sol `ultra` |

`ultra` is a reserve tier. Do not use it as the routine starting point when `high` can frame the
task and expose whether more reasoning is needed.

## Practical Routing Sequence

```text
Sol high: inspect, judge, decompose
    |
    +-- Luna medium/high: mechanical or tightly specified task
    |
    +-- Terra medium/high: substantive bounded task
    |
    `-- Sol xhigh/max/ultra: unresolved or high-risk task

Sol high: review, integrate, verify, synthesize
```

The parent model does not need to change identity mid-task. In Codex, the usual implementation is
to keep the parent on Sol and select a lower model plus reasoning effort when spawning a bounded
worker. Escalate by returning judgment to the parent or spawning a stronger reviewer when needed.

## Source Rationale

This policy adapts Simon Willison's observation that judgment, review, and synthesis benefit from
the strongest model while bounded implementation can often move to a less expensive model:

- [Fable's judgement](https://simonwillison.net/2026/Jul/3/judgement/)
- [The new GPT-5.6 family: Luna, Terra, Sol](https://simonwillison.net/2026/Jul/9/gpt-5-6/)
