import re
import unittest
from pathlib import Path


BUNDLE = Path(__file__).resolve().parents[1]
SKILLS = BUNDLE / "skills"
DOCS = BUNDLE / "docs"
REFERENCES = SKILLS / "orchestrator-boot" / "references"
ACTIVE = {
    "plan-issues",
    "reconcile-board",
    "claim-issue",
    "design-issue",
    "implement-issue",
    "self-review",
    "open-pr",
    "iterate-pr",
    "complete-issue",
    "handoff-issue",
    "continue-issue",
    "orchestrator-boot",
    "orchestrator-autopilot",
}
RETIRED = {
    "board-status",
    "create-issue",
    "revise-plan",
    "plan-issue",
    "execute-issue",
    "self-review-pr",
    "process-external-review",
}
STATES = {"Backlog", "Ready", "In progress", "Done"}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def skill(name: str) -> str:
    return read(SKILLS / name / "SKILL.md")


def skill_output(name: str) -> str:
    return skill(name).split("## Output\n", 1)[1]


def normalized(text: str) -> str:
    return " ".join(text.split())


def active_documents() -> list[Path]:
    return sorted(
        path
        for name in ACTIVE
        for path in (SKILLS / name).rglob("*")
        if path.suffix in {".md", ".yml", ".py"}
    )


def repository_configs(config: str | None = None) -> list[tuple[str, str]]:
    if config is None:
        config = read(REFERENCES / "RESOURCE-MAP.yml")
    repos = config.split("\nrepos:\n", 1)[1]
    key = r"(?:[\w-]+|<repo-key>)"
    return re.findall(rf"^  ({key}):\n(.*?)(?=^  {key}:\n|\Z)", repos, re.M | re.S)


