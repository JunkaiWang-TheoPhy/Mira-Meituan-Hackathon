const fallbackSeed = {
  event_type: "period_care_needed",
  location_label: "演示区域A",
  weather: "下雨",
  time: "20:47",
  heart_state: "low_energy",
  activity_state: "长时间静止",
  budget_before: 1260,
  budget_after: 1217.3,
  eta_minutes: 28,
  policy_status: "confirmation_required",
  selected_skill: "instant-retail-skill",
  static_order_label: "demo-order-public",
  items: [
    { name: "暖宝宝", quantity: 1, price: 12.9 },
    { name: "热饮", quantity: 1, price: 9.9 },
    { name: "常用卫生用品", quantity: 1, price: 19.9 }
  ],
  timeline: [
    ["20:47:03", "Heartbeat triggered", "system", "周期检查触发"],
    ["20:47:04", "Life event extracted", "watch / calendar", "识别到需要低打扰关怀"],
    ["20:47:06", "Skill selected", "runtime", "选择 instant-retail-skill"],
    ["20:47:07", "Policy gate", "policy", "需要用户确认"],
    ["20:47:15", "User confirmation", "console", "等待用户确认"]
  ]
};

const state = {
  confirmed: false,
  seed: fallbackSeed
};

function money(value) {
  return `¥${Number(value).toFixed(2)}`;
}

async function loadSeed() {
  try {
    const response = await fetch("../../config/mira_console_seed.mock.json");
    if (!response.ok) {
      throw new Error(`seed fetch failed: ${response.status}`);
    }
    state.seed = await response.json();
  } catch {
    state.seed = fallbackSeed;
  }
}

function renderState() {
  const seed = state.seed;
  document.querySelector("#stateLocation").textContent = seed.location_label;
  document.querySelector("#stateWeather").textContent = seed.weather;
  document.querySelector("#stateTime").textContent = seed.time;
  document.querySelector("#stateHeart").textContent = seed.heart_state;
  document.querySelector("#stateActivity").textContent = seed.activity_state;
  document.querySelector("#stateBudget").textContent = money(seed.budget_before);
}

function renderItems() {
  const seed = state.seed;
  const body = document.querySelector("#itemsBody");
  const total = seed.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  body.innerHTML = [
    ...seed.items.map((item) => `
      <tr>
        <td>${item.name}</td>
        <td>${item.quantity}</td>
        <td>${money(item.price)}</td>
        <td>${seed.eta_minutes} min</td>
      </tr>
    `),
    `
      <tr>
        <td><strong>合计</strong></td>
        <td><strong>${seed.items.length}</strong></td>
        <td><strong>${money(total)}</strong></td>
        <td><strong>${seed.eta_minutes} min</strong></td>
      </tr>
    `
  ].join("");
  document.querySelector("#selectedSkill").textContent = seed.selected_skill;
}

function renderTimeline() {
  document.querySelector("#timeline").innerHTML = state.seed.timeline.map(([time, title, source, body], index) => `
    <article class="step">
      <div class="time">${time}</div>
      <div class="dot ${index % 2 ? "amber" : ""}"></div>
      <div class="step-card">
        <h3>${title}<span class="chip">${source}</span></h3>
        <p>${body}</p>
      </div>
    </article>
  `).join("");
}

function renderPolicy() {
  const suffix = state.confirmed ? " -> user_confirmed" : "";
  document.querySelector("#policyStatus").textContent = `${state.seed.policy_status}${suffix}`;
  document.querySelector("#recordState").textContent = state.confirmed ? "记录状态：已记录 (Mock)" : "记录状态：待确认";
}

function renderBudget() {
  document.querySelector("#budgetBefore").textContent = money(state.seed.budget_before);
  document.querySelector("#budgetAfter").textContent = money(state.seed.budget_after);
}

function renderOrder() {
  const label = state.confirmed ? state.seed.static_order_label : "等待确认";
  document.querySelector("#orderId").textContent = `订单 ID：${label}`;
  document.querySelector("#confirmBtn").textContent = state.confirmed ? "已确认，刷新履约状态" : "模拟用户确认";
}

function render() {
  renderState();
  renderItems();
  renderTimeline();
  renderPolicy();
  renderBudget();
  renderOrder();
}

document.querySelector("#confirmBtn").addEventListener("click", () => {
  state.confirmed = true;
  render();
});

document.querySelector("#refreshBtn").addEventListener("click", render);

loadSeed().then(render);
