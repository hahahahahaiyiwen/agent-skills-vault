"""Document contracts, not a simulation of agent behavior or GitHub."""

import re
import unittest
from pathlib import Path


BUNDLE = Path(__file__).resolve().parents[1]
SKILLS = BUNDLE / "skills"
DOCS = BUNDLE / "docs"
REFERENCES = SKILLS / "orchestrator-boot" / "references"
ACTIVE = {
    "plan-issues", "reconcile-board", "claim-issue", "design-issue",
    "implement-issue", "self-review", "open-pr", "iterate-pr",
    "complete-issue", "handoff-issue", "continue-issue",
    "orchestrator-boot", "orchestrator-autopilot",
}
STATES = {"Backlog", "Ready", "In progress", "Done"}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def normalized(text: str) -> str:
    return " ".join(text.split())


def skill(name: str) -> str:
    return read(SKILLS / name / "SKILL.md")


def runtime_documents() -> list[Path]:
    return sorted(
        path for path in SKILLS.rglob("*.md")
        if path.name == "SKILL.md" or path.parent.name == "references"
    )


def repository_configs(config: str) -> list[tuple[str, str]]:
    uncommented = re.sub(r"(?m)^[ \t]*#.*\n?", "", config)
    repos = uncommented.split("\nrepos:\n", 1)[1]
    key = r"(?:[\w-]+|<repo-key>)"
    return re.findall(rf"^  ({key}):\n(.*?)(?=^  {key}:\n|\Z)", repos, re.M | re.S)


class DocumentIntegrityTests(unittest.TestCase):
    def test_skill_inventory_and_frontmatter(self) -> None:
        self.assertEqual({p.parent.name for p in SKILLS.glob("*/SKILL.md")}, ACTIVE)
        descriptions = []
        for name in sorted(ACTIVE):
            with self.subTest(skill=name):
                match = re.match(
                    r"\A---\nname: ([a-z-]+)\ndescription: ([^\n]+)\n---\n",
                    skill(name),
                )
                self.assertIsNotNone(match)
                if match:
                    self.assertEqual(match[1], name)
                    descriptions.append(match[2])
                self.assertTrue((SKILLS / name / "README.md").is_file())
        self.assertEqual(len(descriptions), len(set(descriptions)))

    def test_skills_express_intent_guidance_and_outcome(self) -> None:
        for name in sorted(ACTIVE):
            with self.subTest(skill=name):
                body = skill(name)
                sections = ["Use", "Guidance", "Outcome"]
                if name != "orchestrator-boot":
                    sections = ["When to use", "Preflight", "Input", "Guidance", "Output"]
                self.assertEqual(
                    re.findall(r"^## ([^\n]+)$", body, re.M),
                    sections,
                )
                self.assertNotIn("## Steps", body)
                self.assertNotIn("`not_ready`", body)

    def test_dev_flow_separates_delivery_endpoints_from_optional_activities(self) -> None:
        flow = read(REFERENCES / "DEV-FLOW.md")
        names = {
            name for name in ACTIVE
            if re.search(rf"(?<![\w-]){re.escape(name)}(?![\w-])", flow)
        }
        self.assertEqual(names, ACTIVE)
        self.assertIn("## Issue delivery cycle\n", flow)
        delivery = flow.split("## Issue delivery cycle\n", 1)[1].split("\n## ", 1)[0]
        route = re.search(r"```text\n(.*?)```", delivery, re.S)
        self.assertIsNotNone(route)
        if route:
            self.assertEqual(re.findall(r"[a-z]+(?:-[a-z]+)+", route[1]), [
                "claim-issue", "design-issue", "implement-issue",
                "self-review", "open-pr", "iterate-pr", "complete-issue",
            ])
        for concept in (
            "`claim-issue` and `complete-issue` are the required endpoints",
            "intermediate skills are optional", "in any order",
            "not mandatory checkpoints",
            "`complete-issue` requires a PR, not an invocation of `open-pr`",
        ):
            self.assertIn(concept.lower(), normalized(delivery).lower())
        self.assertNotIn("plan-issues", delivery)

    def test_roadmap_planning_is_a_separate_lifecycle(self) -> None:
        flow = read(REFERENCES / "DEV-FLOW.md")
        self.assertIn("## Roadmap planning cycle\n", flow)
        planning = normalized(
            flow.split("## Roadmap planning cycle\n", 1)[1].split("\n## ", 1)[0]
        )
        for concept in (
            "product/project", "roadmap", "plan-issues",
            "adding, editing, or removing", "separate from delivering one issue",
            "do not restart planning",
        ):
            self.assertIn(concept, planning)

    def test_handoff_and_continuation_transfer_existing_delivery_work(self) -> None:
        flow = read(REFERENCES / "DEV-FLOW.md")
        self.assertIn("## Handoff between handling agents\n", flow)
        transfer = normalized(
            flow.split("## Handoff between handling agents\n", 1)[1].split("\n## ", 1)[0]
        )
        for concept in (
            "handoff-issue -> continue-issue", "releases",
            "next handling agent", "same issue and task branch",
            "next useful activity", "not a new claim",
        ):
            self.assertIn(concept, transfer)

    def test_core_describes_the_model_not_general_session_policies(self) -> None:
        core = read(REFERENCES / "CORE.md")
        self.assertEqual(re.findall(r"^## (.+)$", core, re.M), [
            "GitHub development state",
            "One handling agent, one issue, one worktree",
            "Local worktree layout",
            "Load missing configuration",
        ])
        self.assertNotRegex(core, r"(?m)^\d+\. |^```")
        self.assertNotRegex(core, r"\b(?:gh|git|az) (?:api|project|push|clone|boards)\b")
        self.assertNotIn("PROJECT.md", core)
        self.assertNotRegex(core, r"Scope and authority|Safety and evidence|Context and coordination")

    def test_boot_documents_reference_roles_and_loading(self) -> None:
        readme = normalized(read(SKILLS / "orchestrator-boot" / "README.md"))
        for name in ("CORE.md", "DEV-FLOW.md", "RESOURCE-MAP.yml", "INITIALIZE.md"):
            self.assertIn(name, readme)
        self.assertIn("advisory lifecycle", readme)
        self.assertIn("one handling agent", readme)
        self.assertEqual(readme.count("| On boot. |"), 3)
        self.assertIn("Requested entries are missing or incomplete", readme)
        self.assertNotIn("Shared policies: authority", readme)

    def test_handling_agent_terminology_is_consistent(self) -> None:
        aliases = re.compile(r"\b(?:main[\s-]+agents?|handlers?)\b", re.I)
        for path in BUNDLE.rglob("*.md"):
            with self.subTest(file=path.relative_to(BUNDLE)):
                self.assertNotRegex(read(path), aliases)

    def test_relative_references_and_markdown_links_resolve(self) -> None:
        for path in [*SKILLS.rglob("*.md"), *DOCS.glob("*.md")]:
            references = re.findall(r"`([^`\n]*\\[^`\n]*\.(?:md|yml))`", read(path))
            links = re.findall(r"\]\(([^)]+)\)", read(path))
            for target in [*references, *links]:
                if "://" in target or target.startswith("#") or "<" in target:
                    continue
                with self.subTest(file=path.relative_to(BUNDLE), target=target):
                    target_path = target.split("#", 1)[0]
                    resolved = path.parent.joinpath(
                        *re.split(r"[\\/]", target_path)
                    ).resolve()
                    self.assertIn(BUNDLE.resolve(), resolved.parents)
                    self.assertTrue(resolved.is_file())

    def test_fences_are_balanced(self) -> None:
        for path in [*SKILLS.rglob("*.md"), *DOCS.glob("*.md")]:
            with self.subTest(file=path.relative_to(BUNDLE)):
                self.assertEqual(len(re.findall(r"^```", read(path), re.M)) % 2, 0)

    def test_runtime_guidance_stays_small_including_references(self) -> None:
        words = lambda text: len(text.split())
        runtime = runtime_documents()
        self.assertLessEqual(sum(words(read(p)) for p in runtime), 6500)
        self.assertLessEqual(
            words(skill("orchestrator-boot")) + words(read(REFERENCES / "CORE.md")),
            650,
        )
        limits = {"orchestrator-autopilot": 700, "complete-issue": 500, "self-review": 450}
        for name in sorted(ACTIVE):
            with self.subTest(skill=name):
                self.assertLessEqual(words(skill(name)), limits.get(name, 400))

    def test_no_retired_skills_or_parallel_policy_engine(self) -> None:
        obsolete = (
            r"evaluate_workflow_policy|evaluate_review_budget|max_parallel_issues"
            r"|max_self_review_rounds|max_plan_revisions|max_ci_wait|wait_for_ci"
            r"|self-review-pr|process-external-review|execute-issue"
        )
        for path in runtime_documents():
            with self.subTest(file=path.relative_to(BUNDLE)):
                self.assertNotRegex(read(path), obsolete)
        self.assertFalse(list(SKILLS.rglob("*.pyc")))


