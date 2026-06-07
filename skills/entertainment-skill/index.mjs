export function inferEnergyMode(context) {
  return context.heart_state === "low_energy" ? "quiet" : "active";
}

export function searchEntertainmentOptions(location, energyMode) {
  if (energyMode === "quiet") {
    return [{ title: "安静咖啡馆与居家观影", location, total_price: 0 }];
  }
  return [{ title: "展览与 Livehouse 备选", location, total_price: 88 }];
}

export function createWeekendPlanPreview(option) {
  return {
    kind: "entertainment_plan_preview",
    ...option,
    requires_confirmation: false
  };
}
