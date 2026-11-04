---
name: adaptive-model-routing
description: >-
  Choose models, reasoning effort and service tiers for engineering work.
  Apply at the start of substantial work and when risk, usage or failed
  attempts warrant a different route.
---

# Adaptive Model Routing

Choose the least costly route that reliably meets the required quality.
Include retries, review and handoff costs. Preserve scope, permissions and
verification.

| Family | Use |
| --- | --- |
| Terra | Default for clear goals or effective direction, including computer use |
| Luna | Clear, low-risk work with established patterns and objective checks |
| Sol | Discovery, unfamiliar code, design, diagnosis and routine review |
| Astra | Exceptional ambiguity, complex architecture or consequential review |

Judge uncertainty, consequences and verification quality, not file count.
Any suitable model may own work end to end; stronger-model framing or review
is not mandatory for routine work. Delegate only when authorised and useful.
Keep ownership disjoint and review proportionate to risk.

Use only models and efforts advertised by the target runtime. Start with the
selected model's advertised default effort; preserve explicit user choices.
Never accidentally inherit another model's effort. Increase effort for a
bounded reasoning problem; change models when capability is missing.

## Fast requires explicit approval

Use normal/default service. Never inherit the caller's speed. Fast approval
covers only the work explicitly authorised: a Sol Fast caller does not
authorise an Astra Fast child or reviewer.

Before dispatch or reuse, select and verify tier separately from model and
effort. If normal service cannot be selected or verified, report the limitation
and do not silently launch priority work. Config changes do not alter running
sessions.

## Reassess when needed

Check applicable usage windows before substantial work and routing decisions.
Below **10% remaining** in any known applicable window, conserve usage and ask
before Astra, including reviews and fallbacks. Exactly 10% uses normal routing.
Missing usage is unknown; disclose it. Never lower required quality or consume
reset credits without explicit approval.

Reassess after scope changes, consequential decisions, weak verification or
two evidence-based failed attempts. Escalate for a specific capability need;
return clarified work to a cheaper route when the saving exceeds handoff cost.
Verify that the change helped.

Consult [the reference](references/codex-models.md) only when needed for usage
accounting, availability fallbacks or price/performance evidence. Verify dated
model IDs and figures against current runtime metadata and primary sources.
