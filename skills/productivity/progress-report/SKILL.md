---
name: progress-report
description: >-
  Create and update a readable HTML progress report for a project, migration or
  multi-agent delivery. Use when the user needs an overview of every slice,
  explicit completed/total scores, evidence, remaining work and concrete next
  actions. Uses structured Markdown and a bundled Python renderer and layout.
---

# Progress Report

Create a report that someone passing by can understand without asking each
agent for an update. Use plain UK English. Explain what works, what remains
and the next concrete action. Keep the bundled visual format.

## Create or update a report

1. Read the latest source evidence and the existing report input. Confirm the
   complete goal, its sensible slices and any separate first-release boundary.
   Ask only for facts or decisions that materially affect the report.
2. Start from [the example input](examples/example.md). Follow
   [the input format](references/input-format.md). Keep one authoritative
   Markdown input for each report.
3. Keep slice IDs, item IDs and item boundaries stable between updates. Retain
   deferred work in the full goal. If requirements change, explain the change
   and its effect on the denominator in `Limitations`.
4. Add observed evidence, including its timestamp, source and revision. Update
   each item's delivery states from that evidence. Describe an unknown state
   as pending; do not infer publication, checks, acceptance or deployment.
5. Run the renderer from this skill directory:

   ```sh
   python3 scripts/render.py /absolute/path/report.md /absolute/path/report.html
   ```

6. Open the generated report for the user. Inspect the rendered desktop and
   narrow layout, expand a checklist and inspect print behaviour when the
   available preview supports it. Report any preview limitation directly.
   Refine the input or bundled layout with the user.

## Scoring and delivery states

An item earns one point when it is implemented, published and its recorded
checks have passed. Local and hosted checks are recorded separately. A check
may be marked `not-required` only with evidence explaining why it does not
apply. Partly completed items earn no point. Selecting a library or preparing
an implementation earns no completed point.

Record implementation, local checks, publication, hosted checks, acceptance,
merging and deployment separately. Whole-slice acceptance needs its own
evidence even when every checklist item earns a point.

The renderer derives the navigation, overview, scores, progress bars, working
behaviour, remaining work and next actions from the same item records. Do not
write separate copies of those facts or hand-edit the generated HTML.

Scores count named items of different sizes. Do not average them into an
overall percentage, invent effort estimates or use them to predict a date.
Show a separate first-release count using the explicit item scope. Full-goal
work remains visible and does not block that smaller boundary's item count.
The count alone does not declare a release ready.

## Bundled files

- [Renderer](scripts/render.py): Python standard library only; no installation.
- [HTML template](assets/report.html), [reference styles](assets/report.css)
  and [checklist styles](assets/checklist.css): fixed
  sidebar, cards, expandable checklist tables, responsive layout and print
  layout. Checklist tables use the reference's Item, State, and Evidence or
  remaining work columns; each state can expand to show delivery details.
- [Example input](examples/example.md) and [output](examples/example.html):
  fictional facts that demonstrate the format and delivery states.
- [Retained MedTracker reference](references/medtracker-migration-status.html):
  the design snapshot copied on 6 October 2026. Its progress figures are
  historical. It is a visual reference, not current project evidence.

Keep this practical. Add no report-generator test suite or testing project.
Render a representative example and inspect it visually. The renderer's
input validation catches missing fields, invalid states and evidence links.
Repository checks remain part of publishing an authored skill change.

`task test` validates the published inventory and the repository's existing
Ruby and security checks. It does not lint this skill's Markdown, check its
local links or exercise its renderer. Before publishing a change here, also
lint this skill's Markdown, check its local links, and render a representative
input with `scripts/render.py`. These are direct publishing checks, not a new
generator test suite or task gate. Use the example's local Markdown settings
when linting its fixed input format.
