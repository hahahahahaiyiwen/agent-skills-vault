---
name: complete-issue
description: Verify delivery, merge where applicable, close the issue, and safely clean resources and reconcile dependent work.
---

# Complete Issue

## Use

If shared context is missing, load `orchestrator-boot`.
When evidence permits completion, or completion was interrupted. Require the
handler and local environment; released work returns `not_ready` with suggested
`continue-issue`.

## Steps

1. Read the outcome, blockers, handling, and PR linkage. Inspect merge/closure
   first. For an already merged PR, skip the merge gates and finish missing
   postconditions; deleted refs or changed rules do not require another merge.
   With no PR, verify the accepted no-PR outcome, required child/dependency
   outcomes, and absence of unmerged implementation; then proceed to step 5.
2. Before merging, require satisfied blockers, acceptance, current clean
   self-review, CI, and required decisions. Use
   `..\iterate-pr\references\PR-STATE.md` for the actual head/base requirements
   and verify any caller-authorized exception applies to this PR repository.
   For a required queue, assess its admission requirements rather than waiting
   for checks that can run only after entry.
   Unknown evidence, drafts, closed-unmerged PRs, or non-clean review cannot
   permit merging. For needed repairs, return `not_ready` and suggest
   `iterate-pr`. If the caller explicitly chooses to observe this wait, return
   `waiting` with head/base, all unmet conditions, and unchanged handling;
   otherwise hand off an actual wait. Never restart an exhausted review run to
   pass this gate.
3. Choose one integration path. For a required merge queue without an eligible
   admin bypass, use `gh pr merge` with explicit PR/repository and
   `--match-head-commit <reviewed-head>` without forcing a method.
   Otherwise select a permitted merge method consistent with rules and project
   guidance; call the same command with its method flag. Prefer normal merge;
   add `--admin` only for a current, explicit caller-authorized exception that
   passes the PR-state reference's guards. Recheck its authority and CI before
   the operation.
   Do not use `--delete-branch`; cleanup is separate. If GitHub denies the
   operation, refresh state and apply step 2's wait handling or report/handoff
   the blocker, not weaken protection or blindly retry.
4. Verify `mergedAt`, merge commit, base, and head before reporting integration,
   including admin merge. Enqueueing/deferred merge is `waiting_for_merge`:
   save a `merge_queue` handoff that resumes on merge or actionable queue failure,
   not merely because the pre-queue checks still pass.
5. Close a verified merge or verified no-PR outcome as `state_reason=completed`,
   if still open; record evidence. Cancellation and duplicate closure are not
   completion. Do not invent an empty PR or silently reinterpret cancellation.
6. Perform cleanup from the main checkout, not the worktree being removed.
   Fast-forward the local default branch only if clean and safe. Remove the
   exact task worktree only when clean and its commits are accounted for.
   Delete only its unattached local branch whose head matches the completed
   task head; preserve extra local commits. For squash/rebase, verify the PR's
   integrated task head rather than relying on ancestry.
7. Skip an absent remote task ref; otherwise delete only if it still matches
   the integrated task head, not the merge commit. For no-PR work, require it
   to remain at the claim base. Use an expected-head check, for example
   `git push --force-with-lease=refs/heads/<branch>:<integrated-head> origin :refs/heads/<branch>`.
   Preserve advanced refs and unverified resources; never assume access to a
   previous machine or remove another agent's worktree.
8. Reconcile the issue, parent, and dependents; verify `Done` and report newly
   Ready work without claiming it. Post one `## COMPLETE` with outcome/evidence,
   validation, approval/exception basis when used, actual cleanup, state, and
   `Handling: released`.

## Output

Return `completed`, `not_ready`, `waiting`, `waiting_for_merge`, `handed_off`, or
`partial_failure`, with outcome/evidence, handling state, cleanup, status, and
suggested next action. Distinguish completed delivery from unfinished cleanup;
preserve residual work and record a cleanup handoff. Re-runs finish only missing
postconditions.
