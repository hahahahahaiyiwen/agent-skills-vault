---
name: open-pr
description: Publish or update one issue-linked PR with acceptance evidence and a clean self-review.
---

# Open PR

## Use

If shared context is missing, load `orchestrator-boot`.
As the active handler with a ready worktree. Publication requires that
`self-review` returns `clean`; discovery may find work already merged.
Released work returns `not_ready` with suggested `continue-issue`.

## Steps

1. Search all PR states for the exact remote head repository/branch. Reuse one
   open PR; return `already_merged` with suggested `complete-issue`; hand off a
   closed-unmerged PR for disposition. Resolve ambiguous linkage before mutation.
   Identify the existing PR's base; for a new PR, use the discovered default
   branch or explicitly intended base.
2. Verify issue/branch linkage, blockers, accepted design, acceptance evidence,
   and required local validation. Require clean review for the current base/head
   and guidance. Return a current report-only `findings` result without fixing
   or repeating it. For other missing, stale, or non-clean prerequisites, return
   `not_ready` with the affected Dev step as the suggested next skill.
   Do not start that stage or reset an existing self-review run.
3. Verify local/remote heads match and intended commits are pushed. Read PR
   instructions and `..\iterate-pr\references\PR-STATE.md` for GitHub requirements.
   With no PR, read only the base-branch requirements, not nonexistent PR state.
   Checks available only after PR creation may be pending, never called passing.
   Do not submit a known branch-owned failure as ready.
4. Create or update the PR against that resolved base. Include the issue link,
   bounded scope, acceptance/validation
   evidence, design/manifest references, clean review link, and excluded follow-ups.
   For default-branch targets, include a closing reference; cross-repository
   syntax is `Closes owner/repo#number`. Non-default targets ignore closing
   keywords: preserve explicit issue/PR cross-links, not an automatic-close
   assumption. Preserve human-authored content and update only changed metadata.
5. Verify the durable issue/PR association and repository/head/base SHAs.
   Record an issue progress link only when evidence changes and reconcile changed task facts,
   keeping `In progress`. Then return `not_ready` with suggested `self-review`
   if the base changed. Do not start PR iteration or duplicate unchanged review.

## Output

Return `ready_for_pr_review`, `already_merged`, `not_ready`, `findings`,
`handed_off`, or `partial_failure`, with PR, head/base, evidence, and status.
Suggested next skill: `iterate-pr` after `ready_for_pr_review`, or
`complete-issue` after `already_merged`. Preserve remote state and hand off if
publication cannot safely finish. Completion still requires the guarded merge conditions.
