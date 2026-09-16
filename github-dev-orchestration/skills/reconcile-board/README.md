# Reconcile Board

This module owns four-state projection and board reporting, including a
strictly read-only mode. It consumes native graph and handling facts rather
than inventing an activation policy. Preserve complete pagination, targeted
refreshes, dependency precedence, and the distinction between retained work,
an active handler, and a waiting handoff.
Reuse verified completion/release evidence for Done history while surfacing
unfinished cleanup; Done is not proof that the handler has released ownership.
