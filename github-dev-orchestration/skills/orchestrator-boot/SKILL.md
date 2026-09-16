---
name: orchestrator-boot
description: Initialize the bundled workspace map on explicit first use, then load lifecycle guidance and the selected project's context.
---

# Orchestrator Boot

## Use

At session start or when project context is missing. Reuse unchanged context.
An explicit, non-read-only boot also initializes missing or incomplete mapping.
Implicit calls only load. Boot does not start lifecycle work or mutate GitHub.

## Steps

1. Read `references\CORE.md`, `references\DEV-FLOW.md`, and
   `references\RESOURCE-MAP.yml`. Resolve the map relative to this installed
   skill, not the working directory. Anchor the workspace root to the caller's
   workspace or this invocation's starting directory; retain it across later
   directory changes.
2. Inspect the map before resolving its values. Missing, malformed, or template
   mapping, or an unmapped requested repository, needs configuration.
   Keep complete mappings unchanged unless reconfiguration is requested.
   When setup or reconfiguration is needed, only an explicit, non-read-only
   boot may load `references\INITIALIZE.md` and populate or repair the bundled
   map in place.
   Implicit or read-only calls needing setup return `needs_configuration`
   without setup or writes; suggest explicit boot.
   An unreadable existing map is an error, not permission to overwrite it.
   The worktree token `<feature-name>` is not an unresolved setup value.
3. Resolve the Project owner, number, and four status names. Select a repository
   from the issue/PR, explicit input, or current workspace; board-wide requests
   need no eager repository selection or reading of every manifest.
   Report conflicting mappings rather than silently retargeting them.
4. Resolve checkout/worktree paths from the workspace root and
   `repos.<key>.manifest` from the repository root. Canonical paths, including
   symlink targets, must stay inside their respective roots. Treat a mapping
   marked `status: reference` as read-only.
5. Read repository instructions and the manifest when configured; retain its
   revision and project settings without interpreting workflow policy.
   Preserve the caller's guidance and decisions; loading configuration grants
   no new authority.
   If no checkout exists, read the manifest from GitHub at the remote default
   branch and record its commit/blob. For local guidance, record a Git revision
   or digest. Reuse guidance already verified during initialization.
   Unreadable declared guidance returns `needs_configuration`, not `loaded`.
6. Return context and the next skill to the caller; do not invoke it.
   Initialization may read Project metadata, not board items. Cloning,
   reconciliation, and PR requirement reads remain with their owning actions.
   Read-only requests stay read-only. Do not load initialization guidance on
   an ordinary configured boot.

## Output

Return `loaded` or `needs_configuration`, with the board/repository mapping,
map path/revision and any saved changes, workspace root, guidance revisions,
project settings, caller guidance, missing values or failed operations, and
suggested next skill. Return `loaded` only after the map and required guidance
are usable; saving configuration alone is not successful loading.
