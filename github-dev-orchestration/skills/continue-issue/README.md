# Continue Issue

Continuation resumes existing issue work without a new claim or branch.
Preflight loads missing orchestration context; input identifies the issue
and optionally its handoff comment.

Check current issue/PR state, resume conditions, and handling before restoring
the existing branch and worktree through the mapped main worktree. Preserve
dirty/divergent work and explicit holds; completed or cancelled work is not
restarted. Merged work needs only missing completion updates or cleanup, not
a recreated task branch or worktree.

Record the handling agent, branch/head, and next action in a `## CONTINUE`
issue comment. Carry forward unresolved decisions, findings, the selected review
threshold, and remaining review budget.
A missing old heading does not block recovery, and suggested next steps are
not required stages. Return the resumed context and next action or the blocker,
without automatically executing another delivery action.
