# GitHub PR Requirements

On-demand reads for PR submission, iteration, and completion. Keep the
summary limited to requirements and actionable evidence, not raw histories.
Reuse unchanged detail but refresh head/base and requirements before merge.

## Read the PR and feedback

```powershell
gh pr view <number> --repo <owner/repo> --json `
  number,url,state,isDraft,headRefName,headRefOid,baseRefName,baseRefOid,mergeable,mergeStateStatus,reviewDecision,mergedAt,mergeCommit

gh pr checks <number> --repo <owner/repo> --json name,state,bucket,link
```

Checks exit code 8 means pending, not a command failure or success. Other
failures must be distinguished from an empty required-check set. Verify
required checks apply to the exact head, including required App identities,
and recheck the head after reading. GitHub's allowed success/neutral/skipped
conclusions are not equivalent to a missing, pending, cancelled, or failed run.

Read review submissions, PR discussion, and inline comments with paginated
REST calls (`pulls/<number>/reviews`, `issues/<number>/comments`, and
`pulls/<number>/comments` under the repository endpoint). Use GraphQL for
`reviewThreads` resolution/outdated state, requested reviewers, and nested
comments; paginate each needed connection. A truncated list cannot prove
that no unresolved feedback or required review remains.

Required approving identities, CODEOWNER and last-push requirements use
GitHub's current review decision plus reviewer/commit/dismissal metadata.
Comments and self-review records are not approving GitHub reviews. Verify
caller-supplied decisions and exceptions while preserving explicit user holds
and addressing actual feedback.

## Read current base-branch requirements

URL-encode the actual PR base branch, which need not be the default branch.
Read both effective rulesets and classic protection:

```powershell
gh api --paginate -H "X-GitHub-Api-Version: 2026-03-10" `
  repos/<owner>/<repo>/rules/branches/<encoded-base>

gh api -H "X-GitHub-Api-Version: 2026-03-10" `
  repos/<owner>/<repo>/branches/<encoded-base>/protection

gh api repos/<owner>/<repo> --jq `
  '{allow_merge_commit,allow_squash_merge,allow_rebase_merge,delete_branch_on_merge}'
```

Only an authoritative absent-protection response means no classic protection.
Authorization, transport, parsing, or pagination failure leaves requirements
unknown; do not substitute an empty rule set or declare the PR completable.

Combine applicable requirements rather than picking the more permissive source:

- Approvals, CODEOWNER/named reviewers, stale-review dismissal, and latest-push
  approval from effective PR rules and classic protection.
- Required checks and their App/integration identities, including strict
  up-to-date requirements and any required workflows.
- Thread resolution, including classic `required_conversation_resolution.enabled`.
- Merge queue, linear history, and other applicable restrictions.
- Allowed merge methods: intersect repository-enabled methods with applicable
  ruleset, queue, linear-history, and project requirements. Omit queue-only
  method restrictions only for an authorized direct queue bypass. An empty
  intersection is a completion blocker, not hands-free merge capability.

Do not treat `mergeable` alone as permission to merge. Unknown or unsupported
requirements need an explicit problem report, not a permissive default.

## Verify merge exceptions

Preserve normal GitHub requirements and project/issue approval requests unless
the current caller supplies an explicit exception for this PR repository.
Verify the waived gates, authority source, and current applicability; configuration
or an earlier run is not permission. The calling workflow selects policy,
not this reference.

Before using a caller-authorized `--admin` exception, require:

- Acceptance, current clean self-review, required local validation, and actual
  feedback resolutions are verified for the head being merged.
- All reported CI checks and expected required checks/workflows are satisfied,
  with required App identities. Missing, pending, cancelled, failed, or unknown
  CI blocks admin merge, including failures not marked required by protection.
  No checks reported is not success when CI is expected but has not started.
  Establish an intentional no-CI case explicitly. If CI needs the merge queue,
  use the normal queue path where possible or hand off; do not skip that CI.
- Explicit user holds and every non-bypassed requirement are satisfied,
  including thread resolution, mergeability, strict up-to-date requirements,
  and allowed merge methods. Refresh head/base and evidence immediately before
  merging; changed code invalidates the earlier review/check decision.

[`--admin`](https://cli.github.com/manual/gh_pr_merge) is broad, not a
review-only bypass. Prefer normal merge when all native requirements already
pass; otherwise use it only for the verified exception, with
`--match-head-commit <reviewed-head>`. GitHub must permit the current actor's
operation; repository access does not guarantee bypass rights. A denial or
unexpected failure requires fresh state and an explicit handoff/problem report,
not changing protection, waiving CI, or blind retry.

## Completion versus waiting

Distinguish the next action from final merge permission:

- New actionable feedback or a branch-owned CI failure permits repair assessment
  even while other merge gates remain unmet. Preserve explicit user holds.
- Direct merge needs acceptance, clean self-review, CI, and every non-bypassed
  requirement satisfied for the current head.
- Queue admission needs acceptance, clean self-review, and the applicable
  pre-queue checks, approvals, and other entry requirements satisfied. Checks
  that run only in the merge queue are evaluated after entry; they cannot block
  entry or be waived for direct/admin merge.
- Once queued, wait for merge or actionable queue failure, not already-passing
  pre-queue checks. Queue entry is not a completed merge.

Apply verified caller authority to workflow-only waits, never an explicit hold.
Unchanged waits do not need another comment.

## Observe pending CI

Only when the caller chooses to wait, use one attached watcher or event
subscription with conservative polling, not repeated lifecycle calls or
unchanged GitHub comments. For reported checks:

```powershell
gh pr checks <number> --repo <owner/repo> --watch --fail-fast --interval 30
```

Watch all reported checks, not only required ones. If expected checks have not
registered, verify a queued/running workflow for the current head and observe
its startup first. Missing checks without observable pending work, unreadable
state, or watcher errors need an explicit blocker report, not an indefinite
wait or a success-shaped fallback.

Stop the watcher before leaving observation, including on interruption, CI
failure/cancellation, a known head/base change, or a new non-CI blocker.
A watcher finishing is not merge authorization: refresh PR state, head/base,
all reported and expected checks, feedback, and requirements before deciding
the next action. A changed head/base invalidates the old readiness decision.
Exit code 8 remains pending; an empty check set or command failure is not CI
success. Terminal CI failures return to assessment for branch-owned repairs
or an infrastructure handoff, not a blind rerun.
