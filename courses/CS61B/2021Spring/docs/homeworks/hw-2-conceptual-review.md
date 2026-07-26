---
title: "HW 2：概念复习"
description: "CS61B Spring 2021 HW 2：概念复习中文学习资料。"
---

# Homework 2：概念复习

> 原文：https://sp21.datastructur.es/materials/hw/hw2/hw2.pdf<br>
> 日期：2021 年 3 月 15 日<br>
> 说明：题目正文由 ChatGPT 直接翻译；代码、方法名与数学符号保持原样。

## 1. 渐近分析热身

请给出 `foo(n)` 最紧确的渐近界。

```java
public int foo(int n) {
    if (n == 0) {
        return 0;
    }
    bloop(n);
    return foo(n / 3) + foo(n / 3) + foo(n / 3);
}

public int bloop(int n) {
    for (int i = 0; i < n; i += 1) {
        System.out.println("Ah, loops too");
    }
    return n;
}
```

## 2. 渐近分析杂题

**注意：**这些题比较难。若某题卡了很久，请先做其他题，并在 Ed 发帖或参加 Office Hours。对下列方法，请用 Θ 记号给出运行时间。答案应写成关于 `N` 的尽可能简单的函数，不要保留不必要的首项常数或低阶项。

### (a) `mystery1(n)`

```java
public void mystery1(int n) {
    for (int i = n; i > 0; i = i / 2) {
        for (int j = 0; j < 100000000; j += 2) {
            System.out.println("Hello World");
        }
    }
}
```

给出 `mystery1(n)` 的 Θ 运行时间。

### (b) `mystery2(n)`

```java
public void mystery2(int n) {
    for (int i = 1; i < n; i += 1) {
        for (int j = 0; j < n; j += 1) {
            i = i * 2;
            j = j * 2;
        }
    }
}
```

给出 `mystery2(n)` 的 Θ 运行时间。

### (c) `mystery3(n)`

下面哪一个求和式能够表示 `mystery3(n)` 完成的工作量？不必化简求和式，只需写出开头若干项和最后一项。

```java
public void mystery3(int n) {
    for (int i = n; i > 0; i = i / 2) {
        for (int j = 1; j < i * i; j *= 2) {
            System.out.println("Hello World");
        }
    }
}
```

### (d) `mystery4(n)`

给出 `mystery4(n)` 的 Θ 运行时间。假设 `SLList` 构造方法、`size` 和 `addFirst` 方法均为常数时间。

```java
public void mystery4(int n) {
    SLList<Integer> list = new SLList<>();
    for (int i = 1; list.size() < n; i += 1) {
        for (int j = 0; j < i; j += 1) {
            list.addFirst(j);
        }
        System.out.print(list.size() + " + ");
    }
}
```

## 3. WQU（加权 Quick Union）

### (a)

画出元素编号为 `0` 到 `10` 的 Weighted Quick Union 对象，它由下列 `connect` 调用产生。**不要使用路径压缩。**同时写出最终底层数组。

当连接两个权重相同的集合时，用根编号较大的集合做父集合；这与 Discussion 6 中的平局规则相反。

```java
connect(0, 1);
connect(2, 3);
connect(9, 5);
connect(5, 7);
connect(7, 1);
connect(4, 2);
connect(3, 1);
```

### (b)

假设单个结点的高度为 `0`。对于包含 16 个已连接元素的 Quick Union 对象：

- 可能的最小高度是多少？
- 可能的最大高度是多少？

对于 Weighted Quick Union 对象，再回答同样两个问题。

### (c)

对于包含 `N` 个已连接元素的 Quick Union 对象，`connect` 与 `isConnected` 的最好和最坏运行时间分别是什么？对于 Weighted Quick Union 对象又如何？

## 4. Switcheroo

### (a)

考虑下面的 2-3 树。把它转换为 LLRB（左倾红黑树），然后插入数字 `11`。描述为了重新平衡树而执行的 **6 个 LLRB 操作**。可用的操作为：

- `rotateRight(x)`
- `rotateLeft(x)`
- `colorFlip(x)`

原始 2-3 树：

```text
                         [20]
                 /                   \
             [9, 17]                [24, 40]
          /      |      \          /    |      \
       [3,5]  [10,15]  [18]     [21,23] [30] [50,51]
```

### (b)

插入 `11` 并完成 LLRB 平衡后，从根到叶子的最长路径上共有多少个结点？

### (c)

插入 `11` 并完成 LLRB 平衡后，从根到叶子的最长路径上共有多少条红链接？

## 5. 手工哈希

假设把下列单词按给定顺序插入一张起初为空的哈希表：

```text
kerfuffle, broom, hroom, ragamuffin, donkey, brekky,
blob, zenzizenzizenzic, drap
```

假设：

1. `String` 的哈希码就是字符串长度（注意：Java 实际并非这样实现）。
2. 使用**分离链表法（separate chaining）**解决冲突。
3. 哈希表内部数组初始长度为 `4`。
4. 当负载因子等于 `1` 时，把内部数组长度翻倍。

请用盒子与指针图画出最终哈希表。对最终哈希表中的每个索引，写出其中存储的所有字符串；若为空，写 `none`。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/hw/hw2/hw2.pdf<br){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
