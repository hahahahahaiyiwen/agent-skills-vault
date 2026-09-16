- Do not preserve backward compatibility. Remove obsolete paths instead of
  adding compatibility layers, fallbacks, or migrations.
- Build the smallest complete solution that meets current requirements and
  works end to end. Grow it incrementally; avoid speculative abstractions,
  configuration, indirection, and temporary architecture.
- Separate concerns into cohesive modules with explicit boundaries. Use small,
  domain-oriented contracts across module and external-system boundaries;
  depend on those contracts rather than infrastructure details, and avoid
  abstractions without a meaningful boundary.
- Test behavior at meaningful boundaries, including expected outcomes, edge
  cases, and failures. Prefer simple test doubles, and use integration tests
  where contracts meet real systems.
- Use existing dependencies before writing new implementations or adding
  packages. Check their documentation and types, and prefer established,
  maintained libraries when they reduce complexity or improve reliability.
- Treat design and module documentation as an evolving specification. Define
  goals, constraints, and acceptance criteria before substantial work, and
  keep documentation aligned with changes to behavior, contracts, invariants,
  and architectural decisions.