---
name: claim-issue
description: Claim an eligible GitHub issue, prepare its worktree, and record the claim.
---

# Claim Issue

## When to use

To claim a new issue and prepare its worktree for development.

## Preflight

Invoke `orchestrator-boot` if `..\orchestrator-boot\references\RESOURCE-MAP.yml`
is not in context.

## Input

The target GitHub issue, identified by URL or repository and issue number.

## Guidance

- Confirm the issue is open, its blocking dependencies are completed, and no
  active or preparing handling agent owns it. Use `continue-issue` for existing
  branch/PR work instead of a second claim.
- Prepare or verify the main worktree at `repos.<key>.path`. Create the task
  branch and issue worktree from the intended base using the configured layout
  or repository conventions. Preserve existing work; do not bypass a claim
  conflict with another branch.
- Post a GitHub issue comment headed `## CLAIM`, identifying the handling agent,
  branch, and base commit. Update a configured board item to `In progress`.

## Output

Report the claim and worktree, or why the claim was declined. Include any
partial setup if the attempt failed.
