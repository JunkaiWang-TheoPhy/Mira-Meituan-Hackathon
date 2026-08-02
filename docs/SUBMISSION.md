# 竞赛提交材料

## 作品名称

Mira：基于 OpenClaw 的本地生活私人管家

## 作品简介

Mira 是一个基于 OpenClaw 风格机制构建的本地生活私人管家。它不是“你问它答”的搜索助手，而是通过手表、眼镜、手机、日程和天气等状态事件，主动判断用户当下可能需要的生活行动，并在用户确认后完成 mock 推荐、mock 下单、配送 ETA 展示和预算记录。

当前主 Demo 聚焦即时零售：当用户处于晚间加班、低能量、天气下雨、临时缺少生活用品等状态时，Mira 会先选择 `period-care-restock` 规划常用补给包，再把 mock 库存、mock 配送时效和 mock 订单交给 `instant-retail-skill`。由于涉及金钱和敏感上下文，Mira 必须先通过 policy gate 并等待用户确认，之后才会生成 mock 订单和履约状态。

项目同时提供餐饮推荐、日程出行提醒、礼物鲜花规划、日用品补货和小钱包预算等扩展场景，展示 AI 从“更聪明的搜索框”走向“会主动安排生活节奏的本地生活管家”的可能性。

## 口号

工作交给别的工具，生活由 Mira 帮你安排。

## 技术亮点

- Heartbeat 主动触发：不是等待用户搜索，而是定时识别生活风险和机会。
- Memory 风格偏好：公开 mock 保存忌口、常用商品、预算和最近选择。
- Skill 封装：经期补货、即时零售、餐饮、出行、礼物鲜花、日用品和小钱包预算各自独立。
- Bridge/Safety Layer：OpenClaw 风格工具只看到高层生活动作，底层 mock API 被隔离。
- Policy gate：金钱、敏感上下文、位置和预算风险必须用户确认。
- Roadshow console：状态、事件、Skill、Policy、预算、履约六块视图。

## 团队分工

产品与路演角色负责产品定位、Demo 剧本和提交材料；Agent 架构角色负责 OpenClaw 风格 runtime、Skill 和 policy gate；工程角色负责 mock 本地生活服务、life bridge、前端控制台和测试；演示角色负责视频、现场节奏和评委 walkthrough。

## 作品链接

填写公开 GitHub 仓库或在线 Demo 页面。

## 补充链接

填写 Demo 视频、架构文档、路演脚本、评委 walkthrough 和 mock 数据说明。

## 非官方声明

本项目是 hackathon mock demo，不调用真实平台 API，不创建真实订单，不采集真实健康、身份或位置数据。所有用户、区域、库存、预算、订单和配送 ETA 均为公开演示数据。

## 收尾句

Mira 负责懂你，OpenClaw 负责调度，本地生活履约能力负责把事办成。
