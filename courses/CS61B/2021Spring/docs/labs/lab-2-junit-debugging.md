---
title: "Lab 2：JUnit 与调试"
description: "CS61B Spring 2021 Lab 2：JUnit 与调试中文学习资料。"
---

# Lab 2：JUnit 测试与调试

> 原文：https://sp21.datastructur.es/materials/lab/lab2/lab2<br>
> 说明：正文由 ChatGPT 直接翻译；代码、类名、方法名和 IDE 菜单名称保持原样。

## Lab 前准备

1. 完成 Lab 2 Setup。
2. 在课程仓库根目录运行：

```bash
git pull skeleton master
```

应获得 `lab2/` 文件夹。

## 简介

本 Lab 学习：

- 使用 IntelliJ Debugger；
- 在 IntelliJ 中编写和运行 JUnit 测试；
- 用测试定位并修复 `IntList` 相关错误。

按 Lab 2 Setup 中的 Project Setup 流程操作，但导入的是 `lab2/pom.xml`，不是 `lab2setup/pom.xml`。

## 调试器基础

### Breakpoint 与 Step Into

1. 打开并运行 `DebugExercise1.main`。
2. 控制台会打印三条语句，其中一条明显不正确。
3. 不要仅靠肉眼逐行找 bug。打印语句虽然有用，但有三个缺点：
   - 必须修改代码；
   - 必须提前知道要打印什么；
   - 大量文本输出不易阅读。
4. 用 Debug 模式运行 `DebugExercise1`。
5. 在 `int t3 = 3;` 所在行左侧点击，设置红色 breakpoint。
6. 再次 Debug，程序会在该行暂停。

调试时要采用“科学调试”思路：先提出对代码行为的假设，再用变量状态和单步执行验证或否定假设，逐步缩小 bug 范围。

若底部只显示 Debugger 而没有 Console，可把 Console 标签拖到右侧，使调试器与输出同时可见。

### Step Over、Step Into 与 Step Out

- **Step Over**：执行当前行，但不进入被调用方法内部。
- **Step Into**：进入当前行调用的方法。
- **Step Out**：运行到当前方法返回，然后回到调用方。

在 `DebugExercise2` 中：

1. 在 `main` 调用 `sumOfElementwiseMaxes` 的行设置 breakpoint。
2. Debug 后 Step Into 进入 `sumOfElementwiseMaxes`。
3. 对调用 `arrayMax` 的行使用 Step Over，观察结果是否符合预期。
4. 若结果异常，再重新运行并 Step Into `arrayMax` 定位问题。
5. 对 `max` 不要盲目 Step Into；先 Step Over 判断它的输入输出是否有问题。有 bug 时可直接重写。
6. 对 `arraySum` 与 `add` 重复相同过程。
7. 修复两个 bug 后，确认给定输入下 `sumOfElementwiseMaxes` 输出正确。这里只是检查，不构成严格正确性证明。

### 调试回顾

你应理解：

- breakpoints；
- step over；
- step into；
- step out。

IntelliJ 还有 Watches、Evaluate Expression、条件断点等功能，后续 Lab 会继续使用。

## JUnit 与单元测试

单元测试把程序拆成最小可测试单元，逐个验证方法及边界情况。它也会推动更好的代码结构：一个方法最好只做一件事。

打开 `ArithmeticTest.java`，观察 JUnit imports 和两个测试方法。基本格式：

```java
@Test
public void testMethod() {
    assertEquals(<expected>, <actual>);
}
```

- `assertEquals` 比较实际值和期望值。
- 每个测试方法前写 `@Test`。
- 一个测试可包含多个 `assertEquals` / `assertTrue`。
- JUnit 测试方法必须是非 `static`。

## 在 IntelliJ 中运行 JUnit

1. 打开 `ArithmeticTest.java`。
2. 选择 **Run → Run...**。
3. 选择带红绿箭头图标的 `ArithmeticTest`。
4. 失败信息会指出行号、期望值和实际值。

JUnit 会短路：一个测试方法中的第一个 assert 失败后，该方法停止，JUnit 继续运行下一个测试。点击失败栈中的 `ArithmeticTest.java:<line>` 可跳到对应代码行。

修复 `Arithmetic.java` 中的错误，可直接检查代码，也可用 Debugger 单步执行。

## 应用：IntList

### Starter Code

`IntList` 新增两个便利方法：

```java
IntList lst = IntList.of(1, 2, 3);
IntList empty = IntList.of();
IntList oneElem = IntList.of(7);
IntList manyElems = IntList.of(5, 4, 3, 2, 1);
```

