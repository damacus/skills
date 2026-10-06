# Report input format

The input is structured Markdown with a small YAML-compatible metadata block.
The renderer uses Python's standard library. Metadata is deliberately limited
to four unquoted, single-line `key: value` fields; general YAML is unsupported.

Use [the example](../examples/example.md) as the starting point.

## Document structure

```markdown
---
project: Project name
report: Migration progress
headline: What the reader needs to know now
updated: 6 October 2026 at 14:00 UK time
---

## Overview

Describe the system, the current position and any decision the reader needs.

## Release boundary

Explain the first release and full goal. State any additional release gates.

## Slice foundation | Application foundation

### Details

Accepted: pending
Closes: Explain the agreed whole-slice acceptance checks.

### runner | Application runner

Scope: first-release
Implementation: complete @build
Local checks: passed @build
Publication: published @build
Hosted checks: pending
Acceptance: pending
Merge: unmerged
Deployment: not-deployed
Works: The replacement application starts and serves the existing pages.
Remaining: Hosted checks and whole-slice acceptance remain.
Next: Inspect the hosted run for the published revision.

## Evidence

### build | Published runner and local checks

Observed: 6 October 2026 at 14:00 UK time
Revision: Exact commit, document revision or other identifiable subject
Source: https://example.org/evidence
Note: Describe exactly what this evidence establishes.

## Limitations

State what the available evidence does not establish and any scope changes.
```

Repeat `## Slice ID | Title` for every sensible slice and `### ID | Title`
for every named item. IDs must start with a letter and contain only letters,
digits, underscores or hyphens. Slice and item IDs must be unique across the
report. Evidence IDs have their own namespace.

## States

Every item requires every field shown above. Fields are single-line values.
Use `None` for `Works`, `Remaining` or `Next` when there is nothing to report.

| Field | Allowed values |
| --- | --- |
| Scope | `first-release`, `full-goal` |
| Implementation | `complete`, `in-progress`, `not-started` |
| Local checks | `passed`, `pending`, `failed`, `not-required` |
| Publication | `published`, `unpublished` |
| Hosted checks | `passed`, `pending`, `failed`, `not-required` |
| Acceptance | `passed`, `pending`, `failed`, `not-required` |
| Merge | `merged`, `unmerged` |
| Deployment | `deployed`, `not-deployed` |
| Slice Accepted | `passed`, `pending`, `failed` |

Append evidence references to a state: `passed @local-run @browser-run`.
Positive states and `not-required` require at least one reference. References
must resolve to an evidence record. Pending and failed states may also link
to evidence. For `not-required`, the evidence note must explain the reason.

`full-goal` means deferred from the separately defined first release; the item
still appears in the full denominator. An item can be deferred and in progress
or published at the same time. Deferral is a scope decision, not a delivery
state.

Each item earns exactly one point when `Implementation` is `complete`,
`Publication` is `published`, and both local and hosted checks are `passed`
or explicitly `not-required`. Acceptance, merge and deployment do not follow
automatically from that score. A slice marked accepted must have every item
earning a point, as well as its own acceptance evidence.

Keep evidence tied to the revision that the state describes. Do not reuse a
passing run from an older revision for changed work. The renderer can validate
references, but the author must check what each source proves.

## Prose and links

`Overview`, `Release boundary` and `Limitations` support paragraphs and bullet
lists. Prose fields support `**bold**`, inline code and `[label](URL)` links.
The format does not support arbitrary HTML, nested Markdown, YAML collections
or multiline field values. Text is escaped in the output.

Evidence sources support HTTP, HTTPS, `file:` links and paths. Prefer durable
URLs or absolute paths. Relative links resolve beside the output HTML, so
place the output beside the input when using them. Avoid credentials or
temporary signed URLs. Every evidence record needs an explicit observed time,
revision, source and note; the renderer never invents a current timestamp.

To change progress, edit the Markdown input and render again. Keep the
generated output and its input together. The standalone output bundles its
styles and needs no network connection to display.
