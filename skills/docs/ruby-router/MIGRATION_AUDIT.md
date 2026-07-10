# Ruby Skill Consolidation Audit

## Decision

Publish one Ruby ecosystem skill named `ruby`. Retire the former standalone
Ruby, Rails, test, quality, navigation, and PostgreSQL names as a documented
breaking consolidation.

The `vercel-labs/skills` CLI filters `--skill` by direct, case-insensitive
equality with the name discovered from `SKILL.md`. It has no alias or redirect
mechanism. A thin compatibility skill would either duplicate the router or be
incomplete when installed alone.

The standalone `postgresql-rails-analyzer` is therefore not needed. Its useful
capability remains in `references/postgresql-rails.md`, loaded by `ruby` only
after PostgreSQL is detected.

## Dispositions

- **Retained** means useful specialist judgment remains.
- **Rewritten** means the intent remains with project-aware boundaries.
- **Dropped** means the material is generic model knowledge or needless
  output prescription.
- **Broken** means promised files or behavior did not exist or were unsafe to
  assume.

## `postgresql-rails-analyzer`

Retained:

- N+1, query-plan, index, configuration, schema, batching, counter-cache, and
  monitoring concerns.
- PgHero, `pg_stat_statements`, Bullet, and Rails logs as conditional evidence.
- The warning that static leads require runtime verification.

Rewritten:

- The fixed workflow now starts with the reported problem, repository command
  boundary, and runtime evidence.
- Index recommendations now require predicates, plans, cardinality, existing
  indexes, and write cost.
- Configuration covers effective Rails settings, `DATABASE_URL`, pools,
  process topology, proxies, timeouts, and SSL.
- Migration guidance now covers Rails and PostgreSQL versions, transactions,
  locks, invalid indexes, backfills, rollout, and rollback.
- Findings are prioritized by observed impact and production risk instead of a
  fixed severity template.

Dropped:

- The mandatory report template, emoji output, and generic usage tips.
- Automatic migration generation without repository and production context.

Broken:

- `scripts/analyze_n_plus_one.py`, `scripts/analyze_indexes.py`, and
  `scripts/analyze_config.py` never existed.
- `references/performance_guide.md` and `references/anti_patterns.md` never
  existed.

## `review-ruby-code` and Its References

Retained:

- Repository pattern discovery before design recommendations.
- OOP, Rails, security, test, coverage, and quality concerns as conditional
  review evidence.
- Precise file and line references in the host application's supported format.

Rewritten:

- Scope can be a snippet, file, working tree, commit, branch, or pull request;
  it is no longer assumed to be a feature branch.
- Correctness, data safety, security, compatibility, tests, performance,
  design, and style now form a risk-based review order.
- RubyCritic, SimpleCov, lint, and tests run only when configured and useful.
- Rails patterns, SOLID, and Sandi Metz rules are diagnostic lenses rather than
  universal architecture rules.
- The security checklist is condensed into attack surfaces, evidence
  standards, tool boundaries, and actionable reporting.

Dropped:

- Mandatory `REVIEW.md`, positive-observation filler, fixed sections, and
  VSCode-only `file://` links.
- Large service-object, concern, decorator, SOLID, and Sandi Metz tutorials.

Broken:

- Automatic remote fetch and defaulting the base branch to `main` exceeded the
  task's authority and could review the wrong diff.
- Mandatory RubyCritic and SimpleCov runs assumed tools and configuration.

## `sandi-metz-reviewer`

Retained:

- Shamelessly clear working code before speculative abstraction.
- Incremental refactoring and the ability to justify breaking a heuristic.

Rewritten:

- SRP, dependency direction, Law of Demeter, Tell Don't Ask, OCP, and numeric
  size rules are questions about change cost, not automatic findings.

Dropped:

- The eighteen-smell checklist, naming bans, emoji severity format, fixed
  pass messages, and generic extract-method or polymorphism examples.

## `simplecov`

Retained:

- SimpleCov must start before application code.
- Branch gaps, error paths, authorization, retries, and boundary behavior are
  more useful than a percentage alone.
- Multi-suite, parallel, merge-timeout, and subprocess contracts must remain
  intact.
- Missing files, stale results, late startup, and result-format differences are
  legitimate troubleshooting areas.

Rewritten:

- Coverage runs through Mise, Task, Rake, binstubs, or Bundler in that order.
- Existing versions, formatters, helpers, filters, thresholds, CI, and project
  tasks are detected before advice is given.
