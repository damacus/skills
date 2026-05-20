# Skills

This repository publishes small, composable agent skills.

## Language

Skill: A focused agent capability stored as `skills/<category>/<name>/SKILL.md`, with optional supporting references or scripts beside it.

Runtime skills directory: A local installation target such as `~/.agents/skills` that may contain third-party installed skills.

Curated skills repository: This repository. It contains authored skills only, not vendored or installed third-party skills.

## Rules

- Keep each skill small and composable.
- Keep third-party installed skills out of this repository.
- Use one commit per skill when migrating or adding existing skills.
- Use `skills/<category>/<skill>/SKILL.md` so the repo stays browsable by category while remaining compatible with skills installers.

