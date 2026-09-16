---
name: handoff-issue
description: Persist progress, release active handling, and state the condition and next action for continuation.
---

# Handoff Issue

## Use

If shared context is missing, load `orchestrator-boot`.
When work pauses or changes agent/context. A planning revision without a pause
needs a progress update, not a handoff. Finishing an individual skill or approving
a design is not, by itself, a reason to release handling.

## Steps

1. Verify the handler/acquisition and read current task state. Do not release
   another active agent's work.
2. Push coherent, safe progress from the issue worktree and verify remote
   commits. For planning-only work or failed setup, record what exists without
   inventing a worktree. Never commit secrets or invalid artifacts for handoff.
3. Record the handler/acquisition, progress, accepted decisions, remaining work,
   issue/branch/head/PR, validation, and any active review run. Identify local-only
   state and its recovery limitation; local paths are hints, not prerequisites.
4. Give the pause reason, objective resume condition, and next skill. Use
   `dependency` for native blockers. PR review resumes on new actionable
   feedback or satisfied approvals; CI resumes on actionable result changes;
   `merge_queue` resumes on merge or queue failure, not already-passing checks.
   For a decision, include the request, alternatives, recommendation, and
   source of the approval requirement. Distinguish a workflow-only approval wait
   from an explicit user hold, capability failure, or task dependency; a handoff
   is evidence, not new authority.
5. Post `## HANDOFF` with `Handling: released` before reconciliation; reuse an
   equivalent latest handoff only for the same handling interval. Verify it is
   saved, then stop implementation. Preserve a self-review run's count, including
   exhaustion; handoff is not a new review request.
6. Invoke targeted `reconcile-board`: dependencies mean `Backlog`; design
   approval, PR review, and CI waits remain `In progress`; completed outcomes
   awaiting cleanup stay `Done`. Report incomplete initial setup explicitly.

## Output

Return `handed_off` or `partial_failure`, with the saved record, durable progress,
status, resume condition, suggested next action, and local-only limitations.
A failed GitHub write is not successful ownership release. Do not poll unchanged
waits.
