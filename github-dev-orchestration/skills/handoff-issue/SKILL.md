---
name: handoff-issue
description: Preserve issue progress in GitHub and release handling for another agent or session.
---

# Handoff Issue

## When to use

To pause or transfer an issue, not after every skill return.

## Preflight

Invoke `orchestrator-boot` if `..\orchestrator-boot\references\RESOURCE-MAP.yml`
is not in context.

## Input

The target GitHub issue, identified by URL or repository and issue number,
and the reason for handing it off.

## Guidance

- Confirm you are the current handling agent. Save and push coherent progress
  where possible; verify remote commits and identify local-only limitations.
- Post or update a `## HANDOFF` issue comment with progress, branch/head and PR
  links, key decisions, remaining work, and the next action or resume condition.
  Include unresolved findings, the review threshold, and remaining review budget
  when relevant.
- Verify the comment is saved before releasing handling, then stop changing the
  task branch. Keep board status aligned with actual state: dependency waits are
  `Backlog`; review, approval, or CI waits remain `In progress`.

## Output

Report the handoff comment, released handling, and next action or resume
condition. If saving fails, report the failure without claiming a successful
handoff.
