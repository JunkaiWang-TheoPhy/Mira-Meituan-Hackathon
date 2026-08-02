# Mira：基于 OpenClaw 的本地生活私人管家

> 工作交给别的工具，生活由 Mira 帮你安排；本仓库用公开 mock 数据演示本地生活履约闭环。

Mira 是一个面向路演的 OpenClaw 风格本地生活 Agent。它不是“你问它答”的搜索框，而是把手表、眼镜、手机、日程、天气和预算等状态事件转成一个可确认的生活行动：吃什么、买什么、什么时候出门、是否超预算。

本仓库是 **non-official hackathon mock demo**：不调用真实平台 API，不创建真实订单，不采集真实健康、位置或身份数据。所有画像、区域、库存、预算、订单和配送 ETA 都是公开演示用 mock seed。

```text
multi-device context
-> life event extraction
-> OpenClaw-style heartbeat / memory / skill routing
-> policy gate
-> mock local-life proposal
-> user confirmation
-> mock order / ETA / budget writeback
```

一句话版本：

> Mira 负责懂你，OpenClaw 负责调度，本地生活履约能力负责把事办成。

## 90 秒主 Demo：即时零售

场景：晚上 20:47，用户仍在演示区域 A，天气下雨，手表状态低能量，日程显示连续会议后加班。Mira 不做泛泛搜索，而是识别为一个低打扰的即时生活需求：准备一个常用补给包，先过 policy gate，再等用户确认后生成 mock 订单、配送 ETA 和预算记录。

运行主 demo：

```bash
npm run demo:retail
```

运行完整多场景 demo：

```bash
npm run demo
```

主输出：

```text
runtime/demo-runs/<timestamp>-instant-retail/summary.json
runtime/mock-orders/demo-order-public-*.json
```

这些 runtime 输出会被 `.gitignore` 忽略，提交时只保留目录占位。

## 评委 3 分钟看仓库

1. 先看 [docs/SUBMISSION.md](./docs/SUBMISSION.md)：可直接复制到比赛表单的作品说明。
2. 再看 [docs/architecture-for-judges.md](./docs/architecture-for-judges.md)：状态感知到 mock 履约闭环。
3. 跑 `npm run demo:retail`：验证即时零售主链路。
4. 打开 [web/mira_console/index.html](./web/mira_console/index.html)：查看状态、事件、Skill、Policy、预算、履约六块评委控制台。
5. 看 [docs/data-safety.md](./docs/data-safety.md)：确认脱敏和越权边界。

## 已实现能力

- Mock life event schema：解释“为什么触发、准备做什么、是否有权做”。
- OpenClaw 风格 Skill：即时零售、餐饮、日程出行、娱乐、预算，以及从 `skills.zip` 合入的经期补货、礼物鲜花、小钱包预算、日用品补货。
- Mock local-life service：POI、库存、配送 ETA、订单、用户画像、预算。
- Mira Life Bridge：稳定高层 API，隔离底层 mock 数据。
- Policy gate：金钱、敏感上下文、位置和预算风险都需要确认。
- Roadshow console：六块静态评委视图，使用 `config/mira_console_seed.mock.json`。

## 新增四个生活规划技能

| Skill | 负责什么 | 履约关系 |
| --- | --- | --- |
| `period-care-restock` | 克制地规划常用关怀补给包，是主 Demo 的 planning skill。 | 交给 `instant-retail-skill` 做 mock 库存、ETA、订单。 |
| `gifts-flowers-planner` | 生日、节日、探访、道歉等礼物/鲜花规划。 | 需要确认对象、卡片、地址和时间后再进入 mock 履约。 |
| `pocket-wallet-budget` | 小钱包预算、桶分配、是否超预算。 | 只做 advisory，不直接下单。 |
| `supermarket-daily-supplies` | 日用品缺货和超市补货清单。 | 交给 `instant-retail-skill` 做 mock 履约。 |

## 入口命令

```bash
npm run demo:retail
npm run demo
bash tools/mira_life_bridge/start_bridge.sh
```

Bridge smoke：

```bash
curl http://127.0.0.1:9793/health
curl http://127.0.0.1:9793/v1/mira-life/trigger-event \
  -H "Content-Type: application/json" \
  -d @config/demo_event_period_care_needed.json
```

测试：

```bash
python3 -m unittest discover -s tests
node --check web/mira_console/app.js
```

## 仓库结构

```text
config/                 mock schema, user profile, budget, POI, inventory, delivery, console seed
docs/                   submission copy, judge walkthrough, architecture, scripts, safety
scripts/                event router, mock service, demo runners, report generator
skills/                 OpenClaw-style local-life skill surfaces, including zip-imported planning skills
tools/mira_life_bridge/ loopback bridge and plugin wrapper
web/mira_console/       static judge console
runtime/                ignored demo outputs with .gitkeep placeholders
```

## 安全边界

Mira 可以主动提议，但不能越权执行。涉及金钱、敏感上下文、位置或预算风险时，Mira 只生成可解释方案，必须等待用户确认。本仓库所有订单都是 mock 订单，所有区域都是不可定位 demo bucket。
