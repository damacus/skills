---
name: progress-report
description: >-
  Create and update a readable HTML progress report for a project, migration or
  multi-agent delivery. Use when the user needs every slice, completed/total
  scores, evidence and concrete next actions. Uses authoritative JSON data and
  a bundled Python renderer with a compact human-facing layout.
---

# Progress Report

Keep one machine-readable JSON source and generate HTML for people. Write plain
UK English. Preserve the bundled visual style, with a very short preamble, an
explicit evidence snapshot time and expandable checklists.

## Create or update a report

1. Read the existing JSON and current evidence. Confirm the full goal and any
   separate first-release boundary. Ask only material unresolved questions.
2. Start from [example.json](examples/example.json) and follow the
   [input format](references/input-format.md). JSON is authoritative; do not
   maintain a second Markdown ledger or hand-edit the generated HTML.
3. Keep slice IDs, item IDs, scopes and boundaries stable. Keep deferred work in
   the full goal. Explain any denominator change in `limitations`.
4. Update delivery states only from evidence, retaining its observation time,
   revision and source. Set the timezone-qualified `snapshot_at` and
   `snapshot_timezone`. Reformatting or rendering does not refresh evidence.
5. Keep `headline` brief and `summary` to one short sentence. Author work,
   remaining tasks and next actions once in the item records. The formatter
   derives the slice summaries and consolidated next actions from those records.
   Simplify authoring, not the report's features: preserve navigation, scores,
   working behaviour, remaining work, acceptance criteria and evidence access.
6. Validate without changing the existing HTML, then render with JSON and HTML
   beside each other. Resolve script paths relative to this skill's directory:

   ```sh
   python3 scripts/render.py /absolute/path/report.json --check
   python3 scripts/render.py /absolute/path/report.json /absolute/path/report.html
   ```

7. Open the HTML. Inspect desktop, tablet and narrow layouts. Check the sticky
   sidebar on desktop and the collapsible navigation on mobile. Expand a
   checklist, follow an item/evidence link and inspect print behaviour when
   supported. Use a long report as well as the short example: every sidebar
   link must remain reachable. State any preview limitation.

For an existing Markdown report, convert its records to the documented JSON
shape, preserve IDs and dated evidence, compare scores, then retire Markdown as
an active input. Keep the old file only as a labelled historical archive.

## Agent update contract

Give every agent the JSON path and this skill's path. Use this instruction in
the task brief, including for Luna and SWE:

> Read the progress-report skill and the existing report JSON. Edit only the
> assigned records in JSON; preserve IDs, scope and evidence times. Use exact
> status values and separate `evidence_ids` arrays. Use JSON `null` for missing
> prose. Do not edit HTML, CSS, templates or calculated totals. Run the bundled
> `scripts/render.py REPORT.json --check` and fix any reported error. Report
> changed IDs and the validation result to the report owner.

Use one report owner to apply updates and render the final HTML. When several
agents work concurrently, have them return proposed record updates to that
owner rather than write the shared file. This does not authorise delegation.
The owner uses the bundled template unchanged and inspects the generated report.
Validation checks structure and references; the owner still checks whether the
evidence supports each claimed state. Never edit generated HTML to fix data.

## Scoring and delivery states

An item earns one point only when implementation is complete, publication is
published, and both local and hosted checks passed or are evidenced as not
required. Partial work earns no point. Positive states need evidence references;
not-required checks need an explanation of why the check does not apply.

Record implementation, local checks, publication, hosted checks, acceptance,
merge and deployment separately. Whole-slice acceptance requires its own
evidence, even when every item earns a point. Unknown means pending.

Derive scores and navigation from the JSON records. Never store competing
handwritten totals. Items differ in size: do not average into a percentage or
predict a completion date. Show a separate first-release count from explicit
scope. Deferred full-goal work stays visible; counts do not declare release ready.

## Bundled files and validation

- [Renderer](scripts/render.py): Python standard library; validates required
  fields, IDs, states, snapshot time and evidence references.
- [Template](assets/report.html), [styles](assets/report.css) and
  [checklist styles](assets/checklist.css): sidebar, scores, expandable checklist
  tables, adaptive score cards and print expansion. Whole-slice acceptance,
  working behaviour, remaining work and acceptance criteria stay visible.
  Detailed delivery states expand inside each checklist. Release boundaries,
  scoring guidance, consolidated next actions and evidence remain accessible
  from the navigation. Wide layouts retain the sidebar; narrow layouts use a
  collapsible menu and stack scores and checklist rows without sideways scrolling.
- [JSON example](examples/example.json) and [HTML example](examples/example.html):
  fictional data demonstrating the format.
- [Retained historical design](references/medtracker-migration-status.html):
  design reference with historical facts. Preserve its useful features when
  changing the formatter; do not treat its figures as current evidence.

Do not add a report-generator test suite or testing project. Render the example
and inspect the result. Check representative invalid inputs with the renderer.
Before publishing skill changes, run repository `task test`, lint this skill's
Markdown, check its local links, render the example and run `git diff --check`.
The repository task alone does not cover all of those checks.
