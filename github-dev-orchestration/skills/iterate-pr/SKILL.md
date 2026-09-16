---
name: iterate-pr
description: Address PR feedback and CI, or hand off while waiting for actionable review, approval, or check results.
---

# Iterate PR

## Use

If shared context is missing, load `orchestrator-boot`.
For a submitted issue PR. Read-only assessment needs no ownership; return
`not_ready` with suggested `continue-issue` before changing released work.

## Steps

1. Use `references\PR-STATE.md` to read head/base, required or explicitly
   requested reviews, feedback, threads, CI, and issue decisions/handoffs.
   Include current caller-supplied approval or merge-exception evidence.
   Check merge/closure first: merged work returns `ready_to_complete` with
   suggested `complete-issue` for cleanup. Closed-unmerged or conflicting state
   needs disposition, not another repair.
2. Before repairs or review mutations, preserve a current report-only `findings`
   result: `findings` stops without automatic remediation or another review.
   If repairs need another pass in an exhausted review run, return `not_ready`
   with suggested `self-review` to report the limit before making unreviewed
   fixes. Current clean evidence needs no additional pass for completion.
3. Verify new feedback and branch-owned failures against the accepted outcome
   and surrounding code. If repair requires an outcome/dependency change or a
   revised design, return `not_ready` and suggest `plan-issues` or `design-issue`,
   respectively.
   List independent follow-ups without creating them. Otherwise repair within
   the accepted design, validate, commit, push, and verify the remote head.
   Answer incorrect feedback with evidence. A sticky `CHANGES_REQUESTED` alone
   is not new work; request re-review and wait for new evidence when approval is
   still needed. An approval exception never dismisses valid unaddressed findings.
4. For other missing, stale, or non-clean self-review evidence, return
   `not_ready` with suggested `self-review` or its already-recorded next action.
   Preserve the review run/count; neither a retry nor this skill may reset an
   exhausted run.
   Reuse current clean evidence for CI-only changes.
5. Reply with commit/evidence links; resolve threads only when allowed and
   request re-review when needed. Return `ready_to_complete` for verified direct
   merge readiness or queue admission under the PR-state reference; report which.
   Do not wait for queue-only checks before the PR can enter that queue.
   Apply only verified, current merge exceptions for this PR; otherwise preserve
   normal review and queue requirements.
6. If the caller explicitly chooses to observe this wait, return `waiting`
   with head/base, all unmet conditions, and unchanged handling; do not release
   handling or poll here. Otherwise, for an unmet approval, review, applicable CI,
   an already-entered queue, or infrastructure repair, use one `handoff-issue`
   with a condition covering new actionable feedback or satisfied requirements.
   An explicit user hold remains a wait even if CI passes.
   Already-released work with an unchanged required wait
   returns `waiting`, without setup, polling, or a duplicate handoff.

## Output

Return `ready_to_complete`, `not_ready`, `waiting`, `findings`, `handed_off`, or
`partial_failure`, with head/base, resolutions, evidence, handling state, and
resume conditions.
Suggested next skill after `ready_to_complete`: `complete-issue`.
Do not invoke it here; this skill does not merge or close the issue.
