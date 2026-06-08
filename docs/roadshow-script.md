# Roadshow Script

## 30-Second Opening

Mira 不是一个“附近有什么”的搜索助手。它是一个基于 OpenClaw 风格机制的本地生活管家：先看懂你的状态，再把生活行动准备好，但涉及金钱和敏感上下文时必须等你确认。

## 90-Second Main Demo

现在是晚上 20:47，用户还在演示区域 A。手表状态低能量，日程显示连续会议后加班，天气下雨。Mira 的 heartbeat 触发后，不是推荐一堆店，而是识别为一个低打扰的即时生活需求。

Mira 选择 `instant-retail-skill`，用公开 mock 库存和预算生成常用补给包。Policy gate 判断这涉及金钱和敏感上下文，所以不能自动下单。用户确认后，系统创建 `demo-order-public-*`，返回 28 分钟 ETA，并把预算从 1260 记录到 1217.3。

## 15-Second Safety Note

这个仓库不调用真实平台 API，不创建真实订单，不采集真实健康、身份或位置数据。所有用户、区域、库存、预算和订单都是公开 mock seed。

## Closing Line

Mira 负责懂你，OpenClaw 负责调度，本地生活履约能力负责把事办成。
