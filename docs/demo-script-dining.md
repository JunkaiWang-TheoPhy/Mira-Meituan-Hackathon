# Demo Script: Dining

Duration: 45 seconds.

Mira should not say “附近有几家店，要不要看看？” The point is not search.
The point is a state-aware recommendation.

## Trigger

```text
last_meal_hours = 7.5
recent_food = 麻辣烫, 炸鸡
avoid = 香菜, 太辣
weather = rain
location_label = 演示区域A
budget_remaining = 1217.3
```

## Mira Says

> 你今天午饭吃得少，现在又加班到这个点了。我避开了你最近吃腻的重口味，给你选了一份清淡热汤面，35 分钟到。要我下单吗？

Run all scenarios:

```bash
npm run demo
```
