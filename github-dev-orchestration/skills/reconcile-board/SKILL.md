---
name: reconcile-board
description: Inspect GitHub Project status and align it with current issue and delivery facts.
---

# Reconcile Board

## When to use

To inspect a board or correct issue-status drift.

## Preflight

Invoke `orchestrator-boot` if `..\orchestrator-boot\references\RESOURCE-MAP.yml`
is not in context.

## Input

The configured GitHub Project or affected issues. `--read-only` requests a
snapshot without writes.

## Guidance

- Read current issue, dependency, handling, and PR facts. Inspect affected
  issues and their blockers/dependents for a targeted request; include all pages
  for a whole-board request.
- Derive states using `references\PROJECT.md`; consult
  `..\plan-issues\references\ISSUE-GRAPH.md` for native relationships.
  Report conflicting or unknown evidence rather than guessing.
- In write mode, update only changed statuses and verify saved values.
  `--read-only` means no writes, including comments or ownership changes.

## Output

Report changed or proposed states, actionable or waiting work, and unresolved
facts or failed/partial updates. Reconciliation does not claim work.
