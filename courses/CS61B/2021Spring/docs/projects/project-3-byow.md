---
title: "Project 3：CS61BYoW"
description: "CS61B Spring 2021 Project 3：CS61BYoW中文学习资料。"
---

# Project 3：CS61BYoW

- 原标题：Project 3: CS61BYoW
- 原页面：`https://sp21.datastructur.es/materials/proj/proj3/proj3`
- Phase 1 原截止：2021-04-16
- Phase 2 原截止：2021-04-27

> **文档性质**：本文件依据 CS 61B Spring 2021 官方页面，由 ChatGPT 独立阅读后制作中文学习版。  
> 为保留技术准确性，类名、方法名、文件名、命令、报错文本和 API 名称保持英文。本文采用逐节翻译与重述，而不是网页的逐句镜像。

## 项目目标

与搭档实现 Build Your Own World：

- 根据 seed 生成可探索的随机二维世界。
- 用 tile renderer 显示世界。
- 通过键盘控制角色。
- 支持保存和加载。
- 让字符串输入接口与键盘接口产生一致结果。
- 完成额外游戏功能和人工 checkoff。

这是一个开放度很高的软件工程项目，课程不会规定唯一地图算法。

## Skeleton 结构

核心包通常包括：

- `Core`
- `TileEngine`

关键入口：

- `Core.Main`
- `Core.Engine`
- `interactWithKeyboard()`
- `interactWithInputString(String input)`

应尽量少改 `Main`，把工作委托给 Engine 和自己设计的类。

## Phase 1：World Generation

世界使用 `TETile[][]` 表示。要求：

- 地图具有明显房间、走廊或类似可探索结构。
- 世界不能大面积无意义随机散点。
- 地板区域相连，角色能探索合理区域。
- 边界和墙体视觉正确。
- 相同 seed 必须生成完全相同的世界。
- 不同 seed 应生成不同世界。
- 返回的 tile 数组尺寸和方向符合 skeleton。

随机数必须来自同一个由 seed 初始化的 `Random` 对象。所有生成决策按确定顺序执行。

## 主菜单与 Seed 输入

`interactWithKeyboard()` 启动后至少提供：

- `N`：新世界
- `L`：加载
- `Q`：退出

选择新世界后输入数字 seed，并用 `S` 结束 seed 输入。界面应显示当前输入的 seed。

## Design Document

文档包含：

1. Classes and Data Structures
2. Algorithms
3. Persistence

要明确：

- 世界如何表示。
- 房间/走廊如何生成和连接。
- 玩家状态放在哪里。
- 输入如何被解析。
- 存档保存什么。
- 键盘输入和字符串输入如何复用逻辑。

## Phase 2：Interactivity

### UI 外观

提供主菜单、游戏世界与 HUD。鼠标悬停时，HUD 应显示 tile 的描述或环境信息。

### UI 行为

玩家通过键盘移动。不能穿墙；合法移动更新 avatar 位置。程序应持续响应输入并重绘。

### 保存与加载

规格使用类似 `:Q` 的命令保存并退出。加载后必须恢复与退出前相同的世界和玩家状态。

### 字符串输入

例如：

```text
n123sssww:q
l...
```

`interactWithInputString` 不显示 GUI，而是返回处理完全部输入后的世界。键盘和字符串模式必须共享同一命令语义。

## Ambition Score

项目要求实现额外功能。原页面列出许多候选方向，例如：

- 改变 avatar 外观或名字。
- 不同主题世界。
- 多语言界面。
- 鼠标菜单。
- 图片 tile。
- 音乐和音效。
- 小地图。
- 世界旋转。
- 日期时间 HUD。
- 点击寻路。
- 双人游戏。

选择功能时应优先完成可测试、与核心架构兼容的一项，而不是堆很多半成品。

## Grader

Phase 1 主要测试：

- 能返回世界。
- 同 seed 可复现。
- 不同 seed 有差异。

Phase 2 主要测试：

- seed 与移动序列决定性。
- 保存加载与连续输入等价。
- 字符串接口行为稳定。

大部分项目分数还来自人工 checkoff，因此“只过 autograder”不等于项目完整。

## 提交前检查

- 搭档信息正确。
- 相同 seed 与输入始终可复现。
- 输入解析大小写和终止规则正确。
- 键盘和字符串接口共用状态机。
- 存档从全新进程可恢复。
- 世界可探索、无明显越界或破碎边界。
- Design Document 更新。
- Demo 流程已排练。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/proj/proj3/proj3){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
