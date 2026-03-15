# 🗺️ Voyage

Voyage builds complete travel itineraries from goals and constraints. It plans routes, recommends activities and dining, identifies lodging options, and manages reservations. Voyage optimizes for preferences while respecting constraints (budget, time, accessibility). Every itinerary is editable and reservations are auditable.

---

## 📖 Overview

Travel planning, itinerary construction, and reservation management. Builds optimized itineraries with lodging, dining, and activity recommendations.

---

## 🔧 Tool Surface

- `voyage.trip.create` — create trip with destination, duration, constraints
- `voyage.itinerary.generate` — generate initial itinerary
- `voyage.itinerary.edit` — modify itinerary (reorder, swap activities)
- `voyage.recommendations.lodging` — lodging options with reviews and availability
- `voyage.recommendations.dining` — dining recommendations matching preferences
- `voyage.recommendations.activities` — activities with duration and suitability
- `voyage.reservations.list` — current reservations with confirmation details
- `voyage.reservations.manage` — modify or cancel reservations
- `voyage.status` — active trips, itinerary completion, reservation status

---

## 📊 Output & Journals

Trip records, itinerary versions with edit history, and reservation logs.

---



---

## 📚 Documentation

Read `SKILL.md` for operational details, schemas, and validation rules.

See `references/` for detailed specifications and examples.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
