---
name: continue-issue
description: Restore existing issue work and its local environment, then suggest the next unfinished action.
---

# Continue Issue

## Use

If shared context is missing, load `orchestrator-boot`.
For existing work. The agent, machine, checkout, and local paths may differ
from the original handler's environment.

## Steps

1. Read the issue, native blockers, branch/PR, and latest handling/handoff
   records. No existing work on an open Ready issue means `claim_required`.
   Resolve work from GitHub references, not a previous local path.
   Use only handoffs not superseded by a later acquisition.
2. Inspect closure/merge before old review waits. Return `already_completed`
   if nothing remains; suggest `complete-issue` for verified merge cleanup.
   Cleanup skips obsolete delivery gates, not ownership/environment checks.
   Cancellation returns `waiting` with suggested `plan-issues`, never automatic
   reopening.
3. For unfinished delivery, evaluate the current resume condition against
   evidence, including current decisions or exceptions supplied by the caller.
   Record their authority source; an old handoff grants no new authority.
   Explicit user holds and ambiguous wait origins remain unresolved.
   Evaluate PR review/queue waits through the PR-state reference, including
   current CI and bypass restrictions. Return `waiting` without setup or another
   comment while a required condition is unsatisfied.
   New actionable feedback or a CI failure can permit repair while merge gates
   remain unmet; do not require merge readiness before restoring repair work.
4. Verify no other agent is handling or preparing the issue. When acquiring
   released work, record `## CONTINUE` with `Handling: preparing`, handler,
   branch/head, answered handoff, and triggering evidence.
   Reuse this agent's verified acquisition.
5. Follow `..\orchestrator-boot\references\LOCAL-ENV.md`: clone/fetch, restore the
   existing worktree, and prepare declared setup. Preserve dirty/divergent work.
   Use integrated-commit recovery for a merged PR without recreating deleted
   remote refs.
6. Verify guidance, head, blockers, handling, and environment readiness; update
   a new record to `Handling: active` and invoke targeted `reconcile-board`.
   Identify the next unfinished action, not the whole Dev cycle; do not execute it:

| Need | Suggested next skill |
|---|---|
| Graph/outcome revision | `plan-issues` |
| Missing/changed design or required approval | `design-issue` |
| Unfinished implementation | `implement-issue` |
| Review of the current solution | `self-review` |
| Cleanly reviewed work without a PR | `open-pr` |
| PR feedback/checks or completion assessment | `iterate-pr` |
| Satisfied completion evidence or merged-PR cleanup | `complete-issue` |

7. Use the recorded next action as a hint, not a stale command. Preserve any
   current self-review run and iteration count. Record setup failure through
   `handoff-issue`; do not report continuation with a missing environment.

## Output

Return `continued`, `waiting`, `claim_required`, `already_completed`, or
`partial_failure`, with handling/evidence references, branch/head, environment
result, status, and suggested next skill. Continuation ends after restoration
and routing; the next lifecycle action belongs to the caller.
