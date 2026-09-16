# Why These Agent Rules Exist

The rules in [`../AGENTS.md`](../AGENTS.md) are intentionally concise. They
give coding agents a small set of durable engineering constraints without
prescribing a detailed process for every task. This README records the
reasoning behind those constraints so the rules can be interpreted and evolved
without losing their original intent.

Short instructions are easier for an agent to apply consistently alongside the
requirements, codebase conventions, and more specific instructions in nested
`AGENTS.md` files. The detailed rationale belongs here so it does not dilute
the rules that should remain prominent during implementation.

## Build the smallest complete solution

Starting with an end-to-end working slice exposes real requirements and
integration constraints earlier than building speculative infrastructure.
Incremental growth keeps each step usable and verifiable while reducing the
risk of investing in abstractions or configuration that the product never
needs.

"Smallest" does not mean incomplete or disposable. A solution should meet the
current requirements cleanly and leave a sound foundation for the next
capability. Temporary architecture often becomes permanent, so short-term
speed should not create an intentional replacement project.

## Establish meaningful boundaries

Cohesive modules and explicit boundaries localize change, clarify ownership,
and keep domain behavior independent from infrastructure details. Small,
domain-oriented contracts make collaborations understandable and allow
implementations to change without leaking storage, transport, or framework
concerns throughout the system.

A contract is broader than a language-level interface. It can be an API, type,
protocol, schema, function signature, or message format. The goal is not to
create an interface for every class; an abstraction should represent a real
module or external-system boundary. Otherwise, it adds indirection without
reducing coupling.

## Test behavior at the boundaries

Meaningful boundaries provide stable seams for testing observable behavior.
Tests should verify outcomes, important edge cases, and failure paths rather
than mirror internal implementation details. This makes refactoring safer
without forcing tests to change whenever private structure changes.

Simple test doubles keep unit tests focused and understandable when a boundary
has an external dependency. Integration tests remain necessary where contracts
meet real systems because they verify assumptions that an in-memory substitute
cannot, such as serialization, persistence, network behavior, and framework
configuration.

## Reuse dependencies deliberately

Existing dependencies should be examined before adding custom code or another
package. Reusing a capability already present in the project reduces the
maintenance, security, and operational surface area. Checking documentation
and types prevents unnecessary reimplementation based on an incorrect
assumption about what a dependency supports.

When a new dependency is justified, an established and actively maintained
library is usually more reliable than a local implementation of common
functionality. A package is not automatically simpler, however; it should
reduce total system complexity or provide a clear reliability benefit.

## Keep documentation as an evolving specification

Code records what the system does, but it often does not preserve why a choice
was made, which constraints shaped it, or how completion is judged. Defining
goals, constraints, and acceptance criteria before substantial work gives both
people and agents a shared target and limits accidental scope growth.

Documentation must evolve with the implementation. Changes to behavior,
contracts, invariants, or architectural decisions should update the relevant
design or module documentation in the same body of work. This prevents future
agents from treating stale documentation as authoritative and allows work to
continue across sessions without reconstructing prior decisions.

## How the rules work together

These rules are mutually reinforcing rather than independent mandates:

- An evolving specification defines the intended outcome.
- The smallest complete slice tests that intent against a working system.
- Explicit boundaries keep the slice understandable and extensible.
- Boundary-focused tests protect behavior as the system grows.
- Deliberate dependency reuse avoids unnecessary code and operational burden.

Terms such as "substantial work" and "meaningful boundary" are intentionally
proportional. Small documentation or configuration changes should not require
new architectural layers, interfaces, or process artifacts. More specific
subdirectories may add stricter rules when their domain genuinely requires
them.