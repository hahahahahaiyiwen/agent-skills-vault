# Self Review

Self-review assesses the issue's solution in its project context, with the
whole worktree available for exploration. A diff is an entry point, not the
review boundary. Preserve independent findings and exact-code evidence.

Project settings choose report-only `single_pass` or bounded `until_clean`.
Keep run/pass state durable on the issue; continuation cannot reset it.
Final-pass findings stop before unreviewed fixes. These settings never authorize
GitHub bypass; the caller supplies any required approvals or merge exceptions,
and CI remains required.
Return review results to the caller. A needed design/planning stage returns
`not_ready` without resetting the review run; clean review does not publish a PR.
