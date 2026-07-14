# Skills

[![skills.sh](https://skills.sh/b/damacus/skills)](https://skills.sh/damacus/skills)

Agent skills curated for my own workflows.

## Install

Install the full collection:

```sh
npx skills@latest add damacus/skills
```

Install a single skill:

```sh
npx skills@latest add damacus/skills --skill <skill-name>
```

Install the Ruby router globally into the shared agent skill directory:

```sh
npx skills@latest add damacus/skills --skill ruby --global
```

## Available Skills

Skills are organized by category under `skills/`.

### Engineering

- **[cli-design](./skills/engineering/cli-design/SKILL.md)**
- **[go-optimizer](./skills/engineering/go-optimizer/SKILL.md)**
- **[structure-codebase](./skills/engineering/structure-codebase/SKILL.md)**

### Language

- **[fish-shell](./skills/language/fish-shell/SKILL.md)**
- **[ruby](./skills/language/ruby/SKILL.md)** — Ruby and Rails router covering
  RSpec, Minitest, Cucumber, quality, coverage, databases, and tooling.

The `ruby` skill replaces the former standalone Rails, RSpec, SimpleCov,
RuboCop, RubyCritic, Ruby LSP, design-review, and PostgreSQL analyzer entry
points. Install and invoke `ruby`; it conditionally loads only the guidance the
detected project and task require.

### Operations

- **[accounting-sync](./skills/operations/accounting-sync/SKILL.md)**
- **[alert-investigator](./skills/operations/alert-investigator/SKILL.md)**
- **[chef-custom-resources](./skills/operations/chef-custom-resources/SKILL.md)**
- **[failing-deployments](./skills/operations/failing-deployments/SKILL.md)**
- **[modernize](./skills/operations/modernize/SKILL.md)**

### Productivity

- **[storyboard](./skills/productivity/storyboard/SKILL.md)**
- **[translate](./skills/productivity/translate/SKILL.md)**

### Security

- **[security-maintenance](./skills/security/security-maintenance/SKILL.md)**

### TUI

- **[tui-expert](./skills/tui/tui-expert/SKILL.md)**

### UI

- **[ui-professional](./skills/ui/ui-professional/SKILL.md)**

### Workflow

- **[adaptive-model-routing](./skills/workflow/adaptive-model-routing/SKILL.md)**
- **[gh-address-comments](./skills/workflow/gh-address-comments/SKILL.md)**
- **[github-pr](./skills/workflow/github-pr/SKILL.md)**
- **[retro](./skills/workflow/retro/SKILL.md)**
- **[screenshot-github](./skills/workflow/screenshot-github/SKILL.md)**

## Layout

- `skills/engineering/`
- `skills/language/`
- `skills/operations/`
- `skills/productivity/`
- `skills/security/`
- `skills/tui/`
- `skills/ui/`
- `skills/workflow/`

## Validation

Run the focused authored-source checks from the repository root:

```sh
task test
```

This validates the Ruby package, all published skill frontmatter, internal
links, the README inventory, router targets, bundled scripts, and Markdown for
the changed Ruby-router documentation. Unrelated legacy Markdown is outside
this focused gate.
