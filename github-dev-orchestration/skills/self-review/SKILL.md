---
name: self-review
description: Independently assess an issue's solution in full project context, reporting findings once or iterating toward a clean review.
---

# Self Review

## Use

If shared context is missing, load `orchestrator-boot`.
After implementation or a later review request; a PR is not required. Require
the active handler and ready environment. Give the independent reviewer the
entire issue worktree for exploration; only the handler owns fixes.

## Steps

1. Load configured manifest guidance and `repos.<key>.self_review` from
   `RESOURCE-MAP.yml`. Defaults: `mode: until_clean`, `max_iterations: 3`.
   Settings must be a mapping: `mode` is `single_pass` or `until_clean`;
   `max_iterations` is a positive integer, not a boolean.
   Report malformed or unknown settings before review; do not silently default
   invalid values. `single_pass` always permits one pass.
2. Prepare reviewer context: worktree path, design, acceptance criteria, manifest,
   and repository instructions. Use the diff to locate changes, not to limit
   review. Explore architecture, callers, dependencies, unchanged code, tests,
   and failure behavior as needed. Run targeted checks or isolated experiments;
   leave tracked files and the task branch unchanged. Whole-worktree access
   does not mean loading every file into context.
3. Require a clean worktree matching the committed head; identify base/head and
   guidance revisions. Reuse clean evidence only with a verifiable reviewer
   source, unchanged context, and no later unresolved finding. Malformed or
   conflicting records, or `clean` with nonzero findings, cannot authorize
   progression. Findings need not be on changed lines; list independent
   improvements as suggested `plan-issues` follow-ups without creating them here.
4. Start or resume a review run, pinning its mode/limit. Continuation and fixes
   preserve the run and count. Only a later independent review request starts
   a new run; a retry is not one. New settings apply to new runs.
   Recover existing results instead of duplicating a pass; reuse a finished
   single-pass report only for the same request and revisions. Check remaining
   passes before launching the reviewer. An exhausted run must hand off without
   another pass. Before each pass, record `## SELF REVIEW` with run ID/request,
   mode/limit, pass number, reviewer/source, base branch/SHA, head SHA, guidance
   revisions, and result `started`. A started pass counts, including an
   interrupted one.
5. Run the independent investigation and report all supported issue-relevant
   findings, including high-level design flaws. Finish the record with `clean`,
   `findings_remaining`, or `interrupted`, findings/count, evidence/source, and
   resolutions. Changed code/guidance invalidates a pass's clean result. Apply
   the configured mode:

| Result | Action |
|---|---|
| No findings; reviewed code and guidance remain current | Return `clean`. |
| Findings in `single_pass` | Return `findings`; do not automatically fix or repeat. |
| Findings in `until_clean`, with passes remaining | If remediation needs another lifecycle stage, return `not_ready` with that suggested skill and preserve the run/count. Otherwise the handler fixes, validates, commits, and pushes; independently review again in the same run. |
| Findings or an incomplete review with no passes remaining | Hand off with reason `review_limit`; do not make unreviewed final fixes. Resume only for a later independent review request. |

6. A fix is not a clean review; verification consumes a pass too. Repeated
   non-progress, unavailable review capability, or execution failure requires
   `handoff-issue` with a concrete condition. Keep unresolved findings visible;
   an interrupted pass is not clean evidence.

## Output

Return `clean`, `findings`, `not_ready`, `handed_off`, or `partial_failure`, with
run/pass count, effective settings, reviewed revisions, and evidence. Keep
records on the issue and link them from a PR if present.
Suggested next skill after `clean`: `open-pr`, or `iterate-pr` for an existing PR.
`findings` stops for the caller to decide remediation. Do not publish or advance
the PR here. CI remains required; self-review mode grants no merge exception.
