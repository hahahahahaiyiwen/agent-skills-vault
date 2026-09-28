---
name: plan-issues
description: Review the product/project roadmap and add, edit, or remove planned GitHub issues and relationships.
---

# Plan Issues

## When to use

To create or revise the product/project roadmap. An implementation approach
change alone does not require planning.

## Preflight

Invoke `orchestrator-boot` if `..\orchestrator-boot\references\RESOURCE-MAP.yml`
is not in context.

## Input

The GitHub repository or Project and the goals or roadmap changes to plan.
A read-only request returns proposals without writes.

## Guidance

- Review project guidance and related open and closed issues before creating
  new work. Raise consequential uncertainty about scope or priorities.
- Add, edit, or remove issues from the plan with clear outcomes and acceptance
  criteria. Preserve human content, active work, and issue history; record
  material reasons on affected issues.
- Maintain native parent/sub-issue and blocked-by links using
  `references\ISSUE-GRAPH.md`. Add issues to the configured Project and update
  only affected statuses using `..\reconcile-board\references\PROJECT.md`.

## Output

Report changed or proposed issues and relationships, their rationale, and
unresolved decisions or failed/partial updates. Planning does not claim or
implement the work.
