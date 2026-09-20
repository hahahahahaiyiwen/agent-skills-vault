---
name: multi-dimensional-analysis
description: Interpret multi-dimensional problem spaces using General Morphological Analysis, with dimensions, possible values, configurations, and compatibility constraints. Supports more than two dimensions and any relevant number of categories per dimension. Useful for explaining or reviewing human- or agent-authored analyses without prescribing the agent's reasoning process or output format.
---

# Multi-Dimensional Analysis

## Purpose

**General Morphological Analysis (GMA)**, developed by Fritz Zwicky and extended
through cross-consistency assessment, provides this skill's foundation. It
organizes a problem space through dimensions and possible conditions, making
combinations and constraints visible in human- or agent-authored analyses.
It is not a universal model for everything called multi-dimensional analysis.

## Core model

- **Dimension or parameter:** a relevant aspect of the bounded problem.
- **Values or conditions:** distinguishable possibilities for that dimension.
  They may be qualitative categories rather than numbers.
- **Morphological field:** the space of combinations of those values.
- **Configuration:** one combination containing one value from each dimension.
- **Cross-consistency assessment:** pairwise examination of whether values from
  different dimensions can coexist, with reasons for compatibility judgments.

There is no fixed number of dimensions or categories. Different dimensions can
have different numbers of values. Crossing two binary dimensions gives a 2x2
field; that is one possible case, not a limit on this framework.

## What makes the analysis informative

- **Meaningful definitions:** dimensions answer distinct questions; values have
  consistent meanings and explicit category boundaries where relevant.
- **Visible interactions:** dimensions need not be statistically independent.
  Dependencies and incompatibilities connect them rather than disappearing
  into separate columns.
- **Traceable constraints:** logical contradictions, empirical limitations,
  and policy or preference judgments remain distinguishable. An undesirable
  combination is not necessarily an impossible one.
- **Honest consistency claims:** pairwise compatibility does not guarantee
  joint feasibility; constraints involving several dimensions may also matter.
  Unassessed relationships remain unknown.
- **Bounded coverage:** the field reflects the chosen scope and conditions,
  not every real-world possibility. A partial field is not an exhaustive study.

The interpretive value comes from relationships among dimensions, not their
count. A list of factors under headings alone is not a morphological analysis.

## Example

A reference-reader design might contain this illustrative field:

| Dimension | Possible conditions |
|---|---|
| Connectivity during use | Continuous; intermittent; none. |
| Data location | Remote only; local copy available. |
| Freshness requirement | Live; daily snapshot; no fixed bound. |

These three dimensions define `3 x 2 x 3 = 18` candidate configurations before
constraints. No connectivity combined with remote-only data cannot support
reading that data during use. Other combinations still require assessment;
they are not automatically feasible or desirable designs.

This exposes relationships that an isolated discussion of connectivity or
freshness would miss, without requiring a three-dimensional visualization.

## Boundaries

GMA structures configurations and consistency, not causal effects or an
automatic ranking of alternatives. Comparing performance or recommending a
configuration needs its own evidence and preference basis, not invented weights.

No matrix, exhaustive enumeration, or fixed agent reasoning sequence is required
to explain or review the framework. Preserve source meaning, uncertainty, and
counterevidence; missing values are not permission to fabricate conditions or
expand the task solely to complete the field.

## Foundation

[Tom Ritchey, General Morphological Analysis](https://www.swemorph.com/ma.html).
