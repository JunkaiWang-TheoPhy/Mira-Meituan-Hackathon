import fs from "node:fs";
import path from "node:path";

const ROOT = path.resolve(new URL("../../", import.meta.url).pathname);

function readJson(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(ROOT, relativePath), "utf8"));
}

export function summarizeWallet(budget = readJson("config/mira_budget.mock.json")) {
  return {
    kind: "pocket_wallet_summary",
    currency: budget.currency,
    wallet_remaining: budget.budget_remaining,
    buckets: budget.categories,
    recommended_split: {
      daily_supplies: 0.5,
      period_care: 0.2,
      gifts_flowers: 0.25,
      buffer: 0.05
    }
  };
}

export function checkPurchaseFit(category, amount, budget = readJson("config/mira_budget.mock.json")) {
  const bucket = budget.categories[category] ?? { remaining: budget.budget_remaining };
  const fits = Number(amount) <= Number(bucket.remaining);
  return {
    kind: "pocket_wallet_decision",
    category,
    amount,
    remaining_before: bucket.remaining,
    remaining_after: Number((bucket.remaining - amount).toFixed(2)),
    decision: fits ? "buy now" : "ask user for approval to exceed budget",
    requires_confirmation: !fits
  };
}
