---
name: iterate-pr
description: Review PR comments, address justified findings, and reply with the outcome.
---

# Iterate PR

## When to use

To respond to review feedback on an open PR.

## Preflight

Invoke `orchestrator-boot` if `..\orchestrator-boot\references\RESOURCE-MAP.yml`
is not in context.

## Input

The target GitHub PR, identified by URL or repository and PR number.
Read-only/report-only requests allow assessment, not code changes or posted replies.

## Guidance

- Confirm the PR is open and read current review comments with the linked
  issue context.
- Address findings selectively against issue scope, acceptance criteria, and
  project principles. Verify and push fixes; raise consequential uncertainty
  before making speculative changes.
- Reply in the review threads with the fix or reasons for non-action.
  Resolve only addressed threads when permitted; avoid duplicate replies.

## Output

Report fixes, replies, and unresolved findings or decisions. Identify failed
or partial updates; this action does not merge the PR.
