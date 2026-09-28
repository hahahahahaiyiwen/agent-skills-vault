# Handoff Issue

Handoff preserves issue progress for another handling agent or session.
Preflight loads missing orchestration context; input identifies the issue
and why work is being handed off.

A `## HANDOFF` issue comment contains progress, branch/head and PR links,
important decisions, remaining work, and the next action or resume condition.
Keep unresolved findings, the selected review threshold, and remaining review
budget when relevant, and identify anything that is still local-only.

Verify the record before releasing handling, then stop changing the task branch.
Report the saved handoff or the failure; a failed write does not release handling.
Board status follows actual blockers, not the mere fact of a transfer.
