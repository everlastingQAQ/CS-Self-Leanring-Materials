---
title: "Lab 13：Project 3 交互"
description: "CS61B Spring 2021 Lab 13：Project 3 交互中文学习资料。"
---

# Lab 13：Project 3 Phase 2 入门——交互

- 原标题：Lab 13: Getting Started on Project 3, Phase 2
- 原页面：`https://sp21.datastructur.es/materials/lab/lab13/lab13`

> **文档性质**：本文件依据 CS 61B Spring 2021 官方页面，由 ChatGPT 独立阅读后制作中文学习版。  
> 为保留技术准确性，类名、方法名、文件名、命令、报错文本和 API 名称保持英文。本文采用逐节翻译与重述，而不是网页的逐句镜像。

## 实验目标

使用 `StdDraw` 与 `java.util.Random` 制作一个类似 Simon 的记忆游戏，为 BYOW Phase 2 的键盘交互、逐帧绘制和游戏循环做准备。

## 游戏规则

程序逐个闪现一串随机字符。玩家在字符消失后输入相同序列：

- 第一轮长度为 1。
- 每成功一轮，序列长度增加。
- 输入错误时游戏结束或显示失败状态。

## 需要实现的方法

### `generateRandomString`

生成指定长度的随机小写字符串。必须使用对象中统一维护的随机数生成器，以保证 seed 可复现。

### `drawFrame`

清空并重绘当前画面。应处理：

- 中央主文字。
- 轮数。
- 是否等待输入。
- 提示信息。
- 必要的双缓冲显示。

### `flashSequence`

按顺序显示目标字符，每个字符显示一段时间，字符之间留空白间隔。不要阻塞到完全无法刷新界面。

### `solicitNCharsInput`

监听键盘，收集恰好 `n` 个字符。每收到一个字符，可更新界面反馈。

### `startGame`

组织完整游戏循环：

1. 初始化轮数。
2. 生成目标字符串。
3. 闪现序列。
4. 获取玩家输入。
5. 比较结果。
6. 成功则进入下一轮。
7. 失败则结束。

## Helpful UI

原实验鼓励添加清晰的状态提示，例如：

- “Watch!”
- “Type!”
- 当前 round
- 成功或失败反馈

UI 不应只“能用”，还要让玩家知道程序当前处于哪种状态。

## 对 BYOW 的意义

Phase 2 同样需要：

- 键盘事件循环。
- 持续重绘。
- 模式切换。
- 可复现随机性。
- 将控制逻辑与绘制逻辑分开。

## 完成标准

所有指定方法实现，游戏可连续进行多轮，输入读取稳定，并按要求提交。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/lab/lab13/lab13){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
