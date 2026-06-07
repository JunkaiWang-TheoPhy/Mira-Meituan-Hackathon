const BRIDGE_URL = process.env.MIRA_LIFE_BRIDGE_URL ?? "http://127.0.0.1:9793";
const TOKEN = process.env.MIRA_LIFE_BRIDGE_TOKEN;

async function callBridge(path, payload) {
  const response = await fetch(`${BRIDGE_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(TOKEN ? { Authorization: `Bearer ${TOKEN}` } : {})
    },
    body: JSON.stringify(payload ?? {})
  });
  if (!response.ok) {
    throw new Error(`Mira bridge error ${response.status}: ${await response.text()}`);
  }
  return response.json();
}

export async function mira_trigger_event(event) {
  return callBridge("/v1/mira-life/trigger-event", event);
}

export async function mira_propose_action(event) {
  return callBridge("/v1/mira-life/propose-action", event);
}

export async function mira_confirm_action(proposal) {
  return callBridge("/v1/mira-life/confirm-action", proposal);
}

export async function mira_cancel_action(reason) {
  return callBridge("/v1/mira-life/cancel-action", { reason });
}

export async function mira_check_budget(category) {
  return callBridge("/v1/mira-life/check-budget", { category });
}

export async function mira_place_mock_order(proposal) {
  return callBridge("/v1/mira-life/place-mock-order", proposal);
}

export async function mira_track_fulfillment(order) {
  return callBridge("/v1/mira-life/track-fulfillment", order);
}
