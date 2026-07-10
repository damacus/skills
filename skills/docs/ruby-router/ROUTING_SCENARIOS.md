# Ruby Router Acceptance Scenarios

These scenarios test routing judgment, command-boundary preservation, and
proportionate verification. The expected references are the smallest normal
set. A concrete repository may justify one additional focused reference.

## Plain Ruby Gem With Minitest

- Detect: gemspec, `Rakefile`, `test/`, and Minitest helper.
- Load: `project-discovery.md`, `gems-and-cli.md`, `testing.md`, and
  `minitest.md`.
- Enter through: Mise, otherwise Task, then the existing Rake task.
- Verify first: the named test or one test file.

## Rails App Whose Taskfile Enters Docker Compose

- Detect: locked Rails, application config, Task definition, and Compose
  service.
- Load: `project-discovery.md` and `rails.md`, plus only task-specific
  references.
- Enter through: the Task command inside Compose, never equivalent host Ruby.
- Verify first: the narrow Rails task supported by the wrapper.

## Failing RSpec Request Spec

- Detect: `rspec-rails`, request spec, and helper configuration.
- Load: `project-discovery.md`, `rails.md`, `testing.md`, and `rspec.md`.
- Enter through: the wrapper and its supported file or line selector.
- Verify first: the exact failing example.

## Failing Cucumber Scenario

- Detect: Cucumber gems, feature, profiles, and support files.
- Load: `project-discovery.md`, `rails.md` when applicable, `testing.md`, and
  `cucumber.md`.
- Enter through: the configured profile and project wrapper.
- Verify first: the scenario line or name.

## SimpleCov Gap

- Detect: `.simplecov`, early require, coverage task, and result format.
- Load: `project-discovery.md`, `testing.md`, the active framework reference,
  and `coverage.md`.
- Enter through: the coverage-enabled project task.
- Verify first: the relevant test, then the smallest valid coverage scope.

## RuboCop and RubyCritic Quality Request

- Detect: locked gems, configuration, and quality tasks.
- Load: `project-discovery.md` and `quality.md`; add `code-review.md` for a
  design assessment.
- Enter through: the configured quality wrapper.
- Verify first: changed files or the affected directory.

## PostgreSQL Rails Query or Migration

- Detect: `pg` adapter, effective DB config, schema, and query or migration.
- Load: `project-discovery.md`, `rails.md`, `database.md`, and
  `postgresql-rails.md`.
- Enter through: the repository database or Compose task.
- Verify first: focused query evidence or the migration check.

## Non-PostgreSQL Rails Database

- Detect: SQLite, MySQL, Trilogy, or another adapter.
- Load: `project-discovery.md`, `rails.md`, and `database.md`; never
  `postgresql-rails.md`.
- Enter through: the adapter's configured project task.
- Verify first: the focused model, query, or migration check.

## Sorbet or RBS Contract Change

- Detect: `sorbet/`, inline `sig`, `sig/`, Steep, or RBS configuration.
- Load: `project-discovery.md` and `types.md`, plus the behavior-specific
  reference.
- Enter through: the existing type task.
- Verify first: the narrow type check and affected behavior test.

## Ruby LSP Unavailable During Refactor

- Detect: no semantic tool is exposed; symbols include Ruby or Rails DSL use.
- Load: `project-discovery.md`, `navigation.md`, and `code-review.md`.
- Enter through: `rg`, the relative outline script, and project tests.
- Verify first: callers, syntax, then the focused test.

## Smoke-Test Rules

- Do not preload every reference and then claim routing succeeded.
- Project discovery is universal; specialist references are conditional.
- Repeated model selections are smoke evidence, not deterministic unit output.
- File existence, frontmatter, links, packaging, and command precedence are
  deterministic validation.