- Complexity, churn, and coverage may be combined as evidence without fixed
  grades.

Dropped:

- Universal 90/80 thresholds, browser opening, pre-commit hooks, watch mode,
  summary scripts, and static external-reference tutorials.

Broken:

- Automatic Gemfile edits, formatter installation, and `bundle install` were
  unauthorized dependency changes.
- Fixed GitHub Actions and Spring recipes could contradict the locked versions
  and repository workflow.

## `design-patterns-ruby`

Retained and rewritten:

- A named pattern is recommended only when it resolves observed coupling or
  change cost and matches the repository architecture.

Dropped:

- The GoF selection catalogue, complete implementations, and Ruby tutorials
  for abstract methods, accessors, Marshal, Mutex, and YARD.

Broken:

- The creational, structural, and behavioral reference files did not exist.
- The hard-coded Ruby 3.2 requirement ignored the repository's locked runtime.

## `rails`

Retained:

- Rails application shape, controllers, views, routes, Active Record, jobs,
  mailers, Cable, storage, caching, frontend, security, performance, i18n,
  APIs, testing, and debugging remain routable concerns.

Rewritten:

- The locked Rails version replaces a Rails 8.1-only manual.
- Mise, Task, Rake, binstubs, Bundler, and Docker Compose replace direct host
  command recipes.
- Components and adapters are detected instead of assuming a full-stack app.
- Nearby routes, namespaces, policies, serializers, forms, jobs, and service
  boundaries override generic conventions.

Dropped:

- Universal thin-controller, service-object, concern, generator, fixture, and
  factory prescriptions.
- Generic scaffold examples already understood by the model.

Broken:

- All nine promised Rails topic reference files were absent.

## `rspec`

Retained:

- Focused file, line, description, tag, and seed-based execution.
- Verifying doubles, observable outcomes, regression-first work, and careful
  handling of Rails helpers and suite configuration.

Rewritten:

- Test level, factories or fixtures, hooks, shared examples, metadata, drivers,
  and cleaning strategy follow nearby repository examples.
- Direct RSpec commands are fallbacks after repository wrappers.
- Broad instance and chained stubs need a concrete legacy constraint.

Dropped:

- DSL and matcher tutorials, universal FactoryBot patterns, canonical helper
  files, and generic job, mailer, upload, query, or callback examples.
- Browser-opening and interactive-debug recipes as automatic behavior.

Broken:

- All seven promised RSpec reference files were absent.

## `rubocop`

Retained:

- Targeted lint, offense interpretation, and the safe versus unsafe correction
  distinction.

Rewritten:

- The repository wrapper, locked version, inherited configuration, plugins,
  and changed scope determine commands and behavior.
- Safe correction is still reviewed for unrelated churn.

Dropped:

- Canonical configuration, todo generation, hooks, CI setup, and static
  extension catalogues.

Broken:

- The five promised configuration and cop reference guides were absent.

## `ruby-lsp`

Retained:

- Semantic definitions, references, hover, diagnostics, and hierarchy are
  preferred when an actual semantic tool is exposed.
- `rg`, the bundled outline script, targeted reads, caller searches, tests, and
  lint form an explicit fallback.
- Rails DSLs and metaprogramming remain residual risks for text search.
- `ruby_outline.rb` moved into `ruby/scripts/` and remains executable.

Rewritten:

- The outline script is resolved relative to the installed skill instead of a
  hard-coded user path.

## `rubycritic`

Retained:

- Complexity, duplication, churn, and smells can guide a focused assessment.
- Before-and-after comparison and incremental remediation remain useful.

Rewritten:

- RubyCritic runs only when configured, requested, or materially useful.
- Existing project integration replaces automatic hook, CI, config, browser,
  and report creation.

Dropped:

- Universal 90/95 scores, A/B grades, automatic post-edit analysis, and
  mandatory smell remediation.

Broken:

- `scripts/check_quality.sh` and every promised supporting reference were
  absent.
- Automatic gem installation and Gemfile edits were unauthorized.

## Publication Consequences

- New installs use `--skill ruby` or install the full collection.
- Old `--skill rails`, `--skill rspec`, `--skill simplecov`, and similar names
  no longer resolve after publication.
- PostgreSQL prompts route through `ruby`; there is no standalone analyzer.
- README and release handoff must identify this as a breaking skill-name
  consolidation.
- Source validation never refreshes `~/.agents/skills`. That live runtime
  mutation requires separate permission because it affects running agents.
