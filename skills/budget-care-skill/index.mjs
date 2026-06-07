import fs from "node:fs";
import path from "node:path";

const ROOT = path.resolve(new URL("../../", import.meta.url).pathname);

function readJson(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(ROOT, relativePath), "utf8"));
}

export function checkBudget(category) {
  const budget = readJson("config/mira_budget.mock.json");
  return budget.categories[category] ?? { remaining: budget.budget_remaining };
}

export function recordPlannedSpend(category, amount) {
  const bucket = checkBudget(category);
  return {
    category,
    amount,
    remaining_after: Number((bucket.remaining - amount).toFixed(2)),
    mock_only: true
  };
}

export function summarizeLifeBudget() {
  return readJson("config/mira_budget.mock.json");
}

export function proposeLowerCostAlternative(proposal) {
  return {
    ...proposal,
    note: "已进入预算保护模式，优先推荐低价或必要项。"
  };
}
