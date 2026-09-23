---
name: orchestrator-autopilot
description: Personally drive Ready and resumable issues through the lifecycle, one at a time, using each repository's autopilot policy.
---

# Orchestrator Autopilot

## Use

If shared context is missing, load `orchestrator-boot`.
Run only on an explicit request to drive the board. The agent running this
skill is the issue handler throughout claim/continuation, development, and
completion/handoff. Independent reviewers may assist, not take over delivery.

## Steps

1. Obtain a complete board view through `reconcile-board`, including all pages.
   For a read-only request, use `reconcile-board --read-only` and return
   `snapshot` without claim or other writes; incomplete reads return
   `partial_failure`. Report unresolved/reference-only issue items and non-issue
   items. No label, original-agent, or tracking-parent filter applies.
2. Execute sequentially: finish or durably hand off the current issue before
   selecting another. Prefer existing work that can advance, including
   merged-PR cleanup; enter through `continue-issue`. Unclaimed Ready work
   enters through `claim-issue`; a retained branch means continuation.
   Use available Project priority, then repository/issue identity for stable
   ties. Do not take over another preparing/active handler.
   Evaluate approval-waiting candidates under step 3 before concluding that
   none can advance; reconciliation reports facts, not mode-based authority.
   Before stopping, also consider released CI-only waits when step 3 enables
   observation.
3. Before handling a selected issue, read `repos.<key>.autopilot` from loaded
   `RESOURCE-MAP.yml`. Require a mapping with `mode`, set to `auto-approval` or
   `reasonable-approval`, and optional `wait_for_ci`; no other keys.
   `wait_for_ci` must be a YAML boolean: omitted or `false` means hand off on
   pending CI; `true` means wait until CI finishes, with no configured timeout.
   Reject quoted booleans, numbers, and null. Missing, malformed, or unsupported
   settings are a configuration problem, not permission to assume authority or
   silently exclude Ready work. Record the setting revision. Re-resolve on
   repository changes, especially for a PR in another repository.

| Mode | Approval decisions made by this agent |
|---|---|
| `auto-approval` | Select and approve recommended plan/design/implementation choices without routine human confirmation. After clean self-review and CI, authorize guarded admin bypass of PR-approval/merge-queue gates where GitHub permits it. |
| `reasonable-approval` | Read the referenced manifest. Proceed when the recommendation fits its constraints and delegation, has no material ambiguity, and needs no explicit approval. Otherwise hand off with the proposed decision and reason. Keep normal GitHub review and merge-queue requirements; this mode does not authorize admin bypass. |

   Missing or unreadable manifest guidance is not authority for reasonable
   self-approval. Preserve CORE's user holds, constraints, and quality gates.
   Interpret modes here only. When a lifecycle step reaches a decision or
   approval point, apply the selected mode using that step's evidence;
   those skills do not select approval policy.
   Record decision/exception evidence and authority; never fabricate human
   approval. Apply this judgment to reported approval waits, not an
   explicit user hold or an ambiguous requirement.
   Configuration or a historical handoff alone grants no authority outside
   this explicit run. Recheck relevant guidance before consequential decisions
   and merge; changed authority requires a fresh request, not self-escalation.
4. Claim or continue the issue yourself, prepare its local environment, and
   follow the loaded `DEV-FLOW.md` routing and each skill's next action.
   Each skill returns its result; this explicitly requested workflow owns the
   next invocation. Consume `not_ready` and its suggested prerequisite before
   retrying the blocked action, preserving partial progress and review-run state.
   A skill return is not an issue handoff or the end of this workflow.
   Do not repeat an unchanged prerequisite cycle; report the blocker and hand
   off rather than alternating skills without progress. Development may call
   `plan-issues`, not start the resulting issues before the current interval ends.
   Only this skill interprets `wait_for_ci`. Before PR actions, tell the called
   skill whether this caller will observe CI-only waits instead of releasing
   handling; ordinary skills return wait facts, not policy decisions.
   Use `complete-issue` for eligible queue admission or merge/cleanup, with only
   the exceptions authorized above. Closing an unmerged PR is not completion.
5. With `wait_for_ci: true`, observe a `waiting` result only when pending CI is
   the sole unmet gate under current approval authority. Use the CI observation
   guidance in `..\iterate-pr\references\PR-STATE.md`.
   Retain active handling and the local environment; do not hand off or start
   another issue while observing. For already-released work, observe read-only
   without acquisition; call `continue-issue` only after the resume condition
   is satisfied, rechecking ownership.
   Stop observation on CI completion, failure, cancellation, or changed
   head/base; refresh PR state and use `iterate-pr` for repair or completion
   assessment. Waiting does not restart self-review or consume review passes;
   reuse unchanged clean evidence, not evidence invalidated by changed code.
6. Preserve project review settings and run counts: autopilot retries are not
   independent review requests. Report-only `findings` require `handoff-issue`,
   awaiting a remediation decision without automatic fixes.
   A `review_decision` handoff requires resolving the specific finding's
   action or scope/design uncertainty; neither approval mode can replace that
   evidence with blanket approval or relabel it as non-actionable.
   When actual human involvement, an explicit user hold, unavailable capability,
   or an external wait not covered by step 5 prevents progress, stop any watcher,
   preserve work and hand off; then consider another issue. Required human review/approval,
   merge-queue waits, missing/unknown CI, and infrastructure or permission
   blockers are not covered by CI waiting.
   Do not manufacture approval or bypass failing/pending CI.
7. Verify GitHub evidence that your handling interval ended before moving on;
   `waiting` without acquisition needs no new handoff. Failed persistence or
   uncertain ownership means `partial_failure`, not successful release.
   Record unknown outcomes explicitly. Continue after a local failure only
   when no owned handling interval remains; stop if shared state is unreliable.
8. Consume reconciliation results or refresh changed issues, parents, and
   dependents. Do not retry failed or waiting issues without relevant new
   evidence. Except for the configured CI observation in step 5, never poll
   unchanged conditions. Never duplicate handoffs.
   Empty Ready alone is not a stopping test: after ending your handling interval,
   refresh the complete board and outstanding resume conditions.
9. Return `drained` only when the fresh, complete view proves all of:

| Remaining issue state | Required evidence |
|---|---|
| `Ready` | None remain. |
| `In progress` | Each has a durable handoff with an unsatisfied resume condition, and no active/preparing handler. |
| `Backlog` | Each has unsatisfied native issue dependencies. |
| `Done` | Accepted completion is verified. |

   No active/preparing handler may remain in any state, including Done, and no
   completion cleanup may be actionable.
   Unknown states, unresolved issue items, incomplete reads, or failures prevent
   `drained`. Another agent's active work means `paused`, not successful drain.
   On user/platform interruption, stop any watcher, preserve progress and hand off;
   report anything that could not be saved or released. Never change status merely
   to empty Ready.
   End this invocation's autonomy context when the run stops.

## Output

Return `drained`, `snapshot`, `paused`, or `partial_failure`, with completed issue/PR
links, waiting handoffs and resume conditions, remaining Ready/running work,
reported non-issue items, and incomplete operations.
`drained` means the stopping condition holds now, not that every issue is Done.
Keep durable progress on GitHub, not another state journal or issue transcript.
