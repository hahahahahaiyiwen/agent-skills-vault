# Local Development Environment

On-demand shared procedure for `claim-issue` and `continue-issue`. Inputs are
the resolved repository, workspace path, manifest revision, task branch, and
expected remote head. Neither caller succeeds until the environment is ready.

## Prepare or recover

1. Resolve the mapped checkout and worktree paths inside the current workspace.
   If a worktree convention uses `<feature-name>`, substitute a filesystem-safe
   issue number and short name, never an unchecked issue title. Without a
   convention, choose an unused path containing the issue number inside the
   workspace; use a sibling only when contained. For a root checkout, use a
   workspace-local worktree directory excluded from the main checkout's status.
   Do not require a previous machine's paths.
2. If the checkout is absent, clone the configured repository into that path.
   If present, verify it is the expected repository and remote before fetching.
   Do not overwrite a non-repository directory or change an unrelated remote.
3. Resolve recovery before fetching a task ref. For verified completed delivery
   with a deleted ref, use the integrated commit for a merged PR or the recorded
   claim base for a no-PR outcome; do not fetch or recreate the missing ref.
   Fetch the verified recovery commit if absent locally.
   For a retained task ref, fetch the task and base branches without switching
   the main checkout.
   Verify the expected task head against GitHub; unexplained changes require
   fresh task/ownership discovery, not a reset to a recorded old SHA.
4. Inspect `git worktree list --porcelain` and local branches. Reuse the
   matching worktree and upstream if correct. Otherwise attach an isolated
   worktree, tracking the existing task branch or detached at the verified
   recovery commit when the task ref was deleted.
   If the branch already exists, attach that branch rather than recreating it.
   Fast-forward only a clean, behind-only branch. Preserve dirty, ahead, or
   divergent work and report it; never force-checkout, reset, or recreate the
   issue branch from the default branch during continuation.
5. Read the manifest and repository setup instructions in the worktree.
   Reconcile any revision difference from boot before acting on changed
   guidance. Prepare only the declared setup needed for the next
   action; cleanup does not require rebuilding the delivery toolchain.
   Use normal local credential mechanisms; handoffs are not a source of secrets
   or permission to provision services.
6. Run the smallest repository-declared environment check needed for the next
   step. Inspect the worktree and applicable branch/upstream/head, or the
   verified detached recovery commit when the task ref is absent.
   Recheck task handling and blockers before publishing successful acquisition.

A fresh agent may create all of this from GitHub state. A previous checkout,
session, worktree, or environment name is not required.

## Partial failure

Keep verified remote progress and any local changes. Report the failed setup
step and an objective recovery condition through `handoff-issue`; include what
exists locally and remotely. Do not publish a successful claim/continuation
with a missing environment.

An interrupted acquisition may leave a remote branch without a successful
handling record. Verify its provenance before finishing setup; an unfamiliar
branch is not permission to take over. Do not delete it merely to retry.
