# Structured Communication for Software Agents

**Status:** Research synthesis and design direction
**Evidence reviewed through:** 16 September 2026

## Executive conclusion

Difficulty understanding, validating, and resuming AI-assisted software work is
a documented recurring issue. The literature does not support a population
estimate such as "most developers have this problem," because studies use
different tools, tasks, populations, and definitions of understanding.

Two properties must be separated:

1. **Operational coherence:** whether the agent forms an adequate task and
   system model, controls its work, and supports its conclusions with evidence.
2. **Human-facing structure:** whether a reader can efficiently reconstruct
   the outcome, rationale, evidence, uncertainty, and current state.

They produce four importantly different cases:

| Operational work | Human presentation | Likely experience |
|---|---|---|
| Coherent | Structured | Understandable and auditable, though not necessarily correct |
| Coherent | Unstructured | Competent work that feels opaque |
| Incoherent | Structured | Most dangerous: persuasive, organized confabulation |
| Incoherent | Unstructured | Obvious failure |

This document organizes the causes into five layers:

1. grounding and task contract;
2. system/task model and solution formation;
3. planning and control;
4. verification and epistemic integrity;
5. externalization and interface structure.

These layers are a useful synthesis, not a validated mutually exclusive and
collectively exhaustive taxonomy. A failure can span multiple layers or
propagate from one layer to another. Directability and repair are treated as a
cross-cutting interaction property because users may need to correct any layer.

The repository direction is to investigate whether small, on-demand Agent
Skills can improve communication at human-agent boundaries, particularly
grounding and human-facing externalization. Truthful evidence status may be an
important safeguard against making unsupported work more persuasive.

This is a research and design direction, not a settled skill design. This
document does not determine the number of skills, their names, activation
rules, templates, interaction flow, or exact content. The five-layer model is
diagnostic background for future experiments rather than a prescribed agent
procedure.

## Scope and terminology

Here, **legibility** means that a human can, at acceptable cost:

- reconstruct the task and success criteria;
- understand the relevant system model and proposed change;
- determine the current plan, state, and available control points;
- distinguish observation from inference, assumption, and unsupported claim;
- locate source artifacts and resume or hand off the work.

Legibility is not equivalent to correctness, model interpretability, fluent
prose, user trust, preference, visible chain-of-thought, or passing one test
suite.

The evidence below is labeled implicitly by source type:

- **Direct human-AI evidence:** people using or reviewing AI programming tools.
- **Agent or benchmark evidence:** automated traces and outcomes; relevant to
  agent behavior, but not direct evidence of human comprehension.
- **Indirect human-factors or software-engineering evidence:** related causal or
  observational evidence outside coding-agent use.
- **Normative or practice evidence:** standards, templates, and official
  guidance; useful design input, but not proof of efficacy.

## Is the experience common?

### Best-supported claim

> Difficulty understanding, controlling, validating, and repairing
> AI-assisted software work is a recurring documented issue. Existing evidence
> does not establish how prevalent it is across the full developer population.

Evidence comes from several methods and populations:

