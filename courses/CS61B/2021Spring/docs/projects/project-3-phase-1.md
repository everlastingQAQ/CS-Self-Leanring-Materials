---
title: "Project 3 第一阶段"
description: "CS61B Spring 2021 Project 3 第一阶段中文学习资料。"
hide:
  - toc
---

# Project 3 Phase 1：World Generation

- 原截止时间：2021-04-16 23:59 PT
- 关联规格：Project 3: CS61BYoW

> **文档性质**：本文件依据 CS 61B Spring 2021 官方页面，由 ChatGPT 独立阅读后制作中文学习版。  
> 为保留技术准确性，类名、方法名、文件名、命令、报错文本和 API 名称保持英文。本文采用逐节翻译与重述，而不是网页的逐句镜像。

## Phase 1 必做

实现 `interactWithInputString` 的世界生成部分：

- 能解析 `N + seed + S`。
- 返回 `TETile[][]`。
- 同 seed 多次运行完全一致。
- 不同 seed 产生不同世界。
- 本阶段 grader 不测试移动。

## 推荐开发顺序

1. 创建全为 `NOTHING` 的世界。
2. 定义 Room/Region 数据结构。
3. 随机生成不重叠房间。
4. 连接房间。
5. 从 floor 推导 wall，或在绘制时维护墙。
6. 放置 avatar。
7. 用固定 seed 写回归测试。
8. 再接入 renderer 观察。

## 关键测试

```text
generate(123) == generate(123)
generate(123) != generate(124)
```

比较的是每个 tile，而不是对象引用。

## 失败风险

- 在方法内部多次无序创建 `Random`。
- 依赖系统时间。
- 房间生成失败后递归不受控。
- 走廊越界。
- 生成顺序受 HashSet/HashMap 非确定遍历影响。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
