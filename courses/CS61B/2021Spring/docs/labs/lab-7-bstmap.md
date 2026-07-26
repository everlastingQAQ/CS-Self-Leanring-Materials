---
title: "Lab 7：BSTMap"
description: "CS61B Spring 2021 Lab 7：BSTMap中文学习资料。"
---

# Lab 7：BSTMap

> 原文：https://sp21.datastructur.es/materials/lab/lab7/lab7<br>
> 说明：正文由 ChatGPT 直接翻译；接口、类名、方法名和代码保持原样。

## 简介

从零实现 `BSTMap`：以二叉搜索树为核心，实现 `Map61B` 接口。完成后比较：

- 你的 `BSTMap`；
- 基于无序链表的 `ULLMap`；
- Java 内置 `TreeMap`；
- 部分测试还会对比 `HashMap`。

## BSTMap 实现要求

在 `BSTMap.java` 中创建：

```java
public class BSTMap<K extends Comparable<K>, V> implements Map61B<K, V>
```

要求实现 `Map61B` 的全部方法，以下三个除外：

- `remove`
- `iterator`
- `keySet`

本 Lab 必做部分中，这些方法应抛出：

```java
throw new UnsupportedOperationException();
```

代码只有在类和所有接口方法签名都存在后才能编译。可以先为未完成的方法写占位实现并抛异常，再逐个完成。

额外实现不在接口中的：

```java
public void printInOrder()
```

它按 Key 递增顺序打印整张 map。Autograder 不检查输出，但调试很有用。

`K` 必须支持 `compareTo`，因此使用 bounded type parameter。建议定义 private nested `BSTNode` 类保存 key、value、left、right 等信息；具体设计自行决定。

使用 `TestBSTMap.java` 测试。可参考：Lecture 16 slides、课程参考书中的 BST 代码、Princeton Algorithms BST，以及已提供的 `ULLMap.java`。

## 性能测试

### `InsertRandomSpeedTest`

测试随机字符串插入速度。程序询问：

- 每个 String 的长度；
- 插入次数。

然后把随机 String 作为 key，与 Integer value 组成 `<String, Integer>` 对，插入：

- `BSTMap`
- `ULLMap`
- Java `TreeMap`
- Java `HashMap`

用足够大的输入观察渐近趋势，并把结果写入 `speedTestResults.txt`。格式和数据点数量不限。

### `InsertInOrderSpeedTest`

与随机测试类似，但按字典序递增插入字符串。运行后观察 BST 形状及性能变化，与同学或 TA 讨论。

## 可选实现

不计分，但 Autograder 可反馈：

- `iterator()`：返回遍历 key 的 iterator；
- `keySet()`；
- `remove(K key)`；
- `remove(K key, V value)`。

`remove` 规则：key 不存在返回 `null`；存在则删除 `(key, value)` 并返回 value。额外挑战是在不维护第二个“所有 key 集合”实例变量的情况下实现 `keySet` 与 `iterator`。

## 提交

提交：

- `BSTMap.java`
- `speedTestResults.txt`

正常通过 Git 和 Gradescope 提交。Lab 结束时 TA 会讲解参考实现。

## 可选渐近分析题

给定含 `N` 个键值对的 `BSTMap B`，以及随机键值对 `(K, V)`。除非另行说明，复杂度按比较次数计算。

判断 1–7 真/假：

1. `B.put(K, V)` ∈ O(log `N`)
2. `B.put(K, V)` ∈ Θ(log `N`)
3. `B.put(K, V)` ∈ Θ(`N`)
4. `B.put(K, V)` ∈ O(`N`)
5. `B.put(K, V)` ∈ O(`N²`)
6. 令 `g(N)` 为 `N` 次随机 `B.put(K,V)` 后再调用 `B.containsKey(K)` 的平均比较次数，则 `g(N) ~ 2 ln(N)`。这里 `g(N) ~ f(N)` 表示 `g(N)/f(N) -> 1`。
7. 对 `C != K`，同时运行 `B.containsKey(K)` 与 `B.containsKey(C)` ∈ Ω(log `N`)。

第 8 题：`numberOfNodes(b)` 对以 `b.root` 为根、含 `n` 个结点的 BSTMap 运行时间为 Θ(`n`)。给出 `mystery(b,z)` 在 `b` 含 `N` 个结点时最紧的 Big-O 界：

```java
public Key mystery(BSTMap b, int z) {
    if (z > numberOfNodes(b) || z <= 0)
        return null;
    if (numberOfNodes(b.left) == z - 1)
        return b.root.key;
    else if (numberOfNodes(b.left) > z)
        return mystery(b.left, z);
    else
        return mystery(b.right, z - numberOfNodes(b.left) - 1);
}
```

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/lab/lab7/lab7<br){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
