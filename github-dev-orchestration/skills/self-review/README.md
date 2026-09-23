# Self Review

Self-review assesses the issue's solution in its project context, with the
whole worktree available for exploration. A diff is an entry point, not the
review boundary. Preserve independent findings and exact-code evidence.

Triage findings against issue scope, acceptance criteria, the accepted design,
and project principles before fixing anything. Required corrections differ from
optional improvements, intentional tradeoffs, and refuted findings. Preserve the
evidence and reason for not acting; do not expand the issue to satisfy every
suggestion. Ambiguous action or scope/design decisions need a concrete handoff,
not speculative fixes or silent dismissal.

Project settings choose report-only `single_pass` or bounded `until_clean`.
Keep run/pass state durable on the issue; continuation cannot reset it.
Final-pass required fixes stop before unreviewed changes. A current completed
review can be clean with justified non-actionable findings, but never with
required or undecided findings remaining. These settings never authorize
GitHub bypass; the caller supplies any required approvals or merge exceptions,
and CI remains required.
Return review results to the caller. A needed design/planning stage returns
`not_ready` without resetting the review run; clean review does not publish a PR.

The skill is self-contained: prepare, review, triage, and act.
