---
title: "Lab 3：计时与随机测试"
description: "CS61B Spring 2021 Lab 3：计时与随机测试中文学习资料。"
---

# Lab 3：计时测试与随机对比测试

> 原文：https://sp21.datastructur.es/materials/lab/lab3/lab3<br>
> 说明：正文由 ChatGPT 直接翻译；代码、类名、方法名和调试器选项保持原样。

## 简介

本 Lab 将：

- 为 `SLList` 和 `AList` 编写计时测试；
- 为有 bug 的 `AList` 实现编写随机对比测试；
- 学习 conditional breakpoint、resume 和 execution breakpoint。

## List61B 的计时测试

本部分必须使用 `timingtest` package，不要误用 `randomizedtest`。

### 测量使用糟糕扩容策略构造 AList

Starter `AList.addLast` 使用每次只增加 1 个容量的加法扩容：

```java
public void addLast(Item x) {
    if (size == items.length) {
        resize(size + 1);
    }

    items[size] = x;
    size = size + 1;
}
```

任务是在不同 `N` 下，用 `addLast` 构造 `AList` 并输出计时表。输出应类似：

```text
Timing table for addLast
           N     time (s)        # ops  microsec/op
------------------------------------------------------------
        1000         0.00         1000         0.20
        2000         0.01         2000         0.20
        4000         0.01         4000         1.20
        8000         0.04         8000         4.30
       16000         0.10        16000        10.00
       32000         0.50        32000        49.70
       64000         1.15        64000       114.80
      128000         3.74       128000       374.30
```

各列含义：

- `N`：最终数据结构大小；
- `time (s)`：所有操作总用时；
- `# ops`：`addLast` 调用次数；
- `microsec/op`：每次调用的平均微秒数。

本实验中 `N` 与 `# ops` 相同。重点是观察：随着列表变大，每次 `addLast` 的平均耗时明显增加，因此不是常数时间。

小规模数据的计时可能不可靠，原因包括缓存、进程切换、分支预测和计时器精度。分析经验结果时，重点看大 `N` 趋势。不同电脑的绝对时间不同没有关系，只要趋势一致。

### 改为良好扩容策略

把 `AList` 改为乘法扩容，再运行 `timeAListConstruction`。即使 `N = 128000`，构造也应非常快，每次添加只需不到一微秒的量级。

可选实验：

- 把最大 `N` 增加到 1000 万，观察单位操作时间是否仍大致恒定。
- 尝试不同扩容因子，例如 `1.01`：

```java
public void addLast(Item x) {
    if (size == items.length) {
        resize((int) (size * 1.01));
    }

    items[size] = x;
    size = size + 1;
}
```

使用非整数因子时注意取整，并保证新容量确实增大。

### 测量 `SLList.getLast`

有时要测的是“已经构造完成的数据结构上，某个方法的耗时如何随结构大小变化”。流程：

1. 创建 `SLList`。
2. 加入 `N` 个元素。
3. **此时才开始计时。**
4. 执行 `M` 次 `getLast`。
5. 停止计时，计算总时间与单位操作时间。

不要在构造列表前启动计时，否则会把构造成本混入 `getLast` 测量。

编辑 `TimeSLList.timeGetLast`，生成类似：

```text
Timing table for getLast
           N     time (s)        # ops  microsec/op
------------------------------------------------------------
        1000         0.02        10000         1.70
        2000         0.03        10000         3.10
        4000         0.06        10000         6.20
        8000         0.13        10000        12.50
       16000         0.25        10000        25.00
       32000         0.53        10000        52.80
       64000         1.35        10000       135.30
      128000         2.57        10000       257.30
```

这里始终执行 `M = 10000` 次，因此 `N` 与 `# ops` 不同。结果显示 `SLList.getLast` 会随列表增大而变慢。若结果看起来是常数时间，确认你测的是 `SLList` 而不是 `AList`。

Project 1 中的 `LinkedListDeque` 必须让相关端点操作与结构大小无关。思考：为什么 `SLList.getLast` 慢？你的 `LinkedListDeque` 用了什么设计使其更快？

## 随机对比测试

本部分使用 `randomizedtest` package。

### 简单对比测试

对比测试需要两个具有相同接口的实现：

