---
title: "Project 1 EC：自动评分器"
description: "CS61B Spring 2021 Project 1 EC：自动评分器中文学习资料。"
---

# Project 1 额外加分：自动评分器

> 原始页面：<https://sp21.datastructur.es/materials/proj/proj1/proj1ec>
>
> 可选项目，共 32 分额外加分。正文已翻译，代码与精确失败序列格式保持原样。

## 一、目标

你将为 Project 1 的 `ArrayDeque` 编写一个基础随机自动评分器：不断对一个有 bug 的学生实现和一个正确实现执行相同操作，在两者结果第一次不一致时，让 JUnit 测试失败，并显示能复现问题的操作序列。

骨架包含：

- `student/StudentArrayDeque.java`：有 bug 的实现；
- `tester/ArrayDequeSolution.java`：正确实现；
- `tester/AssertEqualsStringDemo.java`：`assertEquals` 消息示例；
- `tester/StudentArrayDequeLauncher.java`：学生实现使用示例。

包用于隔离学生代码和测试基础设施。

获取骨架：

```bash
git pull skeleton master
```

先运行 `StudentArrayDequeLauncher.java`。若环境正确，会打印 0 到 9，顺序不一定固定。

## 二、随机测试

Project 1 正式自动评分器也大量使用随机差分测试：对学生实现和参考实现调用同样的随机操作，一旦结果不同，就打印导致失败的操作序列。

## 三、任务 I：发现错误

在 `tester` 包中新建：

```text
TestArrayDequeEC.java
```

顶部：

```java
package tester;

import static org.junit.Assert.*;
import org.junit.Test;
import student.StudentArrayDeque;
```

编写一个带 `@Test` 的 JUnit 测试，方法名不限。

测试应：

1. 创建 `StudentArrayDeque<Integer>`；
2. 创建 `ArrayDequeSolution<Integer>`；
3. 使用 `StdRandom` 随机选择操作；
4. 对两者执行完全相同的操作；
5. 对有返回值的操作比较结果；
6. 一旦不同，使用断言失败。

不测试：

- `equals(Object o)`；
- `iterator()`。

只使用以下操作就足以找到 bug：

- `addFirst`
- `addLast`
- `removeFirst`
- `removeLast`

也可以测试 `get`、`size` 等。

### 避免空指针

不要从空 deque 删除。

获取返回值时必须用：

```java
Integer x = deque.removeFirst();
```

而不是：

```java
int x = deque.removeFirst();
```

学生实现可能错误地返回 `null`。把 `null Integer` 自动拆箱为基本类型 `int` 会在你的测试代码中抛出 `NullPointerException`，这不是本项目期望的失败方式。

若复制 `StudentArrayDequeLauncher` 的代码，应在 Javadoc 中使用 `@source` 标注来源。

## 四、任务 II：生成有用的失败序列

只说“测试失败”对学生没有帮助。改用：

```java
assertEquals(message, expected, actual);
```

`message` 必须精确包含从测试开始到失败为止的操作序列，而且最后一条必须是产生错误返回值的操作。

例如：

```text
addFirst(5)
addFirst(3)
removeFirst()
```

不要在消息中添加 expected/actual：

```text
addFirst(5)
addFirst(3)
removeFirst(), student was 3, correct was 7
```

上面是错误格式，因为 JUnit 已经通过 `expected` 和 `actual` 参数显示这些值。

也不能记录失败之后的操作，或在一条操作后附加返回值：

```text
addFirst(5)
addFirst(3)
removeFirst(): 3
removeLast(): 4
```

### 推荐做法

随着每次随机操作同步累积：

```java
String message = "";
message += "addFirst(" + value + ")\n";
```

对无返回值操作只追加记录；对有返回值操作，先追加该操作，再比较结果：

```java
message += "removeFirst()\n";
assertEquals(message, solutionResult, studentResult);
```

不要等失败后再尝试重建序列，因为很容易漏掉操作或顺序。

## 五、提示

- 不建议每次比较整个 deque；这无法指出哪一个操作首次返回错误；
- 直接比较 `removeFirst`、`removeLast`、`get`、`size` 的单个返回值更合适；
- `assertEquals(deque1, deque2)` 不会自动逐元素比较，除非该类实现了合适的 `equals`；
- 使用 `StdRandom` 生成操作类型和值；
- 不需要编写异常捕获或主动抛异常；
- 失败必须来自 JUnit 断言，而不是运行时异常；
- 保持测试可重复调试时，可临时固定随机种子，但最终仍应稳定发现 bug。

## 六、FAQ

### 如何测试 `printDeque()`？

需要重定向标准输出，较复杂，且该额外加分评分器不会可靠解析它。测试其他方法即可。

### `reference to assertEquals is ambiguous`

这是重载和自动装箱导致的类型歧义。显式统一 expected 与 actual 类型，例如都使用 `Integer`，并检查导入的断言版本。

### 一直出现 `NullPointerException`

检查：

1. 是否在空队列删除；
2. 是否越界 `get`；
3. 是否把返回值保存到 `int` 而不是 `Integer`。

自动拆箱：

```java
Integer value = null;
int x = value; // NullPointerException
```

### 自动评分器说失败序列格式错误

失败断言的 message 必须：

- 只包含操作序列；
- 每个操作占一行；
- 不含额外解释、返回值或 expected/actual；
- 最后一行必须是首次产生错误结果的操作；
- 测试不得因空指针等异常失败；
- 同一失败序列不要重复出现。

如果是 `size()` 首次错误，必须在序列末尾加入：

```text
size()
```

### 序列仍无法复现

把在线评分器报告的序列复制到一个简单 `Quick.java`：

1. 新建 `StudentArrayDeque`；
2. 按顺序执行所有操作；
3. 打印最后一步结果；
4. 与测试报告对比。

若不一致，通常是测试日志漏记了一步、记录了没执行的操作，或在执行顺序上有偏差。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/proj/proj1/proj1ec){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
