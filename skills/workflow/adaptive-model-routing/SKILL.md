---
name: adaptive-model-routing
description: >-
  Choose models, reasoning effort and service tiers for engineering work.
  Apply at the start of substantial work and when uncertainty, risk, usage
  or failed attempts warrant a different route.
---

# Adaptive Model Routing

Choose the least costly route that can reliably meet the required quality.
Include retries, review and handoff costs. Preserve scope, permissions and
verification; model choice grants no additional authority.

## Choose the route

| Family | Use |
| --- | --- |
| Terra | Default for clear goals or effective direction, including computer use |
| Luna | Clear, low-risk work with established patterns and objective checks |
| Sol | Discovery, unfamiliar code, design, diagnosis and routine review |
| Astra | Exceptional ambiguity, complex architecture or consequential review |

Judge uncertainty, consequences and verification quality, not file count.
Any suitable model may own work end to end. Do not require stronger models
at both ends of routine work.

Use the selected model's advertised default effort unless the user chooses
otherwise or evidence justifies a change. Do not accidentally inherit another
model's effort. Increase effort for a bounded reasoning problem; change models
when capability is missing.

## Fast is explicit

Use normal/default service. Never inherit the caller's speed. Fast approval
covers only the work explicitly authorised: a Sol Fast caller does not
authorise an Astra Fast child or reviewer.

Before dispatch or reuse, select and verify tier separately from model and
effort. If normal service cannot be selected or verified, report the limitation
and do not silently launch priority work. Config changes do not alter running
sessions.

## Usage and dispatch

Check applicable usage windows before substantial work and routing decisions.
Below **10% remaining** in any known applicable window, conserve usage and ask
before Astra, including reviews and fallbacks. Exactly 10% uses normal routing.
Missing usage is unknown; disclose it. Preserve required quality and never
consume reset credits without explicit approval.

Before dispatch, inheritance or reuse, read the relevant sections of
[runtime guidance](references/codex-models.md). Resolve the latest permitted
stable family ID from the target runtime with `scripts/resolve_model.py`, then
preflight it with `--check-model`. Sol 6.0 is excluded. Ambiguous or unavailable
inventory blocks selection; never invent aliases or trust cached IDs.

Delegate only when authorised and worthwhile. Keep ownership disjoint and
review proportionate to risk. Reassess after scope changes, consequential
decisions, weak verification or two evidence-based failed attempts. Escalate
for a specific capability need; return clarified work to a cheaper route when
the saving exceeds handoff cost. Verify that the change helped.
