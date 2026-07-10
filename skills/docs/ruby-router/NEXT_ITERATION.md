# Ruby Router Next Iteration Plan

## Goal

Complete the Ruby-skill consolidation without losing useful specialist
knowledge, accidentally breaking established skill entry points, or allowing
the authored source and installed runtime package to drift apart.

## Non-Goals

- Reintroducing Ruby syntax tutorials or design-pattern catalogues.
- Installing or changing the user's runtime skill package without explicit
  approval.
- Rewriting unrelated skills or fixing the repository-wide Markdown backlog.
- Treating a model-selection smoke test as a deterministic unit test.

## Gate 0: Keep Current Deletions Provisional

Do not commit, publish, or install the current standalone-skill deletions until
the migration audit and compatibility decision below are complete. The working
tree is evidence for the next iteration, not an accepted public API change.

## Phase 1: Audit the Consolidation

Create a migration matrix for every retired Ruby skill:

- `postgresql-rails-analyzer`
- `review-ruby-code`
- `sandi-metz-reviewer`
- `simplecov`
- `design-patterns-ruby`
- `rails`
- `rspec`
- `rubocop`
- `ruby-lsp`
- `rubycritic`

For each original section, record whether it was:

1. retained and its new destination;
2. rewritten because it was too prescriptive or stale;
3. intentionally dropped as generic model knowledge; or
4. removed because it referenced nonexistent files, scripts, or behavior.

Compare against the committed source with `git show`, not memory. Produce the
matrix before changing more consolidated content; implementation starts only
after the matrix has been reviewed.

## Phase 2: Decide Compatibility and Discovery

Decide before finalizing deletions whether former public skill names require:

- thin compatibility routers that explicitly hand off to `ruby`;
- aliases supported by the skills installer; or
- a documented breaking removal.

Test both full-collection installation and representative single-skill
installation. Confirm that searches for Rails, RSpec, Minitest, Cucumber,
SimpleCov, RuboCop, RubyCritic, and PostgreSQL still lead to the Ruby router.
Treat the compatibility approach as an explicit user-facing decision because
it changes published skill names and existing installation commands.

## Phase 3: Implement the Reviewed Migration Map

Apply only the keep, rewrite, and drop decisions recorded in the reviewed
matrix. Keep adapter-neutral and tool-neutral references separate from focused
references such as PostgreSQL, Cucumber, or SimpleCov. Add compatibility stubs
or aliases according to the Phase 2 decision.

After each retired skill is migrated, compare its committed source with the new
destination and mark every matrix row complete before moving to the next skill.
Follow the repository's commit policy when changes are eventually committed;
do not hide unrelated skill migrations in one opaque commit.

## Phase 4: Add Repository Validation

Provide one documented validation entry point, preferably `task test`, that
runs focused checks for:

- Markdown formatting for changed skill files;
- required and unique skill frontmatter;
- internal Markdown links;
- router targets and referenced scripts;
- README entries matching published skills;
- missing skill-relative files promised by commands or examples; and
- executable or imperative automatic install, remote fetch, browser-open, and
  generated-report behavior in generic development skills.

Keep the validator deterministic and local. Do not make unrelated legacy
Markdown failures block Ruby-router work. Avoid naive word bans that would flag
negative guidance such as "do not install".

## Phase 5: Exercise Routing Scenarios

Create a compact acceptance matrix covering at least:

- a plain Ruby gem using Rake and Minitest;
- a Rails app using Task and Docker Compose;
- an RSpec request-spec failure;
- a Cucumber scenario failure;
- SimpleCov coverage analysis;
- RuboCop and RubyCritic quality work;
- PostgreSQL performance and migration work;
- a non-PostgreSQL Rails database task;
- Sorbet or RBS type work; and
- Ruby LSP unavailable with text-search fallback.

For each scenario, verify the smallest expected reference set, command-layer
precedence, container-boundary preservation, and focused verification choice.
Treat model-selection results as repeated smoke-test evidence, not a perfectly
deterministic gate.

## Phase 6: Package and Runtime Smoke Test

Install the authored Ruby skill into an isolated temporary destination using
the supported installer path. Verify that references and executable scripts are
packaged with `SKILL.md` and that no retired broken links return.

With explicit approval, refresh the user's installed runtime skill and open a
fresh Codex task to confirm the new skill catalog and routing behavior. Keep
source generation and runtime installation as separate, documented steps.

## Phase 7: Documentation and Handoff

Update the README with the compatibility decision, consolidated capabilities,
validation command, and installation behavior. Record intentional removals in
release notes or the pull-request description.

## Acceptance Criteria

- Every retired skill section is accounted for in the migration matrix.
- The compatibility decision is explicit before standalone names are removed.
- Every published entry point resolves to real content.
- PostgreSQL retains specialist operational guidance without fabricated tools.
- Minitest and Cucumber have first-class conditional routing.
- One local command validates the Ruby package and publication inventory.
- Temporary installation reproduces the authored package correctly.
- A fresh task exposes the intended skills after an approved runtime refresh.
- Focused checks pass; unrelated repository lint debt is reported separately.
- Only project discovery is loaded universally; specialist guidance remains
  conditional.

## Self-Review

The first draft had four material weaknesses:

1. It allowed content edits during the audit, which could repeat the exact loss
   this iteration exposed. Audit and implementation are now separate phases.
2. It did not prevent current deletions from being committed before a
   compatibility decision. Gate 0 now makes those deletions provisional.
3. Its validator language could encourage brittle keyword scanning. Validation
   is now scoped to real skill-relative promises and imperative behavior while
   allowing negative safety guidance.
4. It risked presenting model-routing smoke tests as deterministic. They are now
   explicitly supporting evidence, with package integrity handled by local
   deterministic checks.

The plan is still substantial. Execute it in two checkpoints:

- **Checkpoint A:** Gate 0, migration audit, and compatibility decision.
- **Checkpoint B:** reviewed migrations, validator, routing scenarios, package
  smoke test, and documentation.

Do not begin Checkpoint B until the compatibility choice and migration matrix
have been reviewed. This keeps the next iteration evidence-led and gives the
user a clear stop point before another broad structural change.
