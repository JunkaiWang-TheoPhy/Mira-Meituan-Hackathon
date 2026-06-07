export function readUpcomingSchedule() {
  return {
    title: "跨区会议",
    starts_at: "08:00",
    commute_risk: "high"
  };
}

export function estimateCommuteRisk(event, currentLocation, weather) {
  return {
    risk: weather === "rain" ? "high" : "medium",
    estimated_commute_minutes: weather === "rain" ? 45 : 36,
    current_location: currentLocation,
    event
  };
}

export function proposeDeparturePlan(event, traffic) {
  return {
    event,
    pickup_time: "07:10",
    estimated_commute_minutes: traffic.estimated_commute_minutes,
    buffer_minutes: 15
  };
}

export function createRideReservationPreview(event, pickupTime = "07:10") {
  return {
    kind: "ride_reservation_preview",
    title: "明早会议出行安排",
    pickup_time: pickupTime,
    total_price: 58,
    requires_confirmation: true,
    event
  };
}
