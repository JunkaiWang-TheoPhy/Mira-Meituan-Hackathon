# Mira：基于 OpenClaw 的本地生活私人管家

> 工作交给别的工具，生活由 Mira 帮你安排，美团负责把事办成。

Mira 不是一个“你问它答”的查询助手，而是一个基于 OpenClaw 思路构建的本地生活管家。它通过眼镜、手表和手机等多端状态事件理解用户最近的生活处境，再通过 Memory、Heartbeat、Skill、Gateway 和 Bridge/Safety Layer，调用餐饮、即时零售、出行预约、娱乐推荐和预算管理等本地生活能力，完成从“状态感知”到“推荐决策”再到“确认履约”的闭环。

30 秒 Demo 视频位：录制后把视频链接放在这里。当前仓库先提供 [30 秒视频脚本](./docs/demo-video-storyboard.md) 和一键 mock demo。

```text
watch / glasses / phone context
-> life event extraction
-> OpenClaw-style memory + heartbeat
-> life intent decision
-> Meituan local-life skills
-> recommendation / confirmation / mock order / delivery tracking
-> life memory writeback
```

一句话版本：

> Mira 负责懂你，OpenClaw 负责调度，美团负责办成。

## 主 Demo：即时零售

用户处于晚间加班、低能量、天气下雨、长时间没有离开公司等状态时，Mira 不做泛泛搜索，而是判断这是一个即时生活需求。它结合用户常用清单、附近门店库存、配送 ETA 和预算约束，主动生成一个补给包方案，并在用户确认后完成 mock 下单、配送 ETA 展示和预算记录。

```bash
npm run demo:retail
```

或者：

```bash
bash scripts/run_instant_retail_demo.sh
```

输出会写入：

```text
runtime/demo-runs/<timestamp>-instant-retail/summary.json
runtime/mock-orders/mock-order-*.json
```

## 我们实现了什么

- 多端状态事件 mock：手表、眼镜、手机、日程、位置、天气。
- `mira_life_event.schema.json`：解释“为什么触发、准备做什么、是否有权做”。
- OpenClaw 风格 Skill：`dining`、`instant-retail`、`schedule-mobility`、`entertainment`、`budget-care`。
- Mock 本地生活服务：POI、库存、配送 ETA、订单、用户画像和预算。
- Mira Life Bridge：把底层 mock API 封装成稳定的高层生活工具。
- Policy gate：涉及金钱、敏感上下文、预算和隐私时必须确认。
- 静态评委控制台：[web/mira_console/index.html](./web/mira_console/index.html)。
- 提交材料和路演脚本：[docs/SUBMISSION.md](./docs/SUBMISSION.md)。

## 快速开始

环境要求：

- Python 3.10+
- Node.js 18+ 仅用于 `npm run ...` 包装命令；核心 runtime 使用 Python 标准库。

运行主 demo：

```bash
python3 scripts/run_instant_retail_demo.py
```

运行三个核心场景：

```bash
python3 scripts/run_mira_demo.py
```

生成生活日报：

```bash
python3 scripts/generate_life_report.py
```

运行测试：

```bash
python3 -m unittest discover -s tests
```

启动本地 bridge：

```bash
bash tools/mira_life_bridge/start_bridge.sh
```

触发主事件：

```bash
curl http://127.0.0.1:9793/v1/mira-life/trigger-event \
  -H "Content-Type: application/json" \
  -d @config/demo_event_period_care_needed.json
```

## 仓库结构

```text
.
├── README.md
├── config/
│   ├── mira_life_event.schema.json
│   ├── mira_user_profile.mock.json
│   ├── mira_budget.mock.json
│   ├── meituan_poi.mock.json
│   ├── meituan_inventory.mock.json
│   ├── meituan_delivery.mock.json
│   └── release_life_bundles.json
├── docs/
│   ├── SUBMISSION.md
│   ├── architecture-for-judges.md
│   ├── demo-script-instant-retail.md
│   ├── demo-script-dining.md
│   ├── demo-script-mobility.md
│   ├── data-safety.md
│   └── meituan-mock-api-contract.md
├── skills/
│   ├── dining-skill/
│   ├── instant-retail-skill/
│   ├── schedule-mobility-skill/
│   ├── entertainment-skill/
│   └── budget-care-skill/
├── scripts/
│   ├── life_event_router.py
│   ├── mock_meituan_service.py
│   ├── run_instant_retail_demo.py
│   ├── run_mira_demo.py
│   └── generate_life_report.py
├── tools/mira_life_bridge/
├── web/mira_console/
└── runtime/
```

## 和 Mira Light 的关系

本项目复用了 Mira 的主动感受型 AI 架构，但不再把主能力放在“灯光/动作回应”上。原 Mira Light 的链路是：

```text
视觉事件 -> 场景选择 -> 灯光/动作回应
```

这次改造成：

```text
多端状态事件 -> 生活意图判断 -> 本地生活 Skill -> 美团履约闭环
```

Mira Light 可以作为空间化提示终端：Mira 判断你可能需要晚饭或补给包时，手机弹出确认，桌面设备用低打扰灯光提醒你。但主角是本地生活履约闭环，不是硬件本身。

## 安全边界

这个仓库只使用虚构画像和 mock 订单，不采集真实健康数据，不做医疗诊断，不创建真实订单。涉及金钱、敏感上下文、位置和预算超限的动作都必须经过 policy gate 和用户确认。

