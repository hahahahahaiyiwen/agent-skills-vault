# Initialize the Bundled Map

Load only during an explicit, non-read-only boot that needs initialization
or reconfiguration. Initialize `RESOURCE-MAP.yml` beside this reference
in place; do not create a second map at the workspace root or elsewhere.
If the file is missing, create it at that same bundled path using the structure
below. An inaccessible existing file is not a missing template.

1. Inspect existing values and the workspace anchor. Preserve configured
   entries, comments, and project settings; change only missing values or
   requested corrections. Ask before repurposing a map that conflicts with
   another workspace or repository. Do not reset it to template defaults.
2. Discover facts read-only from the request, repository instructions, existing
   checkouts, and Git remotes. Reuse an existing checkout, including `path: .`
   when it is the workspace root; do not impose a `repos` directory layout.
   If no checkout exists, collect missing repository URLs and intended paths
   with step 3's questions, without cloning. Do not scan unrelated directories
   or infer a Project number from a repository owner. Keep credentials out of
   the map; use credential-free repository URLs and the environment's normal
   authentication.
   Use only the Project metadata procedure in
   `..\..\reconcile-board\references\PROJECT.md` to confirm the Project owner
   (user or organization), number/URL, and four status options when identifiers
   are known. Otherwise collect them in step 3 and verify before writing.
   Do not enumerate board items, reconcile status, or create GitHub resources.
   Unavailable repositories, Projects, or permissions are explicit setup blockers.
3. Present the target file and known values, then ask for missing or ambiguous
   choices together. Do not ask again for facts already established.

| Map data | Required resolution |
|---|---|
| `organization` | Project owner `name`/`url`; `project_board.number`/`url` and `statuses` mapping Backlog, Ready, In progress, and Done to existing option names. |
| `repos` | Only requested or clearly intended repositories: unique key, `git`, workspace-relative `path`, and `status` (`active` or `reference`). Board-only setup may leave this mapping empty. |
| Repository guidance | `manifest` only when declared or selected; resolve it from the repository root, never guess a filename. Remove unused optional template fields such as `manifest`, `desc`, or `lang`, not existing configured entries. |
| Local layout | For active work, choose a contained `worktrees.convention`. Preserve the runtime `<feature-name>` token while replacing setup tokens such as `<repo-key>` and `<worktree-parent>`. |
| Skill settings | Preserve existing choices and present template defaults. Obtain an unresolved approval-mode choice from the user or unambiguous applicable guidance; repository access does not supply it. |

   For supported settings and types, read only configuration definitions from
   `..\..\self-review\SKILL.md` and `..\..\orchestrator-autopilot\SKILL.md` when
   needed, including when the template file is missing. Collecting settings
   does not apply workflow policy or authorize execution; do not invoke those
   skills. For new reference-only repositories, omit delivery settings.
4. Validate the proposed map before writing: separate top-level `organization`
   and `repos` mappings; matching owner/Project URLs and positive integer
   Project number; four distinct status options; verified repository identities;
   supported setting values and types. Choices must be single values, not
   pipe-separated alternatives; booleans and integers must have their actual
   YAML types. Resolve all setup placeholders in the chosen entries, removing
   an unused repository template stub for board-only setup.
   Apply boot's path containment and guidance rules before saving. Resolve
   symlink targets; check worktree conventions without expanding them into an
   actual worktree. Verify a declared manifest locally or at the remote default
   branch without cloning, and retain its revision for boot to reuse.
   If required choices are declined or evidence remains unavailable, return
   `needs_configuration` with the unresolved fields; leave the existing map
   intact rather than inventing values or publishing a partial configuration.
5. Apply the resolved changes to the bundled file only. Re-read the saved YAML
   and verify its structure, types, and resolved values against the agreed map.
   Record its path and revision, then finish boot's context loading and return.
   A failed write or mismatched readback is `needs_configuration`, not success;
   report any partial local changes. No second configuration file, state journal,
   automatic commit, or onward lifecycle invocation is part of initialization.
