# 🌊 Voyage

> **Travel planning, itinerary construction, and reservation management.**

## Why Voyage?

Planning a trip involves dozens of small decisions — flights, hotels, restaurants, activities — across multiple sites and booking platforms. Voyage handles the full workflow: researching options, comparing prices, building itineraries, and managing reservations. When Spot books a restaurant, Voyage gets the update automatically.

Skill packages follow the [agentskills.io](https://agentskills.io/specification) open standard and are compatible with OpenClaw, Hermes Agent, Claude, and any agentskills.io-compliant client.

## Quick Start

```
# Plan a trip
"Plan a weekend trip to Portland for next month"

# Check itinerary
"What's my itinerary looking like?"

# Book a hotel
"Find me a hotel in downtown Portland"
```

## What It Does

Voyage manages the full travel planning workflow: destination research, flight and hotel comparison, itinerary construction, and reservation management. It integrates with Spot (restaurant bookings) and Sands (calendar events) to keep your trip synchronized across skills.

## Dependencies

- [Sands](https://github.com/indigokarasu/sands) — calendar events for trip dates
- [Spot](https://github.com/indigokarasu/spot) — restaurant bookings become Travel Context entries
- Travel booking APIs (flights, hotels)

## Changelog

### v2.7.5 — April 12, 2026
- Replaced agent-browser with web-browsing capability for portability

---

*Voyage is part of the [OCAS Agent Suite](https://github.com/indigokarasu).*