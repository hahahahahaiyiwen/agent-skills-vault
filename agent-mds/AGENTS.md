- Build the smallest complete solution that meets current requirements and
  works end to end. Grow it incrementally; avoid speculative abstractions,
  configuration, indirection, and temporary architecture.
- Separate concerns into cohesive modules with explicit boundaries. Use small,
  domain-oriented contracts across module and external-system boundaries;
  depend on those contracts rather than infrastructure details, and avoid
  abstractions without a meaningful boundary.
- Write unit tests before implementing or changing behavior. Specify meaningful
  boundary contracts through expected outcomes, edge cases, and failures; do
  not retrofit tests merely to mirror completed code. Prefer simple test doubles,
  and use integration tests where contracts meet real systems.
- During development, run targeted unit and integration tests, plus narrowly
  scoped E2E checks when needed. Reserve the full E2E suite for final validation
  after development is complete.
- Use existing dependencies before writing new implementations or adding
  packages. Check their documentation and types, and prefer established,
  maintained libraries when they reduce complexity or improve reliability.
- Treat design and module documentation as an evolving specification. Define
  goals, constraints, and acceptance criteria before substantial work, and
  keep documentation aligned with changes to behavior, contracts, invariants,
  and architectural decisions.