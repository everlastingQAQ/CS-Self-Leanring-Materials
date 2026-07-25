---
title: "Lab 2：JUnit 与调试"
description: "CS61B Spring 2021 Lab 2：JUnit 与调试中文学习资料。"
hide:
  - toc
---

# Lab 2：JUnit 测试与调试

- 原标题：Lab 2: JUnit Tests and Debugging
- 原页面：`https://sp21.datastructur.es/materials/lab/lab2/lab2`

> **文档性质**：本文件依据 CS 61B Spring 2021 官方页面，由 ChatGPT 独立阅读后制作中文学习版。  
> 为保留技术准确性，类名、方法名、文件名、命令、报错文本和 API 名称保持英文。本文采用逐节翻译与重述，而不是网页的逐句镜像。

## 实验目标

学习两项贯穿整门课程的能力：

1. 使用 IntelliJ Debugger 定位程序运行错误。
2. 使用 JUnit 编写和运行单元测试。

开始前执行：

```bash
git pull skeleton master
```

并以 `lab2/pom.xml` 为入口导入 Maven 项目。

## 1. Debugger 基础

### Breakpoint

断点使程序在某一行执行前暂停。暂停后可以查看：

- 当前局部变量
- 对象字段
- 调用栈
- 当前执行位置

### Step Into

进入当前行调用的方法内部。适合怀疑 bug 位于被调用方法时使用。

### Step Over

执行当前行，但不进入方法内部。适合只关心调用结果时使用。

### Step Out

继续执行直到当前方法返回。误进入不重要的方法时，可快速退出。

### 调试原则

不要凭感觉乱改代码。先确认：

1. 实际值是什么？
2. 预期值是什么？
3. 两者第一次出现差异的位置在哪里？
4. 这个差异是由哪一行或哪一次调用产生的？

## 2. JUnit 与单元测试

JUnit 测试通常通过 `@Test` 标记测试方法，并使用断言比较结果。例如：

```java
@Test
public void testSum() {
    assertEquals(11, Arithmetic.sum(5, 6));
}
```

测试方法应短小、明确，一次验证一个行为。JUnit 的一个测试方法中，断言失败后会停止执行该方法剩余部分，然后继续其他测试。

## 3. 在 IntelliJ 中运行测试

运行测试类后：

- 绿色表示通过。
- 红色表示失败。
- 点击失败位置可跳到对应测试代码。
- 先读 expected 与 actual，再进入 Debugger。

原实验中的 `ArithmeticTest` 会暴露错误实现，例如预期 `5 + 6 = 11`，实际代码却给出错误结果。任务是利用测试或调试器修复它。

## 4. IntList 应用练习

实验通过 `IntList` 练习：

- 迭代链表节点
- 使用嵌套辅助方法
- 为便于调试而重构代码
- 处理容易出错的特殊链表结构

重点不是只让测试变绿，而是学会把复杂逻辑拆成更容易观察和验证的小方法。

## 提交前检查

- 所有要求的 JUnit 测试通过。
- 没有为了通过测试而删除断言。
- 能解释 breakpoint、step into、step over、step out 的区别。
- 已提交 Lab 2 指定文件。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/lab/lab2/lab2){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
