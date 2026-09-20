---
name: causal-analysis
description: Interpret causal claims in human- or agent-authored explanations, incident reports, and proposals using causal directed acyclic graphs. Make variables, causal assumptions, confounding, mediation, and selection effects understandable without prescribing the agent's reasoning process or output format.
---

# Causal Analysis

## Purpose

**Causal directed acyclic graphs (DAGs)** provide this skill's foundation.
They represent assumptions about causal relationships, distinguishing an
explanation of what produces an outcome from a description of what accompanies
it. This is a bounded graphical framework, not every method of causal analysis.

For a reader, its value is making the proposed causal structure and its
alternatives inspectable, including assumptions hidden in an apparently
straightforward explanation.

## Core model

- **Variable:** a property that can take different values, with a defined
  subject, context, and time frame.
- **Directed edge:** an assumed direct causal influence, relative to the
  variables included in the model. An arrow is not merely an association.
- **Causal path:** a chain such as `X -> M -> Y`; `M` mediates influence
  along that path.
- **Common-cause path:** a fork such as `X <- Z -> Y`; `Z` can account for
  an association between `X` and `Y` without `X` causing `Y`.
- **Collider:** a common effect, as in `X -> C <- Y`. Conditioning on that
  effect, including selecting cases by it, can introduce an association.

A DAG has no directed cycles. Feedback needs time-indexed variables or a
different model, not a cycle silently added to a DAG.

## What makes the explanation informative

- **A clear causal question:** setting a variable independently of its usual
  causes differs from selecting cases with that observed value.
- **Declared assumptions:** observed associations, proposed mechanisms, and
  causal claims remain distinguishable. Several graphs may fit the same
  observations.
- **Meaningful omissions:** in a specified DAG, a missing edge asserts the
  absence of a direct influence within that model; it does not mean "not yet
  examined." An incomplete sketch and possible unmeasured common causes need
  to remain explicit rather than being treated as a complete causal model.
- **Relevant conditioning:** a common cause, mediator, and collider have
  different roles. Automatically controlling for every available variable
  can distort the causal question rather than clarify it.

The graph describes qualitative structure. It does not supply effect sizes,
probabilities, or evidence that its assumptions are true.

## Example

An incident report notes that outages with more responders lasted longer.
Incident severity may cause both larger response teams and longer outages.
That common-cause explanation competes with the claim that additional
responders caused delay.

A review can expose the missing distinction between association and effect
without asserting that either explanation has been established. A hypothesis
about coordination overhead still needs support beyond the association.

## Boundaries

Temporal order, correlation, and a plausible story do not by themselves
establish causation. A DAG alone also does not determine counterfactual
outcomes; those require further model assumptions.

No diagram, statistical procedure, experiment, or sequence of agent reasoning
is required merely to interpret this framework. Preserve author intent,
competing explanations, uncertainty, and the distinction between evidence
and inference. Missing support does not authorize invented causes or extra
investigation outside the task.

## Foundation

[Stanford Encyclopedia of Philosophy, Causal Models](https://plato.stanford.edu/entries/causal-models/).