class ConfigurationTests(unittest.TestCase):
    def test_template_preserves_four_distinct_board_states(self) -> None:
        config = read(REFERENCES / "RESOURCE-MAP.yml")
        self.assertEqual(set(re.findall(r"^([a-z_]+):", config, re.M)), {"organization", "repos"})
        statuses = dict(re.findall(
            r"^      (backlog|ready|in_progress|done): (.+)$", config, re.M
        ))
        self.assertEqual(statuses, {
            "backlog": "Backlog", "ready": "Ready",
            "in_progress": "In progress", "done": "Done",
        })
        self.assertNotRegex(config, r"(?m)^\s*(workflow|in_review|skip_stages):")

    def test_configured_review_limit_is_positive_not_a_fixed_default(self) -> None:
        repos = repository_configs(read(REFERENCES / "RESOURCE-MAP.yml"))
        self.assertEqual([name for name, _ in repos], ["<repo-key>"])
        body = repos[0][1]
        review = re.search(
            r"^    self_review:\n      mode: (single_pass|until_clean)\n"
            r"      max_iterations: ([1-9][0-9]*)$", body, re.M,
        )
        self.assertIsNotNone(review)
        if review:
            self.assertGreater(int(review[2]), 0)
        self.assertNotIn("wait_for_ci", body)
        self.assertRegex(body, r"(?m)^      mode: <approval-mode>$")

    def test_template_renders_without_treating_comments_as_configuration(self) -> None:
        template = read(REFERENCES / "RESOURCE-MAP.yml")
        values = {
            "<owner-name>": "example-owner",
            "<owner-url>": "https://github.com/example-owner",
            "<project-number>": "7",
            "<project-board-url>": "https://github.com/users/example-owner/projects/7",
            "<repo-key>": "example-repo",
            "<main-worktree-path>": ".",
            "<git-url>": "https://github.com/example-owner/example-repo",
            "<description>": "Example project",
            "<programming-language>": "Python",
            "<manifest-path>": r"docs\PRODUCT_MANIFEST.md",
            "<worktree-parent>": ".worktrees",
        }
        for mode in ("auto-approval", "reasonable-approval"):
            with self.subTest(mode=mode):
                rendered = template.replace("<approval-mode>", mode)
                for placeholder, value in values.items():
                    rendered = rendered.replace(placeholder, value)
                self.assertEqual(set(re.findall(r"<[a-z-]+>", rendered)), {"<feature-name>"})
                body = repository_configs(rendered)[0][1]
                self.assertRegex(body, rf"(?m)^    autopilot:\n      mode: {mode}\n")
                self.assertIn(r"convention: '.worktrees\example-repo-<feature-name>'", body)

    def test_boot_loads_model_context_and_delegates_missing_configuration(self) -> None:
        boot = skill("orchestrator-boot")
        description = boot.split("\ndescription: ", 1)[1].split("\n", 1)[0]
        self.assertIn("Load the GitHub development orchestration model", description)
        guidance = boot.split("## Guidance\n", 1)[1].split("\n## Outcome", 1)[0]
        self.assertEqual(len(re.findall(r"^- ", guidance, re.M)), 2)
        for concept in (
            r"Read `references\RESOURCE-MAP.yml`",
            "requested entries are missing or incomplete",
            r"follow `references\INITIALIZE.md`",
            r"Load `references\CORE.md` and `references\DEV-FLOW.md`",
        ):
            self.assertIn(concept, normalized(guidance))
        self.assertIn("Report any unresolved configuration", normalized(boot))

    def test_lifecycle_skills_load_context_before_using_target_input(self) -> None:
        for name in (
            "plan-issues", "reconcile-board", "orchestrator-autopilot",
            "claim-issue", "design-issue", "implement-issue", "self-review", "open-pr",
            "iterate-pr", "complete-issue", "handoff-issue", "continue-issue",
        ):
            with self.subTest(skill=name):
                body = skill(name)
                self.assertIn("## Preflight\n", body)
                preflight = normalized(
                    body.split("## Preflight\n", 1)[1].split("\n## ", 1)[0]
                )
                self.assertIn(
                    r"Invoke `orchestrator-boot` if "
                    r"`..\orchestrator-boot\references\RESOURCE-MAP.yml` is not in context",
                    preflight,
                )
                self.assertIn("## Input\n", body)
                inputs = normalized(body.split("## Input\n", 1)[1].split("\n## ", 1)[0])
                if name == "plan-issues":
                    concepts = ("GitHub repository or Project", "goals", "read-only")
                elif name == "reconcile-board":
                    concepts = ("configured GitHub Project or affected issues", "--read-only")
                elif name == "orchestrator-autopilot":
                    concepts = ("configured GitHub Project", "requested scope", "read-only request")
                else:
                    target = "PR" if name == "iterate-pr" else "issue"
                    concepts = (f"GitHub {target}", "URL", f"repository and {target} number")
                for concept in concepts:
                    self.assertIn(concept, inputs)

    def test_core_distinguishes_missing_context_from_missing_setup(self) -> None:
        core = normalized(read(REFERENCES / "CORE.md"))
        for concept in (
            "missing from the active context",
            "`RESOURCE-MAP.yml`", "`repos.<key>`",
            "repository instructions", "configured manifest",
            "Reuse loaded values",
            "not been configured", "explicit setup",
            "Unused settings do not block",
        ):
            self.assertIn(concept, core)

    def test_configuration_model_distinguishes_path_locations(self) -> None:
        setup = normalized(read(REFERENCES / "INITIALIZE.md"))
        for concept in (
            "workspace-relative `path`",
            "main worktree on the repository default branch",
            "repository-relative `manifest`",
            "workspace-relative, contained `worktrees.convention` for issue worktrees",
            "`<feature-name>` is a runtime token",
        ):
            self.assertIn(concept, setup)

    def test_main_worktree_mapping_and_issue_layout_are_explicit(self) -> None:
        core = read(REFERENCES / "CORE.md")
        self.assertIn("## Local worktree layout\n", core)
        layout = normalized(core.split("## Local worktree layout\n", 1)[1].split("\n## ", 1)[0])
        for concept in (
            "`repos.<key>.path`",
            "Repository default branch (normally `main`)",
            "`repos.<key>.worktrees.convention`",
            "Issue task branch",
            "retained workspace root, not the current working directory",
            "Prepare or verify the main worktree from `repos.<key>.git`",
            "paths distinct and contained",
            "never switch the main worktree to an issue branch",
        ):
            self.assertIn(concept, layout)
        config = read(REFERENCES / "RESOURCE-MAP.yml")
        self.assertRegex(config, r"(?m)^    path: <main-worktree-path>$")

    def test_setup_is_explicit_in_place_and_not_a_github_workflow(self) -> None:
        setup = normalized(read(REFERENCES / "INITIALIZE.md"))
        for concept in (
            "explicit, non-read-only",
            "bundled file in place",
            "Do not create a second map",
            "Configuration is the only mutation here",
            "Do not clone",
            "enumerate board items",
            "reconcile statuses",
            "create GitHub resources",
        ):
            self.assertIn(concept, setup)

    def test_optional_configuration_does_not_become_a_stage_checklist(self) -> None:
        setup = normalized(read(REFERENCES / "INITIALIZE.md"))
        self.assertIn("Optional", setup)
        self.assertIn("only the requested entries", setup)
        self.assertIn("four distinct", setup)
        self.assertIn("interpreted by the owning skill when invoked", setup)
        self.assertIn("not authority or prerequisites for unrelated actions", setup)

    def test_initialization_requests_missing_configuration_without_steps(self) -> None:
        setup = read(REFERENCES / "INITIALIZE.md")
        self.assertEqual(re.findall(r"^## (.+)$", setup, re.M), [
            "Boundary", "Configuration model",
        ])
        model = normalized(setup.split("## Configuration model\n", 1)[1])
        self.assertIn(
            "Ask the user when any requested entries or their required values are missing",
            model,
        )
        self.assertNotRegex(setup, r"(?m)^\d+\. ")


