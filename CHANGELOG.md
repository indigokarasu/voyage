## [2026-04-04] Spec Compliance Update

### Changes
- Added missing SKILL.md sections per ocas-skill-authoring-rules.md
- Updated skill.json with required metadata fields
- Ensured all storage layouts and journal paths are properly declared
- Aligned ontology and background task declarations with spec-ocas-ontology.md

### Validation
- ✓ All required SKILL.md sections present
- ✓ All skill.json fields complete
- ✓ Storage layout properly declared
- ✓ Journal output paths configured
- ✓ Version: 2.5.0 → 2.5.1

# CHANGELOG

## [2.5.0] - 2026-04-02

### Added
- Structured entity observations in journal payloads (`entities_observed`, `relationships_observed`, `preferences_observed`)
- `user_relevance` tagging on journal observations (default `user` for travel-related entities)
- Entity/Person (travel companions) added to ontology types
- Elephas journal cooperation in skill cooperation section

## 2.4.0 — 2026-03-30

### Added
- `references/plans/trip-planning.plan.md` — bundled workflow plan: destination research → itinerary → accommodation
- Ontology mapping: Voyage works with Place (venues/airports/hotels), Concept/Event (trips), and Concept/Action (bookings)

## Prior

See git log for earlier history.