class LifecycleContractTests(unittest.TestCase):
    def test_installed_skill_inventory(self) -> None:
        actual = {path.parent.name for path in SKILLS.glob("*/SKILL.md")}
        self.assertEqual(actual, ACTIVE)
        for name in RETIRED:
            with self.subTest(retired=name):
                self.assertFalse((SKILLS / name).exists())

    def test_frontmatter_matches_directory_and_descriptions_are_unique(self) -> None:
        descriptions = []
        for name in sorted(ACTIVE):
            with self.subTest(skill=name):
                match = re.match(
                    r"\A---\nname: ([a-z-]+)\ndescription: ([^\n]+)\n---\n",
                    skill(name),
                )
                self.assertIsNotNone(match)
                if match is not None:
                    self.assertEqual(match[1], name)
                    descriptions.append(match[2])
                self.assertTrue((SKILLS / name / "README.md").is_file())
        self.assertEqual(len(descriptions), len(set(descriptions)))

    def test_active_skills_share_section_structure_and_lazy_boot(self) -> None:
        for name in sorted(ACTIVE):
            with self.subTest(skill=name):
                body = skill(name)
                self.assertEqual(
                    re.findall(r"^## ([^\n]+)$", body, re.M),
                    ["Use", "Steps", "Output"],
                )
                steps = re.findall(r"^(\d+)\. ", body, re.M)
                self.assertEqual(steps, [str(n) for n in range(1, len(steps) + 1)])
                self.assertGreater(len(steps), 0)
                if name != "orchestrator-boot":
                    use = body.split("## Use\n", 1)[1].split("## Steps\n", 1)[0]
                    self.assertIn("If shared context is missing", use)
                    self.assertIn("`orchestrator-boot`", use)

    def test_routing_matches_the_active_inventory(self) -> None:
        routing = read(REFERENCES / "DEV-FLOW.md")
        routed = set(re.findall(r"^\| [^|\n]+ \| `([^`]+)` \|$", routing, re.M))
        self.assertEqual(routed, ACTIVE)

    def test_documented_inventory_matches_all_active_skills(self) -> None:
        model = read(DOCS / "STATE-MACHINE.md")
        rows = re.findall(
            r"^\| (Plan|Dev|Shared|Deferred) \| `([^`]+)` \| .+ \|$",
            model,
            re.M,
        )
        self.assertEqual({name for _, name in rows}, ACTIVE)
        self.assertNotIn("Deferred", {group for group, _ in rows})
        self.assertIn("thirteen active skills", normalized(model))

    def test_active_documents_do_not_reference_retired_skills(self) -> None:
        removed = "|".join(re.escape(name) for name in sorted(RETIRED))
        pattern = rf"(?<![\w-])(?:{removed})(?![\w-])"
        for path in active_documents():
            with self.subTest(path=path.relative_to(BUNDLE)):
                self.assertNotRegex(read(path), pattern)
                self.assertNotIn("In review", read(path))

    def test_active_documents_have_no_retired_policy_or_diagnostic_contract(self) -> None:
        pattern = (
            r"evaluate_workflow_policy|evaluate_review_budget"
            r"|max_self_review_rounds|max_plan_revisions|max_ci_wait"
            r"|workflow\.review|workflow\.merge|hands_free_completion_possible"
            r"|events\.jsonl|session-state|evidence_log|ImproveOrchestartion"
        )
        for path in active_documents():
            with self.subTest(path=path.relative_to(BUNDLE)):
                self.assertNotRegex(read(path), pattern)

    def test_explicit_relative_references_resolve(self) -> None:
        pattern = r"`([^`\n]*\\[^`\n]*\.(?:md|yml|py))`"
        count = 0
        for path in active_documents():
            for reference in re.findall(pattern, read(path)):
                with self.subTest(path=path.relative_to(BUNDLE), reference=reference):
                    target = path.parent.joinpath(*reference.split("\\")).resolve()
                    self.assertIn(SKILLS.resolve(), target.parents)
                    self.assertTrue(target.is_file())
                    count += 1
        self.assertGreater(count, 10)

    def test_markdown_links_resolve_without_external_lookup(self) -> None:
        for path in [*active_documents(), *DOCS.glob("*.md")]:
            for target in re.findall(r"\]\(([^)]+)\)", read(path)):
                if "://" in target or target.startswith("#"):
                    continue
                with self.subTest(path=path.relative_to(BUNDLE), target=target):
                    target_path = target.split("#", 1)[0]
                    self.assertTrue((path.parent / target_path).is_file())

    def test_fenced_examples_are_balanced(self) -> None:
        for path in [*active_documents(), *DOCS.glob("*.md")]:
            with self.subTest(path=path.relative_to(BUNDLE)):
                self.assertEqual(len(re.findall(r"^```", read(path), re.M)) % 2, 0)

    def test_workspace_config_has_four_states_and_no_generic_policy(self) -> None:
        config = read(REFERENCES / "RESOURCE-MAP.yml")
        sections = set(re.findall(r"^([a-z_]+):", config, re.M))
        self.assertEqual(sections, {"organization", "repos"})
        statuses = dict(re.findall(r"^      (backlog|ready|in_progress|done): (.+)$", config, re.M))
        self.assertEqual(
            statuses,
            {"backlog": "Backlog", "ready": "Ready", "in_progress": "In progress", "done": "Done"},
        )
        self.assertNotRegex(config, r"(?m)^\s*(workflow|in_review|admin_bypass):")

    def test_resource_map_is_a_template_with_real_defaults(self) -> None:
        config = read(REFERENCES / "RESOURCE-MAP.yml")
        self.assertEqual([name for name, _ in repository_configs()], ["<repo-key>"])
        for placeholder in (
            "<owner-name>", "<owner-url>", "<project-number>", "<project-board-url>",
            "<checkout-path>", "<git-url>", "<manifest-path>", "<approval-mode>",
            "<worktree-parent>", "<feature-name>",
        ):
            self.assertIn(placeholder, config)
        self.assertRegex(config, r"(?m)^    number: <project-number>$")
        self.assertRegex(config, r"(?m)^      mode: <approval-mode>$")
        self.assertRegex(config, r"(?m)^      wait_for_ci: false$")
        self.assertRegex(config, r"(?m)^      max_iterations: 3$")
        self.assertNotRegex(config, r"(?m)^\s*(?:mode|wait_for_ci):.*\|")

    def test_template_can_render_typed_repository_configuration(self) -> None:
        template = read(REFERENCES / "RESOURCE-MAP.yml")
        values = {
            "<owner-name>": "example-owner",
            "<owner-url>": "https://github.com/example-owner",
            "<project-number>": "7",
            "<project-board-url>": "https://github.com/users/example-owner/projects/7",
            "<repo-key>": "example-repo",
            "<checkout-path>": ".",
            "<git-url>": "https://github.com/example-owner/example-repo",
            "<description>": "Example project",
            "<programming-language>": "Python",
            "<manifest-path>": r"docs\PRODUCT_MANIFEST.md",
            "<worktree-parent>": ".worktrees",
        }
        for mode, wait in (("auto-approval", "true"), ("reasonable-approval", "false")):
            with self.subTest(mode=mode, wait=wait):
                rendered = template
                for placeholder, value in values.items():
                    rendered = rendered.replace(placeholder, value)
                rendered = rendered.replace("<approval-mode>", mode)
                rendered = rendered.replace("wait_for_ci: false", f"wait_for_ci: {wait}")
                self.assertEqual(set(re.findall(r"<[a-z-]+>", rendered)), {"<feature-name>"})
                self.assertRegex(rendered, r"(?m)^    number: 7$")
                repos = repository_configs(rendered)
                self.assertEqual([name for name, _ in repos], ["example-repo"])
                body = repos[0][1]
                self.assertRegex(body, r"(?m)^    path: \.$")
                self.assertRegex(body, rf"(?m)^      mode: {mode}$")
                self.assertRegex(body, rf"(?m)^      wait_for_ci: {wait}$")
                self.assertIn(r"convention: '.worktrees\example-repo-<feature-name>'", body)

    def test_repository_review_settings_use_valid_modes_and_limits(self) -> None:
        configured = 0
        for name, body in repository_configs():
            if not re.search(r"^    status: active$", body, re.M):
                continue
            with self.subTest(repository=name):
                settings = re.search(
                    r"^    self_review:\n"
                    r"      mode: ([a-z_]+)\n"
                    r"      max_iterations: ([1-9][0-9]*)\n",
                    body,
                    re.M,
                )
                self.assertIsNotNone(settings)
                if settings is not None:
                    self.assertIn(settings[1], {"single_pass", "until_clean"})
                    self.assertGreater(int(settings[2]), 0)
                    configured += 1
        self.assertGreater(configured, 0)

    def test_both_design_documents_have_the_four_state_model(self) -> None:
        for path in (DOCS / "README.md", DOCS / "STATE-MACHINE.md"):
            with self.subTest(document=path.name):
                states = set(re.findall(r"^\| `([^`]+)` \|", read(path), re.M)) & (
                    STATES | {"In review"}
                )
                self.assertEqual(states, STATES)

    def test_boot_is_a_small_loader_with_lazy_initialization(self) -> None:
        boot = skill("orchestrator-boot")
        initial_read = boot.split("1. ", 1)[1].split("\n2. ", 1)[0]
        inputs = set(re.findall(r"`references\\([^`]+)`", initial_read))
        self.assertEqual(inputs, {"CORE.md", "DEV-FLOW.md", "RESOURCE-MAP.yml"})
        self.assertIn(r"`references\INITIALIZE.md`", boot)
        self.assertIn(
            "Do not load initialization guidance on an ordinary configured boot",
            normalized(boot),
        )
        self.assertNotIn("gh project", boot)
        self.assertNotIn("LOCAL-ENV.md", boot)
        self.assertIn("do not invoke it", boot)
        self.assertIn("Read-only requests stay read-only", normalized(boot))

    def test_boot_initializes_only_for_explicit_non_read_only_requests(self) -> None:
        boot = normalized(skill("orchestrator-boot"))
        for requirement in (
            "Inspect the map before resolving its values",
            "Missing, malformed, or template mapping, or an unmapped requested repository",
            "When setup or reconfiguration is needed, only an explicit, non-read-only boot may load",
            "populate or repair the bundled map in place",
            "Implicit or read-only calls needing setup return `needs_configuration` without setup or writes",
            "An unreadable existing map is an error, not permission to overwrite it",
            "Keep complete mappings unchanged unless reconfiguration is requested",
            "The worktree token `<feature-name>` is not an unresolved setup value",
        ):
            self.assertIn(requirement, boot)
        self.assertLess(boot.index("Inspect the map"), boot.index("Resolve checkout/worktree paths"))
        self.assertLess(boot.index("Inspect the map"), boot.index("Read repository instructions"))
        self.assertIn("Return `loaded` only after the map and required guidance are usable", boot)
        self.assertIn("saving configuration alone is not successful loading", boot)

    def test_boot_anchors_map_and_workspace_independently(self) -> None:
        boot = normalized(skill("orchestrator-boot"))
        for requirement in (
            "Resolve the map relative to this installed skill, not the working directory",
            "Anchor the workspace root to the caller's workspace or this invocation's starting directory",
            "retain it across later directory changes",
            "Report conflicting mappings rather than silently retargeting them",
            "map path/revision and any saved changes, workspace root",
        ):
            self.assertIn(requirement, boot)
        self.assertIn(
            "Use workspace-specific installed copies when different workspaces need independent mappings",
            normalized(read(SKILLS / "orchestrator-boot" / "README.md")),
        )

    def test_initialization_discovers_only_needed_read_only_metadata(self) -> None:
        setup = normalized(read(REFERENCES / "INITIALIZE.md"))
        for requirement in (
            "Discover facts read-only",
            "existing checkouts, and Git remotes",
            "including `path: .` when it is the workspace root",
            "do not impose a `repos` directory layout",
            "without cloning",
            "Do not scan unrelated directories",
            r"`..\..\reconcile-board\references\PROJECT.md`",
            "Project owner (user or organization), number/URL, and four status options",
            "when identifiers are known",
            "Otherwise collect them in step 3 and verify before writing",
            "Do not enumerate board items, reconcile status, or create GitHub resources",
            "Keep credentials out of the map",
            "Unavailable repositories, Projects, or permissions are explicit setup blockers",
            "Board-only setup may leave this mapping empty",
        ):
            self.assertIn(requirement, setup)
        self.assertIn(
            "Initialization may read Project metadata, not board items",
            normalized(skill("orchestrator-boot")),
        )

    def test_initialization_collects_choices_without_applying_policy(self) -> None:
        setup = normalized(read(REFERENCES / "INITIALIZE.md"))
        for requirement in (
            "Present the target file and known values",
            "ask for missing or ambiguous choices together",
            "Do not ask again for facts already established",
            "Obtain an unresolved approval-mode choice from the user or unambiguous applicable guidance",
            "repository access does not supply it",
            "read only configuration definitions",
            r"`..\..\self-review\SKILL.md`",
            r"`..\..\orchestrator-autopilot\SKILL.md`",
            "including when the template file is missing",
            "Collecting settings does not apply workflow policy or authorize execution",
            "do not invoke those skills",
            "For new reference-only repositories, omit delivery settings",
        ):
            self.assertIn(requirement, setup)

    def test_initialization_preserves_config_and_verifies_in_place_save(self) -> None:
        setup = normalized(read(REFERENCES / "INITIALIZE.md"))
        for requirement in (
            "Initialize `RESOURCE-MAP.yml` beside this reference in place",
            "do not create a second map at the workspace root or elsewhere",
            "If the file is missing, create it at that same bundled path",
            "An inaccessible existing file is not a missing template",
            "Preserve configured entries, comments, and project settings",
            "change only missing values or requested corrections",
            "Ask before repurposing a map that conflicts with another workspace or repository",
            "Do not reset it to template defaults",
            "Apply the resolved changes to the bundled file only",
            "Re-read the saved YAML and verify its structure, types, and resolved values",
            "Record its path and revision",
            "A failed write or mismatched readback is `needs_configuration`, not success",
            "report any partial local changes",
            "No second configuration file, state journal, automatic commit, or onward lifecycle invocation",
        ):
            self.assertIn(requirement, setup)
        self.assertLess(setup.index("Validate the proposed map"), setup.index("Apply the resolved changes"))
        self.assertLess(setup.index("Re-read the saved YAML"), setup.index("finish boot's context loading"))

    def test_initialization_requires_complete_typed_values(self) -> None:
        setup = normalized(read(REFERENCES / "INITIALIZE.md"))
        for requirement in (
            "separate top-level `organization` and `repos` mappings",
            "matching owner/Project URLs and positive integer Project number",
            "verified repository identities",
            "supported setting values and types",
            "Choices must be single values, not pipe-separated alternatives",
            "booleans and integers must have their actual YAML types",
            "Resolve all setup placeholders",
            "Preserve the runtime `<feature-name>` token",
            "Remove unused optional template fields",
            "Apply boot's path containment and guidance rules before saving",
            "Resolve symlink targets",
            "Verify a declared manifest locally or at the remote default branch without cloning",
            "If required choices are declined or evidence remains unavailable",
            "leave the existing map intact rather than inventing values or publishing a partial configuration",
        ):
            self.assertIn(requirement, setup)

    def test_manifest_resolution_supports_a_missing_checkout(self) -> None:
        boot = normalized(skill("orchestrator-boot"))
        self.assertIn("`repos.<key>.manifest` from the repository root", boot)
        self.assertIn("If no checkout exists", boot)
        self.assertIn("remote default branch", boot)
        self.assertIn("needs_configuration", boot)
        self.assertIn("manifest when configured", boot)

    def test_design_and_implementation_respect_configured_manifests(self) -> None:
        for name in ("design-issue", "implement-issue"):
            with self.subTest(skill=name):
                body = normalized(skill(name))
                self.assertIn("`repos.<key>.manifest`", body)
                self.assertIn("`RESOURCE-MAP.yml`, when configured", body)
                self.assertRegex(body, r"repository(?:-relative| root)")
                self.assertIn("repository instructions", body)
                self.assertIn("report unreadable declared guidance", body)

    def test_read_only_reconciliation_and_complete_pagination(self) -> None:
        reconcile = normalized(skill("reconcile-board"))
        project = read(SKILLS / "reconcile-board" / "references" / "PROJECT.md")
        self.assertIn("--read-only", reconcile)
        self.assertIn("forbids all writes, labels, and comments", reconcile)
        self.assertIn("--paginate", project)
        self.assertIn("hasNextPage endCursor", project)
        self.assertIn("projectItems", project)
        self.assertNotIn("--limit 500", project)

    def test_dependency_precedence_and_continuation_are_explicit(self) -> None:
        reconcile = skill("reconcile-board")
        dependency = reconcile.index("| Unsatisfied issue dependencies")
        unblocked_wait = reconcile.index("| No issue blockers")
        ready_resume = reconcile.index("| Dependency handoff cleared")
        active = reconcile.index("| Successful claim/continuation")
        self.assertLess(dependency, unblocked_wait)
        self.assertLess(unblocked_wait, ready_resume)
        self.assertLess(ready_resume, active)
        self.assertIn("retain the branch for `continue-issue`", reconcile)

    def test_native_graph_completion_and_separate_cycle_checks(self) -> None:
        graph = normalized(read(SKILLS / "plan-issues" / "references" / "ISSUE-GRAPH.md"))
        self.assertIn("state_reason=completed", graph)
        self.assertIn("dependencies/blocked_by", graph)
        self.assertIn("dependencies/blocking", graph)
        self.assertIn("Hierarchy and dependency graphs are checked separately", graph)
        self.assertIn("numeric database `id`", graph)

    def test_claim_and_continue_share_environment_recovery(self) -> None:
        for name in ("claim-issue", "continue-issue"):
            with self.subTest(skill=name):
                body = skill(name)
                self.assertIn(r"..\orchestrator-boot\references\LOCAL-ENV.md", body)
                self.assertIn("Handling: preparing", body)
                self.assertIn("Handling: active", body)
        environment = normalized(read(REFERENCES / "LOCAL-ENV.md"))
        for requirement in (
            "checkout is absent, clone",
            "worktree",
            "repository setup instructions",
            "behind-only",
            "partial",
        ):
            self.assertIn(requirement, environment.lower())

    def test_single_handler_and_cross_agent_recovery(self) -> None:
        core = normalized(read(REFERENCES / "CORE.md"))
        self.assertIn("exactly one agent", core)
        self.assertIn("Serialize acquisition of the same issue", core)
        self.assertIn("only the active handler changes the task branch", core)
        continuation = normalized(skill("continue-issue"))
        self.assertIn("no other agent is handling or preparing", continuation)
        self.assertIn("agent, machine, checkout, and local paths may differ", continuation)
        self.assertIn("next unfinished action, not the whole Dev cycle", continuation)
        self.assertIn("claim_required", continuation)
        self.assertLess(
            continuation.index("Inspect closure/merge before old review waits"),
            continuation.index("evaluate the current resume condition"),
        )
        self.assertIn("without recreating deleted remote refs", continuation)

    def test_handoff_is_durable_before_reconciliation(self) -> None:
        handoff = normalized(skill("handoff-issue"))
        self.assertLess(handoff.index("Post `## HANDOFF`"), handoff.index("Invoke targeted"))
        self.assertIn("Handling: released", handoff)
        self.assertIn("objective resume condition", handoff)
        self.assertIn("local-only state", handoff)
        self.assertIn("PR review resumes on new actionable feedback", handoff)
        self.assertIn("merge_queue", handoff)
        self.assertIn("failed GitHub write is not successful ownership release", handoff)

    def test_development_routes_to_review_before_submission(self) -> None:
        flow = read(REFERENCES / "DEV-FLOW.md").split("```text\n", 1)[1].split("```", 1)[0]
        self.assertLess(flow.index("implement-issue"), flow.index("self-review"))
        self.assertLess(flow.index("self-review"), flow.index("open-pr"))
        self.assertIn("ready_to_implement", skill("design-issue"))
        self.assertIn("ready_for_review", skill("implement-issue"))
        self.assertIn("`self-review` returns `clean`", skill("open-pr"))

    def test_self_review_does_not_accept_contradictory_clean_evidence(self) -> None:
        review = normalized(skill("self-review"))
        for requirement in (
            "a PR is not required",
            "Require clean committed work",
            "base/head SHAs and issue/design/guidance revisions",
            "verifiable reports for unchanged revisions",
            "no later unresolved findings",
            "completed current independent pass",
            "no required or undecided findings remaining",
            "changed revisions invalidate clean evidence",
            "Missing or conflicting evidence is never clean",
            "on the issue",
        ):
            self.assertIn(requirement, review)

    def test_review_scope_is_the_solution_not_only_changed_lines(self) -> None:
        review = normalized(skill("self-review"))
        for requirement in (
            "whole worktree",
            "Give the independent reviewer the issue scope",
            "acceptance criteria, accepted design, manifest, repository principles",
            "Require the active handler and ready environment",
            "Independently inspect relevant context, not only changed lines",
            "including design flaws",
            "the reviewer remains read-only and reports supported findings",
        ):
            self.assertIn(requirement, review)
        for path in active_documents():
            if path.suffix == ".md":
                with self.subTest(path=path.relative_to(BUNDLE)):
                    self.assertNotRegex(
                        normalized(read(path)),
                        r"review the (?:issue )?branch diff|complete-diff review|changed full diff",
                    )

    def test_review_modes_and_validation_are_explicit(self) -> None:
        review = normalized(skill("self-review"))
        for requirement in (
            "`repos.<key>.self_review`",
            "`RESOURCE-MAP.yml`",
            "a mapping with `mode` (`single_pass` or `until_clean`, default)",
            "`max_iterations` (default 3",
            "positive integer, not a boolean",
            "Reject malformed/unknown settings",
            "`single_pass` permits one pass",
            "returns `findings` without fixes or repeats",
            "handler fixes only scoped corrections, validates, commits, pushes",
        ):
            self.assertIn(requirement, review)

    def test_review_run_counts_started_and_verification_passes(self) -> None:
        review = normalized(skill("self-review"))
        self.assertLess(
            review.index("record `## SELF REVIEW` as `started`"),
            review.index("Independently inspect"),
        )
        for requirement in (
            "run/request",
            "pinned mode/limit",
            "pass number",
            "reviewer/source",
            "base/head SHAs",
            "issue/design/guidance revisions",
            "`started`",
            "`findings_remaining`",
            "`interrupted`",
            "Started, interrupted, and verification passes count",
            "Fixes, retries, and continuation never reset the run",
            "only a later independent review request starts a new run with new settings",
            "single-pass reuse requires the same request",
            "check the remaining budget",
            "check that a verification pass remains before fixing",
            "`review_limit`",
            "without unreviewed final fixes",
        ):
            self.assertIn(requirement, review)

    def test_self_review_has_four_self_contained_steps(self) -> None:
        review = skill("self-review")
        self.assertEqual(
            re.findall(r"^\d+\. \*\*([A-Za-z]+)\.\*\*", review, re.M),
            ["Prepare", "Review", "Triage", "Act"],
        )
        self.assertNotIn("references\\", review)
        self.assertFalse((SKILLS / "self-review" / "references").exists())
        self.assertLess(review.index("**Triage.**"), review.index("**Act.**"))
        self.assertLess(
            review.index("Reuse only verifiable reports"),
            review.index("check the remaining budget"),
        )

    def test_finding_dispositions_are_scoped_and_preserve_evidence(self) -> None:
        review = skill("self-review")
        triage = review.split("3. **Triage.**", 1)[1].split("4. **Act.**", 1)[0]
        self.assertEqual(
            set(re.findall(r"`(fix|no_fix|needs_decision)`", triage)),
            {"fix", "no_fix", "needs_decision"},
        )
        for requirement in (
            "Assess the problem, not automatically its suggested fix",
            "issue scope, acceptance criteria, accepted design, manifest, repository principles",
            "`fix` for required scoped corrections or introduced regressions",
            "`no_fix` for evidenced refutations, accepted tradeoffs, or unrelated follow-ups (list only)",
            "Preserve original findings",
            "dispositions, evidence, rationale, authority, and remaining count",
            "before fixes or handoff",
        ):
            self.assertIn(requirement, normalized(review))

    def test_ambiguous_review_action_hands_off_before_fixes_in_either_mode(self) -> None:
        review = normalized(skill("self-review"))
        for requirement in (
            "`needs_decision` for unresolved action or scope/design questions",
            "In either mode, unresolved decisions require `handoff-issue`",
            "reason `review_decision`, alternatives, recommendation",
            "the specific decision needed to resume, not speculative edits",
            "Missing triage remains undecided",
        ):
            self.assertIn(requirement, review)
        self.assertLess(review.index("`review_decision`"), review.index("handler fixes"))

    def test_completed_review_and_dispositions_are_saved_before_handoff(self) -> None:
        review = normalized(skill("self-review"))
        persisted = review.index("save pass result")
        self.assertLess(persisted, review.index("unresolved decisions require `handoff-issue`"))
        self.assertLess(persisted, review.index("handler fixes"))
        self.assertIn(
            "dispositions, evidence, rationale, authority, and remaining count on the issue before fixes or handoff",
            review,
        )

    def test_non_actionable_findings_can_be_clean_without_waiving_blockers(self) -> None:
        review = normalized(skill("self-review"))
        for requirement in (
            "no required or undecided findings remaining",
            "Non-action cannot waive acceptance, regressions, quality gates, or user requirements",
            "Needed design/planning returns `not_ready`",
            "the handler fixes only scoped corrections",
            "independently reviews again",
            "Review grants no exception to CI, required approvals, or thread resolution",
            "`single_pass` permits one pass and returns `findings` without fixes or repeats",
        ):
            self.assertIn(requirement, review)
        self.assertIn("Justified non-action or clarification alone needs no extra pass", review)
        self.assertLess(review.index("Return `clean` only"), review.index("`review_limit`"))

    def test_disposition_only_clarification_does_not_reset_or_spend_a_pass(self) -> None:
        review = normalized(skill("self-review"))
        for requirement in (
            "Reuse only verifiable reports for unchanged revisions and no later unresolved findings",
            "Justified non-action or clarification alone needs no extra pass",
            "continuation never reset the run",
            "changed revisions invalidate clean evidence",
        ):
            self.assertIn(requirement, review)
        for name in ("handoff-issue", "continue-issue"):
            with self.subTest(skill=name):
                self.assertIn(
                    "finding dispositions and unresolved decisions",
                    normalized(skill(name)),
                )

    def test_review_decision_handoff_is_not_satisfied_by_blanket_approval(self) -> None:
        autopilot = normalized(skill("orchestrator-autopilot"))
        self.assertIn("A `review_decision` handoff requires resolving the specific finding's", autopilot)
        self.assertIn("neither approval mode can replace that evidence with blanket approval", autopilot)
        self.assertIn(
            "A review-decision wait needs resolution of that uncertainty, not only workflow approval",
            normalized(skill("continue-issue")),
        )
        self.assertIn(
            "the specific decision needed to resume",
            normalized(skill("self-review")),
        )

    def test_pr_feedback_uses_scoped_triage_before_repairs(self) -> None:
        iteration = normalized(skill("iterate-pr"))
        self.assertIn(r"`..\self-review\SKILL.md`", iteration)
        self.assertIn("without invoking another review", iteration)
        self.assertLess(
            iteration.index("Triage new feedback"),
            iteration.index("Otherwise repair within the accepted design"),
        )
        self.assertLess(
            iteration.index("`review_decision`"),
            iteration.index("Otherwise repair within the accepted design"),
        )
        for requirement in (
            "Preserve justified `no_fix` dispositions unless relevant new evidence changes their basis",
            "not every review suggestion requires implementation",
            "addressing only required corrections",
            "read-only or already-released assessment instead returns `waiting`",
            "without acquiring or releasing handling",
        ):
            self.assertIn(requirement, iteration)

    def test_publication_and_merge_share_review_disposition_gates(self) -> None:
        publication = normalized(skill("open-pr"))
        self.assertIn(r"`..\self-review\SKILL.md`", publication)
        self.assertIn("required or undecided findings cannot count as clean", publication)
        pr = normalized(read(SKILLS / "iterate-pr" / "references" / "PR-STATE.md"))
        self.assertIn(r"`..\..\self-review\SKILL.md`", pr)
        self.assertIn("without starting another review here", pr)
        self.assertIn("required or undecided findings block progression", pr)
        self.assertIn("does not waive required GitHub approvals or thread resolution", pr)

    def test_handoff_and_continuation_preserve_review_runs(self) -> None:
        handoff = normalized(skill("handoff-issue"))
        continuation = normalized(skill("continue-issue"))
        self.assertIn("review run's count, including exhaustion", handoff)
        self.assertIn("handoff is not a new review request", handoff)
        self.assertIn("Preserve any current self-review run and iteration count", continuation)

    def test_non_clean_review_stops_callers_without_automatic_retry(self) -> None:
        outputs = skill_output("self-review")
        self.assertEqual(
            set(re.findall(r"`([a-z_]+)`", outputs)),
            {"clean", "findings", "not_ready", "handed_off", "partial_failure"},
        )
        for name in ("open-pr", "iterate-pr"):
            with self.subTest(skill=name):
                body = normalized(skill(name))
                self.assertIn("`findings`", body.split("## Output", 1)[1])
                self.assertIn("reset", body)
        self.assertIn(
            "`findings` stops without automatic remediation",
            normalized(skill("iterate-pr")),
        )
        completion = normalized(skill("complete-issue"))
        self.assertIn("non-clean review cannot permit merging", completion)
        self.assertIn("Never restart an exhausted review run", completion)

    def test_pr_requirements_cover_classic_protection_and_impossible_methods(self) -> None:
        pr = normalized(read(SKILLS / "iterate-pr" / "references" / "PR-STATE.md"))
        for requirement in (
            "required_conversation_resolution.enabled",
            "empty intersection",
            "App/integration identities",
            "latest-push",
            "actual PR base branch",
            "unknown",
        ):
            self.assertIn(requirement, pr)
        iteration = normalized(skill("iterate-pr"))
        self.assertIn("CHANGES_REQUESTED", iteration)
        self.assertIn("wait for new evidence", iteration)

    def test_completion_binds_merge_and_cleanup_to_expected_heads(self) -> None:
        completion = normalized(skill("complete-issue"))
        for requirement in (
            "--match-head-commit",
            "--force-with-lease",
            "Do not use `--delete-branch`",
            "waiting_for_merge",
            "state_reason=completed",
            "verified no-PR outcome",
            "skip the merge gates",
            "previous machine",
            "not merely because the pre-queue checks still pass",
            "preserve extra local commits",
            "remain at the claim base",
            "Skip an absent remote task ref",
        ):
            self.assertIn(requirement, completion)

    def test_autopilot_is_sequential_and_keeps_the_same_agent(self) -> None:
        autopilot = normalized(skill("orchestrator-autopilot"))
        for requirement in (
            "Execute sequentially",
            "finish or durably hand off the current issue before selecting another",
            "The agent running this skill is the issue handler throughout",
            "Independent reviewers may assist, not take over delivery",
            "Claim or continue the issue yourself",
            "after ending your handling interval",
        ):
            self.assertIn(requirement, autopilot)
        self.assertNotRegex(autopilot, r"\b(?:worker|dispatch|delegate|delegated)\b")
        for path in active_documents():
            with self.subTest(path=path.relative_to(BUNDLE)):
                self.assertNotIn("max_parallel_issues", read(path))

    def test_autopilot_requires_request_and_preserves_read_only_use(self) -> None:
        autopilot = normalized(skill("orchestrator-autopilot"))
        for requirement in (
            "only on an explicit request",
            "`reconcile-board --read-only`",
            "`snapshot` without claim or other writes",
            "incomplete reads return `partial_failure`",
        ):
            self.assertIn(requirement, autopilot)
        self.assertNotRegex(autopilot, r"\bgh\s")

    def test_autopilot_resumes_existing_work_and_uses_lifecycle_routing(self) -> None:
        autopilot = normalized(skill("orchestrator-autopilot"))
        for requirement in (
            "Prefer existing work that can advance",
            "merged-PR cleanup",
            "enter through `continue-issue`",
            "Unclaimed Ready work enters through `claim-issue`",
            "a retained branch means continuation",
            "No label, original-agent, or tracking-parent filter",
            "`DEV-FLOW.md` routing and each skill's next action",
            "Development may call `plan-issues`",
            "not start the resulting issues before the current interval ends",
        ):
            self.assertIn(requirement, autopilot)

    def test_autopilot_preserves_handler_identity_and_serial_release(self) -> None:
        autopilot = normalized(skill("orchestrator-autopilot"))
        for requirement in (
            "Do not take over another preparing/active handler",
            "Claim or continue the issue yourself",
            "Verify GitHub evidence that your handling interval ended before moving on",
            "`waiting` without acquisition needs no new handoff",
            "Failed persistence or uncertain ownership means `partial_failure`",
            "only when no owned handling interval remains",
        ):
            self.assertIn(requirement, autopilot)

    def test_autopilot_preserves_review_modes_and_durable_run_counts(self) -> None:
        autopilot = normalized(skill("orchestrator-autopilot"))
        for requirement in (
            "Preserve project review settings and run counts",
            "autopilot retries are not independent review requests",
            "Report-only `findings`",
            "require `handoff-issue`",
            "awaiting a remediation decision without automatic fixes",
            "Do not manufacture approval or bypass failing/pending CI",
        ):
            self.assertIn(requirement, autopilot)

    def test_autopilot_stop_requires_fresh_complete_board_evidence(self) -> None:
        autopilot = normalized(skill("orchestrator-autopilot"))
        for requirement in (
            "complete board view",
            "including all pages",
            "Do not retry failed or waiting issues without relevant new evidence",
            "Except for the configured CI observation in step 5",
            "never poll unchanged conditions",
            "Never duplicate handoffs",
            "Empty Ready alone is not a stopping test",
            "refresh the complete board and outstanding resume conditions",
            "Return `drained` only when the fresh, complete view proves all",
            "| `Ready` | None remain.",
            "durable handoff with an unsatisfied resume condition",
            "no active/preparing handler",
            "unsatisfied native issue dependencies",
            "Accepted completion is verified",
            "Unknown states, unresolved issue items, incomplete reads, or failures prevent `drained`",
            "Another agent's active work means `paused`",
            "Never change status merely to empty Ready",
        ):
            self.assertIn(requirement, autopilot)
        output = skill("orchestrator-autopilot").split("## Output\n", 1)[1]
        self.assertEqual(
            set(re.findall(r"`([a-z_]+)`", output)),
            {"drained", "snapshot", "paused", "partial_failure"},
        )

    def test_autopilot_failure_and_interruption_are_not_success(self) -> None:
        autopilot = normalized(skill("orchestrator-autopilot"))
        for requirement in (
            "Record unknown outcomes explicitly",
            "stop if shared state is unreliable",
            "On user/platform interruption",
            "preserve progress and hand off",
            "report anything that could not be saved or released",
        ):
            self.assertIn(requirement, autopilot)
        for path in (DOCS / "README.md", DOCS / "STATE-MACHINE.md"):
            with self.subTest(document=path.name):
                self.assertNotIn("deferred", read(path).lower())

    def test_autopilot_settings_are_per_repository_with_approval_modes(self) -> None:
        configured = 0
        for name, body in repository_configs():
            with self.subTest(repository=name):
                if re.search(r"^    status: active$", body, re.M):
                    settings = re.search(
                        r"^    autopilot:\n      mode: ([a-z-]+|<approval-mode>)\n"
                        r"(?:      wait_for_ci: (true|false)\n)?(?=    [a-z_]+:)",
                        body,
                        re.M,
                    )
                    self.assertIsNotNone(settings)
                    if settings is not None:
                        allowed = {"auto-approval", "reasonable-approval"}
                        if name == "<repo-key>":
                            allowed.add("<approval-mode>")
                        self.assertIn(settings[1], allowed)
                    configured += 1
                else:
                    self.assertNotRegex(body, r"(?m)^    autopilot:")
        self.assertGreater(configured, 0)
        self.assertNotRegex(
            read(REFERENCES / "RESOURCE-MAP.yml"), r"(?m)^\s+mode: auto\s*$"
        )
        autopilot = normalized(skill("orchestrator-autopilot"))
        for requirement in (
            "`repos.<key>.autopilot`",
            "`RESOURCE-MAP.yml`",
            "Require a mapping with `mode`",
            "`auto-approval` or `reasonable-approval`",
            "optional `wait_for_ci`; no other keys",
            "Missing, malformed, or unsupported settings",
            "not permission to assume authority",
            "Record the setting revision",
            "Re-resolve on repository changes",
        ):
            self.assertIn(requirement, autopilot)

    def test_only_autopilot_documents_interpret_approval_profiles(self) -> None:
        for path in active_documents():
            if path == REFERENCES / "RESOURCE-MAP.yml":
                continue
            with self.subTest(path=path.relative_to(BUNDLE)):
                body = read(path)
                self.assertNotRegex(body, r"autopilot:auto\b|`interactive`|mode: auto\b(?!-)")
                if SKILLS / "orchestrator-autopilot" not in path.parents:
                    self.assertNotRegex(
                        body,
                        r"\b(?:auto-approval|reasonable-approval|reaonable-approval)\b"
                        r"|repos\.<key>\.autopilot|invocation policy|wait_for_ci",
                    )

    def test_ci_wait_setting_is_optional_boolean_with_template_default(self) -> None:
        for name, body in repository_configs():
            with self.subTest(repository=name):
                values = re.findall(r"^      wait_for_ci: (.*)$", body, re.M)
                if re.search(r"^    status: active$", body, re.M):
                    self.assertLessEqual(len(values), 1)
                    self.assertTrue(all(value in {"true", "false"} for value in values))
                    if name == "<repo-key>":
                        self.assertEqual(values, ["false"])
                else:
                    self.assertEqual(values, [])
        autopilot = normalized(skill("orchestrator-autopilot"))
        for requirement in (
            "`wait_for_ci` must be a YAML boolean",
            "omitted or `false` means hand off on pending CI",
            "`true` means wait until CI finishes, with no configured timeout",
            "Reject quoted booleans, numbers, and null",
            "Only this skill interprets `wait_for_ci`",
            "Before PR actions, tell the called skill whether this caller will observe CI-only waits",
        ):
            self.assertIn(requirement, autopilot)

    def test_ci_wait_retains_handling_and_does_not_repeat_self_review(self) -> None:
        autopilot = normalized(skill("orchestrator-autopilot"))
        for requirement in (
            "With `wait_for_ci: true`",
            "observe a `waiting` result only when pending CI is the sole unmet gate",
            "under current approval authority",
            r"`..\iterate-pr\references\PR-STATE.md`",
            "Retain active handling and the local environment",
            "do not hand off or start another issue while observing",
            "Waiting does not restart self-review or consume review passes",
            "reuse unchanged clean evidence, not evidence invalidated by changed code",
        ):
            self.assertIn(requirement, autopilot)

    def test_released_ci_wait_is_observed_without_premature_continuation(self) -> None:
        autopilot = normalized(skill("orchestrator-autopilot"))
        for requirement in (
            "Before stopping, also consider released CI-only waits",
            "For already-released work, observe read-only without acquisition",
            "call `continue-issue` only after the resume condition is satisfied",
            "rechecking ownership",
        ):
            self.assertIn(requirement, autopilot)
        self.assertIn(
            "Return `waiting` without setup or another comment while a required condition is unsatisfied",
            normalized(skill("continue-issue")),
        )

    def test_pr_actions_return_caller_managed_waits_without_releasing_handling(self) -> None:
        for name in ("iterate-pr", "complete-issue"):
            with self.subTest(skill=name):
                body = normalized(skill(name))
                self.assertIn("If the caller explicitly chooses to observe this wait", body)
                self.assertIn("return `waiting`", body)
                self.assertIn("head/base, all unmet conditions, and unchanged handling", body)
                self.assertIn("`waiting`", skill_output(name))
                self.assertIn("handling state", skill_output(name))
        self.assertIn("do not release handling or poll here", normalized(skill("iterate-pr")))
        completion = normalized(skill("complete-issue"))
        self.assertIn("otherwise hand off an actual wait", completion)
        self.assertIn("refresh state and apply step 2's wait handling", completion)
        self.assertIn("save a `merge_queue` handoff", completion)

    def test_ci_observation_watches_all_checks_and_verifies_current_results(self) -> None:
        reference = read(SKILLS / "iterate-pr" / "references" / "PR-STATE.md")
        observation = normalized(reference.split("## Observe pending CI\n", 1)[1])
        for requirement in (
            "one attached watcher or event subscription with conservative polling",
            "not repeated lifecycle calls or unchanged GitHub comments",
            "--watch --fail-fast --interval 30",
            "Watch all reported checks, not only required ones",
            "verify a queued/running workflow for the current head",
            "Missing checks without observable pending work",
            "watcher errors need an explicit blocker report",
            "Stop the watcher before leaving observation",
            "A watcher finishing is not merge authorization",
            "refresh PR state, head/base, all reported and expected checks, feedback, and requirements",
            "A changed head/base invalidates the old readiness decision",
            "Exit code 8 remains pending",
            "an empty check set or command failure is not CI success",
            "Terminal CI failures return to assessment",
            "not a blind rerun",
        ):
            self.assertIn(requirement, observation)
        command = re.search(r"^gh pr checks .+ --watch .+$", reference, re.M)
        self.assertIsNotNone(command)
        if command is not None:
            self.assertNotIn("--required", command[0])

    def test_ci_wait_reassesses_failures_and_preserves_other_handoffs(self) -> None:
        autopilot = normalized(skill("orchestrator-autopilot"))
        for requirement in (
            "Stop observation on CI completion, failure, cancellation, or changed head/base",
            "refresh PR state and use `iterate-pr` for repair or completion assessment",
            "Required human review/approval, merge-queue waits, missing/unknown CI",
            "infrastructure or permission blockers are not covered by CI waiting",
            "On user/platform interruption, stop any watcher",
        ):
            self.assertIn(requirement, autopilot)
        model = normalized(read(DOCS / "STATE-MACHINE.md"))
        self.assertIn("direct calls still hand off by default", model)
        self.assertIn("without a configured timeout", model)
        self.assertIn("an agent observing CI may remain active", model)

    def test_autopilot_authority_is_current_and_repository_scoped(self) -> None:
        autopilot = normalized(skill("orchestrator-autopilot"))
        for requirement in (
            "Re-resolve on repository changes, especially for a PR in another repository",
            "Configuration or a historical handoff alone grants no authority outside this explicit run",
            "Interpret modes here only",
            "When a lifecycle step reaches a decision or approval point",
            "apply the selected mode using that step's evidence",
            "those skills do not select approval policy",
            "never fabricate human approval",
            "changed authority requires a fresh request, not self-escalation",
            "End this invocation's autonomy context",
        ):
            self.assertIn(requirement, autopilot)
        boot = normalized(skill("orchestrator-boot"))
        self.assertIn("project settings without interpreting workflow policy", boot)
        self.assertIn("loading configuration grants no new authority", boot)

    def test_reasonable_approval_is_manifest_guided_without_admin_bypass(self) -> None:
        autopilot = skill("orchestrator-autopilot")
        modes = dict(
            re.findall(
                r"^\| `(auto-approval|reasonable-approval)` \| (.+) \|$",
                autopilot,
                re.M,
            )
        )
        self.assertEqual(set(modes), {"auto-approval", "reasonable-approval"})
        for requirement in (
            "without routine human confirmation",
            "After clean self-review and CI",
            "guarded admin bypass",
        ):
            self.assertIn(requirement, modes["auto-approval"])
        for requirement in (
            "Read the referenced manifest",
            "fits its constraints and delegation",
            "has no material ambiguity",
            "needs no explicit approval",
            "Otherwise hand off with the proposed decision and reason",
            "Keep normal GitHub review and merge-queue requirements",
            "this mode does not authorize admin bypass",
        ):
            self.assertIn(requirement, modes["reasonable-approval"])
        self.assertIn(
            "Missing or unreadable manifest guidance is not authority for reasonable self-approval",
            normalized(autopilot),
        )

    def test_design_and_implementation_consume_caller_decisions(self) -> None:
        core = normalized(read(REFERENCES / "CORE.md"))
        for requirement in (
            "current caller or workflow supplies decision authority and required approvals",
            "lifecycle skills perform actions rather than select policy",
            "Without explicit delegation",
            "with the human and obtain approval",
            "another repository's authorization is not permission for the current operation",
        ):
            self.assertIn(requirement, core)
        design = normalized(skill("design-issue"))
        for requirement in (
            "explaining alternatives and the recommendation",
            "Resolve required decisions and approvals under the caller's authority",
            "decision/approval basis",
            "Missing or declined required approval never permits `ready_to_implement`",
        ):
            self.assertIn(requirement, design)
        implementation = normalized(skill("implement-issue"))
        for requirement in (
            "If design or required approval is missing, return `not_ready`",
            "do not perform that stage here",
            "routine choices within the accepted design independently",
            "If a material approach change is needed, return `not_ready`",
        ):
            self.assertIn(requirement, implementation)
        planning = normalized(skill("plan-issues"))
        self.assertIn("Settle the proposed plan and required approvals before graph writes", planning)

    def test_caller_decisions_resolve_waits_without_fabricating_consent(self) -> None:
        continuation = normalized(skill("continue-issue"))
        for requirement in (
            "current decisions or exceptions supplied by the caller",
            "an old handoff grants no new authority",
            "Explicit user holds and ambiguous wait origins remain unresolved",
            "including current CI and bypass restrictions",
        ):
            self.assertIn(requirement, continuation)
        self.assertIn(
            "Distinguish a workflow-only approval wait from an explicit user hold",
            normalized(skill("handoff-issue")),
        )
        reconciliation = normalized(skill("reconcile-board"))
        self.assertIn("Report unmet approvals and their recorded source", reconciliation)
        self.assertIn("The caller decides whether it can supply a missing decision", reconciliation)
        autopilot = normalized(skill("orchestrator-autopilot"))
        self.assertIn("Evaluate approval-waiting candidates under step 3", autopilot)
        self.assertIn("Apply this judgment to reported approval waits", autopilot)
        self.assertIn("not an explicit user hold or an ambiguous requirement", autopilot)

    def test_admin_merge_requires_current_explicit_exception_and_all_ci(self) -> None:
        pr = normalized(read(SKILLS / "iterate-pr" / "references" / "PR-STATE.md"))
        for requirement in (
            "Preserve normal GitHub requirements and project/issue approval requests",
            "current caller supplies an explicit exception for this PR repository",
            "Verify the waived gates, authority source, and current applicability",
            "configuration or an earlier run is not permission",
            "The calling workflow selects policy, not this reference",
            "Before using a caller-authorized `--admin` exception",
            "All reported CI checks and expected required checks/workflows are satisfied",
            "Missing, pending, cancelled, failed, or unknown CI blocks admin merge",
            "including failures not marked required by protection",
            "No checks reported is not success",
            "Establish an intentional no-CI case explicitly",
            "If CI needs the merge queue",
            "Explicit user holds and every non-bypassed requirement",
            "strict up-to-date requirements",
            "broad, not a review-only bypass",
            "--match-head-commit",
            "GitHub must permit the current actor's operation",
            "not changing protection, waiving CI, or blind retry",
        ):
            self.assertIn(requirement, pr)
        self.assertIn(
            "gh pr checks <number> --repo <owner/repo> --json name,state,bucket,link",
            pr,
        )

    def test_pr_skills_consume_exceptions_without_selecting_policy(self) -> None:
        iteration = normalized(skill("iterate-pr"))
        self.assertIn("current caller-supplied approval or merge-exception evidence", iteration)
        self.assertIn("An approval exception never dismisses valid unaddressed findings", iteration)
        self.assertIn("otherwise preserve normal review and queue requirements", iteration)
        self.assertIn(
            "Completion still requires the guarded merge conditions",
            normalized(skill("open-pr")),
        )
        completion = normalized(skill("complete-issue"))
        for requirement in (
            "verify any caller-authorized exception applies to this PR repository",
            "add `--admin` only for a current, explicit caller-authorized exception",
            "Recheck its authority and CI before the operation",
            "If GitHub denies the operation",
            "without an eligible admin bypass",
            "including admin merge",
            "approval/exception basis when used",
        ):
            self.assertIn(requirement, completion)

    def test_one_skill_request_returns_without_onward_sequencing(self) -> None:
        core = normalized(read(REFERENCES / "CORE.md"))
        for requirement in (
            "Complete only the requested skill's defined action",
            "return its outcome to the caller",
            "For a direct one-skill request, report the result and stop",
            "Suggested next skills are advisory, not instructions to invoke them",
            "Only an explicitly requested multi-step workflow owns onward sequencing",
            "Do not ask to start another stage as part of normal completion",
            "Approval alone accepts a decision; it does not authorize the next stage",
        ):
            self.assertIn(requirement, core)
        flow = normalized(read(REFERENCES / "DEV-FLOW.md"))
        self.assertIn("not permission for a skill to invoke its successor", flow)
        self.assertIn("A direct invocation stops at its result, including after approval", flow)

    def test_leaf_outputs_return_advisory_next_actions(self) -> None:
        for name in sorted(ACTIVE - {"orchestrator-autopilot"}):
            with self.subTest(skill=name):
                output = normalized(skill_output(name))
                self.assertTrue(output.startswith("Return "))
                self.assertRegex(output.lower(), r"\bsuggested next (?:skill|action)\b")

    def test_leaf_skills_do_not_command_another_lifecycle_stage(self) -> None:
        supporting = {"orchestrator-boot", "reconcile-board", "handoff-issue"}
        stages = "|".join(re.escape(name) for name in sorted(ACTIVE - supporting))
        command = re.compile(
            rf"\b(?:run|invoke|enter|use|revisit|route(?:s)? to|return to)\s+`(?:{stages})`",
            re.I,
        )
        for name in sorted(ACTIVE - {"orchestrator-autopilot"}):
            with self.subTest(skill=name):
                self.assertNotRegex(normalized(skill(name)), command)

    def test_manual_claim_design_and_implementation_have_terminal_results(self) -> None:
        cases = (
            ("claim-issue", "claimed", "design-issue"),
            ("design-issue", "ready_to_implement", "implement-issue"),
            ("implement-issue", "ready_for_review", "self-review"),
        )
        for name, outcome, next_skill in cases:
            with self.subTest(skill=name):
                output = normalized(skill_output(name))
                self.assertIn(f"`{outcome}`", output)
                self.assertIn(f"`{next_skill}`", output)
                self.assertIn("Suggested next skill", output)
        self.assertIn("Return without starting either skill", skill_output("claim-issue"))
        self.assertIn(
            "Stop this action after recording approval; do not implement or automatically hand off",
            normalized(skill_output("design-issue")),
        )
        self.assertIn(
            "do not invoke either as part of implementation",
            normalized(skill_output("implement-issue")),
        )

    def test_design_approval_question_contains_the_design_and_only_the_decision(self) -> None:
        design = normalized(skill("design-issue"))
        for requirement in (
            "Before asking for human approval",
            "self-contained design brief",
            "approval tool's message",
            "goal, approach, affected areas, key tradeoffs/risks, and scope boundaries",
            "including changes outside the repository",
            "a link to the full design",
            "cannot replace it",
            'Ask only "Approve this design?"',
            "`approve_design` or `revise_design`",
            "Do not bundle implementation or handoff into the approval choices",
            "Handle requested revisions within this design action",
        ):
            self.assertIn(requirement.lower(), design.lower())
        self.assertLess(design.index("self-contained design brief"), design.index('Ask only'))
        self.assertLess(design.index("return `not_ready`"), design.index("Before asking"))
        for unsupported_choice in ("approve_and_implement", "handoff_without_implementation"):
            self.assertNotIn(unsupported_choice, design)

    def test_supporting_operations_and_handling_survive_a_normal_return(self) -> None:
        core = normalized(read(REFERENCES / "CORE.md"))
        self.assertIn(
            "Supporting context loading, environment preparation, and board reconciliation",
            core,
        )
        self.assertIn("needed for the current action are allowed", core)
        self.assertIn(
            "A normal skill return does not release active handling or require a handoff",
            core,
        )
        self.assertIn("Hand off only for an actual pause, blocker, interruption, or transfer", core)
        self.assertIn(
            "Finishing an individual skill or approving a design is not, by itself, a reason to release handling",
            normalized(skill("handoff-issue")),
        )
        continuation = normalized(skill("continue-issue"))
        self.assertIn("Identify the next unfinished action", continuation)
        self.assertIn("do not execute it", continuation)
        self.assertIn("Continuation ends after restoration and routing", continuation)

    def test_missing_stage_is_reported_instead_of_executed(self) -> None:
        core = normalized(read(REFERENCES / "CORE.md"))
        self.assertIn(
            "A different lifecycle stage is not an implicit prerequisite or follow-up",
            core,
        )
        self.assertIn(
            "return `not_ready` with the missing prerequisite and suggested next skill",
            core,
        )
        for name in (
            "design-issue", "implement-issue", "self-review",
            "open-pr", "iterate-pr", "complete-issue",
        ):
            with self.subTest(skill=name):
                self.assertIn("`not_ready`", skill_output(name))
        review = normalized(skill("self-review"))
        self.assertIn("Needed design/planning returns `not_ready` with the next skill", review)
        self.assertIn("preserving the run/count", review)
        iteration = normalized(skill("iterate-pr"))
        self.assertIn("`not_ready` with suggested `self-review`", iteration)
        self.assertIn("preserve a current report-only `findings` result", iteration)
        self.assertIn("For other missing, stale, or non-clean self-review evidence", iteration)
        publication = normalized(skill("open-pr"))
        self.assertIn("For other missing, stale, or non-clean prerequisites", publication)
        self.assertLess(
            publication.index("reconcile changed task facts"),
            publication.index("Then return `not_ready`"),
        )

    def test_explicit_workflow_consumes_returns_and_invokes_next_stages(self) -> None:
        autopilot = normalized(skill("orchestrator-autopilot"))
        for requirement in (
            "Each skill returns its result",
            "this explicitly requested workflow owns the next invocation",
            "Consume `not_ready` and its suggested prerequisite before retrying the blocked action",
            "preserving partial progress and review-run state",
            "A skill return is not an issue handoff or the end of this workflow",
        ):
            self.assertIn(requirement, autopilot)

    def test_callers_stop_on_missing_boot_configuration(self) -> None:
        core = normalized(read(REFERENCES / "CORE.md"))
        self.assertIn(
            "If boot returns `needs_configuration`, stop the calling skill with `partial_failure`",
            core,
        )
        self.assertIn("report the missing configuration; do not initialize implicitly", core)
        self.assertIn(
            "Read-only requests and reference-only mappings apply to supporting operations too",
            core,
        )
        for name in sorted(ACTIVE - {"orchestrator-boot"}):
            with self.subTest(skill=name):
                self.assertIn("`partial_failure`", skill_output(name))

    def test_planning_pause_has_an_honest_result_before_graph_writes(self) -> None:
        planning = normalized(skill("plan-issues"))
        for requirement in (
            "If a decision cannot be settled",
            "use `handoff-issue` only for your own handling interval",
            "Otherwise return `needs_decision` with the proposal and missing decision",
            "recording it on an existing affected issue when available",
            "Do not create a handoff-only issue or release another handler's work",
            "Record `## PLAN` on the affected issue or common parent",
        ):
            self.assertIn(requirement, planning)
        self.assertIn("`needs_decision`", skill_output("plan-issues"))
        self.assertLess(planning.index("return `needs_decision`"), planning.index("create or revise native"))

    def test_pr_iteration_checks_review_constraints_before_repairs(self) -> None:
        iteration = normalized(skill("iterate-pr"))
        guard = iteration.index("Before repairs or review mutations")
        repairs = iteration.index("Otherwise repair within the accepted design")
        self.assertLess(guard, repairs)
        self.assertLess(
            iteration.index("If repairs need another pass in an exhausted review run"),
            repairs,
        )
        self.assertIn("`findings` stops without automatic remediation or another review", iteration)
        self.assertIn("before making unreviewed fixes", iteration)
        self.assertIn("Current clean evidence needs no additional pass for completion", iteration)

    def test_queue_admission_does_not_wait_for_queue_only_checks(self) -> None:
        pr = normalized(read(SKILLS / "iterate-pr" / "references" / "PR-STATE.md"))
        for requirement in (
            "Queue admission needs acceptance, clean self-review",
            "applicable pre-queue checks, approvals, and other entry requirements satisfied",
            "Checks that run only in the merge queue are evaluated after entry",
            "they cannot block entry or be waived for direct/admin merge",
            "Queue entry is not a completed merge",
        ):
            self.assertIn(requirement, pr)
        iteration = normalized(skill("iterate-pr"))
        self.assertIn("Return `ready_to_complete` for verified direct merge readiness or queue admission", iteration)
        self.assertIn("Do not wait for queue-only checks before the PR can enter that queue", iteration)
        self.assertIn("an already-entered queue", iteration)
        completion = normalized(skill("complete-issue"))
        self.assertIn(
            "For a required queue, assess its admission requirements rather than waiting for checks",
            completion,
        )
        self.assertIn("Choose one integration path", completion)
        self.assertLess(
            completion.index("For a required merge queue without an eligible admin bypass"),
            completion.index("Otherwise select a permitted merge method"),
        )
        self.assertIn("`--match-head-commit <reviewed-head>` without forcing a method", completion)

    def test_no_pr_completion_is_resolved_before_pr_gates(self) -> None:
        completion = normalized(skill("complete-issue"))
        self.assertIn(
            "With no PR, verify the accepted no-PR outcome, required child/dependency outcomes, and absence of unmerged implementation",
            completion,
        )
        self.assertLess(completion.index("With no PR"), completion.index("Before merging"))
        self.assertIn("then proceed to step 5", completion)
        self.assertIn("Close a verified merge or verified no-PR outcome", completion)

    def test_publication_discovers_existing_work_before_review_gates(self) -> None:
        publication = normalized(skill("open-pr"))
        self.assertLess(
            publication.index("Search all PR states for the exact remote head repository/branch"),
            publication.index("Require clean review for the current base/head"),
        )
        self.assertLess(
            publication.index("return `already_merged`"),
            publication.index("Require clean review for the current base/head"),
        )
        self.assertIn(
            "With no PR, read only the base-branch requirements, not nonexistent PR state",
            publication,
        )
        self.assertLess(
            publication.index("Require clean review for the current base/head"),
            publication.index("Create or update the PR"),
        )

    def test_non_default_pr_targets_preserve_durable_issue_association(self) -> None:
        publication = normalized(skill("open-pr"))
        for requirement in (
            "Identify the existing PR's base",
            "default branch or explicitly intended base",
            "Create or update the PR against that resolved base",
            "For default-branch targets, include a closing reference",
            "Non-default targets ignore closing keywords",
            "preserve explicit issue/PR cross-links, not an automatic-close assumption",
            "Verify the durable issue/PR association",
        ):
            self.assertIn(requirement, publication)

    def test_four_board_states_require_distinct_project_options(self) -> None:
        project = normalized(read(SKILLS / "reconcile-board" / "references" / "PROJECT.md"))
        self.assertIn("Require four distinct status option IDs", project)
        self.assertIn("mapping two lifecycle states to one option loses readiness", project)
        self.assertIn(
            "four distinct status options",
            normalized(read(REFERENCES / "INITIALIZE.md")),
        )

    def test_current_resume_triggers_can_permit_repair_before_merge(self) -> None:
        continuation = normalized(skill("continue-issue"))
        self.assertLess(
            continuation.index("Use only handoffs not superseded by a later acquisition"),
            continuation.index("evaluate the current resume condition"),
        )
        self.assertIn(
            "New actionable feedback or a CI failure can permit repair while merge gates remain unmet",
            continuation,
        )
        self.assertIn("do not require merge readiness before restoring repair work", continuation)
        model = normalized(read(DOCS / "STATE-MACHINE.md"))
        self.assertIn("reconcile the board and return the suggested next action to the caller", model)
        self.assertIn("Continuation does not execute that action or restart Dev", model)

    def test_worktree_fallback_stays_within_a_root_workspace(self) -> None:
        environment = normalized(read(REFERENCES / "LOCAL-ENV.md"))
        for requirement in (
            "Without a convention, choose an unused path containing the issue number inside the workspace",
            "use a sibling only when contained",
            "For a root checkout, use a workspace-local worktree directory",
            "excluded from the main checkout's status",
        ):
            self.assertIn(requirement, environment)
        self.assertIn(
            "including `path: .` when it is the workspace root",
            normalized(read(REFERENCES / "INITIALIZE.md")),
        )

    def test_completed_cleanup_recovers_before_fetching_deleted_refs(self) -> None:
        environment = normalized(read(REFERENCES / "LOCAL-ENV.md"))
        self.assertLess(
            environment.index("Resolve recovery before fetching a task ref"),
            environment.index("For a retained task ref, fetch the task and base branches"),
        )
        for requirement in (
            "integrated commit for a merged PR or the recorded claim base for a no-PR outcome",
            "do not fetch or recreate the missing ref",
            "detached at the verified recovery commit",
            "cleanup does not require rebuilding the delivery toolchain",
            "verified detached recovery commit when the task ref is absent",
        ):
            self.assertIn(requirement, environment)
        self.assertIn(
            "Perform cleanup from the main checkout, not the worktree being removed",
            normalized(skill("complete-issue")),
        )

    def test_handoff_reuse_is_bound_to_the_handling_interval(self) -> None:
        handoff = normalized(skill("handoff-issue"))
        self.assertIn("Record the handler/acquisition", handoff)
        self.assertIn("equivalent latest handoff only for the same handling interval", handoff)
        self.assertLess(handoff.index("Record the handler/acquisition"), handoff.index("Post `## HANDOFF`"))

    def test_autopilot_stops_prerequisite_loops_and_checks_done_ownership(self) -> None:
        autopilot = normalized(skill("orchestrator-autopilot"))
        for requirement in (
            "Do not repeat an unchanged prerequisite cycle",
            "report the blocker and hand off rather than alternating skills without progress",
            "No active/preparing handler may remain in any state, including Done",
            "no completion cleanup may be actionable",
        ):
            self.assertIn(requirement, autopilot)
        self.assertTrue(normalized(skill_output("orchestrator-autopilot")).startswith("Return "))
        self.assertIn(
            "Reuse verified completion/release records for Done items",
            normalized(skill("reconcile-board")),
        )

    def test_removed_evaluators_and_bytecode_are_not_shipped(self) -> None:
        for path in SKILLS.rglob("*"):
            with self.subTest(path=path.relative_to(BUNDLE)):
                self.assertNotEqual(path.suffix, ".pyc")
                self.assertNotIn(path.name, {"evaluate_workflow_policy.py", "evaluate_review_budget.py"})


if __name__ == "__main__":
    unittest.main()