class IndependentActionTests(unittest.TestCase):
    def test_request_boundaries_remain_in_lifecycle_and_action_guidance(self) -> None:
        guidance = normalized(read(DOCS / "README.md"))
        for concept in (
            "not a mandatory chain",
            "A direct request ends after its action",
            "Decision approval does not silently expand execution scope",
        ):
            self.assertIn(concept, guidance)
        self.assertIn(
            "Approval does not itself start implementation",
            normalized(skill("design-issue")),
        )
        self.assertNotIn("CORE's authority boundaries", read(REFERENCES / "DEV-FLOW.md"))

    def test_publication_is_not_merge_readiness_or_optional_review(self) -> None:
        publication = normalized(skill("open-pr"))
        for concept in (
            "optional self-review",
            "not publication gates",
            "explicit publication requirements",
            "draft", "pending CI",
            "not merge readiness",
        ):
            self.assertIn(concept, publication)
        self.assertNotIn(r"..\self-review\SKILL.md", publication)

    def test_implementation_does_not_require_a_design_stage(self) -> None:
        implementation = normalized(skill("implement-issue"))
        for concept in (
            "issue's scope", "task worktree", "repository instructions",
            "any approved design", "Preserve unrelated work",
        ):
            self.assertIn(concept, implementation)
        self.assertNotIn(r"..\design-issue\SKILL.md", implementation)
        self.assertNotIn("ready_to_implement", implementation)

    def test_implementation_records_finished_work_and_verification(self) -> None:
        implementation = skill("implement-issue")
        guidance = implementation.split("## Guidance\n", 1)[1].split("\n## ", 1)[0]
        self.assertEqual(len(re.findall(r"^- ", guidance, re.M)), 3)
        for concept in (
            "Verify changed behavior", "focused tests and project-required checks",
            "address failures before reporting implementation complete",
            "Once implementation is complete, post or update a GitHub issue comment "
            "headed `## IMPLEMENT`",
            "change summary, verification results", "remaining limitations",
        ):
            self.assertIn(concept, normalized(guidance))
        self.assertIn("## Output\n", implementation)
        output = normalized(implementation.split("## Output\n", 1)[1])
        for concept in (
            "failed or partial updates",
            "do not start review or publication unless requested",
        ):
            self.assertIn(concept, output)

    def test_design_records_approved_design_without_starting_implementation(self) -> None:
        design = skill("design-issue")
        guidance = design.split("## Guidance\n", 1)[1].split("\n## ", 1)[0]
        self.assertEqual(len(re.findall(r"^- ", guidance, re.M)), 3)
        for concept in (
            "in-scope design", "key decisions and tradeoffs",
            "Confirm user approval or approval within authority delegated by the request "
            "or project guidance",
            "Once approved, post or update a GitHub issue comment headed `## DESIGN`",
            "summarizing the design and key decisions",
        ):
            self.assertIn(concept, normalized(guidance))
        self.assertIn("No claim or prepared worktree is needed", normalized(design))
        self.assertIn("## Output\n", design)
        output = normalized(design.split("## Output\n", 1)[1])
        for concept in (
            "approval status", "pending decisions or failed comment writes",
            "Approval does not itself start implementation",
        ):
            self.assertIn(concept, output)
        for path in runtime_documents():
            with self.subTest(file=path.relative_to(BUNDLE)):
                self.assertNotRegex(read(path), r"## (PLAN|PROGRESS|SELF REVIEW)")

    def test_planning_changes_real_scope_not_ordinary_implementation_choices(self) -> None:
        plan = normalized(skill("plan-issues"))
        for concept in (
            "product/project roadmap",
            "An implementation approach change alone does not require planning",
            "related open and closed issues before creating new work",
            "Add, edit, or remove issues from the plan",
            "clear outcomes and acceptance criteria",
            "Preserve human content, active work, and issue history",
            "record material reasons on affected issues",
            "Raise consequential uncertainty",
            "native parent/sub-issue and blocked-by links",
            "only affected statuses",
            "read-only request returns proposals without writes",
            "Planning does not claim or implement the work",
        ):
            self.assertIn(concept, plan)
        self.assertNotRegex(plan, r"invoke `reconcile-board`")

    def test_existing_handoffs_are_evidence_not_old_workflow_commands(self) -> None:
        continuation = normalized(skill("continue-issue"))
        for concept in (
            "suggested next steps are not required stages",
            "explicit holds",
            "remaining review budget",
        ):
            self.assertIn(concept, continuation)

    def test_core_identifies_concrete_github_records(self) -> None:
        core = normalized(read(REFERENCES / "CORE.md"))
        for concept in (
            "Issue body", "Project board", "native parent/dependency links",
            "Remote task branch and PR", "Issue/PR",
            "not an activity transcript",
        ):
            self.assertIn(concept, core)


