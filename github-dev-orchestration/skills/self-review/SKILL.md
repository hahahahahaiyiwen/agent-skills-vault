---
name: self-review
description: Independently review an issue's solution, triage findings against its scope and design principles, and fix selectively or hand off unresolved decisions.
---

# Self Review

## Use

If shared context is missing, load `orchestrator-boot`.
After implementation or a later review request; a PR is not required.
Require the active handler and ready environment.

## Steps

1. **Prepare.** Give the independent reviewer the issue scope, acceptance
   criteria, accepted design, manifest, repository principles, and whole worktree.
   Require clean committed work; identify base/head SHAs and issue/design/guidance
   revisions. Validate `repos.<key>.self_review` in `RESOURCE-MAP.yml`: a mapping
   with `mode` (`single_pass` or `until_clean`, default) and `max_iterations`
   (default 3; positive integer, not a boolean). Reject malformed/unknown settings.
2. **Review.** Reuse only verifiable reports for unchanged revisions and no later
   unresolved findings; single-pass reuse requires the same request.
   Otherwise check the remaining budget and record `## SELF REVIEW` as `started`
   on the issue with run/request, pinned mode/limit, pass number, reviewer/source,
   and revisions. Independently inspect relevant context, not only changed lines,
   including design flaws; the reviewer remains read-only and reports supported
   findings.
   Started, interrupted, and verification passes count. Fixes, retries, and
   continuation never reset the run; only a later independent review request
   starts a new run with new settings.
3. **Triage.** Assess the problem, not automatically its suggested fix:
   `fix` for required scoped corrections or introduced regressions;
   `no_fix` for evidenced refutations, accepted tradeoffs, or unrelated follow-ups
   (list only);
   `needs_decision` for unresolved action or scope/design questions.
   Non-action cannot waive acceptance, regressions, quality gates, or user
   requirements. Preserve original findings; save pass result (`clean`,
   `findings_remaining`, or `interrupted`), dispositions, evidence, rationale,
   authority, and remaining count on the issue before fixes or handoff. Missing
   triage remains undecided. In either mode, unresolved decisions require
   `handoff-issue` with reason `review_decision`, alternatives, recommendation,
   and the specific decision needed to resume, not speculative edits.
4. **Act.** Return `clean` only for a completed current independent pass with no
   required or undecided findings remaining. Justified non-action or clarification
   alone needs no extra pass; changed revisions invalidate clean evidence.
   `single_pass` permits one pass and returns `findings` without fixes or repeats
   when corrections remain. In `until_clean`, check that a verification pass
   remains before fixing; otherwise hand off with `review_limit`, without
   unreviewed final fixes.
   Needed design/planning returns `not_ready` with the next skill, preserving
   the run/count. Otherwise the handler fixes only scoped corrections, validates,
   commits, pushes, and independently reviews again. Interruption, unavailable
   review, failure, or repeated non-progress also requires handoff.
   Missing or conflicting evidence is never clean.

## Output

Return `clean`, `findings`, `not_ready`, `handed_off`, or `partial_failure`, with
run/pass state, revisions, dispositions, and issue evidence linked from any PR.
Suggested next skill after `clean`: `open-pr` or `iterate-pr`; do not invoke it here.
Review grants no exception to CI, required approvals, or thread resolution.
