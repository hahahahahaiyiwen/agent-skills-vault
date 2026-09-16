---
name: claim-issue
description: Acquire new Ready work and prepare its remote branch, local worktree, and development environment.
---

# Claim Issue

## Use

If shared context is missing, load `orchestrator-boot`.
For unclaimed Ready work. Existing task branches, PRs, or released claims return
`continue_existing` with `continue-issue` as the suggested next skill.

## Steps

1. Use targeted `reconcile-board` and read the contract, native blockers,
   assignees, handling records, branches, and PRs. Require an open Ready issue,
   satisfied dependencies, project guidance, and no conflicting handler.
2. Choose handler/claim identifiers and discover the default branch's remote
   SHA. Use `issue/<number>` or the repository's deterministic branch convention;
   never choose another ref to evade an acquisition conflict.
3. Recheck status, blockers, and handling immediately before creating the ref:

   ```powershell
   gh api --method POST repos/<owner>/<repo>/git/refs `
     -f ref='refs/heads/<task-branch>' -f sha='<base-sha>'
   ```

   An existing ref or lost race returns to discovery, not takeover.
4. Verify the ref and post `## CLAIM` with `Handling: preparing`, handler/claim
   IDs, branch/base SHAs, and manifest revision.
5. Follow `..\orchestrator-boot\references\LOCAL-ENV.md` to clone if absent,
   attach the worktree, and prepare repository-declared setup.
6. Recheck ownership, head, blockers, and environment readiness. Update the
   record to `Handling: active`, include setup evidence, and reconcile the issue
   to `In progress`. Do not report a successful claim before setup succeeds.
7. After interruption, finish the same verified acquisition's missing steps.
   Preserve remote work and use `handoff-issue` for a setup failure; an
   unverified branch without a claim record is not yours to reset or delete.

## Output

Return `claimed`, `continue_existing`, `waiting`, or `partial_failure`, with the
claim record, branch/head, worktree/setup result, and status.
Suggested next skill: `design-issue` after `claimed`, or `continue-issue` after
`continue_existing`. Return without starting either skill.
