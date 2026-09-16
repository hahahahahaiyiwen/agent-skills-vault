# Iterate PR

This module owns submitted PR feedback and check handling, including external
review waits. The shared PR-state reference is also used at submission and
completion. Preserve head-bound evidence, complete required-review/check reads,
sticky-review handling, and handoff instead of unchanged polling. An explicit
caller-managed wait instead returns `waiting` with all unmet conditions and
unchanged handling; the caller observes it, not this skill. Only the
active issue handler repairs the branch. Propagate non-clean self-review
results; PR iteration is not a way to reset its run limit.
Consume current approval/exception evidence from the caller, not an inferred
policy. Exceptions never dismiss actual feedback or CI failures.
Check report-only findings and exhausted review runs before repairs, not after
changing the branch. A clean final pass still permits completion.
Needed design/planning/self-review returns `not_ready` with a suggested next
skill. Completion is also a suggestion, not an automatic invocation.
Distinguish direct merge readiness, queue admission, and an already-entered
queue wait; queue-only checks cannot prevent the step that enqueues the PR.
