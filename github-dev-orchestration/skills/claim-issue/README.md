# Claim Issue

Claim starts new issue delivery: confirm satisfied dependencies and availability,
create the issue worktree, and record the handling agent and branch on the
GitHub issue. Existing branch/PR work belongs to `continue-issue`.

Prepare or verify the mapped main worktree at `repos.<key>.path` before creating
the issue worktree from the intended base. Main stays on the repository default
branch; issue worktrees use the configured layout or repository conventions.

Use a `## CLAIM` heading with a concise body identifying the handling agent,
branch, and base commit. The heading is a record label, not proof of current
ownership.

Preflight invokes `orchestrator-boot` only when the resource map is not in context.
The target issue is the input; the output reports the claim or why it was declined,
including partial setup if the attempt failed. Claiming does not start design
or implementation.
