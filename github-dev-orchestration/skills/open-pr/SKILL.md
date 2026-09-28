---
name: open-pr
description: Create or update an issue-linked GitHub PR.
---

# Open PR

## When to use

To publish an issue's work for collaboration or review, including a draft.

## Preflight

Invoke `orchestrator-boot` if `..\orchestrator-boot\references\RESOURCE-MAP.yml`
is not in context.

## Input

The target GitHub issue, identified by URL or repository and issue number.
Include the task branch, base, or draft preference if known.

## Guidance

- Check the head repository/branch, base, and all PR states. Reuse a matching
  open PR; report merged work and clarify closed-unmerged matches rather than
  silently replacing them.
- Push intended commits and create or update the PR with scope, verification,
  and remaining work. Preserve human-authored content; link the issue and use
  explicit cross-links for non-default targets.
- Use a draft for unfinished work. Honor explicit publication requirements;
  otherwise pending CI and optional self-review are not publication gates.

## Output

Report the PR link, published revision, draft status, and any failed or partial
updates. Publication is not merge readiness; do not merge or wait for CI.