`toString` / `print` 提供可读字符串表示：

```java
IntList lst = IntList.of(1, 2, 3);
System.out.println(lst.toString());
// Output: 1 -> 2 -> 3
```

这些方法主要用于简化测试的构造和错误输出。

### Part A：调试 `addConstant`

`IntListExercises.addConstant` 应原地给每个元素加常数：

```java
IntList lst = IntList.of(1, 2, 3);

addConstant(lst, 1);
System.out.println(lst.toString());
// Output: 2 -> 3 -> 4

addConstant(lst, 4);
System.out.println(lst.toString());
// Output: 6 -> 7 -> 8
```

Starter code 有 bug。`AddConstantTest.java` 提供三个测试。逐个 Debug 测试，定位并修复错误。

### Part B：嵌套 helper 与为调试重构

`setToZeroIfMaxFEL` 的规则：对链表中的每个结点，考察“从该结点开始的后缀链表”的最大值；若最大值的第一位与最后一位相同，则把当前结点值设为 `0`。`FEL` 即 first equals last。

例：

```text
55 -> 22 -> 45 -> 44 -> 5
```

变为：

```text
0 -> 22 -> 45 -> 0 -> 0
```

原因：

- 从 55 开始最大值为 55，首尾相同，55 置零。
- 从 22 开始最大值为 45，首尾不同，22 不变。
- 从 45 开始最大值为 45，首尾不同，45 不变。
- 从 44 开始最大值为 44，首尾相同，44 置零。
- 从 5 开始最大值为 5，首尾相同，5 置零。

先思考 `5 -> 535 -> 35 -> 11 -> 10 -> 0` 的结果，再查看 `SetToZeroIfMaxFELTest.testZeroOutFELMaxes3`。

运行测试后会发现 test 3 失败：

1. 在 `setToZeroIfMaxFEL` 第一行设置 breakpoint。
2. 只 Debug `testZeroOutFELMaxes3`。
3. 对嵌套表达式 `firstDigitEqualsLastDigit(max(p))`，IntelliJ 会要求选择进入哪个方法。
4. 为方便调试，把一行重构为：

```java
int currentMax = max(p);
boolean firstEqualsLast = firstDigitEqualsLastDigit(currentMax);
if (firstEqualsLast) {
    p.first = 0;
}
```

5. 先用 Step Over 找出哪一次 `max` 或 `firstDigitEqualsLastDigit` 返回错误，再 Step Into 错误方法。不要把每次调用的每一行都走一遍。
6. 找到并修复 bug。完成后可保留重构形式，也可改回一行。

真实开发中，理想做法是先分别测试 `max` 和 `firstDigitEqualsLastDigit`。

### Part C：棘手的 IntList——`squarePrimes`

`squarePrimes` 应：

- 原地把所有素数元素平方；
- 合数保持不变；
- 至少改动一个元素则返回 `true`，否则返回 `false`。

示例：

```java
IntList lst = IntList.of(14, 15, 16, 17, 18);
System.out.println(lst.toString());
// Output: 14 -> 15 -> 16 -> 17 -> 18

boolean changed = squarePrimes(lst);
System.out.println(lst.toString());
// Output: 14 -> 15 -> 16 -> 289 -> 18

System.out.println(changed);
// Output: true
```

方法使用 `Primes.isPrime(int x)`。把它当作黑盒：Step Over 检查输入输出，不必进入其复杂实现。

任务：

1. 编写多个 JUnit 测试，覆盖不同输入，同时检查链表修改结果和返回布尔值。
2. Starter test `SquarePrimesTest.testSquarePrimesSimple` 会通过，因此必须设计一个能失败的新测试。
3. 测试失败后，用 Debugger 定位 bug。
4. 修复 bug。修复本身代码很短，难点在定位。

## 提交

Push 到 GitHub，再提交到 Gradescope。部分测试为 Hidden，失败信息故意较模糊，目的是训练你独立测试与调试，而不是依赖 autograder 提示。

## 完整回顾

本 Lab 覆盖：

- Step Into / Over / Out；
- 单元测试整体思想；
- JUnit 语法；
- 编写 JUnit 测试；
- 用 JUnit 失败结果启动调试；
- Style Checker。

### 常见问题：`String` 或 `String.equals()` 显示为红色

这是 JDK 配置问题。打开 **File → Project Structure → Project → Project SDK**。例如 Java 版本为 15.0 时，应使用 15.0 SDK 和 Level 15 Project Language Level。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/lab/lab2/lab2<br){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