class BoardAndOwnershipTests(unittest.TestCase):
    def test_planning_and_reconciliation_have_concise_guidance_and_honest_output(self) -> None:
        for name in ("plan-issues", "reconcile-board"):
            with self.subTest(skill=name):
                body = skill(name)
                guidance = body.split("## Guidance\n", 1)[1].split("\n## ", 1)[0]
                self.assertEqual(len(re.findall(r"^- ", guidance, re.M)), 3)
                self.assertIn("## Output\n", body)
                output = normalized(body.split("## Output\n", 1)[1])
                self.assertIn("changed or proposed", output)
                self.assertIn("failed/partial updates", output)

    def test_board_updates_are_targeted_and_not_reconciler_exclusive(self) -> None:
        core = normalized(read(REFERENCES / "CORE.md"))
        project = normalized(read(SKILLS / "reconcile-board" / "references" / "PROJECT.md"))
        self.assertIn("Any acting skill may update affected board items", core)
        self.assertIn("not after every skill", core)
        self.assertIn(
            "only for board operations",
            normalized(read(REFERENCES / "DEV-FLOW.md")),
        )
        self.assertIn("Any acting skill", project)
        self.assertIn("projectItems", project)
        self.assertIn("hasNextPage endCursor", project)
        self.assertIn("four distinct", project)
        for path in runtime_documents():
            self.assertNotRegex(read(path), r"(?:alone|only this skill) updates.*status")

    def test_four_states_preserve_dependencies_waits_and_completion(self) -> None:
        project = read(SKILLS / "reconcile-board" / "references" / "PROJECT.md")
        states = set(re.findall(r"`(Backlog|Ready|In progress|Done)`", project))
        self.assertEqual(states, STATES)
        body = normalized(project)
        for concept in (
            "dependency wait has cleared",
            "retain the branch",
            "review, approval, or CI",
            "Cancellation",
            "unknown",
        ):
            self.assertIn(concept, body)
        reconcile = normalized(skill("reconcile-board"))
        self.assertIn("--read-only", reconcile)
        self.assertIn("no writes", reconcile)
        self.assertIn("all pages", reconcile)

    def test_reconciliation_scopes_reads_and_limits_mutations_to_status(self) -> None:
        reconcile = normalized(skill("reconcile-board"))
        for concept in (
            "current issue, dependency, handling, and PR facts",
            "affected issues and their blockers/dependents for a targeted request",
            "all pages for a whole-board request",
            "Report conflicting or unknown evidence rather than guessing",
            "update only changed statuses and verify saved values",
            "`--read-only` means no writes, including comments or ownership changes",
            "Reconciliation does not claim work",
        ):
            self.assertIn(concept, reconcile)

    def test_board_reference_preserves_access_boundaries_without_command_recipes(self) -> None:
        project = read(SKILLS / "reconcile-board" / "references" / "PROJECT.md")
        for concept in (
            "gh project view", "gh project field-list",
            "missing options are configuration gaps",
            "Failed or partial reads cannot establish a complete snapshot",
            "gh project item-add", "gh project item-edit",
            "verify saved values",
            "read-only requests and reference-only entries",
            "report failed/partial updates",
        ):
            self.assertIn(concept, normalized(project))
        self.assertNotIn("```", project)

    def test_native_graph_has_separate_hierarchy_and_dependency_semantics(self) -> None:
        graph = normalized(read(SKILLS / "plan-issues" / "references" / "ISSUE-GRAPH.md"))
        for concept in (
            "numeric database `id`", "dependencies/blocked_by",
            "dependencies/blocking", "state_reason=completed",
            "Hierarchy and dependency graphs are checked separately",
            "self-links and cycles", "a parent may depend on a child",
            "--paginate", "unknown, not empty",
            "not issue numbers or GraphQL node IDs",
            "POST sub_issues", "DELETE sub_issue", "sub_issue_id=<child-id>",
            "POST dependencies/blocked_by", "issue_id=<blocker-id>",
            "DELETE dependencies/blocked_by/<blocker-id>",
            "Read current links before writing", "verify changes",
            "report failed/partial updates",
        ):
            self.assertIn(concept, graph)
        self.assertNotIn("```", graph)
        self.assertIn("parent", normalized(skill("plan-issues")))

    def test_acquisition_preserves_single_handling_agent_and_existing_resources(self) -> None:
        core = normalized(read(REFERENCES / "CORE.md"))
        for concept in (
            "**handling agent**",
            "responsible for advancing an issue and changing its task branch",
            "until handoff or completion",
            "one issue at a time", "one issue worktree",
            "Only the handling agent changes the issue branch",
            "independent reviewers",
            "Read-only assessment and non-code outcomes need no worktree",
            "Complete or hand off before taking another issue",
            "continuation reuses the remote task branch",
        ):
            self.assertIn(concept, core)
        claim = normalized(skill("claim-issue"))
        for concept in (
            "existing", "conflict", "preparing", "active",
            "repository conventions", "`continue-issue`",
        ):
            self.assertIn(concept, claim)
        self.assertIn("do not bypass a claim conflict with another branch", claim)
        continuation = normalized(skill("continue-issue"))
        self.assertIn("no other active or preparing handling agent", continuation)

    def test_claim_guidance_is_eligibility_worktree_and_recording(self) -> None:
        claim = skill("claim-issue")
        guidance = claim.split("## Guidance\n", 1)[1].split("\n## ", 1)[0]
        self.assertEqual(len(re.findall(r"^- ", guidance, re.M)), 3)
        self.assertNotIn("```", claim)
        for concept in (
            "issue is open", "blocking dependencies are completed",
            "Prepare or verify the main worktree at `repos.<key>.path`",
            "Create the task branch and issue worktree",
            "from the intended base",
            "Post a GitHub issue comment headed `## CLAIM`",
            "the handling agent, branch, and base commit",
        ):
            self.assertIn(concept, normalized(guidance))
        self.assertIn("## Output\n", claim)
        output = normalized(claim.split("## Output\n", 1)[1])
        for concept in ("claim and worktree", "claim was declined", "partial setup"):
            self.assertIn(concept, output)

    def test_continuation_restores_existing_work_and_records_handling(self) -> None:
        continuation = normalized(skill("continue-issue"))
        for concept in (
            "current issue/PR state", "latest handoff",
            "conditions are met", "completed or cancelled work needs no new claim",
            "existing task branch and worktree", "remote references",
            "main worktree at `repos.<key>.path`",
            "preserving dirty or divergent work",
            "A merged PR needs only missing completion updates or cleanup",
            "not a recreated branch or worktree",
            "`## CONTINUE` issue comment", "handling agent", "branch/head",
            "`In progress` only for resumed work",
        ):
            self.assertIn(concept, continuation)
        output = normalized(skill("continue-issue").split("## Output\n", 1)[1])
        for concept in ("next action", "cannot proceed", "failed or partial updates"):
            self.assertIn(concept, output)

    def test_handoff_records_progress_before_releasing_handling(self) -> None:
        handoff = normalized(skill("handoff-issue"))
        for concept in (
            "pause or transfer", "not after every skill return",
            "current handling agent", "verify remote commits", "local-only",
            "`## HANDOFF` issue comment",
            "progress, branch/head and PR links",
            "key decisions, remaining work",
            "next action or resume condition", "remaining review budget",
            "Verify the comment is saved before releasing handling",
            "stop changing the task branch",
            "dependency waits are `Backlog`", "remain `In progress`",
            "If saving fails", "without claiming a successful handoff",
        ):
            self.assertIn(concept, handoff)

    def test_operational_waits_allow_repairs_without_overriding_holds(self) -> None:
        continuation = normalized(skill("continue-issue"))
        for concept in (
            "conditions are met or new actionable CI failures, review feedback, or "
            "queue failures permit scoped repairs despite an operational wait",
            "no other active or preparing handling agent",
            "Honor explicit holds",
        ):
            self.assertIn(concept, continuation)
        self.assertNotIn("Resume only when its conditions are met", continuation)
        handoff = normalized(skill("handoff-issue"))
        self.assertIn("Separate explicit holds from operational waits", handoff)
        self.assertIn("Pending CI alone is not a reason to hand off", handoff)
        self.assertIn("actual interruption or transfer requires release", handoff)


