# Complete Issue

Completion checks the issue's PR, merges ready work, posts a `## COMPLETE`
issue comment with the delivered outcome and merged PR, then closes the issue
and updates its configured board item to `Done`. After closure, remove the
delivered issue worktree and fast-forward the mapped main worktree.

Preflight invokes `orchestrator-boot` when the resource map is not in context.
Input identifies the issue and may include its PR and an explicit admin-bypass
request. Only that request permits `--admin`; it does not waive CI, explicit
holds, or other non-bypassed requirements.

Immediately before merging, refresh native blocking dependencies and confirm
completed closure. Cancelled dependencies or unknown/incomplete reads block
completion, including admin-bypass requests. Already-merged recovery does not
replay this pre-merge check.

A missing, draft, closed-unmerged, or unready PR prevents completion. Queue entry
and scheduled auto-merge remain pending until the PR actually merges. An already
merged PR needs only missing completion updates or cleanup, not another merge.
Optional intermediate skill invocations are not prerequisites.

Work from `repos.<key>.path`, the main worktree on the repository default branch.
Remove only the exact, clean issue worktree whose branch/head matches delivered
work; preserve extra commits and use PR evidence for squash/rebase merges.
Main updates are fast-forward-only. Preserve dirty, ahead, or divergent states
and report unavailable local worktrees rather than claiming cleanup succeeded.
Record actual cleanup and main-update results in `## COMPLETE` before releasing
handling; incomplete local cleanup does not undo verified delivery.
