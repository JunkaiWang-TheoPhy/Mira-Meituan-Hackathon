export function planGiftOccasion(context = {}) {
  const budget = Number(context.budget_remaining ?? 160);
  const deadline = context.deadline ?? "本周内";
  return {
    kind: "gift_flowers_plan",
    title: "生日礼物与鲜花提醒",
    recipient_group: context.recipient_group ?? "family",
    occasion: context.occasion ?? "birthday",
    deadline,
    budget_limit: Math.min(budget, 160),
    tiers: [
      { name: "budget", estimate: 68, idea: "实用小礼物 + 简短卡片" },
      { name: "balanced", estimate: 128, idea: "鲜花 + 轻量礼物" },
      { name: "nicer", estimate: 158, idea: "花束 + 偏好礼物" }
    ],
    requires_confirmation: true
  };
}

export function createGiftReminder(plan) {
  return {
    kind: "gift_reminder_preview",
    title: plan.title,
    reminder_offsets: ["7 days before", "2 days before"],
    requires_confirmation: true
  };
}