- `AListNoResizing`：容量固定 1000，不实用但实现简单，可信度高，作为“参考实现”。
- `BuggyAList`：会扩容和缩容，逻辑更复杂，且已知含有 bug，作为“被测实现”。

先写 JUnit 测试 `testThreeAddThreeRemove`：

1. 向两个实现依次添加相同的三个值（例如 4、5、6）。
2. 连续调用三次 `removeLast`。
3. 每次都比较两个实现的返回值。

### 随机调用方法

新建 JUnit 测试 `randomizedTest()`，先只对 `AListNoResizing` 随机调用 `addLast` 与 `size`：

```java
AListNoResizing<Integer> L = new AListNoResizing<>();

int N = 500;
for (int i = 0; i < N; i += 1) {
    int operationNumber = StdRandom.uniform(0, 2);
    if (operationNumber == 0) {
        int randVal = StdRandom.uniform(0, 100);
        L.addLast(randVal);
        System.out.println("addLast(" + randVal + ")");
    } else if (operationNumber == 1) {
        int size = L.size();
        System.out.println("size: " + size);
    }
}
```

`StdRandom.uniform(0, 2)` 返回 `[0, 2)` 中的随机整数，即 0 或 1。

### Conditional Breakpoint 与 Resume

1. 在 `int operationNumber = ...` 行设置 breakpoint。
2. Debug 测试，打开 Java Visualizer。
3. Step Over 后观察 `operationNumber`。
4. 点击 **Resume**，程序会一直运行到再次命中 breakpoint。
5. 重复 Resume，观察数组逐渐填入元素。
6. 右击 breakpoint，在 Condition 中输入：

```java
L.size() == 12
```

7. Resume，程序会在列表大小达到 12 时暂停。
8. 完成练习后删除条件断点，避免影响后续调试。

### 加入更多随机操作

把随机操作扩展为：

- `addLast`
- `size`
- `getLast`
- `removeLast`

相应扩大 `StdRandom.uniform` 的范围。只有当 `L.size() > 0` 时才能调用 `getLast` 和 `removeLast`，否则会崩溃。

### 加入随机对比

为参考实现和 `BuggyAList` 执行完全相同的每一个操作；对有返回值的方法，用 JUnit 比较两个返回值。

### 运行随机测试

多运行几次测试，小 `N` 时可能通过也可能失败。把 `N` 提高到 5000，通常几乎每次都会失败。

随机测试的重要限制：

- 随机序列不一定触发隐蔽 bug；
- 不应替代精心设计的确定性单元测试；
- 更适合作为补充测试手段。

### 修复 Bug 与 Execution Breakpoint

失败时通常看到：

```text
java.lang.ArrayIndexOutOfBoundsException: Index 7 out of bounds for length 7
at randomizedtest.BuggyAList.resize(BuggyAList.java:31)
```

使用异常执行断点：

1. 打开 Breakpoints 窗口。
2. 勾选 **Any Exception**。
3. 设置条件：

```java
this instanceof java.lang.ArrayIndexOutOfBoundsException
```

4. Debug 测试，程序会在异常即将发生时暂停。
5. 在 Visualizer 中系统检查数组、size 和 resize 参数。

卡住时重点检查传给 `resize` 的参数，并追踪 `removeLast` 如何导致这个错误参数产生。

找到 bug 后修复并重跑随机测试。

**注意：**不要在没有条件时长期勾选 Any Exception，因为 JUnit 启动过程会产生并忽略一些内部异常，调试器会停在无关位置。完成后取消 Java Exception Breakpoints。

### 清理测试

随机测试中的打印日志只为教学方便。修复完成后删除所有 `System.out.println`，避免真实测试输出大量无用文本。工程中通常使用 logging，而不是直接 print；Project 1 Extra Credit 会进一步介绍。

## 总结

本 Lab 完成了：

- 经验测量构造数据结构的时间；
- 测量方法运行时间如何依赖结构大小；
- 两个实现之间的对比测试；
- 随机调用方法与随机对比；
- IntelliJ Resume；
- 条件断点；
- 异常执行断点。

## 提交

正常提交到 autograder。它会检查计时测试输出，以及修复后的 `BuggyAList` 是否正确。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/lab/lab3/lab3<br){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
