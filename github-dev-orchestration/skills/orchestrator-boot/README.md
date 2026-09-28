# Orchestrator Boot

Boot loads the GitHub development orchestration model and workspace configuration.
It is a context loader, not a prerequisite for every GitHub action.

| Reference | Owns | Load when |
|---|---|---|
| `references\CORE.md` | GitHub records; one handling agent, one issue, one worktree; main/issue worktree layout; reloading missing configuration. | On boot. |
| `references\DEV-FLOW.md` | Roadmap planning and issue delivery, their advisory lifecycle routes, and handoff/continuation between handling agents. | On boot. |
| `references\RESOURCE-MAP.yml` | Repository/Project mappings and optional skill settings. | On boot. |
| `references\INITIALIZE.md` | The configuration model and user input for missing requested entries or values. No development setup or task execution. | Requested entries are missing or incomplete. |

Keep both cycles visible. Issue delivery requires claim/completion endpoints,
not every intermediate skill invocation or the order shown.
Load the board and operational references only for actions that need them.

`references\RESOURCE-MAP.yml` is the installed skill's optional workspace map.
Explicit setup may initialize it in place using `references\INITIALIZE.md`;
implicit/read-only requests do not write it. Known repository actions need not
wait for unused board or skill settings. Declared unreadable guidance and
conflicting required values remain explicit problems.

The map is relative to the installed skill. `repos.<key>.path` identifies the main
worktree on the repository default branch; issue worktrees use the configured
convention or repository layout. Both paths use the retained workspace root,
while manifests use repository roots. Keep paths contained and separate.
Use workspace-specific installed copies for independent maps.

Optional review settings, interpreted only when reviewing:

```yaml
self_review:
  mode: until_clean
  max_iterations: 3
```

An explicit limit overrides the omitted-setting default; merely configuring
review does not require it for every task. Self-review asks for a severity
threshold if missing; `until_clean` targets zero findings at that level or
higher within the iteration cap. Workflow settings likewise grant no authority
just by being loaded. Environment setup, Project operations, and PR requirements
stay on demand.
