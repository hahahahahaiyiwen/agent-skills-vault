# Core Orchestration Model

## GitHub development state

| Information | GitHub location |
|---|---|
| Outcome and acceptance criteria | Issue body |
| Plan and work status | Project board and native parent/dependency links |
| Implementation | Remote task branch and PR |
| Decisions, progress, and handoffs | Issue/PR text or linked repository document |

Persist consequential decisions and enough progress to resume, not an activity
transcript. Any acting skill may update affected board items when task facts
change, not after every skill.

## One handling agent, one issue, one worktree

- The **handling agent** is the agent currently responsible for advancing an
  issue and changing its task branch. It retains that role until handoff or
  completion, working on one issue at a time with one issue worktree on the
  task branch during implementation.
- Only the handling agent changes the issue branch; independent reviewers inspect
  without taking over. Read-only assessment and non-code outcomes need no worktree.
- Record the handling agent and branch on the issue/PR; do not take over another
  active handling agent. Complete or hand off before taking another issue.
  For unfinished work, continuation reuses the remote task branch and may
  recreate the worktree on another machine.

## Local worktree layout

Resolve worktree paths from the retained workspace root, not the current working
directory.

| Worktree | Location | Branch |
|---|---|---|
| Main | `repos.<key>.path` | Repository default branch (normally `main`) |
| Issue | `repos.<key>.worktrees.convention` when configured, otherwise repository layout | Issue task branch |

Prepare or verify the main worktree from `repos.<key>.git` before creating issue
worktrees. Keep paths distinct and contained in the workspace; never switch the
main worktree to an issue branch.

## Load missing configuration

- When repository/Project mapping or project guidance is missing from the active
  context, reload only relevant `repos.<key>`/board entries in `RESOURCE-MAP.yml`,
  repository instructions, and the configured manifest. Reuse loaded values;
  refresh them when the configuration changes.
- `orchestrator-boot` resolves missing context. If required values have not been
  configured, request explicit setup rather than initializing during unrelated
  work. Unused settings do not block a known repository or PR action.
