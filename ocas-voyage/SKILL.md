---
name: ocas-voyage
description: >
  Travel planning, itinerary construction, and reservation management.
  Builds optimized itineraries with lodging, dining, and activity
  recommendations grounded in constraints and preferences.
---

# Voyage

Voyage builds travel itineraries with lodging, dining, and activity recommendations. It respects constraints (budget, dietary, pace), optimizes logistics, and produces reservation-ready plans.

## When to use

- Plan a multi-day trip with itinerary
- Build or optimize a travel itinerary
- Recommend lodging, restaurants, or activities for a trip
- Manage reservation planning and checklists
- Optimize an existing itinerary for feasibility

## When not to use

- Generic travel inspiration with no planning intent
- Airfare-only or points-only optimization
- Visa, customs, or medical-travel compliance as primary task
- Presenting uncertain availability as confirmed facts

## Core promise

Turn a destination and constraints into a feasible, reservation-aware itinerary. Every recommendation cites reasoning. Uncertainty about availability or hours is flagged, not hidden.

## Commands

- `voyage.plan.trip` — create a full trip plan from destination, dates, and constraints
- `voyage.recommend.lodging` — lodging recommendations based on trip context
- `voyage.recommend.food` — restaurant recommendations based on route and preferences
- `voyage.recommend.activities` — activity recommendations based on interests and logistics
- `voyage.optimize.itinerary` — optimize an existing itinerary for feasibility and logistics
- `voyage.status` — current plan state, pending reservations, open decisions

## Invariants

- Never present uncertain operating hours or availability as confirmed
- Respect dietary constraints in all food recommendations
- Budget awareness throughout — surface cost implications
- Reservation-ready means actionable, not auto-booked (unless explicitly enabled)

## Support file map

- `references/voyage_schemas.md` — TripPlan, ItineraryDay, Recommendation, ReservationItem
- `references/itinerary_constraints.md` — constraint types, optimization rules, feasibility checks
- `references/recommendation_style.md` — explanation quality, evidence grounding, tone

## Storage layout

```
.voyage/
  config.json
  state.json
  events.jsonl
  decisions.jsonl
  plans/
```

## Validation rules

- Every recommendation includes reasoning
- Dietary constraints applied before suggestions surface
- Walking distances and transit times are feasible
- Uncertain availability explicitly flagged
