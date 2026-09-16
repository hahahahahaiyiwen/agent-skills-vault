---
name: plan-issues
description: Create or revise the issue graph from project goals, high-level design, or development discoveries.
---

# Plan Issues

## Use

If shared context is missing, load `orchestrator-boot`.
For initial planning or changes to outcomes, decomposition, or dependencies.
An implementation choice within one outcome belongs in `design-issue`.

## Steps

1. Read the configured project manifest, relevant design, and affected issues.
   Search related open and closed issues before creating work. Use project
   guidance for just-enough high-level design. Settle the proposed plan and
   required approvals before graph writes; reuse accepted, unchanged decisions.
   If a decision cannot be settled, use `handoff-issue` only for your own
   handling interval. Otherwise return `needs_decision` with the proposal and
   missing decision, recording it on an existing affected issue when available.
   Do not create a handoff-only issue or release another handler's work.
2. Define each issue's goal, bounded work, acceptance criteria, and non-goals;
   identify its parent or root status and blockers or lack of them. Parenthood
   does not imply a dependency. A tracking parent that requires child outcomes
   needs explicit blocked-by links; state when completion needs no PR.
3. Use `references\ISSUE-GRAPH.md` to create or revise native relationships.
   Check existing edges, cycles, and self-links; preserve human content and
   completed history. Coordinate changes to another handler's active work.
   Record evidence for scope/dependency revisions rather than quietly dropping
   acceptance requirements.
4. If a new prerequisite stops your current issue, preserve it through
   `handoff-issue` with reason `dependency`. An independent follow-up does not
   pause that work.
5. Add new issues to the Project once and invoke `reconcile-board` for affected
   issues, parents, and dependents. Cancellation or duplicate replacement does
   not satisfy dependents; reconcile the canonical replacement explicitly.
6. Record `## PLAN` on the affected issue or common parent, with the design
   decision and its approval/autonomy basis, guidance revisions, changed issue
   references, and next action. Link detailed design rather than copying it.
   After a partial write, finish verified missing steps instead of duplicating
   issues or rolling back durable work.

## Output

Return `planned`, `unchanged`, `needs_decision`, `handed_off`, or `partial_failure`,
with issue URLs, graph changes, reconciled states, unresolved decisions, and a
suggested next action.
Do not start Dev or claim newly Ready work here.
