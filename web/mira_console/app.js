const state = {
  confirmed: false,
  orderId: "等待确认",
  items: [
    { name: "暖宝宝", quantity: 1, price: 12.9, eta: "28 min" },
    { name: "热饮", quantity: 1, price: 9.9, eta: "28 min" },
    { name: "常用卫生用品", quantity: 1, price: 19.9, eta: "28 min" }
  ],
  events: [
    ["20:47:03", "heartbeat", "system", "心跳检查完成"],
    ["20:47:04", "period_care_needed", "watch / calendar", "识别到用户可能需要关怀补给"],
    ["20:47:06", "skill_selected", "runtime", "选择 instant-retail-skill"],
    ["20:47:07", "policy_gate", "policy_engine", "需要用户确认后下单"],
    ["20:47:15", "user_confirmed", "console", "等待确认"]
  ]
};

const timelineSteps = [
  {
    time: "20:47:03",
    tone: "teal",
    title: "Heartbeat 触发",
    chips: ["周期: 60s", "来源: watch / glasses / phone / calendar"],
    body: "系统心跳检查完成，开始评估用户状态与环境。"
  },
  {
    time: "20:47:04",
    tone: "amber",
    title: "生活事件识别",
    chips: ["period_care_needed", "置信度: 0.82"],
    body: "用户可能身体不适，结合日程、心率、天气、历史偏好识别为需要关怀场景。"
  },
  {
    time: "20:47:06",
    tone: "teal",
    title: "技能选择",
    chips: ["instant-retail-skill", "主 Demo"],
    body: "匹配到常用补给包场景，进入即时零售技能流程。"
  },
  {
    time: "20:47:07",
    tone: "amber",
    title: "策略与安全门控",
    chips: ["需要确认", "预算检查通过", "mock_private"],
    body: "金额在预算内，涉及敏感上下文，需要用户显式确认后才可下单。"
  },
  {
    time: "20:47:15",
    tone: "teal",
    title: "用户确认",
    chips: ["渠道: Console"],
    body: "用户回复：好。"
  },
  {
    time: "20:47:16",
    tone: "amber",
    title: "Mock 订单创建",
    chips: ["ETA: 28 min", "状态: rider_assigned"],
    body: "Mock 订单已创建，进入履约跟踪流程。"
  }
];

function money(value) {
  return `¥${value.toFixed(2)}`;
}

function renderItems() {
  const body = document.querySelector("#itemsBody");
  const total = state.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  body.innerHTML = [
    ...state.items.map((item) => `
      <tr>
        <td>${item.name}</td>
        <td>${item.quantity}</td>
        <td>${money(item.price)}</td>
        <td>${item.eta}</td>
      </tr>
    `),
    `
      <tr>
        <td><strong>合计</strong></td>
        <td><strong>${state.items.length}</strong></td>
        <td><strong>${money(total)}</strong></td>
        <td><strong>28 min</strong></td>
      </tr>
    `
  ].join("");
  document.querySelector("#budgetBefore").textContent = money(1260);
  document.querySelector("#budgetAfter").textContent = money(1260 - total);
}

function renderTimeline() {
  document.querySelector("#timeline").innerHTML = timelineSteps.map((step) => `
    <article class="step">
      <div class="time">${step.time}</div>
      <div class="dot ${step.tone === "amber" ? "amber" : ""}"></div>
      <div class="step-card">
        <h3>${step.title}${step.chips.map((chip) => `<span class="chip">${chip}</span>`).join("")}</h3>
        <p>${step.body}</p>
      </div>
    </article>
  `).join("");
}

function renderEvents() {
  const rows = [...state.events];
  if (state.confirmed) {
    rows[4] = ["20:47:15", "user_confirmed", "console", "用户确认下单"];
    rows.push(["20:47:16", "mock_order_created", "bridge", "Mock 订单已创建"]);
  }
  document.querySelector("#eventsBody").innerHTML = rows.map((row) => `
    <tr>
      <td>${row[0]}</td>
      <td>${row[1]}</td>
      <td>${row[2]}</td>
      <td>${row[3]}</td>
    </tr>
  `).join("");
}

function renderOrder() {
  document.querySelector("#orderId").textContent = `订单 ID：${state.orderId}`;
  document.querySelector("#recordState").textContent = state.confirmed ? "记录状态：已记录 (Mock)" : "记录状态：待确认";
  document.querySelector("#confirmBtn").textContent = state.confirmed ? "已确认，刷新履约状态" : "模拟用户确认";
}

function render() {
  renderItems();
  renderTimeline();
  renderEvents();
  renderOrder();
}

document.querySelector("#confirmBtn").addEventListener("click", () => {
  state.confirmed = true;
  state.orderId = "mock-order-1747498036";
  render();
});

document.querySelector("#refreshBtn").addEventListener("click", render);

render();
