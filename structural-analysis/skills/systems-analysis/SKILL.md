---
name: systems-analysis
description: Interpret feedback-driven behavior in human- or agent-authored explanations and proposals using causal-loop diagrams from system dynamics. Make signed influences, reinforcing and balancing loops, system boundaries, and delays understandable without prescribing the agent's reasoning process or output format.
---

# Systems Analysis

## Purpose

**Causal-loop diagrams**, used in system dynamics, provide this skill's
foundation. They explain how interactions can return to influence their
starting conditions, so the behavior of a whole system may differ from the
intended effect of a local change.

This skill concerns qualitative feedback structure, not every meaning of
systems analysis or a complete simulation model.

## Core model

- **Boundary:** the behavior, context, and time horizon being represented,
  distinguishing included interactions from external influences.
- **Variable:** a quantity or condition that can increase or decrease,
  such as queue length, response time, or demand.
- **Signed influence:** `+` means increasing the source makes the target
  higher than it otherwise would be; `-` means lower, other influences held
  constant. These signs do not mean good and bad.
- **Feedback loop:** a directed chain returning to its starting variable.
  A reinforcing loop amplifies a change; a balancing loop opposes it.
- **Delay:** a lag between an influence and its response, which can make
  short-term and longer-term behavior differ.

For fixed link signs, an even number of negative links, including zero,
defines a reinforcing loop; an odd number defines a balancing loop.
The label describes feedback polarity, not a guaranteed outcome.

## What makes the explanation informative

- **Interpretable links:** variable names and directions have clear meanings.
  Observed co-movement alone does not establish a causal influence.
- **Complete feedback relationships:** a chain that never returns to its
  starting variable is not a loop. Local benefits and returning effects
  remain distinguishable.
- **Visible competing loops:** several loops may interact, and their relative
  influence may change with conditions or time. One loop does not explain
  every observed behavior.
- **Explicit limits:** omitted external drivers, uncertain signs, operating
  ranges, and relevant delays remain visible. A balancing loop need not be
  stable, and reinforcing feedback is not necessarily undesirable.

The value is seeing how responses can alter the conditions that prompted them,
rather than treating consequences as a one-way list.

## Example

In an illustrative service, higher latency causes more timeouts, which trigger
more retries, adding load and further increasing latency. These assumed links
form a reinforcing loop.

A response that increases retry backoff as latency rises can introduce a
balancing loop by reducing retry load. Its delays and interaction with the
first loop matter; the diagram alone does not establish that the service will
stabilize or quantify an effective backoff.

This can reveal why a proposal addressing only individual failed requests
misses the behavior of the combined system.

## Boundaries

Causal-loop diagrams are hypotheses about feedback, not proof of causation or
numerical predictions. Stocks, flows, equations, and evidence may be needed
for quantitative modeling; they are not supplied by drawing signed arrows.

No mandatory diagram or agent reasoning sequence follows from this framework.
Preserve the author's scope and uncertainty. Missing links or delays remain
unknown rather than being invented to make a loop look complete.

## Foundation

[Colleen P. Lannon, Causal Loop Construction: The Basics](https://thesystemsthinker.com/causal-loop-construction-the-basics/).
