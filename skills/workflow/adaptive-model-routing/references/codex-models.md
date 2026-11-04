# Runtime Guidance

Read the sections needed for the current dispatch or reuse decision.

## Model resolution

Family names are policy labels, not API aliases. Obtain current model IDs,
descriptions, availability, release status and supported/default efforts from
the target tool and host. Do not reuse another host's inventory or old prices,
benchmarks or defaults.

Exclude Sol 6.0 (`gpt-6-sol`, `gpt-6.0-sol` and equivalent aliases), retired,
deprecated, legacy, previous-generation, older, preview, experimental and beta
models. Exclusions also apply to fallbacks, inheritance and cached agents.

Pass the advertised inventory as JSON on stdin to the bundled helper:

```text
python3 scripts/resolve_model.py --family terra
python3 scripts/resolve_model.py --check-model ACTUAL_ADVERTISED_MODEL_ID
```

Input is `{"models": [...]}`. Entries require `id` and may include
`description`, `status`, `available`, `is_latest`, `default_reasoning_effort`
and `supported_reasoning_efforts`. Copy runtime metadata; do not invent it.
The helper supports canonical numeric GPT family IDs. Other naming schemes
need verified canonical metadata and a helper update.

The helper compares eligible stable versions numerically. Contradictory
duplicate metadata, conflicting latest markers or ambiguous versions block
selection. It rejects superseded IDs during preflight. Missing inventory
blocks selection too; continue independent authorised work where possible.

Recheck at later routing decisions. Never dispatch new work to an excluded or
superseded agent. Switching or replacing it still requires existing authority.

## Tool settings

Inspect omission and fork semantics. Omit model only after verifying the
parent's exact ID. Omit effort only if that uses the selected model's default;
otherwise pass its advertised default explicitly. If no default is exposed,
retain a known supported setting and disclose the uncertainty.

Select `default` tier explicitly when omission inherits `priority`. Verify
`thread_settings_applied.thread_settings.service_tier` where available.
Missing tier evidence remains unknown. A priority-only tool cannot satisfy
normal routing without explicit Fast approval for that work. Global config
neither proves nor changes an existing session's tier.

## Usage evidence

Use applicable `rateLimitsByLimitId` buckets, falling back to legacy
`rateLimits` when applicable mapped data is unavailable. Inspect all applicable
windows; exclude unrelated model-specific buckets. Remaining percentage is
`max(0, min(100, 100 - usedPercent))`.

A known window below 10% triggers conservation even if another is unknown.
If none is known to be low, retain normal routing and disclose missing data.
Restore normal routing at the next decision after recovery. API prices do not
establish Codex allowance consumption or separate model allowances.

In the existing usage record, retain session/parent IDs, agent name/path and
timestamped model, effort and tier changes. Use recorded settings evidence;
do not infer historic settings from today's config. Track token deltas with
cached and uncached input separately. Cached input is part of input; reasoning
tokens are part of output. Do not sum cumulative snapshots or infer actual
charges from settings and token totals.

## Availability fallbacks

- Terra or Luna unavailable: use the other or Sol when suitable.
- Sol unavailable: use Terra or Luna only if quality remains adequate.
- Astra unavailable: use Sol only if it can reliably meet the requirement.
- Use Astra when needed or the only suitable option; ask first under low limits.
- No suitable permitted model: report the blocker. Preserve quality, scope
  and permissions through every fallback.

Brief the owner with the objective, repository rules, owned paths, prohibited
actions, acceptance checks and escalation conditions. These can come directly
from the request; do not create extra handoff documents for clear work.
