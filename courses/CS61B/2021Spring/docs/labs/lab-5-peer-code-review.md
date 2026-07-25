---
title: "Lab 5：同伴代码审查"
description: "CS61B Spring 2021 Lab 5：同伴代码审查中文学习资料。"
---

# Lab 5：Project 1 同伴代码审查

- 原标题：Lab 5: Project 1 Peer Code Review
- 原页面：`https://sp21.datastructur.es/materials/lab/lab5/lab5`

> **文档性质**：本文件依据 CS 61B Spring 2021 官方页面，由 ChatGPT 独立阅读后制作中文学习版。  
> 为保留技术准确性，类名、方法名、文件名、命令、报错文本和 API 名称保持英文。本文采用逐节翻译与重述，而不是网页的逐句镜像。

## 前置纪律

原课程会在 Lab 中展示部分 Project 1 官方实现。因此必须先完成 Project 1 的最终提交，再参加本 Lab；看过官方方案后继续提交项目会构成学术诚信问题。

## 实验目标

与 1～3 名同学比较 Project 1 实现，重点审查：

- `LinkedListDeque`
- `ArrayDeque`

目的不是选出“谁写得最好”，而是理解同一个 API 可以有不同设计，并从别人代码中发现自己的可改进点。

## 1. LinkedListDeque 审查

关注：

- 是否使用 sentinel。
- 空 deque 时指针关系是否统一。
- `addFirst`、`addLast` 是否为常数时间。
- `removeFirst`、`removeLast` 是否正确维护双向链接。
- `get` 与递归版 `getRecursive` 是否边界正确。
- 是否存在重复分支和特殊情况堆叠。

## 2. ArrayDeque 审查

关注：

- 环形数组的索引设计。
- `nextFirst` 与 `nextLast` 的含义是否一致。
- 扩容时元素是否按逻辑顺序复制。
- 缩容阈值是否符合规格。
- 空结构和单元素结构是否正确。
- 是否频繁移动所有元素，导致操作退化。

## 3. 代码质量维度

审查时不只看“能不能通过测试”，还要讨论：

- 命名是否表达意图。
- 辅助方法是否减少重复。
- 不变量是否清晰。
- 边界条件是否集中处理。
- 注释是否解释原因，而不是复述代码。
- 实现是否过度复杂。

## 4. 自我反思与提交

记录至少几个具体发现：

- 自己做得好的设计。
- 别人方案中值得吸收的思路。
- 未来会怎样重构。
- 哪些错误本可通过更好的测试提前发现。

## 完成标准

完成同伴比较、填写自我反思，并按原课程要求提交 checkoff/反思材料。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/lab/lab5/lab5){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
