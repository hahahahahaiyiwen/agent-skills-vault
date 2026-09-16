---
name: reconcile-board
description: Inspect or repair the four-state board and report claimable, resumable, waiting, or inconsistent work.
---

# Reconcile Board

## Use

If shared context is missing, load `orchestrator-boot`.
For a board snapshot or after graph/lifecycle changes. This skill alone updates
Project status. `--read-only` forbids all writes, labels, and comments.

## Steps

1. Reuse loaded mapping and metadata. Inspect only the changed issues and their
   parents/dependents, or all pages for a board request. Use
   `references\PROJECT.md` and `..\plan-issues\references\ISSUE-GRAPH.md`.
2. Read contracts, issue state/reason, blockers, branch/PR linkage, and latest
   handling/handoff records. Read `..\iterate-pr\references\PR-STATE.md` only
   when review/check details are needed to explain a wait or next action.
   Report unmet approvals and their recorded source, including explicit user
   holds. The caller decides whether it can supply a missing decision; do not
   infer new authority from configuration.
   Reuse verified completion/release records for Done items; inspect unfinished
   cleanup instead of replaying completed delivery.
3. Check for contradictory evidence, then apply the first matching row:

| Evidence | State or action |
|---|---|
| Closed as completed with accepted outcome and merge/no-PR evidence | `Done` |
| Cancellation, missing graph data, conflicting handlers, or ambiguous PR linkage | Report the problem; do not infer readiness or completion. |
| Active handler gains a blocker without a handoff | Report the required handoff to that handler before changing status. |
| Unsatisfied issue dependencies | `Backlog`, even with a branch or PR. |
| No issue blockers, but started work awaits a required decision, review, or CI | `In progress`; preserve the wait. |
| Dependency handoff cleared, with no later successful continuation | `Ready`; retain the branch for `continue-issue`. |
| Successful claim/continuation or another handoff for started work | `In progress` |
| No existing work and no blockers | `Ready` |

4. Report partial setup or an unexplained branch instead of assuming an active
   handler. Do not mutate drafts, read-only mappings, or unresolved repositories.
   Parenthood alone proves neither blocking nor completion; tracking parents
   need their acceptance evidence before `complete-issue`.
5. In write mode, recheck facts, apply only changed statuses, and verify saved
   values. In read-only mode, report proposed changes without applying them.
   Never clear a human wait because an unrelated check completed.

## Output

Return `reconciled`, `snapshot`, or `partial_failure`, with issue/state, handler
or wait, suggested next skill, blockers, changes, and incomplete operations.
Distinguish fresh claims from continuation; summarize Done history.
