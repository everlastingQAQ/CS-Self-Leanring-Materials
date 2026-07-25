---
title: "Lab 3：计时与随机测试"
description: "CS61B Spring 2021 Lab 3：计时与随机测试中文学习资料。"
---

# Lab 3：计时测试与随机对比测试

- 原标题：Lab 3: Timing Tests and Randomized Comparison Tests
- 原页面：`https://sp21.datastructur.es/materials/lab/lab3/lab3`

> **文档性质**：本文件依据 CS 61B Spring 2021 官方页面，由 ChatGPT 独立阅读后制作中文学习版。  
> 为保留技术准确性，类名、方法名、文件名、命令、报错文本和 API 名称保持英文。本文采用逐节翻译与重述，而不是网页的逐句镜像。

## 实验目标

本实验把“正确性”与“性能”放在一起训练：

- 为 `SLList` 和 `AList` 编写计时测试。
- 用随机对比测试寻找 `BuggyAList` 的错误。
- 学习 conditional breakpoint、resume 和 execution breakpoint。

## 1. AList 扩容策略计时

实验比较两种扩容思想：

- 加法式扩容：容量每次只增加固定值。
- 乘法式扩容：容量按比例增长。

加法式扩容会频繁复制数组，构造大列表时性能恶化；乘法式扩容的均摊性能更好。计时结果应通过表格观察输入规模增长时耗时如何变化，而不只看一次运行。

## 2. SLList 的 `getLast`

对不同长度的 `SLList` 反复调用 `getLast`，观察耗时随列表长度增长。单向链表若没有尾指针，获取最后元素需要从头走到尾，因此通常与列表长度成正比。

这也解释 Project 1 为什么要求 `LinkedListDeque.getLast` 的时间不依赖结构大小：设计中必须保留能直接访问末端的信息。

## 3. 随机对比测试

测试思路：

- `AListNoResizing` 很简单，可作为可信参考实现。
- `BuggyAList` 支持扩缩容，更复杂，也更可能有 bug。
- 对两个对象执行完全相同的随机操作。
- 每一步比较它们的返回值和状态。

先写固定序列测试，例如连续加入三个值，再连续删除三个值。随后把操作选择和数据改为随机生成。

## 4. 记录操作历史

随机测试失败时，仅知道“值不一样”还不够。应记录此前执行过的操作，使失败能被复现。例如打印：

```text
addLast(4)
addLast(7)
removeLast()
...
```

这样可以把随机失败变成确定性的最小调试案例。

## 5. 条件断点

当循环执行很多次时，普通断点会反复停住。条件断点可只在某个状态出现时暂停，例如：

- 列表大小等于某值
- 某次删除返回异常值
- 循环计数达到失败附近

`Resume` 用于继续运行到下一个断点；execution breakpoint 可在方法进入或退出时暂停。

## 完成标准

- 生成并解释两类计时表。
- 能从数据中区分加法扩容和乘法扩容。
- 完成随机对比测试。
- 能稳定复现并修复 `BuggyAList` 的 bug。
- 测试代码清晰，不依赖反复撞 Autograder。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/lab/lab3/lab3){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
