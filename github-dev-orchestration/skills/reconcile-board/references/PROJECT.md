# Board State and Project Access

Any acting skill may update affected items; reconciliation is not a required
round trip.

## Four states

| State | Evidence |
|---|---|
| `Backlog` | At least one native dependency is unsatisfied; preserve active work before pausing. |
| `Ready` | New unblocked work, or a released dependency wait has cleared; retain the branch for continuation. |
| `In progress` | Started, unblocked work, including waits for review, approval, or CI. |
| `Done` | Accepted outcome delivered, issue closed as completed, and PR merged where applicable. |

Cancellation is not delivery. Parent links are not blockers or completion
evidence; a branch or assignee alone does not prove active handling. Report
conflicts or unknown evidence, and residual cleanup separately from delivery.

## Project access

Resolve the configured Project owner/number, Status field, and four distinct
option IDs with `gh project view` and `gh project field-list`. Reuse unchanged
metadata; missing options are configuration gaps.

Paginate relevant connections. For one issue, select the configured Project in
its `projectItems`; for whole-board reads, follow
`pageInfo { hasNextPage endCursor }` through all pages.
Failed or partial reads cannot establish a complete snapshot.

Attach missing items with `gh project item-add`; update statuses with
`gh project item-edit` using resolved project/item/field/option IDs. Refresh
facts, update only changed statuses, and verify saved values. Respect read-only
requests and reference-only entries; report failed/partial updates.
