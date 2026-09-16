---
name: design-issue
description: Design an issue's solution using its acceptance criteria and the configured project manifest.
---

# Design Issue

## Use

If shared context is missing, load `orchestrator-boot`.
After claim/continuation or when the solution needs revision. The active
handler must have the issue's local environment.

## Steps

1. Read repository instructions and `repos.<key>.manifest` from loaded
   `RESOURCE-MAP.yml`, when configured. Resolve the manifest from the repository
   root; respect its goals, architecture, tradeoffs, and delegated decisions.
   Reuse unchanged guidance/design; report unreadable declared guidance rather
   than ignoring it.
2. Read the accepted outcome and relevant code, tests, and dependencies.
   Map acceptance criteria to behavior, interfaces, evidence, documentation,
   and important compatibility/failure cases. Scale design effort to the task;
   a small issue may need only a few sentences.
3. If outcomes, shared design, decomposition, or dependencies must change first,
   return `not_ready` with `plan-issues` as the suggested next skill.
   List independent follow-ups without expanding the accepted outcome.
4. Settle material choices, explaining alternatives and the recommendation.
   Resolve required decisions and approvals under the caller's authority.
   Before asking for human approval, put a self-contained design brief in the
   approval tool's message: goal, approach, affected areas, key tradeoffs/risks,
   and scope boundaries, including changes outside the repository. A link to
   the full design may accompany the brief, but cannot replace it.
   Ask only "Approve this design?" with `approve_design` or `revise_design`.
   Do not bundle implementation or handoff into the approval choices.
   Handle requested revisions within this design action; re-brief material
   revisions before approval. Use `handoff-issue`
   for an actual pause, unresolved blocker, or transfer, not a live discussion
   or ordinary return after approval.
   Missing or declined required approval never permits `ready_to_implement`.
5. Record `## DESIGN` with the approach, acceptance/evidence mapping, decisions,
   guidance revisions, decision/approval basis, and next action. Link detailed
   design where useful.
   Do not claim acceptance is complete before evidence exists.

## Output

Return `ready_to_implement`, `not_ready`, `handed_off`, or `partial_failure`, with
the design and manifest references, decisions, and evidence plan.
Suggested next skill after `ready_to_implement`: `implement-issue`.
Stop this action after recording approval; do not implement or automatically
hand off. Design alone does not change board status.
