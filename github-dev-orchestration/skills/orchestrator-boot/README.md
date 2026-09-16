# Orchestrator Boot

Boot owns local map initialization, context loading, and routing, not lifecycle
execution. `CORE.md` and `DEV-FLOW.md` are the small shared inputs.
`references\RESOURCE-MAP.yml` ships as a placeholder template and becomes the
installed skill's workspace mapping in place. Do not create a second map.

Explicit first-use boot loads `references\INITIALIZE.md`, discovers available
facts, collects unresolved choices, and saves and re-reads the bundled map.
Configured boot skips initialization and preserves existing values. Implicit
or read-only boot reports `needs_configuration` without setup or writes when
configuration is missing; an unreadable file is never permission to replace it.

Repository manifests remain repository-owned. Their paths are relative to the
repository; checkout/worktree paths use the workspace root retained by boot,
not a later working directory. The map itself is relative to this installed
skill. Use workspace-specific installed copies when different workspaces need
independent mappings; never silently repurpose another workspace's map.

Optional repository entries can supply guidance and small skill settings:

```yaml
manifest: docs\PRODUCT_MANIFEST.md
self_review:
  mode: until_clean
  max_iterations: 3
```

`self-review` validates these options when invoked: `single_pass` is report-only;
`until_clean` allows bounded review/fix/review. The limit counts review passes
per run, including verification, and survives continuation.

Workflow settings are opaque to boot and interpreted by their owning skill.
Loading configuration never starts execution or grants decision authority.
A caller stops on `needs_configuration`; it cannot continue with a template.

Initialization reads repository and Project metadata only; it neither enumerates
board items nor mutates GitHub. Only a verified map and readable required guidance
permit `loaded`; a successful write alone does not. Load `references\LOCAL-ENV.md` only
when claiming or continuing work. Graph, reconciliation, and PR operations stay
with their owning skills. Keep initialization details off the normal boot path.
