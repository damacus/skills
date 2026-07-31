<!-- markdownlint-configure-file {"MD013":{"line_length":100,"code_blocks":false,"tables":false}} -->

# Stack Pull Requests Source Notes

Load this reference for provenance, teaching, or preview-specific updates. Ordinary delivery-shape
decisions should use the durable rules in the main skill.

## Upstream

This skill adapts Paul Hammond's
[`stack-pull-requests` skill](https://github.com/citypaul/.dotfiles/blob/edf5519aa4bbea03b22217079b3c0e9d303fddd7/claude/.claude/skills/stack-pull-requests/SKILL.md)
at commit `edf5519aa4bbea03b22217079b3c0e9d303fddd7`.

The upstream material is licensed under the MIT License. The license text is included in
[`../LICENSE`](../LICENSE).

The adaptation preserves the upstream distinctions between stories, implementation slices, pull
request boundaries, hard and flow lineage, per-boundary verification, safe intermediate states,
lower-owned corrections, and bottom-up landing. It removes hard dependencies on companion skills
that may not be installed and separates durable Git behavior from changing GitHub preview behavior.

## Current Official GitHub Sources

GitHub's preview and extension behavior changes quickly. Prefer these current first-party sources:

| Source | Guidance used |
| --- | --- |
| [GitHub Stacked PRs](https://github.github.com/gh-stack/) | Current preview status, native stack model, UI behavior, extension installation, and high-level workflow. |
| [GitHub Stacked PRs overview](https://github.github.com/gh-stack/introduction/overview/) | Stack rules, focused diffs, CI enforcement, merging, rebasing, local tools, and repository enablement. |
| [CLI commands](https://github.github.com/gh-stack/reference/cli/) | Live command surface for stack creation, submission, navigation, sync, modification, and cleanup. |
| [`github/gh-stack`](https://github.com/github/gh-stack) | Extension README, implementation status, installation, local metadata, exit codes, and command caveats. |
| [GitHub Actions events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows) | Ordinary pull request base filters and the `merge_group` trigger required by merge-queue checks. |
| [GitHub Copilot stacking tutorial](https://docs.github.com/en/copilot/tutorials/stack-ai-generated-code-in-pull-requests) | Plan small coherent layers, build and review from the bottom, keep corrections in the owning layer, and propagate changes upward. |
| [Review AI-generated code](https://docs.github.com/en/copilot/tutorials/review-ai-generated-code) | Check context, intent, maintainability, dependencies, test integrity, and plausible-looking wrong code. |

Useful secondary sources retained from upstream:

- [Graphite: How to structure a stack](https://graphite.com/docs/how-to-structure-your-stacks)
- [Graphite: Best practices for reviewing stacks](https://graphite.com/docs/best-practices-for-reviewing-stacks)
- [Graphite: CI optimizations](https://graphite.com/docs/stacking-and-ci)
- [Sapling: Stacks of commits](https://sapling-scm.com/docs/overview/stacks/)

## Verified Adaptation Notes

As of 2026-07-31:

- GitHub describes native stacked pull requests as a private preview, not public preview.
- `gh stack` is supplied by the official `github/gh-stack` extension rather than GitHub CLI core.
- Native functionality requires the preview to be enabled for the repository.
- The extension README says `gh stack push` uses safe-lease, atomic pushes.
- The extension documents `gh stack merge` but reports it as not implemented.
- The GitHub UI can merge a selected pull request and the unmerged pull requests below it; current
  documentation should be rechecked before relying on exact partial-merge or queue behavior.
- Portable dependent pull requests remain possible but use ordinary immediate-base CI semantics
  and need manual stack documentation, lower-first landing, and upstack maintenance.

These are observations, not permanent contracts. The main skill therefore requires current official
documentation and live help before preview-specific operations.

## Updating The Skill

When GitHub changes the preview:

1. Re-read the official overview, CLI reference, extension README, and merge guidance.
2. Run `gh --version`, `gh extension list`, and `gh stack --help` in the active environment.
3. Check whether repository enablement is still required.
4. Verify submit, push, sync, rebase, modify, merge, and merge-queue behavior.
5. Update operational wording and the dated notes, not the durable scope and lineage rules.
6. Preserve tests with their owning behavior and keep every intermediate branch known-good.
