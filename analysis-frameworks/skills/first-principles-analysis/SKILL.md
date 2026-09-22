---
name: first-principles-analysis
description: Interpret foundational claims in human- or agent-authored proposals, explanations, and designs using the axiomatic method as a framework. Distinguish definitions, premises, inherited choices, and deductive consequences without treating assumptions as facts or prescribing the agent's reasoning process or output format.
---

# First-Principles Analysis

## Purpose

**The axiomatic method** provides this skill's foundation: starting premises
and inference rules are distinguished from the consequences derived from them.
Applied to a proposal, this structure makes its foundations and dependencies
inspectable, including whether an inherited design choice is actually necessary.

This is a bounded interpretation of first-principles analysis, not a claim that
the phrase names one standardized engineering or innovation algorithm. Formal
axioms and empirical starting assumptions do not have the same epistemic status.

## Core model

- **Primitive concepts and definitions:** the objects and meanings used in the
  model. Defining a term does not establish a fact about the world.
- **Foundational premises:** propositions accepted as starting points rather
  than derived within this model. Their status as premises does not establish
  their truth or make them universally fundamental.
- **Inference rules:** what licenses a conclusion from the premises, distinct
  from evidence for the premises themselves.
- **Derived consequences:** conclusions that follow deductively if the
  premises hold and the inferences are valid.
- **Interpretation:** how the model's concepts and assumptions correspond to
  the subject being examined, including its domain and limits.

The relevant distinction is between what the explanation assumes and what it
establishes from those assumptions, not between familiar and novel ideas.

## What makes the analysis informative

- **Premise status:** definitions, empirical evidence, laws within their domain,
  provisional assumptions, and stakeholder requirements remain distinguishable.
  Goals and preferences are not deduced from physical facts alone.
- **Necessity versus convention:** "we have always used this design" does not
  establish that the design is required. A necessary constraint is not a
  sufficient design; feasibility does not establish optimality or uniqueness.
- **Noncircular support:** the desired conclusion is not hidden in a premise
  and then presented as independently established. Calling something a
  principle supplies no additional justification.
- **Conditional scope:** uncertainty and omitted conditions remain visible.
  A valid derivation within a model does not establish that the model applies
  to the actual system.

## Example

A proposal selects a database because similar products use it. Its hypothetical
workload is 1,000 distinct records per day, each with an uncompressed payload of
2 KiB, retained for 30 days.

Under those assumptions, a full retention window contains
`1,000 x 30 x 2 = 60,000 KiB` of uncompressed payload, before indexes,
replication, or other overhead. This derived quantity helps characterize the
need independently of the borrowed implementation. It neither selects a
database nor validates the workload estimates.

The workload figures remain assumptions unless supported; correct arithmetic
does not turn them into first principles about the real system.

## Boundaries

Breaking a problem into smaller parts is not by itself a derivation from first
principles. Analogy, prior evidence, and existing solutions can still be useful.
Questioning a design choice does not authorize discarding binding requirements
or rebuilding a system outside the task's scope.

No formal proof, reasoning transcript, or fixed agent reasoning sequence is
required to explain or review this framework. Preserve author intent and
uncertainty. Missing support stays missing rather than being replaced by
invented axioms; empirical claims and proposed designs still need validation.

## Foundation

[Encyclopedia of Mathematics, Axiomatic method](https://encyclopediaofmath.org/wiki/Axiomatic_method).
[Stanford Encyclopedia of Philosophy, Aristotle's Logic](https://plato.stanford.edu/entries/aristotle-logic/) discusses first principles and demonstration.
