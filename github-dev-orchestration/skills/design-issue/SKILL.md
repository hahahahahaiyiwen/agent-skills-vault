---
name: design-issue
description: Develop an issue's design and record the approved design in GitHub.
---

# Design Issue

## When to use

To develop or revise an issue's design. No claim or prepared worktree is needed.

## Preflight

Invoke `orchestrator-boot` if `..\orchestrator-boot\references\RESOURCE-MAP.yml`
is not in context.

## Input

The target GitHub issue, identified by URL or repository and issue number.

## Guidance

- Propose an in-scope design using the issue, relevant code, and project guidance.
  Explain key decisions and tradeoffs.
- Confirm user approval or approval within authority delegated by the request
  or project guidance.
- Once approved, post or update a GitHub issue comment headed `## DESIGN`,
  summarizing the design and key decisions.

## Output

Report the design, approval status, and issue-comment link. Identify pending
decisions or failed comment writes. Approval does not itself start implementation.
