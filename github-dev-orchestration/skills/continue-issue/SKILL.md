---
name: continue-issue
description: Restore existing GitHub issue work and record the new handling agent.
---

# Continue Issue

## When to use

To resume an issue after handoff or in a new agent session.

## Preflight

Invoke `orchestrator-boot` if `..\orchestrator-boot\references\RESOURCE-MAP.yml`
is not in context.

## Input

The target GitHub issue, identified by URL or repository and issue number.
Include a handoff link if known.

## Guidance

- Check current issue/PR state and the latest handoff. Resume when its
  conditions are met or new actionable CI failures, review feedback, or queue
  failures permit scoped repairs despite an operational wait. Require that no
  other active or preparing handling agent owns the work. Honor explicit holds;
  completed or cancelled work needs no new claim.
- From the main worktree at `repos.<key>.path`, restore the existing task branch
  and worktree from remote references as needed, preserving dirty or divergent
  work. A merged PR needs only missing completion updates or cleanup, not a
  recreated branch or worktree.
- Post or update a `## CONTINUE` issue comment with the handling agent,
  branch/head, and next action for resumed work. Retain unresolved decisions,
  findings, review threshold, and remaining review budget; suggested next steps
  are not required stages. Update the configured board item to `In progress` only
  for resumed work.

## Output

Report resumed handling, the worktree and next action, or why continuation
cannot proceed. Identify failed or partial updates; do not execute further
work unless requested.
