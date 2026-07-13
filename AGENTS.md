# Agent Instructions

This repository is the authored source for `damacus/skills`.

## Repository Rules

- Store skills under `skills/<category>/<skill>/`.
- Every skill must include a `SKILL.md` with YAML frontmatter containing `name` and `description`.
- Supporting files should live beside the skill in `references/`, `scripts/`, `assets/`, or another clearly named local folder.
- Do not commit installed third-party skills or runtime lock files.
- Migrate or add existing skills with one commit per skill.
- Keep lock files and runtime installation state in `damacus/agent-skills`, not this source repository.

## Tooling Discovery and Validation

- Start with `Taskfile.yml`; `task -l` lists the repository's supported checks.
- Run `task test` before publishing a skill change. It validates the published skill inventory, relevant Markdown, internal links, and authored scripts.
- For a new skill, inspect a nearby skill in the same category and update the README inventory and category layout when needed.
- Use `git diff --check` before committing; it is also part of the standard test task.
