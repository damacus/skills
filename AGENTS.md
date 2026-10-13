# Agent Instructions

This repository is the authored source for `damacus/skills`.

## Repository Rules

- Store skills under `skills/<category>/<skill>/`.
- Edit authored skills here, then refresh global installations. Do not create or
  edit competing copies in project repositories or installation directories.
- Every skill must include a `SKILL.md` with YAML frontmatter containing `name` and `description`.
- Supporting files should live beside the skill in `references/`, `scripts/`, `assets/`, or another clearly named local folder.
- Do not commit installed third-party skills or runtime lock files.
- Migrate or add existing skills with one commit per skill.
- Keep lock files and runtime installation state in `damacus/agent-skills`, not this source repository.

## Tooling Discovery and Validation

- Start with `Taskfile.yml`; `task -l` lists the repository's supported checks.
- Run `task test` before publishing a skill change. It checks frontmatter and
  README inventory across all skills; Markdown lint covers README, Ruby and
  security Markdown only. Link and content checks cover the Ruby skill, and
  script syntax validation covers its outline script. Workflow and MedTracker
  Markdown are not currently linted by this task; review their content manually.
- For a new skill, inspect a nearby skill in the same category and update the README inventory and category layout when needed.
- Use `git diff --check` before committing; it is also part of the standard test task.
