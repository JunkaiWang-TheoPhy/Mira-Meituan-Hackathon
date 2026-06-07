# Demo Script: Instant Retail

Duration: 90 seconds.

## Setup

```json
{
  "user": "Demo User",
  "location": "公司附近",
  "budget_remaining": 1260,
  "preferences": {
    "delivery_preference": "30分钟内优先",
    "avoid": ["太辣", "冰饮"],
    "usual_care_items": ["暖宝宝", "热饮", "常用卫生用品"]
  },
  "privacy": {
    "demo_mode": true,
    "real_personal_data": false
  }
}
```

## Trigger

```text
20:47
用户还在公司
手表状态：低能量，长时间未离开
日程：今天连续会议
天气：下雨
Memory：用户有常用应急补给包
```

## Mira Says

> 你现在可能不太舒服。我按你常用清单配了一个补给包，附近门店有货，预计 28 分钟到。要我帮你买过来吗？

## User

> 好。

## Execution

```text
instant-retail-skill
-> 查询附近库存
-> 选择 ETA 短且不超预算的商品
-> 创建订单预览
-> 用户确认
-> mock 下单
-> 返回配送 ETA
-> 预算记录
```

## Judge Console Readout

```text
[20:47:03] Heartbeat triggered
[20:47:04] 状态：晚间加班 / 长时间未离开 / 天气下雨
[20:47:05] Memory：用户常用应急补给包
[20:47:06] Skill selected：instant-retail-skill
[20:47:07] 库存匹配：附近便利店有货
[20:47:08] ETA：28min
[20:47:09] Policy：confirmation_required
[20:47:15] 用户确认
[20:47:16] Mock order created
[20:47:17] Budget updated
```

Run:

```bash
bash scripts/run_instant_retail_demo.sh
```
