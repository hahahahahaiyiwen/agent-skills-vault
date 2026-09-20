---
name: temporal-analysis
description: Interpret state-dependent behavior in human- or agent-authored process descriptions, plans, and specifications using statecharts and W3C SCXML concepts. Make states, events, guarded transitions, hierarchy, concurrency, and completion scope understandable without prescribing the agent's reasoning process or output format.
---

# Temporal Analysis

## Purpose

**Statecharts**, using the hierarchical and parallel state-machine concepts
defined by W3C SCXML, provide this skill's foundation. They clarify what can
happen in a given state and how events and conditions affect subsequent
behavior.

This skill addresses state-dependent change, not every form of time analysis.
It helps interpret process descriptions and specifications without treating
them as scripts for the agent's own reasoning or execution.

## Core model

- **State:** a named condition or mode, distinct from an event or an action.
- **Event:** an occurrence relevant to the model, generated internally or
  externally.
- **Transition and guard:** a permitted response, potentially changing the
  active states. A guard is a condition for eligibility, not a task to execute.
  Transitions may be event-triggered or eventless.
- **Action:** an effect associated with entry, exit, or a transition; requesting
  an operation is not the same as observing its successful completion.
- **Compound state:** when active, an exclusive parent has one active immediate
  child. Active descendants imply active ancestors.
- **Parallel state:** when active, its regions are all active, each with its own
  state. This is logical concurrency, not a guarantee of simultaneous execution.
- **Entry and completion:** initial states describe entry; final states mark
  completion within their enclosing scope, not necessarily success.

The active configuration includes the relevant ancestors and concurrent
regions, not just one label for the entire system.

## What makes the behavior interpretable

- **State versus occurrence:** "waiting," "a response arrived," and "send a
  request" describe different things; interchangeable labels obscure behavior.
- **Explicit conditions:** triggers, guards, and dependencies explain when a
  transition is possible. Unspecified failure or cancellation behavior remains
  unspecified, not an implicit successful path.
- **Scoped completion:** one region finishing does not mean all parallel
  regions or the whole process have finished. A completed failure is not a
  successful outcome.
- **Temporal honesty:** concurrency does not establish an arbitrary order.
  Durations and deadlines need explicit meaning, such as timeout events;
  an arrow alone is not a time estimate.

Statechart variants differ in transition selection and execution semantics.
The SCXML foundation supplies a defined reference, not permission to silently
mix rules from different variants.

## Example

A release description says, "Verify and package the artifact, then publish."
If verification and packaging are concurrent regions, a verification-complete
event alone cannot establish that packaging has finished.

A publication transition guarded by both successful outcomes expresses a
different requirement from one enabled merely because both activities have
stopped. Reviewing the state structure can expose that ambiguity without
inventing a retry, cancellation, or approval policy.

## Boundaries

A permitted path is not evidence that it occurred. Temporal order does not
prove causation, and a state label alone does not prove current real-world
status.

No statechart diagram, SCXML document, or fixed agent reasoning sequence is
required for interpretation. An informal description need not be a complete
executable model. Preserve its scope and uncertainty rather than manufacturing
transitions or requirements to complete the picture.

## Foundation

[W3C, State Chart XML (SCXML): State Machine Notation for Control Abstraction](https://www.w3.org/TR/scxml/).