class ReviewAndMergeTests(unittest.TestCase):
    def test_review_is_optional_and_read_only_assessment_needs_no_claim(self) -> None:
        review = normalized(skill("self-review"))
        for concept in (
            "Read-only review needs no ownership claim",
            "whole worktree", "design",
            "independent, read-only reviewer", "uncommitted",
        ):
            self.assertIn(concept, review)
        self.assertIn(
            "not a publication or merge prerequisite",
            normalized(read(SKILLS / "self-review" / "README.md")),
        )
        self.assertFalse((SKILLS / "self-review" / "references").exists())

    def test_review_settings_bound_the_review_not_other_actions(self) -> None:
        review = normalized(skill("self-review"))
        for concept in (
            "`repos.<key>.self_review`",
            "`until_clean` (default)", "`single_pass` (report-only)",
            "Read-only requests are also report-only",
            "`max_iterations` is a positive integer, not a boolean, default 3",
            "Reject invalid settings",
            "Count all started, interrupted, and verification passes across retries "
            "and continuation",
            "Pause on unknown prior counts",
            "rather than resetting the budget",
        ):
            self.assertIn(concept, review)

    def test_review_requests_an_inclusive_severity_threshold(self) -> None:
        review = skill("self-review")
        self.assertIn("## Input\n", review)
        inputs = normalized(review.split("## Input\n", 1)[1].split("\n## ", 1)[0])
        for concept in (
            "Ask the user for the severity threshold if not supplied",
            "Low, Medium, High, or Critical, in increasing order",
            "Include the selected level and all higher levels",
        ):
            self.assertIn(concept, inputs)

    def test_review_loop_requires_current_threshold_evidence_within_cap(self) -> None:
        review = skill("self-review")
        guidance = review.split("## Guidance\n", 1)[1].split("\n## ", 1)[0]
        self.assertEqual(len(re.findall(r"^- ", guidance, re.M)), 3)
        for concept in (
            "Count findings by severity",
            "Unless report-only, address qualifying findings",
            "verify fixes",
            "Re-review after fixes until zero findings at or above the threshold remain, "
            "or the iteration cap is reached",
            "blockers, or repeated non-progress",
        ):
            self.assertIn(concept, normalized(guidance))
        self.assertIn("## Output\n", review)
        output = normalized(review.split("## Output\n", 1)[1])
        for concept in (
            "reviewed version, threshold, severity counts",
            "remaining findings",
            "Mark the target met only after a completed review of the current version "
            "confirms zero qualifying findings",
            "otherwise report the unmet target and stopping reason",
        ):
            self.assertIn(concept, output)

    def test_review_threshold_and_budget_survive_transfer(self) -> None:
        for name in ("handoff-issue", "continue-issue"):
            with self.subTest(skill=name):
                body = normalized(skill(name))
                self.assertIn("review threshold", body)
                self.assertIn("remaining review budget", body)

    def test_finding_triage_preserves_scope_and_decisions(self) -> None:
        review = normalized(skill("self-review"))
        for concept in (
            "within issue scope and project principles",
            "Raise consequential uncertainty before speculative changes",
            "keep unresolved findings counted",
        ):
            self.assertIn(concept, review)
        iteration = normalized(skill("iterate-pr"))
        for concept in (
            "selectively", "issue scope", "acceptance criteria",
            "project principles", "consequential uncertainty",
            "reasons for non-action", "Resolve only addressed threads when permitted",
        ):
            self.assertIn(concept, iteration)

    def test_pr_iteration_reviews_addresses_and_replies_within_request(self) -> None:
        iteration = skill("iterate-pr")
        guidance = iteration.split("## Guidance\n", 1)[1].split("\n## ", 1)[0]
        self.assertEqual(len(re.findall(r"^- ", guidance, re.M)), 3)
        for concept in (
            "Confirm the PR is open", "read current review comments",
            "Address findings selectively", "Verify and push fixes",
            "Reply in the review threads", "avoid duplicate replies",
        ):
            self.assertIn(concept, normalized(guidance))
        for concept in (
            "Read-only/report-only requests allow assessment, not code changes or posted replies",
            "failed or partial updates", "does not merge the PR",
        ):
            self.assertIn(concept, normalized(iteration))
        self.assertNotIn(r"..\self-review\SKILL.md", iteration)

    def test_pr_discovery_and_non_default_target_linkage(self) -> None:
        publication = normalized(skill("open-pr"))
        for concept in (
            "all PR states", "head repository/branch", "base",
            "Reuse a matching open PR", "clarify closed-unmerged matches",
            "Preserve human-authored content", "link the issue",
            "explicit cross-links for non-default targets",
        ):
            self.assertIn(concept, publication)

    def test_completion_checks_current_readiness_and_explicit_bypass(self) -> None:
        completion = normalized(skill("complete-issue"))
        for concept in (
            "PR status", "acceptance", "CI", "review requirements",
            "accounting for an explicitly requested bypass",
        ):
            self.assertIn(concept, completion)

    def test_queue_admission_and_actual_merge_are_distinct(self) -> None:
        completion = normalized(skill("complete-issue"))
        self.assertIn("`--match-head-commit <verified-head>`", completion)
        self.assertIn("Confirm actual merge", completion)
        self.assertIn("queue entry or scheduled auto-merge is pending, not completion", completion)

    def test_admin_exceptions_preserve_ci_explicit_authority_and_holds(self) -> None:
        completion = normalized(skill("complete-issue"))
        for concept in (
            "Add `--admin` only when input explicitly requests admin bypass",
            "does not waive CI or explicit holds",
            "--match-head-commit",
        ):
            self.assertIn(concept, completion)

    def test_completion_requires_pr_and_retries_only_missing_updates(self) -> None:
        completion = normalized(skill("complete-issue"))
        for concept in (
            "A missing, draft, closed-unmerged, or unready PR blocks completion",
            "If already merged, finish only missing completion updates or cleanup",
        ):
            self.assertIn(concept, completion)
        self.assertNotIn("no-PR outcome", completion)
        self.assertIn(
            "The intermediate skills are optional",
            normalized(read(REFERENCES / "DEV-FLOW.md")),
        )

    def test_completion_refreshes_native_dependencies_before_merge(self) -> None:
        completion = normalized(skill("complete-issue"))
        for concept in (
            "Immediately before merging, refresh the issue's native blocking dependencies",
            "all must be closed with `state_reason=completed`",
            "Cancelled dependencies and unknown or incomplete reads block completion",
            "admin bypass does not waive this",
        ):
            self.assertIn(concept, completion)
        self.assertLess(
            completion.index("If already merged"),
            completion.index("Immediately before merging"),
        )
        self.assertLess(
            completion.index("Immediately before merging"),
            completion.index("Merge the PR using"),
        )
        self.assertLess(
            completion.index("Immediately before merging"),
            completion.index("Close the issue with"),
        )

    def test_completion_records_merged_delivery_before_issue_status(self) -> None:
        completion = skill("complete-issue")
        guidance = normalized(completion.split("## Guidance\n", 1)[1].split("\n## ", 1)[0])
        for concept in (
            "Post or update a `## COMPLETE` issue comment",
            "delivered outcome", "linking the merged PR",
            "Close the issue with `state_reason=completed`",
            "configured board item to `Done`", "release handling",
        ):
            self.assertIn(concept, guidance)
        self.assertLess(guidance.index("Confirm actual merge"), guidance.index("Post or update"))
        self.assertLess(guidance.index("Post or update"), guidance.index("Close the issue"))
        self.assertIn("failed or partial updates", normalized(completion))

    def test_completion_cleans_only_the_delivered_worktree_after_closure(self) -> None:
        completion = normalized(skill("complete-issue"))
        for concept in (
            "After closure, work from the verified main worktree at `repos.<key>.path`",
            "Remove the exact issue worktree",
            "`git worktree remove` without `--force`",
            "only when clean and its branch/head matches the delivered PR",
            "use PR evidence for squash/rebase merges",
            "Skip absent worktrees",
            "Preserve dirty work, extra commits, and unverified worktrees",
        ):
            self.assertIn(concept, completion)
        self.assertLess(completion.index("Close the issue"), completion.index("git worktree remove"))
        self.assertNotIn("git push --delete", completion)

    def test_completion_fast_forwards_main_and_records_cleanup_separately(self) -> None:
        completion = skill("complete-issue")
        guidance = normalized(completion.split("## Guidance\n", 1)[1].split("\n## ", 1)[0])
        for concept in (
            "Fetch the configured repository's remote default branch",
            "clean, behind-only main worktree using `git merge --ff-only`",
            "Leave an up-to-date main unchanged",
            "dirty, ahead, or divergent states without resetting",
            "Record cleanup and main-update results or blockers in `## COMPLETE`, "
            "then release handling",
        ):
            self.assertIn(concept, guidance)
        self.assertLess(guidance.index("Close the issue"), guidance.index("git merge --ff-only"))
        self.assertLess(guidance.index("git merge --ff-only"), guidance.index("release handling"))
        output = normalized(completion.split("## Output\n", 1)[1])
        for concept in (
            "cleanup and main-update status separately",
            "failed or partial updates", "unavailable local worktrees",
        ):
            self.assertIn(concept, output)

    def test_completion_admin_bypass_requires_explicit_input(self) -> None:
        completion = normalized(skill("complete-issue"))
        inputs = normalized(
            skill("complete-issue").split("## Input\n", 1)[1].split("\n## ", 1)[0]
        )
        self.assertIn("explicitly request admin bypass", inputs)
        for concept in (
            "Add `--admin` only when input explicitly requests admin bypass",
            "does not waive CI or explicit holds",
            "`--match-head-commit <verified-head>`",
        ):
            self.assertIn(concept, completion)
        autopilot = normalized(skill("orchestrator-autopilot"))
        self.assertIn("pass an explicit admin-bypass request to `complete-issue`", autopilot)


