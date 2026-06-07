# schedule-mobility-skill

Mira uses this skill when a calendar event, weather, or commute risk suggests
the user should prepare before they ask. The skill proposes departure time and a
mock ride reservation, but it requires confirmation before any reservation.

## Trigger Events

- `calendar_commute_risk`

## Tool Surface

- `readUpcomingSchedule()`
- `estimateCommuteRisk(event, currentLocation, weather)`
- `proposeDeparturePlan(event, traffic)`
- `createRideReservationPreview(event, pickupTime)`
- `confirmRideReservation(previewId)`
