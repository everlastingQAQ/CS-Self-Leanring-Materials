---
title: "HW 3：概念复习"
description: "CS61B Spring 2021 HW 3：概念复习中文学习资料。"
hide:
  - toc
---

# HW 3：Conceptual Review

- 原文件：`https://sp21.datastructur.es/materials/hw/hw3/hw3.pdf`
- 课程日历原截止：2021-05-03
- PDF 标题日期：2021-05-05
- 当年通过 Gradescope Quiz 提交最终答案

> **文档性质**：本文件依据 CS 61B Spring 2021 官方页面，由 ChatGPT 独立阅读后制作中文学习版。  
> 为保留技术准确性，类名、方法名、文件名、命令、报错文本和 API 名称保持英文。本文采用逐节翻译与重述，而不是网页的逐句镜像。

## 1. Heaps of Fun

### 数组堆操作

使用索引 0 留空的最小堆表示，按给定顺序执行 `add` 与 `removeMin`，写出最终数组。

### 判断题

判断命题是 always true、sometimes true 或 never true，并用理由或反例检查：

- `removeMin` 的复杂度。
- `add` 的上下界。
- 插入全局最小值后立刻删除，能否恢复原数组堆形态。
- 有重复值时上述结论是否变化。
- 堆数组是否整体有序。
- 交换每个节点左右子树后是否仍为合法最小堆。

重点：堆的合法性只要求父节点不大于子节点，不要求层序数组全局排序。

## 2. Shortest Paths

给定带权有向图，从 `S` 运行 Dijkstra：

- 写出访问 `B` 后的 `edgeTo` 和 `distTo`。
- 写出算法结束后的两个映射。
- 给出 `S` 到 `G` 的最短路径。
- 给出顶点访问顺序。
- 讨论负权边、权重统一缩放、树图上的更快算法和最短路径树唯一性。

输出格式要求严格，map 中顶点顺序不能改变。

## 3. MSTs

给定无向带权图：

- 从 `S` 运行 Prim。
- 写出访问特定顶点后的 priority queue。
- 写出结束状态。
- 按 Kruskal 顺序列出加入 MST 的边，并按字母规则处理同权边。

概念判断包括：

- 连通图 MST 边数。
- Prim 是否支持负边。
- 最大权边是否可能在 MST。
- Dijkstra 的 SPT 是否可能同时是 MST。
- 唯一边权是否保证唯一 MST。
- 非唯一边权是否必然导致多个 MST。
- 对正权平方是否保持所有 MST。
- 环中最小边是否一定出现在任意 MST。

## 4. Sorting

给定一个未排序数组和多列中间状态，识别：

- Insertion sort
- Selection sort
- Mergesort
- Quicksort
- Heapsort
- LSD radix sort
- MSD radix sort

题目指定：

- Quicksort 使用最左 pivot、无 shuffle、Tony Hoare partition。
- Heapsort 使用 bottom-up heapification 和 max heap。

还要讨论：

- 哪种排序在给定数组上的最佳情况可能最快。
- 有序数组、固定末元素 pivot 时 Quicksort 的复杂度。
- 三数组 partition 能否做稳定 Quicksort。
- Heapsort 的实际速度。
- 精确找 median 作为 pivot 是否值得。
- 两半分别 insertion sort 再 merge 是否稳定。

## 复习原则

这些题不是让你只背复杂度表，而是从算法的中间状态反向识别算法。练习时必须写出每一步的不变量。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/hw/hw3/hw3.pdf){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
