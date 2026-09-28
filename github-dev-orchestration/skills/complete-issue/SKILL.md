---
name: complete-issue
description: Merge a ready GitHub PR, close its issue, clean up the issue worktree, and update the main worktree.
---

# Complete Issue

## When to use

To finish delivery of an issue with a PR and complete local cleanup.

## Preflight

Invoke `orchestrator-boot` if `..\orchestrator-boot\references\RESOURCE-MAP.yml`
is not in context.

## Input

The target GitHub issue, identified by URL or repository and issue number.
Optionally provide its PR and explicitly request admin bypass; otherwise use
normal GitHub merge requirements.

## Guidance

- Check the issue's PR status, acceptance, CI, and review requirements,
  accounting for an explicitly requested bypass. A missing, draft,
  closed-unmerged, or unready PR blocks completion. If already merged, finish
  only missing completion updates or cleanup.
- Merge the PR using `gh pr merge` with `--match-head-commit <verified-head>`.
  Add `--admin` only when input explicitly requests admin bypass; it does not
  waive CI or explicit holds. Confirm actual merge; queue entry or scheduled
  auto-merge is pending, not completion.
- Post or update a `## COMPLETE` issue comment summarizing the delivered outcome
  and linking the merged PR.
- Close the issue with `state_reason=completed`, update its configured board
  item to `Done`.
- After closure, work from the verified main worktree at `repos.<key>.path`.
  Remove the exact issue worktree with `git worktree remove` without `--force`,
  only when clean and its branch/head matches the delivered PR; use PR evidence
  for squash/rebase merges. Skip absent worktrees. Preserve dirty work, extra
  commits, and unverified worktrees.
- Fetch the configured repository's remote default branch. Fast-forward only the
  clean, behind-only main worktree using `git merge --ff-only`. Leave an
  up-to-date main unchanged; report dirty, ahead, or divergent states without
  resetting. Record cleanup and main-update results or blockers in `## COMPLETE`,
  then release handling.

## Output

Report the completed PR and issue, or why completion was declined or remains
pending. Report cleanup and main-update status separately, including failed or
partial updates or unavailable local worktrees.
