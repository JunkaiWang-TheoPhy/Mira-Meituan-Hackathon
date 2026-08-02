import fs from "node:fs";
import path from "node:path";

const ROOT = path.resolve(new URL("../../", import.meta.url).pathname);

function readJson(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(ROOT, relativePath), "utf8"));
}

export function prepareRestockKit(profile = readJson("config/mira_user_profile.mock.json")) {
  const usualItems = profile.preferences.usual_care_items ?? [];
  return {
    kind: "period_care_restock_plan",
    title: "常用舒缓补给包",
    must_buy: usualItems.filter((item) => item !== "热饮"),
    optional: usualItems.filter((item) => item === "热饮"),
    tone: "discreet_practical",
    requires_confirmation: true
  };
}

export function prioritizeCareItems(items, budget = 80) {
  let spent = 0;
  return items
    .map((item) => ({ ...item, priority: item.name === "热饮" ? "optional" : "must-buy" }))
    .filter((item) => {
      const next = spent + item.price * (item.quantity ?? 1);
      if (next > budget && item.priority === "optional") return false;
      spent = next;
      return true;
    });
}

export function createCareRestockPlan(items, context = {}) {
  const total = Number(items.reduce((sum, item) => sum + item.price * (item.quantity ?? 1), 0).toFixed(2));
  return {
    kind: "period_care_restock_plan",
    title: "常用舒缓补给包",
    items,
    estimated_total: total,
    location_label: context.location_label ?? "演示区域A",
    privacy_note: "discreet mock planning only",
    requires_confirmation: true
  };
}