| Study | Design | Relevant finding | Important limitation |
|---|---|---|---|
| [Vaithilingam, Zhang, and Glassman, CHI EA 2022](https://doi.org/10.1145/3491101.3519665) | Controlled within-subject study, N=24 | No statistically significant completion-time or success improvement was detected, although 19/24 participants preferred Copilot. Understanding, editing, and debugging generated code were recurring obstacles. | Brief laboratory tasks and an early Copilot version. Preference is not comprehension or productivity. |
| [Barke, James, and Polikarpova, OOPSLA 2023](https://doi.org/10.1145/3586030) | Qualitative study, N=20 | Identified acceleration and exploration modes. Longer or multiple suggestions could support exploration but also disrupt flow and create cognitive overload. | Researcher-defined tasks and a mostly academic sample; no prevalence estimate. |
| [Mozannar et al., CHI 2024](https://doi.org/10.1145/3613904.3641936) | Behavioral study, N=21, 3,137 labeled coding segments | Thinking about or verifying a suggestion averaged 22.4% of session time. All Copilot-specific states together averaged 51.5%. | Small controlled sample and retrospective labeling. Time spent is a cost, not proof that the time was wasted. |
| [Liang, Yang, and Myers, ICSE 2024](https://doi.org/10.1145/3597503.3608128) | Survey, N=410 from 10,530 invitations | Among respondents, 30% often did not know which input influenced output, 28% often gave up on output, and 26% often had difficulty controlling the tool. Task mismatch, debugging burden, and inability to understand code also affected use. | Approximately 4% response rate, self-selection and recall bias, and varying denominators. Results cannot be generalized to all developers. |
| [Prather et al., TOCHI 2023](https://doi.org/10.1145/3617367) | Observational study, N=19 novice programmers | Observed "shepherding," where users repeatedly tried to coerce the assistant, and "drifting," where suggestions drove the solution without stable user understanding. | Introductory C++ students, one course, and no professional maintenance setting. |
| [Tang et al., VL/HCC 2024](https://doi.org/10.1109/VL/HCC60511.2024.00015) | Randomized study, N=28, with eye tracking and IDE telemetry | Developers often failed to recognize AI provenance. Disclosing provenance changed search, validation, and repair behavior, but increased cognitive workload. | Small tasks and code fragments; disclosure may induce unusual vigilance. |
| [Nam et al., ICSE 2024](https://doi.org/10.1145/3597503.3639187) | Controlled study, N=32 | Contextualized LLM assistance increased completed subtasks, but the study detected no significant improvement in completion time or code-understanding scores. | One prototype, unfamiliar Python APIs, and a limited comprehension measure. |
| [Epperson et al., CHI 2025](https://doi.org/10.1145/3706598.3713581) | Formative interviews and two small user studies | Participants described 50-100+ message agent logs as cumbersome. In one study, participants spent about ten of fifteen minutes reading before editing and valued edit/reset affordances. | Very small samples, two GAIA tasks, and no demonstrated correctness improvement in the first study. |

The evidence triangulates a recurring issue:

- controlled studies identify comprehension and verification cost;
- surveys report task mismatch, opacity, and poor control;
- observations show unstable steering and understanding;
- provenance studies show that users change verification behavior when they
  know work is AI-generated;
- agent studies show specification, coordination, planning, and verification
  failures even when no human-comprehension measure is collected.

Positive productivity results do not contradict this conclusion. AI assistance
can improve speed or throughput on some bounded tasks while still imposing
comprehension, review, maintenance, or handoff costs. Productivity,
correctness, preference, confidence, and understanding must be measured
separately.

## The five-layer model

The layers follow the transformation of work:

> task intent -> working model -> controlled action -> justified claim ->
> human-facing representation

An upstream defect can propagate through the remaining layers. For example, an
underspecified task can produce the wrong system model, which drives a coherent
but irrelevant plan, which is validated against inadequate criteria, and is
then presented as a convincing success.

### Layer 1: Grounding and task contract

#### Failure mechanism

The agent acts on the context visible to it, while the human may assume
unstated repository knowledge, architectural boundaries, risk tolerances, or
non-functional requirements. The two parties may use the same words with
different meanings or disagree about what constitutes completion.

Typical signatures include:

- solving the wrong issue, repository, branch, or component;
- satisfying the literal request while violating tacit compatibility,
  performance, security, or operational requirements;
- treating an example as a complete requirement;
- following stale or conflicting instructions;
- changing out-of-scope files;
- declaring success without agreed acceptance evidence.

#### Evidence and research traditions

This layer connects requirements engineering, conversational common ground,
intent elicitation, task specification, context provenance, and ambiguity
detection.

[Liang et al.](https://doi.org/10.1145/3597503.3608128) found task mismatch,
poor control, and uncertainty about which inputs influenced generated output.
In a manual examination of SWE-bench Lite,
[Agentless](https://doi.org/10.1145/3715754) reported that some task
descriptions omitted critical information or contained misleading proposed
solutions. This demonstrates that the apparent task contract can itself be
defective.

[ISO/IEC/IEEE 29148:2018](https://standards.ieee.org/standard/29148-2018.html)
defines useful requirements properties such as necessity, completeness,
unambiguity, feasibility, verifiability, consistency, and traceability. It is
a normative standard, not evidence that one particular prompt template works.

#### Existing attempts

- task briefs with goal, scope, non-goals, constraints, and definition of done;
- acceptance-criteria and requirement-to-test traceability;
- clarification before consequential or irreversible work;
- repository manifests and instruction-precedence rules;
- provenance showing which files, instructions, and observations support a
  requirement;
- automated requirements-smell checks;
- context retrieval scoped to the current task rather than indiscriminate
  context expansion.

A minimal task contract is:

```text
Goal and user-visible outcome
Repository, branch, component, and environment
In scope and explicitly out of scope
Functional and non-functional constraints
Acceptance checks and definition of done
Known facts and their sources
Assumptions and unresolved questions
Risk or destructive-action level
Decisions requiring human authority
```

#### Limitations

A contract cannot automatically recover tacit organizational knowledge. A
detailed but incorrect contract can anchor all later work. More context is not
always better: models use information in long contexts unevenly
([Liu et al., "Lost in the Middle," TACL 2024](https://doi.org/10.1162/tacl_a_00638)).
Automated ambiguity detection is also imperfect; one industrial and academic
evaluation of requirements smells reported average precision of 59% and recall
of 82%
([Femmer et al., JSS 2017](https://doi.org/10.1016/j.jss.2016.02.047)).

### Layer 2: System/task model and solution formation

#### Failure mechanism

The agent or reviewer lacks an accurate causal and architectural model of the
system. A patch can be locally plausible while relying on the wrong
understanding of control flow, data flow, responsibilities, invariants, or
stakeholder intent.

Typical signatures include:

- fixing the symptom rather than the cause;
- omitting callers, consumers, configuration, or compatibility effects;
- describing control flow without understanding the system purpose;
- inventing rationale for legacy behavior;
- selecting a familiar design that conflicts with repository architecture;
- being unable to predict behavior under a new input.

#### Evidence and research traditions

This layer draws on program comprehension, mental-model construction,
architecture recovery, causal debugging, program slicing, information
foraging, change-impact analysis, and design rationale.

[Pennington's program-comprehension work](https://doi.org/10.1016/0010-0285%2887%2990007-7)
distinguishes a procedural program model from a goal- and domain-oriented
situation model. [LaToza and Myers](https://doi.org/10.1145/1937117.1937125)
surveyed 179 professional developers and found recurring hard-to-answer
questions about intent, rationale, causality, history, and safe change impact.

AI assistance does not automatically solve this problem.
[Nam et al.](https://doi.org/10.1145/3597503.3639187) found more completed
subtasks without a detected code-understanding improvement. In a study of code
summaries, participants using human-written summaries performed significantly
better than those using machine summaries even though perceived quality did
not reveal the difference
([Stapleton et al., ICPC 2020](https://doi.org/10.1145/3387904.3389258)).

#### Existing attempts

- component, dependency, data-flow, and change-impact maps;
- explicit invariants and interface contracts;
- architecture recovery and repository navigation tools;
- program slicing, runtime traces, and causal "why/why-not" debugging;
- assumption tables with source and confidence;
- hypothesis -> observation -> discriminating-check records;
- alternatives linked to explicit decision drivers;
- code-anchored explanations rather than detached narratives.

These should be decision artifacts, not transcripts of private model
reasoning.

#### Limitations

Generated maps and rationales can be confidently wrong. Additional detail can
hide the dependency that matters. A summary can make an incorrect mental model
more memorable. Requiring a full architecture model for every localized change
adds cost and may burden experts without improving outcomes.

### Layer 3: Planning and control

#### Failure mechanism

Long-running work is a control problem: each action changes the repository and
the evidence available for later decisions. Errors compound when the plan is
not updated from observations or when humans cannot intervene at meaningful
boundaries.

Typical signatures include:

- repetitive searches or tool calls;
- premature implementation;
- broad edits without impact assessment;
- mismatch between stated plan and actual actions;
- continuing after decisive failure evidence;
- silently changing strategy;
- premature termination or failure to recognize completion;
- long logs with no inspectable current state.

#### Evidence and research traditions

Relevant areas include planning and replanning, execution monitoring,
supervisory control, mixed initiative, adjustable autonomy, hierarchical task
decomposition, state machines, checkpointing, and rollback.

[Prather et al.](https://doi.org/10.1145/3617367) observed shepherding and
drifting. The MAST taxonomy found repeated steps, context loss,
reasoning-action mismatch, ignored information, and premature termination in
multi-agent traces
([Cemri et al., NeurIPS 2025](https://arxiv.org/abs/2503.13657)).
That is agent-trace evidence, not a direct measure of human legibility.

Several systems attempt to improve control:

- [Plan-and-Solve](https://doi.org/10.18653/v1/2023.acl-long.147) separates
  planning from execution.
- [ReAct](https://arxiv.org/abs/2210.03629) alternates proposed action with
  external observation.
- [CodePlan](https://doi.org/10.1145/3643757) uses dependency-aware,
  change-impact planning for repository tasks.
- [SWE-agent](https://arxiv.org/abs/2405.15793) demonstrates that the
  agent-computer interface materially changes automated repair performance.
- [Agentless](https://doi.org/10.1145/3715754) uses a constrained
  localization -> repair -> validation pipeline and showed that more autonomous
  planning is not inherently better.

These are mainly benchmark results; they do not establish that a human can
understand the resulting trajectory.

#### Existing attempts

- short, editable milestone plans;
- explicit next action and current hypothesis;
- expected changed-file or affected-component lists;
- time, tool, and change budgets;
- checkpoints after risky steps;
- stop, ask, escalate, and rollback conditions;
- state machines and durable handoff state;
- visible plan revisions when evidence changes.

#### Limitations

A plausible plan is not proof of correct execution. Detailed plans can anchor
the agent to an early misunderstanding, consume context, and impede adaptation.
Checkpoints add latency. A useful plan must be provisional and cheap to revise,
not a script that survives disconfirming evidence.

### Layer 4: Verification and epistemic integrity

#### Failure mechanism

The agent may select favorable tests, misread results, confuse absence of
failure with correctness, or narrate checks that were not run. The human must
then determine which claims are supported and whether the evidence is
sufficient.

Typical signatures include:

- "tests pass" without command, scope, environment, or exit status;
- testing only the changed happy path;
- accepting a flawed test oracle;
- self-review that restates the original rationale;
- unsupported confidence;
- concealing failed or skipped checks;
- treating inference as observation;
- syntactically polished but insecure code.

#### Evidence and research traditions

This layer includes verification and validation, test-oracle quality,
provenance, assurance cases, scientific falsification, calibrated trust,
appropriate reliance, and automation bias.

Verification is already a substantial user cost:
[Mozannar et al.](https://doi.org/10.1145/3613904.3641936) measured suggestion
verification at 22.4% of session time. Security studies found vulnerable output
and confidence mismatches in bounded tasks
([Pearce et al., IEEE S&P 2022](https://doi.org/10.1109/SP46214.2022.9833571);
[Perry et al., CCS 2023](https://doi.org/10.1145/3576915.3623157)).

Explanations do not automatically create appropriate reliance:

- explanations can increase agreement with both correct and incorrect advice
  without improving team performance
  ([Bansal et al., CHI 2021](https://doi.org/10.1145/3411764.3445717));
- cognitive-forcing interventions can reduce overreliance but also reduce
  liking and trust
  ([Bucinca et al., CSCW 2021](https://doi.org/10.1145/3449287));
- explanations help most when they make verification meaningfully cheaper or
  incentives justify scrutiny
  ([Vasconcelos et al., CSCW 2023](https://doi.org/10.1145/3579605)).

External feedback is more credible than unsupported introspection.
Feedback-free self-correction can degrade reasoning
([Huang et al., ICLR 2024](https://arxiv.org/abs/2310.01798)), while execution
or test feedback improved code generation in self-debugging benchmarks
([Chen et al., ICLR 2024](https://arxiv.org/abs/2304.05128)).

#### Existing attempts

- exact command, scope, environment, exit status, and artifact capture;
- requirement-to-test and claim-to-evidence traceability;
- canonical regression and acceptance tests;
- independently authored or hidden tests;
- static analysis, type checking, dependency and security checks;
- property, metamorphic, fuzz, and mutation testing where appropriate;
- independent human or tool review rather than same-agent repetition;
- explicit `observed`, `inferred`, `assumed`, `failed`, `skipped`, and `unknown`
  states;
- preservation of failed checks and counterevidence.

A minimal evidence record is:

| Claim | Source/check | Result | Scope/environment | Residual uncertainty |
|---|---|---|---|---|
| Regression is fixed | Exact test identifier and command | Exit code and relevant count | Commit, runtime, and configuration | Untested integration paths |

[NIST SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final) separately
recommends reviewing human-readable code and testing executable code, supporting
defense in depth rather than reliance on a single oracle.

#### Limitations

Tests can be incomplete, flaky, contaminated, or overfit. More verification
activity is not itself evidence of higher correctness. Same-model review is
not fully independent. Provenance disclosure and cognitive forcing can
increase workload. A polished evidence summary can itself create automation
bias unless the source artifacts remain inspectable.

### Layer 5: Externalization and interface structure

#### Failure mechanism

Agent work commonly appears as a chronology of messages, tool calls, partial
hypotheses, and edits. Humans instead need a task-oriented representation of
the current result and its relationships.

Typical signatures include:

- a raw chronological log without an outcome overview;
- rationale separated from the affected code;
- no requirement -> change -> test mapping;
- status claims without source evidence;
- hidden assumptions or unresolved failures;
- excessive explanation that increases search cost;
- a concise but false summary with no drill-down;
- one presentation depth imposed on novices and experts alike.

#### Evidence and research traditions

Relevant fields include external and distributed cognition, cognitive load,
information foraging, signaling, progressive disclosure, software
visualization, traceability, design rationale, and expertise reversal.

Direct evidence includes:

- Ivie's concise explanations anchored to generated code improved
  comprehension-question correctness from 65.0% to 90.2% in its controlled
  study
  ([Yan et al., CHI 2024](https://doi.org/10.1145/3613904.3642239)).
- Live runtime values reduced several workload dimensions on one programming
  task but not another, demonstrating task dependence
  ([Ferdowsi et al., CHI 2024](https://doi.org/10.1145/3613904.3642495)).
- Professional analysts combined explanations and code with intermediate
  tables and visualizations when deciding both what the AI did and whether the
  result made sense
  ([Gu et al., CHI 2024](https://doi.org/10.1145/3613904.3642497)).
- Edit, reset, and history-navigation affordances were valued in the small
  AGDebugger studies
  ([Epperson et al., CHI 2025](https://doi.org/10.1145/3706598.3713581)).

More transparent or structured information is not automatically better.
Transparent simple models improved prediction simulation but not beneficial
reliance and sometimes impaired correction of large errors
([Poursabzi-Sangdeh et al., CHI 2021](https://doi.org/10.1145/3411764.3445315)).
Guidance that helps novices can also become redundant or disruptive for experts
([Kalyuga et al., 2003](https://doi.org/10.1207/S15326985EP3801_4)).

#### Existing attempts

- outcome-first status cards;
- progressive disclosure from summary to working model to raw artifacts;
- code-anchored explanations and inline provenance;
- change maps organized by component and rationale;
- acceptance-criterion -> change -> evidence traceability;
- visualized intermediate state and runtime values;
- filters, search, collapse, and details on demand;
- terse and expanded views for different expertise levels;
- edit, reset, rollback, and history navigation;
- handoff and resumption packets.

A useful presentation order is:

1. outcome and current status;
2. changed components and why;
3. acceptance-criteria coverage;
4. verification evidence;
5. assumptions, risks, and unresolved questions;
6. optional decisions, detailed logs, and full diffs;
7. exact state and next safe action for handoff.

The critical structure is **claim -> evidence -> source artifact**, not merely
"put the summary first."

#### Limitations

Formatting cannot make a false claim true. A polished hierarchy can hide
uncertainty and discourage scrutiny. Too little detail prevents verification;
too much raises search and working-memory costs. Readability and preference
must not substitute for behavioral comprehension and error detection.

## Cross-cutting property: directability and repair

Directability is the user's ability to redirect work. Repair is how the user
and agent recover from a mismatch. They apply to every layer:

| Layer | Example repair |
|---|---|
| Grounding | Correct scope, constraints, priority, or definition of done. |
| System/task model | Challenge an assumption, provide architecture knowledge, or choose an alternative. |
| Planning/control | Pause, narrow, reorder, budget, undo, or terminate work. |
| Verification | Reject an oracle, request stronger evidence, or reopen a claimed success. |
| Externalization | Request more or less detail or navigate to the source artifact. |

This framing follows mixed-initiative and human-AI interaction research.
[Amershi et al.'s 18 guidelines](https://doi.org/10.1145/3290605.3300233),
validated with 49 practitioners across 20 products, include making capabilities
clear and supporting invocation, dismissal, correction, feedback, and global
control.

Directability should be measured through correction uptake, repeated
corrections, rollback success, plan divergence after intervention, residual
misunderstanding, and recovery after a changed requirement or interrupted
session.

## Agent Skill research direction

Agent Skills are a possible delivery mechanism for improving structured
communication. The working hypothesis is that skills focused on observable
human-agent interaction may be less intrusive than instructions that prescribe
how an agent should reason, decompose, plan, or implement.

This hypothesis does not imply a specific skill count or design. Candidate
intervention areas include:

- making the agent's interpretation visible early enough for a user to detect,
  correct, or cancel grounding drift;
- organizing available outcomes and supporting information so a user can
  understand, review, and resume the work;
- communicating the status and provenance of evidence without inventing or
  overstating validation;
- supporting correction, cancellation, expansion, and other repair actions at
  useful interaction boundaries.

These are problem areas to investigate, not required skill responsibilities or
output sections. They may eventually be addressed by one skill, several
skills, another instruction mechanism, interface support, or some combination.

### Relationship to the five layers

Layers 1 and 5 are promising places to begin because they directly concern
human-agent interaction. Layer 4 may supply safeguards for communicating what
is known, inferred, tested, or unknown. This does not settle whether those
concerns should be combined or separated in an implementation.

Layers 2 and 3 remain relevant to overall legibility, but future models may
internalize more generic decomposition, planning, and self-monitoring
capability. Prescribing those processes in a communication skill risks
duplicating model behavior or conflicting with the way a model performs a
task. By contrast, a model cannot internalize the current user's unstated
priorities, newly observed repository state, or the social need for a shared
and auditable understanding.

The boundary is not absolute. Future experiments may find that a small
external artifact from layers 2 or 3 improves communication without harming
task performance. The purpose of this direction is to avoid assuming that
result in advance.

### Does scaffolding interfere with model reasoning?

A skill adds tokens, constraints, examples, and precedence relationships. It
changes the conditional task presented to the model, and that can help or hurt:

- instruction-following performance declines as heterogeneous constraints
  accumulate
  ([FollowBench, ACL 2024](https://doi.org/10.18653/v1/2024.acl-long.257));
- meaning-preserving prompt-format changes can produce large performance
  differences in some settings
  ([Sclar et al., ICLR 2024](https://arxiv.org/abs/2310.11324));
- long instructions can dilute important information because long-context use
  is position-sensitive;
- fixed plans can anchor an early mistake;
- a forced visible chain-of-thought can be unfaithful
  ([Turpin et al., NeurIPS 2023](https://arxiv.org/abs/2305.04388)).

Scaffolding can also improve outcomes when it supplies missing state, a better
action interface, or external feedback. The effect is therefore a
**task-model-prompt interaction**, not suppression of a fixed latent reasoning
ability.

A 2026 preprint directly testing coding-agent skills found no statistically
significant benefit from personalized skills and only a suggestive,
non-significant improvement from generic pooled skills. Generic skills also
increased tokens, tool calls, elapsed time, changed files, patch churn, and
validation activity
([Huang, Du, and Lan, 2026](https://arxiv.org/abs/2608.10319)). Its 13
developers, 42 held-out tasks, simulated follow-ups, and LLM judging materially
limit generalization. It is useful evidence against assuming that persistent
instructions automatically improve an agent.

### Provisional design principles

Future prototypes should be:

- small, on demand, and model-agnostic;
- focused on observable communication rather than private cognition;
- adaptive to task risk, complexity, and user expertise;
- explicit about uncertainty and available evidence;
- easy for a user to correct, bypass, or dismiss;
- free of duplicated repository instructions;
- evaluated through ablation rather than adopted on intuition alone.

Future prototypes should avoid requiring:

- private chain-of-thought or a verbatim reasoning transcript;
- a fixed exhaustive reasoning recipe;
- commentary on every tool call;
- a system map, decision analysis, or multi-step plan solely to satisfy a
  communication format;
- extra implementation or validation solely to make a report look complete;
- unsupported confidence or claims that an action occurred when it did not.

These principles are provisional constraints on experimentation, not settled
skill content.

### Open design questions

The following decisions remain intentionally open:

- whether skills are the right mechanism at all;
- how many skills, if any, should exist;
- which communication moments warrant intervention;
- whether invocation should be explicit, automatic, risk-based, or mixed;
- when an intervention should pause for user input;
- what information is essential versus optional;
- whether any stable output schema is helpful or overly rigid;
- how presentation should adapt to novices and experts;
- how evidence provenance should be represented;
- how skills should interact with repository instructions and product-level
  interfaces;
- whether scripts, templates, or supporting references add enough value to
  justify their context and maintenance cost;
- what names and activation descriptions accurately delimit the final
  behavior.

The [Agent Skills specification](https://agentskills.io/specification)
establishes a possible packaging mechanism with `SKILL.md` and optional
resources. It does not establish that skills are the best intervention or that
any particular skill improves outcomes.

## Evaluation direction

No fixed experimental design should be selected before concrete prototypes
exist. Candidate interventions should be evaluated independently and in
combination where appropriate, using ordinary agent behavior as the control
rather than an intentionally degraded baseline.

Useful study patterns include:

- introducing plausible grounding misunderstandings and measuring whether an
  intervention helps users detect and correct them before costly work;
- presenting the same underlying trajectory and evidence in different forms to
  isolate communication effects from changes in agent behavior;
- running end-to-end ablations to detect changes in task performance, context
  use, interaction cost, and user behavior;
- including plausible but incorrect work to test whether structure improves
  error discrimination or merely increases acceptance.

Relevant measures include:

- task correctness and acceptance-criteria coverage;
- detection, correction, or cancellation of material grounding drift;
- behavioral comprehension and teach-back accuracy;
- time to locate status, evidence, uncertainty, and rationale;
- appropriate reliance on correct and incorrect work;
- confidence calibration;
- confirmation, reading, verification, token, and tool cost;
- correction uptake and recovery after changed requirements;
- handoff and delayed-resumption performance;
- workload and novice/expert interactions.

Adoption should depend on demonstrated improvement in human understanding or
control without unacceptable loss of task performance, context efficiency, or
appropriate skepticism. Preference and polished output alone are insufficient.

## Claims to avoid

- The five layers are not proven to be MECE.
- MECE formatting and the Pyramid Principle have not been shown to improve
  coding-agent comprehension or error detection in controlled studies.
- Skeleton-of-Thought primarily provides latency and answer-quality evidence,
  not evidence of better human mental models
  ([Ning et al., ICLR 2024](https://arxiv.org/abs/2307.15337)).
- Visible chain-of-thought is not necessarily a faithful explanation.
- More explanation, more agents, and more planning are not inherently better.
- Passing tests does not prove correctness when the oracle is incomplete.
- User preference, confidence, or acceptance does not prove productivity,
  correctness, or understanding.
- Benchmark success does not imply that a human can review, maintain, or hand
  off the work.
- Persistent or personalized skills are not yet proven to improve coding-agent
  outcomes reliably.

## Repository position

> Investigate whether on-demand Agent Skills can improve communication between
> agents and humans, especially around grounding, externalization, and truthful
> evidence status, without prescribing how an agent reasons. Keep the number,
> boundaries, activation model, and content of any skills open until prototypes
> are evaluated. Fluent structure, self-review, passing tests, user preference,
> and benchmark success remain insufficient evidence of correctness or
> understanding.
