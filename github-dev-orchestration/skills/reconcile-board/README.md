# Reconcile Board

Reconciliation reads current GitHub facts and proposes or corrects board status.
Preflight loads missing orchestration context; input identifies a Project or
affected issues. `--read-only` prohibits all writes, not just status edits.

Inspect only the requested scope, with complete pagination for whole-board
requests. Report unknown or conflicting state; update only changed statuses and
verify them. No ownership claim or new lifecycle stage is implied.

`references\PROJECT.md` keeps the four-state table and Project access essentials.
Other skills may use it to update affected items directly.
