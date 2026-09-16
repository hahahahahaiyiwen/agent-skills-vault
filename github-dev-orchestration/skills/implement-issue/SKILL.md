---
name: implement-issue
description: Implement and validate an accepted issue design while respecting the configured project manifest.
---

# Implement Issue

## Use

If shared context is missing, load `orchestrator-boot`.
After `design-issue` returns `ready_to_implement` or continuation restores an
accepted design. The active handler works in the issue environment.

## Steps

1. Respect repository instructions and `repos.<key>.manifest` from loaded
   `RESOURCE-MAP.yml`, when configured. This path is repository-relative;
   report unreadable declared guidance. Confirm the design, branch/head,
   blockers, and required decisions are current; preserve unrelated local work.
   If design or required approval is missing, return `not_ready` and suggest
   `design-issue`; do not perform that stage here.
2. Implement the accepted outcome using project conventions. Fix root causes,
   add independent acceptance/regression evidence, and update affected docs.
   Run focused checks while iterating and the repository-required validation.
3. Make routine choices within the accepted design independently. If a material
   approach change is needed, return `not_ready` and suggest `design-issue`.
   For required outcome/dependency changes, suggest `plan-issues` instead.
   List independent follow-ups without creating them or expanding the task.
4. Inspect the change for unintended scope, regressions, secrets, and artifacts.
   Commit intended paths, push, verify the remote head, and record `## PROGRESS`
   with acceptance evidence and validation for that commit.
5. Use `handoff-issue` when a required decision, unavailable environment, or
   interruption blocks progress. Do not report failing checks or pushes as success.
   For an expressly non-code outcome, verify its evidence without inventing
   repository changes or an empty PR.

## Output

Return `ready_for_review`, or `ready_to_complete` for a verified no-PR outcome.
Otherwise return `not_ready`, `handed_off`, or `partial_failure`. Include head,
evidence, and manifest/design references.
Suggested next skill: `self-review` after `ready_for_review`, or `complete-issue`
after `ready_to_complete`; do not invoke either as part of implementation.
