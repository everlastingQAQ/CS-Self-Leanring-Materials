---
title: "Project 3 第二阶段"
description: "CS61B Spring 2021 Project 3 第二阶段中文学习资料。"
---

# Project 3 Phase 2：Interactivity

- 原截止时间：2021-04-27 23:59 PT
- 原课程明确：不得使用 slip days
- 关联规格：Project 3: CS61BYoW

> **文档性质**：本文件依据 CS 61B Spring 2021 官方页面，由 ChatGPT 独立阅读后制作中文学习版。  
> 为保留技术准确性，类名、方法名、文件名、命令、报错文本和 API 名称保持英文。本文采用逐节翻译与重述，而不是网页的逐句镜像。

## Phase 2 必做

- 主菜单。
- Seed 输入界面。
- avatar 移动。
- HUD。
- 保存与加载。
- `interactWithKeyboard`。
- 完整 `interactWithInputString`。
- ambition feature。
- 人工 checkoff。

## 最重要的一致性

下面两种操作必须产生相同最终世界：

1. 一次性输入新建、移动、保存退出，再加载继续。
2. 将等价命令作为完整字符串执行。

保存不应改变世界逻辑结果，只改变状态存放位置。

## 推荐架构

```text
InputSource
    ↓
Command Parser
    ↓
Game State / Engine
    ↓
Renderer（键盘模式才显示）
```

可为键盘和字符串实现不同 InputSource，但后续命令处理必须共享。

## 保存方案

可保存：

- 完整游戏状态对象；或
- seed + 已执行命令历史；或
- 足以重建世界与玩家位置的结构化数据。

无论方案如何，都要支持关闭程序后重新运行加载。

## 提交前端到端测试

- 新建世界。
- 移动若干步。
- `:Q`。
- 新进程启动。
- `L`。
- 世界和 avatar 与退出前一致。
- 继续移动。
- 字符串接口得到同样结果。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
