---
title: "Lab 7：BSTMap"
description: "CS61B Spring 2021 Lab 7：BSTMap中文学习资料。"
---

# Lab 7：BSTMap

- 原标题：Lab 7: BSTMap
- 原页面：`https://sp21.datastructur.es/materials/lab/lab7/lab7`

> **文档性质**：本文件依据 CS 61B Spring 2021 官方页面，由 ChatGPT 独立阅读后制作中文学习版。  
> 为保留技术准确性，类名、方法名、文件名、命令、报错文本和 API 名称保持英文。本文采用逐节翻译与重述，而不是网页的逐句镜像。

## 实验目标

从零实现一个以二叉搜索树为核心的 `BSTMap`，并让它实现 `Map61B` 接口。完成后，与链表 Map `ULLMap` 和 Java `TreeMap` 比较性能。

## 核心文件

创建：

```text
BSTMap.java
```

类声明应实现 `Map61B<K, V>`。本 Lab 要求实现接口中的主要 Map 操作；`remove`、`iterator` 和 `keySet` 可以直接抛出：

```java
throw new UnsupportedOperationException();
```

## 建议的数据结构

定义内部节点：

```text
key
value
left
right
```

并维护：

- 根节点引用
- 当前键值对数量

二叉搜索树不变量：

- 左子树所有 key 小于当前 key。
- 右子树所有 key 大于当前 key。
- 相同 key 的 `put` 应更新 value，而不是增加 size。

## 需要完成的行为

重点方法通常包括：

- `clear`
- `containsKey`
- `get`
- `size`
- `put`
- `printInOrder`

递归实现很自然，但必须处理：

- 空树。
- 查找不存在的 key。
- 更新已有 key。
- 插入新 key 时正确增加 size。

## 性能比较

理论上：

- 平衡 BST 的查找和插入约为 `Θ(log N)`。
- 极度倾斜的 BST 最坏可退化为 `Θ(N)`。
- `ULLMap` 基于无序链表，查找通常为 `Θ(N)`。
- Java `TreeMap` 使用自平衡树，性能更稳定。

实验要求通过实际计时比较，而不是只背复杂度。

## 可选练习

原页面还提供额外的渐进复杂度问题和扩展功能。自学时可进一步实现：

- `keySet`
- `iterator`
- `remove`

## 完成标准

- 编译通过并实现要求的方法。
- 基础与随机测试通过。
- 重复 `put` 不错误增加 size。
- 能解释自己的树在最坏情况下为何可能退化。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/lab/lab7/lab7){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
