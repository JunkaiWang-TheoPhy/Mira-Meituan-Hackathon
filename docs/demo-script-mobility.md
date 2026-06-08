# Demo Script: Mobility

Duration: 45 seconds.

This demo shows that Mira manages life rhythm, not only shopping.

## Trigger

```text
22:00 Heartbeat
明早 8:00 mock 跨区会议
天气：下雨
历史风险：早高峰通勤可能延迟
```

## Mira Says

> 明早 8 点的会离你比较远，早高峰可能要 45 分钟。我建议 7:10 出发，要我帮你预约车吗？

## Execution

```text
npm run demo

schedule-mobility-skill
-> read upcoming schedule
-> estimate commute risk
-> propose departure plan
-> create ride reservation preview
-> wait for user confirmation
```
