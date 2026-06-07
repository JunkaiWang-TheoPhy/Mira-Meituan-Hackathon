import fs from "node:fs";
import path from "node:path";

const ROOT = path.resolve(new URL("../../", import.meta.url).pathname);

function readJson(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(ROOT, relativePath), "utf8"));
}

export function inferMealNeed(context) {
  return {
    needsMeal: Number(context.last_meal_hours ?? 0) >= 6,
    reason: "long_gap_overtime",
    state: context.heart_state ?? "unknown"
  };
}

export function searchDiningCandidates(location = "公司附近") {
  const poi = readJson("config/meituan_poi.mock.json");
  const inventory = readJson("config/meituan_inventory.mock.json");
  const diningStoreIds = new Set(
    poi.filter((store) => store.category === "dining" && store.location_label === location).map((store) => store.poi_id)
  );
  return inventory.filter((item) => diningStoreIds.has(item.store_id) && item.category === "meal" && item.stock > 0);
}

export function filterByRestrictions(candidates, restrictions = [], recentMeals = []) {
  return candidates.filter((item) => {
    const tags = new Set(item.tags ?? []);
    return !restrictions.some((rule) => item.name.includes(rule)) && !recentMeals.includes(item.name) && !tags.has("too_spicy");
  });
}

export function rankByState(candidates, heartState, workStatus, weather, budget) {
  return [...candidates]
    .filter((item) => item.price <= budget)
    .sort((a, b) => {
      const aWarm = Number((a.tags ?? []).includes("warm"));
      const bWarm = Number((b.tags ?? []).includes("warm"));
      return bWarm - aWarm || a.price - b.price;
    });
}

export function createMealOrderPreview(candidate) {
  return {
    kind: "dining_order_preview",
    title: candidate.name,
    items: [{ ...candidate, quantity: 1 }],
    total_price: candidate.price,
    requires_confirmation: true
  };
}
