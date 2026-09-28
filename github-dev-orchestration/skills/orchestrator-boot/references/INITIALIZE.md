# Initialize the Bundled Map

## Boundary

Use only for explicit, non-read-only setup. Initialize or repair the bundled
file in place: `RESOURCE-MAP.yml` beside this reference, even when absent.
Do not create a second map or replace an inaccessible file.

Configuration is the only mutation here. Do not clone, enumerate board items,
reconcile statuses, or create GitHub resources.

## Configuration model

Configure only the requested entries needed for the intended work. Ask the user
when any requested entries or their required values are missing.

| Data | Meaning and location |
|---|---|
| Repository | `repos.<key>.git`, workspace-relative `path` for the main worktree on the repository default branch, and `status` (`active` or `reference`). |
| Guidance/layout | Optional repository-relative `manifest` and workspace-relative, contained `worktrees.convention` for issue worktrees; `<feature-name>` is a runtime token. |
| Board, when needed | `organization.name`/`url` for the user or organization owner; `project_board.number`/`url` and four distinct `statuses` options. Board-only setup may leave `repos` empty. |
| Skill options | Optional data interpreted by the owning skill when invoked, not authority or prerequisites for unrelated actions. |
