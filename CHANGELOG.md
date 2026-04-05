## [2026-04-05] Parallel lodging stack + GoPlaces cooperation

### Added
- Parallel lodging search: Expedia web + Marriott Strider MCP + Marriott AI/FlyAI + Google Hotels all fire simultaneously during `voyage.recommend.lodging`
- `voyage.init` steps 7–10: Marriott Strider MCP installation and Bonvoy OAuth setup, Google Hotels agent-browser check, FLYAI_API_KEY optional setup, GoPlaces availability check
- GoPlaces optional cooperation: location geocoding, distance checks, disambiguation (when `ocas-goplaces` is installed)
- Sift documented as delegation target for all open web research
- `references/lodging-sources.md` — per-source patterns and failure modes
- `references/total-cost.md` — cost breakdown methodology
- `references/booking-gates.md` — pre-booking checklist
- `itineraries/` subdirectory added to storage layout

### Changed
- `voyage.recommend.lodging` description updated to reflect parallel search
- Optional skill cooperation section expanded with GoPlaces and Sift delegation detail
- `filesystem.read` extended to include Taste and Weave data directories
- `filesystem.write` extended to include `itineraries/`

### Validation
- ✓ Version: 2.5.1 → 2.6.0

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
