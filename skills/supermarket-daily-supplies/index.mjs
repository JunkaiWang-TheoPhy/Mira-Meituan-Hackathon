export function planDailySupplies(context = {}) {
  const budget = Number(context.max_budget ?? context.budget_remaining ?? 100);
  const baseItems = [
    { name: "纸巾", priority: "must-buy", estimate: 18 },
    { name: "垃圾袋", priority: "must-buy", estimate: 12 },
    { name: "洗手液", priority: "good-to-have", estimate: 16 },
    { name: "早餐牛奶", priority: "good-to-have", estimate: 24 }
  ];
  let spent = 0;
  const items = baseItems.filter((item) => {
    const next = spent + item.estimate;
    if (next > budget && item.priority !== "must-buy") return false;
    spent = next;
    return next <= budget || item.priority === "must-buy";
  });
  return {
    kind: "daily_supplies_plan",
    title: "日用品补货清单",
    items,
    estimated_total: Number(spent.toFixed(2)),
    budget_limit: budget,
    requires_confirmation: true
  };
}

export function splitByPriority(items) {
  return {
    must_buy: items.filter((item) => item.priority === "must-buy"),
    good_to_have: items.filter((item) => item.priority === "good-to-have"),
    skip: items.filter((item) => item.priority === "skip")
  };
}
