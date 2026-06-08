import fs from "node:fs";
import path from "node:path";

const ROOT = path.resolve(new URL("../../", import.meta.url).pathname);

function readJson(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(ROOT, relativePath), "utf8"));
}

export function listEmergencyKits(profile = readJson("config/mira_user_profile.mock.json")) {
  return {
    title: "常用舒缓补给包",
    items: profile.preferences.usual_care_items,
    confirmationRequired: true
  };
}

export function searchRetailInventory(query, location = "演示区域A") {
  const poi = readJson("config/meituan_poi.mock.json");
  const inventory = readJson("config/meituan_inventory.mock.json");
  const retailStoreIds = new Set(
    poi
      .filter((store) => store.category === "instant_retail" && store.location_label === location && store.open_now)
      .map((store) => store.poi_id)
  );
  const names = new Set(Array.isArray(query) ? query : [query]);
  return inventory.filter((item) => retailStoreIds.has(item.store_id) && item.stock > 0 && names.has(item.name));
}

export function rankRetailOptions(items, profile, budget, etaByStore) {
  return [...items]
    .map((item) => ({
      ...item,
      eta_minutes: etaByStore[item.store_id]?.eta_minutes ?? 99,
      preference_hit: profile.preferences.usual_care_items.includes(item.name)
    }))
    .filter((item) => item.price <= budget)
    .sort((a, b) => Number(b.preference_hit) - Number(a.preference_hit) || a.eta_minutes - b.eta_minutes);
}

export function createRetailOrderPreview(items, address = "演示区域A", budget = 80) {
  const delivery = readJson("config/meituan_delivery.mock.json");
  const total = Number(items.reduce((sum, item) => sum + item.price * (item.quantity ?? 1), 0).toFixed(2));
  const storeId = items[0]?.store_id;
  return {
    kind: "instant_retail_order_preview",
    title: "常用舒缓补给包",
    items,
    address_label: address,
    total_price: total,
    eta_minutes: delivery[storeId]?.eta_minutes ?? null,
    budget_after: Number((budget - total).toFixed(2)),
    requires_confirmation: true
  };
}

export function confirmRetailOrder(orderPreview) {
  return {
    order_id: `mock-order-${Date.now()}`,
    status: "mock_order_created",
    preview: orderPreview
  };
}

export function trackRetailDelivery(orderId, etaMinutes = 28) {
  return {
    order_id: orderId,
    state: "rider_assigned",
    eta_minutes: etaMinutes
  };
}
