# Agent Instructions

This repository is the authored source for `damacus/skills`.

## Repository Rules

- Store skills under `skills/<category>/<skill>/`.
- Every skill must include a `SKILL.md` with YAML frontmatter containing `name` and `description`.
- Supporting files should live beside the skill in `references/`, `scripts/`, `assets/`, or another clearly named local folder.
- Do not commit installed third-party skills or runtime lock files.
- Migrate or add existing skills with one commit per skill.
- Keep lock files and runtime installation state in `damacus/agent-skills`, not this source repository.
