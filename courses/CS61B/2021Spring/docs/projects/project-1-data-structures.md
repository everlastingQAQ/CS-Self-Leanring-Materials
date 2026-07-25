---
title: "Project 1：数据结构"
description: "CS61B Spring 2021 Project 1：数据结构中文学习资料。"
---

# Project 1：Data Structures

- 原标题：Project 1: Data Structures
- 原页面：`https://sp21.datastructur.es/materials/proj/proj1/proj1`
- 原截止时间：2021-02-16

> **文档性质**：本文件依据 CS 61B Spring 2021 官方页面，由 ChatGPT 独立阅读后制作中文学习版。  
> 为保留技术准确性，类名、方法名、文件名、命令、报错文本和 API 名称保持英文。本文采用逐节翻译与重述，而不是网页的逐句镜像。

## 项目目标

实现双端队列 Deque 的两种底层结构，并通过接口、泛型、迭代器和 `equals` 建立可替换抽象：

- `LinkedListDeque<T>`
- `ArrayDeque<T>`
- `Deque<T>` 接口
- `MaxArrayDeque<T>`
- 使用 deque 完成 Guitar Hero 扩展

## Deque API

两种实现都应支持：

```java
addFirst(T item)
addLast(T item)
isEmpty()
size()
printDeque()
removeFirst()
removeLast()
get(int index)
iterator()
equals(Object o)
```

规则：

- `remove` 空结构时返回 `null`。
- `get` 不修改结构。
- `equals` 比较逻辑内容与顺序，不要求底层实现相同。
- 迭代器按从前到后的顺序遍历。

## 1. `LinkedListDeque`

推荐使用双向链表与 sentinel。目标复杂度：

- 两端添加：常数时间
- 两端删除：常数时间
- `size`：常数时间
- `get`：线性时间
- 可额外实现递归 `getRecursive`

关键不变量：

- sentinel 的 `next` 指向第一个节点。
- sentinel 的 `prev` 指向最后一个节点。
- 空结构时两者都指回 sentinel。
- 每个真实节点的前后链接互相一致。

## 2. `ArrayDeque`

使用环形数组，避免每次在头部插入时移动全部元素。常见字段：

- items 数组
- size
- `nextFirst`
- `nextLast`

必须正确处理：

- 下标绕回。
- 扩容。
- 使用率过低时缩容。
- 扩缩容后逻辑顺序不变。
- 泛型数组创建需要类型转换。

不要用 Java 自带集合代替核心实现。

## 3. `Deque` 接口

把共同 API 放入 `Deque.java`，让两种实现都实现它。这样使用者依赖的是行为契约，而不是具体底层结构。

## 4. `iterator` 与 `equals`

`iterator()` 使 deque 可用于 enhanced for。

`equals(Object o)` 应：

1. 处理自身比较。
2. 判断参数是否为 Deque。
3. 比较 size。
4. 逐项使用元素自身的 `equals`。
5. 正确处理 `null` 规则。

不要通过把对象强制转换成某个具体实现来比较。

## 5. `MaxArrayDeque`

在 `ArrayDeque` 基础上接收 `Comparator<T>`，提供：

- 使用默认 comparator 的 `max()`
- 使用临时 comparator 的 `max(Comparator<T>)`

空 deque 时按规格返回相应结果。

## 6. Guitar Hero

项目用 deque 模拟 Karplus–Strong 弦乐算法。你需要理解数据结构不只是练习题，它能作为实时音频系统中的循环缓冲区。

## 测试

应自己编写 JUnit：

- 空结构。
- 单元素。
- 两端交替增删。
- 扩容边界。
- 缩容边界。
- 环形索引跨越数组末端。
- 两种实现之间的 `equals`。
- iterator 顺序。

## 提交前检查

- 所有方法满足复杂度要求。
- 不使用禁止的数据结构。
- 没有内存引用长期保留已删除元素。
- `equals` 对不同实现有效。
- Project 1 最终提交必须在参加 Lab 5 前完成。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/proj/proj1/proj1){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
