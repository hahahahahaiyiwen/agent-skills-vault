---
name: implement-issue
description: Implement an issue-scoped change and record the completed work in GitHub.
---

# Implement Issue

## When to use

To implement or revise an issue's scoped change.

## Preflight

Invoke `orchestrator-boot` if `..\orchestrator-boot\references\RESOURCE-MAP.yml`
is not in context.

## Input

The target GitHub issue, identified by URL or repository and issue number.

## Guidance

- Implement the issue's scope in its task worktree using repository instructions
  and any approved design. Preserve unrelated work.
- Verify changed behavior with focused tests and project-required checks;
  address failures before reporting implementation complete.
- Once implementation is complete, post or update a GitHub issue comment
  headed `## IMPLEMENT` with the change summary, verification results, and any
  remaining limitations.

## Output

Report the implemented change, verification, and issue-comment link, or the
blocker. Identify failed or partial updates; do not start review or publication
unless requested.
