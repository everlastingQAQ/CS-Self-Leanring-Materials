---
title: "Lab 13：Project 3 交互"
description: "CS61B Spring 2021 Lab 13：Project 3 交互中文学习资料。"
---

# Lab 13：Project 3 Phase 2——交互入门

> 原文：https://sp21.datastructur.es/materials/lab/lab13/lab13<br>
> 说明：正文由 ChatGPT 直接翻译；API、类名、方法名和代码保持原样。

## 简介

本 Lab 为 Project 3 第二阶段“Interactivity”做准备。此时不要求 Phase 1 完全结束，但应已接近完成。Lab 代码不会直接进入 Project 3，而是训练 `StdDraw`、随机数、键盘输入和 UI 组织方式。

## Memory Game

使用 `StdDraw` 与 `java.util.Random` 构建类似 Simon 的键盘记忆游戏：

1. 创建游戏窗口。
2. 随机生成目标字符串。
3. 每次显示一个字符。
4. 等待玩家输入同样数量的字符。
5. 正确则进入更长的一轮；错误则显示 Game Over 并结束。

目标字符串第一轮长度为 1，每成功一轮长度加 1。

关键工程原则：先实现职责明确的小过程，再组合成复杂方法。这样 `main` 最终只需少量高层代码，也便于单元测试。

## `generateRandomString`

1. 修改 `MemoryGame` 构造方法，使用第一个程序参数作为 seed 创建 `Random`。
2. 实现 `generateRandomString(int n)`，使用该 `Random` 生成长度为 `n` 的小写字符串。
3. 使用 starter 中的 private `CHARACTERS` 字段。
4. 可直接使用 `java.util.Random`，也可用 `byow.Core.RandomUtils`；后者底层仍调用传入的 `Random`。

Java 字符提示：

```java
char c = 'B';
String s = "and can be longer";
String favClass = "CS 61" + 'B';
String B = Character.toString('B');
```

## `drawFrame`

本 Lab 直接使用 Princeton `StdDraw`，不是 Tile Engine。`StdDraw` 更新画面时需要清空画布并重画整个 frame。

实现 `drawFrame(String s)`：

1. 清空 canvas；
2. 设置大号粗体字体（size 30 合适）；
3. 把输入字符串居中绘制；
4. 显示 canvas。

相关 API：

- `StdDraw.setFont`
- `StdDraw.clear`
- `StdDraw.text`
- `StdDraw.setPenColor`
- `StdDraw.show`

## `flashSequence`

输入目标字符串，逐字符居中显示：

- 每个字符显示 1 秒；
- 字符之间空白 0.5 秒。

## `solicitNCharsInput`

使用：

- `StdDraw.hasNextKeyTyped()`：检查键盘队列中是否还有按键；
- `StdDraw.nextKeyTyped()`：取出并返回最早按下的字符。

实现方法读取 `n` 个按键，拼成字符串并返回。玩家每输入一个字符，都应把当前累计字符串居中显示，让玩家看到已输入内容。

`nextKeyTyped` 返回 `char`，因此只能处理对应字符的键。本 Lab 不实现 Backspace 删除功能。

## `startGame`

把所有子过程组合为完整游戏：

1. 从 round 1 开始。
2. 居中显示 `Round: <round>`。
3. 生成长度等于 round 的随机字符串。
4. 逐字符闪现目标。
5. 读取相同长度输入。
6. 比较：
   - 正确：round 加 1，回到步骤 2；
   - 错误：结束，并居中显示 `Game Over! You made it to round: <round>`。

完成后 `MemoryGame.java` 应可直接运行和游玩。

## 改进 UI

功能完成后，修改 `drawFrame`：游戏未结束时在顶部绘制状态栏：

- 左侧：`Round: <round>`；
- 中间：当前任务 `Watch!` 或 `Type!`；
- 右侧：随机鼓励语。

Starter 提供 `ENCOURAGEMENT` 集合，可自行增加内容。

## 提交与评分

本 Lab 没有 Gradescope code grader。按当学期要求，在截止时间前提交 **Phase 1 Review Form** 即获得 64 分。

即使不直接评分，也强烈建议完成可运行版本；Project 3 遇到渲染或交互问题时，这个小程序可作为清晰参考。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/lab/lab13/lab13<br){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
