---
title: "Lab 12：Project 3 图块渲染"
description: "CS61B Spring 2021 Lab 12：Project 3 图块渲染中文学习资料。"
---

# Lab 12：Project 3 入门——Tile Rendering Engine

- 原标题：Lab 12: Getting Started on Project 3
- 原页面：`https://sp21.datastructur.es/materials/lab/lab12/lab12`

> **文档性质**：本文件依据 CS 61B Spring 2021 官方页面，由 ChatGPT 独立阅读后制作中文学习版。  
> 为保留技术准确性，类名、方法名、文件名、命令、报错文本和 API 名称保持英文。本文采用逐节翻译与重述，而不是网页的逐句镜像。

## 开始前

- 执行 `git pull skeleton master`。
- 以 `proj3` 目录层级导入 IntelliJ，避免 package 问题。
- 阅读 Project 3 Phase 1。
- 与项目搭档尽早沟通。
- Project 3 是长期工程，不适合截止前突击。

## 实验目标

学习 BYOW 使用的二维 tile 渲染系统，并通过 Hex World 练习把抽象世界数据转换成屏幕图形。

## Part I：认识渲染引擎

观察两个示例：

- Boring World：按固定规则放置 tile。
- Random World：使用随机数选择 tile。

重点理解：

- 世界通常表示为 `TETile[][]`。
- 数组坐标与屏幕坐标的关系。
- `TERenderer` 负责把 tile 数组绘制到窗口。
- tile 本身描述字符、前景色、背景色和说明文字。

## Part II：Hex World

### 绘制单个六边形

编写辅助方法，根据边长和起始位置在世界数组中放置六边形。不要为每一行硬编码，应从几何规律计算：

- 每行宽度。
- 每行左侧偏移。
- 上半部分与下半部分的对称关系。

### 绘制六边形镶嵌

把单个六边形组合为规则图案。应拆分辅助方法，避免在一个巨大循环里同时处理形状、位置和 tile 选择。

## 随机性要求

使用统一的 `Random` 对象与确定 seed。相同 seed 应产生相同结果。不要在多个方法中随意 `new Random()`，否则难以复现。

## 对 Project 3 的意义

本 Lab 的代码不一定直接进入最终项目，但训练了：

- 二维世界表示。
- 坐标计算。
- 确定性随机生成。
- 渲染器调用。
- 通过辅助方法分解图形算法。

## 完成标准

- 能显示示例世界。
- 能绘制一个边长可变的六边形。
- 能绘制六边形镶嵌图。
- 无越界写入。
- 相同 seed 的随机效果可复现。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/lab/lab12/lab12){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
