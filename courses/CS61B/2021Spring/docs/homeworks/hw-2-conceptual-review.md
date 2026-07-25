---
title: "HW 2：概念复习"
description: "CS61B Spring 2021 HW 2：概念复习中文学习资料。"
hide:
  - toc
---

# HW 2：Conceptual Review

- 原文件：`https://sp21.datastructur.es/materials/hw/hw2/hw2.pdf`
- 原截止时间：2021-03-15
- 题目数量：5 个主题块

> **文档性质**：本文件依据 CS 61B Spring 2021 官方页面，由 ChatGPT 独立阅读后制作中文学习版。  
> 为保留技术准确性，类名、方法名、文件名、命令、报错文本和 API 名称保持英文。本文采用逐节翻译与重述，而不是网页的逐句镜像。

## 1. 渐进复杂度热身

分析一个递归函数：

- 每次调用先执行线性循环。
- 随后递归调用三个规模约为 `n/3` 的子问题。

要求给出最紧渐进界。重点是建立递推关系，而不是只看单层循环。

## 2. 渐进复杂度综合

包含四段代码，考察：

- 外层变量每次除以 2。
- 巨大但固定次数的内层循环在渐进分析中仍视为常数。
- 循环变量在内层被倍增，改变外层迭代次数。
- 外层规模递减、内层工作量随规模变化时如何写求和式。
- 列表 size 在循环过程中按非线性速度增长时，终止条件如何分析。

答案要求使用尽量简洁的 `Θ` 表达式，去除常数和低阶项。

## 3. WQU

对 0 到 10 的元素按给定顺序执行 `connect`，不使用路径压缩，画出 Weighted Quick Union 数组。

还要分析：

- 16 个连通元素的 Quick Union 最矮/最高树高。
- Weighted Quick Union 的最矮/最高树高。
- `connect` 与 `isConnected` 的最好和最坏复杂度。

## 4. 2-3 Tree 与 LLRB

给定一棵 2-3 树：

1. 转换为 Left-Leaning Red-Black Tree。
2. 插入 11。
3. 描述平衡过程中调用的 `rotateRight`、`rotateLeft`、`colorFlip` 操作。
4. 计算平衡后根到叶子的最长节点数。
5. 计算最长路径中的红链接数。

核心是理解 LLRB 如何编码 2-3 树，而不是机械背旋转模板。

## 5. 机械哈希

依次把一组字符串插入空哈希表：

- 字符串哈希值简化为字符串长度。
- 使用 separate chaining。
- 初始内部数组大小为 4。
- 负载因子等于 1 时容量翻倍。
- 最终画 box-and-pointer 图，并列出每个 bucket 的字符串。

必须在扩容后重新计算 bucket 下标。

## 练习建议

先独立作答，再检查：

- 渐进分析是否误把常数写入结果。
- WQU 是否正确维护负 size。
- LLRB 红链接是否全部左倾。
- 扩容时是否 rehash。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/hw/hw2/hw2.pdf){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
