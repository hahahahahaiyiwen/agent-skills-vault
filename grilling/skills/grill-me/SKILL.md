---
name: grill-me
description: Stress-test the agent's own proposed design, solution, or understanding through bounded, evidence-based self-review. Use when explicitly asked to challenge its proposal, uncover weaknesses, and improve it, rather than interview the user.
disable-model-invocation: true
---

# Grill Me

## Scope

Review the agent's current proposal or explanation against the user's objective
and constraints. Identify that target from the conversation or supplied
artifact; ask for clarification if none is identifiable rather than inventing
a proposal. This is self-review, not an interview of the user.

## Review

Conduct one focused review pass, prioritizing questions whose answers could
change correctness, feasibility, or the recommendation. Useful challenges
include unmet requirements, unsupported assumptions, conflicting claims,
counterexamples, failure paths, and consequential tradeoffs. These are lenses,
not a checklist that must produce an objection in every category.

Answer those challenges using the proposal and relevant accessible evidence.
Use direct lookups where useful; delegate only when available and warranted.
Separate observations, assumptions, and inferences. Do not manufacture an answer
or dismiss a concern merely because the agent proposed the original solution.
If a necessary investigation is pending or blocked, keep the affected finding
open and state that limitation.

Make justified revisions to the proposal or explanation within the requested
scope. Then perform one focused verification of the affected conclusions and
dependencies. If issues remain or that check reveals new ones, report them
rather than restarting the review or making further unverified revisions.
Additional review passes require an explicit request.

## Human input

Ask the user only when a user-owned decision or an unavailable fact materially
blocks the review. Use the host's user-question tool when available; otherwise
ask a concise question. Give the relevant context and a recommendation only
when supported. Do not turn the agent's review questions into a user interview.

Where possible, report a conditional conclusion or unresolved limitation
instead of interrupting. A clarification resumes the current pass, not a fresh
review budget. Respect requests to stop and report the incomplete scope.

## Output and boundaries

Return the material findings, their evidence or uncertainty, the justified
corrections, and any remaining decisions or limitations. Include the revised
proposal when it changed. Do not emit an internal question-and-answer or
reasoning transcript.

If no material issues were found, state the reviewed scope without claiming
that the proposal is proven correct. A pending check or unknown fact is not a
successful verification.

Self-review does not authorize implementation changes, changed requirements,
or work beyond the caller's request. Revise the proposal, not the implementation,
unless that action was separately authorized.
