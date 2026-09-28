---
name: self-review
description: Review an issue's solution and clear findings at a user-selected severity threshold.
---

# Self Review

## When to use

To review an issue's solution. Read-only review needs no ownership claim.

## Preflight

Invoke `orchestrator-boot` if `..\orchestrator-boot\references\RESOURCE-MAP.yml`
is not in context.

## Input

The target GitHub issue, identified by URL or repository and issue number.
Ask the user for the severity threshold if not supplied: Low, Medium, High,
or Critical, in increasing order. Include the selected level and all higher levels.

Honor `repos.<key>.self_review`: `mode` is `until_clean` (default) or
`single_pass` (report-only). Read-only requests are also report-only.
`max_iterations` is a positive integer, not a boolean, default 3.
Reject invalid settings.

## Guidance

- Have an independent, read-only reviewer assess the relevant whole worktree
  and design, including uncommitted changes. Count findings by severity.
- Unless report-only, address qualifying findings within issue scope and project
  principles; verify fixes. Raise consequential uncertainty before speculative
  changes; keep unresolved findings counted.
- Re-review after fixes until zero findings at or above the threshold remain,
  or the iteration cap is reached. Count all started, interrupted, and verification
  passes across retries and continuation. Pause on unknown prior counts, blockers,
  or repeated non-progress rather than resetting the budget.

## Output

Report the reviewed version, threshold, severity counts, fixes, and remaining
findings. Mark the target met only after a completed review of the current version
confirms zero qualifying findings; otherwise report the unmet target and stopping
reason.