class AutopilotTests(unittest.TestCase):
    def test_autopilot_separates_settings_from_concise_loop_guidance(self) -> None:
        body = skill("orchestrator-autopilot")
        guidance = body.split("## Guidance\n", 1)[1].split("\n## ", 1)[0]
        self.assertEqual(len(re.findall(r"^- ", guidance, re.M)), 4)
        self.assertIn("## Input\n", body)
        inputs = normalized(body.split("## Input\n", 1)[1].split("\n## ", 1)[0])
        for concept in (
            "`repos.<key>.autopilot`",
            "operation's repository, including the PR repository",
            "A read-only request returns a snapshot without claims or writes",
        ):
            self.assertIn(concept, inputs)
        self.assertIn("## Output\n", body)
        output = normalized(body.split("## Output\n", 1)[1])
        for concept in (
            "drained, paused, and read-only snapshot", "failed/partial updates",
            "On interruption, hand off owned work where possible and report anything unsaved",
        ):
            self.assertIn(concept, output)

    def test_autopilot_chooses_actions_instead_of_following_stages(self) -> None:
        body = normalized(skill("orchestrator-autopilot"))
        for concept in (
            "explicit request", "same agent", "one issue at a time",
            "do not delegate issue delivery",
            "Choose the next useful action",
            "not a fixed sequence",
            "Design and self-review are optional unless required",
            "Raise consequential uncertainty",
            "review's scope, report-only mode, threshold, and remaining budget",
        ):
            self.assertIn(concept, body)
        self.assertIn("Prefer existing actionable work", body)
        self.assertIn("Use `claim-issue` for new unblocked work", body)
        self.assertIn("`continue-issue` for existing work", body)
        self.assertIn(
            "Finish through `complete-issue` or `handoff-issue` before selecting another issue",
            body,
        )
        self.assertNotIn("consume `not_ready`", body.lower())

    def test_autopilot_modes_are_optional_but_do_not_imply_unbounded_authority(self) -> None:
        body = normalized(skill("orchestrator-autopilot"))
        for concept in (
            "`reasonable-approval` (default)", "`auto-approval`",
            "request/manifest delegation",
            "normal GitHub approvals/queues, with no admin bypass",
            "authorized review/queue exceptions",
            "this explicit run", "PR repository",
            "Neither mode waives CI or explicit holds",
            "Never fabricate human approval",
            "Reject unsupported modes or invalid settings",
        ):
            self.assertIn(concept, body)
        for name in ACTIVE - {"orchestrator-autopilot"}:
            self.assertNotRegex(skill(name), r"auto-approval|reasonable-approval")

    def test_ci_only_wait_retains_handling_without_a_configuration_switch(self) -> None:
        body = normalized(skill("orchestrator-autopilot"))
        for concept in (
            "observable pending CI as the sole remaining gate",
            "one attached CI watcher without a configured timeout",
            "retain owned handling", "keep owned work `In progress`",
            "Do not hand off or select another issue for a CI-only wait",
            "Observe released work read-only",
            "Stop and reassess on completion, failure, interruption, or changed head/base",
            "actionable failures return to scoped repair",
            "Unknown CI and merge-queue waits need their actual resolution, not a CI watcher",
            "Waiting grants no merge permission",
        ):
            self.assertIn(concept, body)
        self.assertNotIn("wait_for_ci", body)
        self.assertNotIn("wait_for_ci", read(REFERENCES / "RESOURCE-MAP.yml"))

    def test_stopping_uses_fresh_evidence_not_an_empty_ready_lane(self) -> None:
        body = normalized(skill("orchestrator-autopilot"))
        for concept in (
            "all pages of the requested board scope",
            "PR repairs and cleanup",
            "Refresh affected facts",
            "do not take over another handling agent",
            "stop on uncertain ownership or failed persistence",
            "do not repeat actions for unchanged waits",
            "Drained requires a fresh, complete view",
            "no actionable work, active/preparing handling agent, or actionable cleanup",
            "An empty Ready lane, unknown state, or incomplete reads cannot establish it",
        ):
            self.assertIn(concept, body)


if __name__ == "__main__":
    unittest.main()
