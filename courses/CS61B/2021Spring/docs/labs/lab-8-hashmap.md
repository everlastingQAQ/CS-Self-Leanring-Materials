---
title: "Lab 8：HashMap"
description: "CS61B Spring 2021 Lab 8：HashMap中文学习资料。"
---

# Lab 8：HashMap

> 原文：https://sp21.datastructur.es/materials/lab/lab8/lab8<br>
> 说明：正文由 ChatGPT 直接翻译；接口、类名、方法名和代码保持原样。

## 简介

实现 `Map61B` 的哈希表版本 `MyHashMap`。完成后比较：

- `MyHashMap`
- 链表实现 `ULLMap`
- Java 内置 `HashMap`
- 使用不同 bucket 数据结构的多个 `MyHashMap` 子类。

## MyHashMap

### 必做接口

Starter code 位于 `MyHashMap.java`。实现 `Map61B` 的全部方法，但 `remove` 可抛：

```java
throw new UnsupportedOperationException();
```

本次必须实现：

- `keySet()`
- `iterator()`，遍历已存储 key

两者可按任意顺序返回 key。建议维护一个 `HashSet` 实例变量存放全部 key。

若想逐步实现，可先写出全部接口方法签名并抛异常，让项目先编译。

### Bucket 与工厂方法

哈希表 bucket 可使用 `LinkedList`、`ArrayList`、`TreeSet`、`PriorityQueue`、`HashSet` 等。Starter 利用多态、继承和 factory method 方便替换 bucket：

```text
Map61B.java
└── MyHashMap.java
    ├── MyHashMapALBuckets.java
    ├── MyHashMapHSBuckets.java
    ├── MyHashMapLLBuckets.java
    ├── MyHashMapPQBuckets.java
    └── MyHashMapTSBuckets.java
```

核心字段：

```java
private Collection<Node>[] buckets;
```

含义：

- `buckets` 是 `MyHashMap` 的 private 数组；
- 每个数组元素是一组 `Node`，即一个 bucket；
- `Node` 是保存单个 key-value mapping 的 private helper；
- `Collection` 是 `ArrayList`、`LinkedList`、`TreeSet`、`HashSet`、`PriorityQueue` 等共同实现的接口。

Java 不能直接创建泛型数组：

```java
new Collection<Node>[size] // 非法
```

应创建：

```java
new Collection[size]
```

然后只把 `Collection<Node>` 放入数组。

创建 bucket 时必须使用：

```java
protected Collection<Node> createBucket() {
    return new LinkedList<>();
}
```

不要在主实现中到处直接 `new LinkedList<>()`，因为子类需要 override `createBucket` 来提供不同 bucket 类型。还提供 `createTable` 和 `createNode` factory；后两者不强制使用，但为风格统一而存在。

### 构造方法

实现：

```java
public MyHashMap();
public MyHashMap(int initialSize);
public MyHashMap(int initialSize, double loadFactor);
```

默认值：

```text
initialSize = 16
loadFactor = 0.75
```

### 实现要求

1. 初始 bucket 数等于 `initialSize`。
2. 当前负载因子超过阈值时扩容：

```text
load = N / M
```

其中 `N` 为键值对数量，`M` 为 bucket 数。
3. 使用 separate chaining 解决冲突。
4. `MyHashMap.java` 只能导入 `ArrayList`、`LinkedList`、`Collection`、`HashSet`、`Iterator`、`Set`；主 bucket 类型必须为允许类型之一。
5. 对 `Collection<Node>[]` 只使用 `Collection` 接口支持的操作；需要的主要方法是 `add`、`remove`、`iterator`。
6. 查找 Node 时遍历 bucket，并用 `.equals()` 比较 key。
7. 必须乘法扩容，不要加法扩容；无需缩容。
8. 在 hashCode 分布良好的假设下，操作应为摊还常数时间。
9. `hashCode()` 可能为负数，计算 bucket index 时必须处理。
10. 重复插入同一个 key 时更新 value，不增加 size。
11. 可假设不会插入 `null` key。

### 测试

- `TestMyHashMap.java`：基本实现。
- `TestMyHashMapBuckets.java`：对每一种 bucket 子类复用基本测试。
- `TestHashMapExtra.java`：可选 remove 测试。

继续性能实验前必须通过前两个测试文件。

## HashMap 速度测试

完成实现后运行：

- `InsertRandomSpeedTest.java`
- `InsertInOrderSpeedTest.java`

随机测试读取输入规模 `N`，生成 `N` 个长度 10 的字符串，作为 `<String,Integer>` 插入 `MyHashMap`、`ULLMap` 和 Java `HashMap`。记录结果到：

```text
lab8/speedTestResults.txt
```

格式与数据点数量不限。

按序插入测试中，你的实现应大致落在 Java HashMap 同一数量级，通常在约 10 倍以内。讨论：什么时候更适合 `BSTMap` / `TreeMap`，而不是 `HashMap`？把回答写入结果文件。

## 更换 Bucket 类型的速度测试

运行 `speed/BucketsSpeedTest.java`。程序读取字符串长度 `L` 和操作规模 `N`，比较：

- `MyHashMapALBuckets`：`ArrayList`
- `MyHashMapLLBuckets`：`LinkedList`
- `MyHashMapTSBuckets`：`TreeSet`
- `MyHashMapPQBuckets`：`PriorityQueue`
- `MyHashMapHSBuckets`：`HashSet`

观察随 `N` 的扩展趋势，讨论并记录结果。

当前泛型实现为了只依赖 `Collection`，即使用 `TreeSet` 或 `HashSet` bucket，也会线性遍历整个 bucket。思考：若能利用 `TreeSet` 的对数查找或 `HashSet` 的常数查找，外层哈希表是否会进一步加速？无需实现，只记录讨论。

## 可选练习

- `remove(K key)`
- `remove(K key, V value)`
- 不维护第二个 key 集合变量而实现 `keySet` 与 `iterator`

`remove`：key 不存在返回 `null`；存在则删除并返回 value。

## 提交

提交：

- `MyHashMap.java`
- `speedTestResults.txt`

正常使用 Git 与 Gradescope。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/lab/lab8/lab8<br){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
