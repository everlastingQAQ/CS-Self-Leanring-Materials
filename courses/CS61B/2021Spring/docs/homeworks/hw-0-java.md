---
title: "HW 0：Java 速成"
description: "CS61B Spring 2021 HW 0：Java 速成中文学习资料。"
hide:
  - toc
---

# HW 0：Java 速成

- 原标题：HW 0: A Java Crash Course
- 原页面：`https://sp21.datastructur.es/materials/hw/hw0/hw0`
- 性质：可选，不提交；无 Java 经验者强烈建议完成

> **文档性质**：本文件依据 CS 61B Spring 2021 官方页面，由 ChatGPT 独立阅读后制作中文学习版。  
> 为保留技术准确性，类名、方法名、文件名、命令、报错文本和 API 名称保持英文。本文采用逐节翻译与重述，而不是网页的逐句镜像。

## 作业目标

本作业假设你已经学过至少一门编程语言，重点不是从零讲编程，而是快速熟悉 Java 写法。课程讲座不会完整覆盖这些语法，但后续默认你会使用。

## 1. 基本程序与静态类型

Java 变量必须声明类型：

```java
int x = 5;
```

每条语句通常以分号结束。输出使用：

```java
System.out.println(x);
```

Java 的类型检查比 Python 等动态语言更严格，不能随意把 `double` 放进 `int` 变量。

## 2. 条件语句与花括号

```java
if (condition) {
    ...
} else if (otherCondition) {
    ...
} else {
    ...
}
```

Java 用花括号而不是缩进确定代码块。课程要求即使分支中只有一条语句，也使用花括号，以减少维护时出现控制流 bug。

## 3. `while` 循环

```java
while (condition) {
    ...
}
```

条件只在每轮开始时检查；循环体中途条件变为 false，不会自动跳出当前轮。

## 4. `double` 与 `String`

- `double` 保存浮点数近似值。
- `String` 保存字符串。
- 字符串可用 `+` 拼接。

作业通过 Achilles 与乌龟追赶示例练习变量、循环和输出。

## 5. 练习：打印三角形

用循环打印：

```text
*
**
***
****
*****
```

不能只写五条固定输出。随后把逻辑抽成：

```java
public static void drawTriangle(int N)
```

并让 `main` 调用它。

## 6. 方法

Java 的函数称为 method。方法签名包含：

- 访问修饰符
- `static` 等修饰符
- 返回类型
- 方法名
- 参数列表

例如：

```java
public static int max(int x, int y)
```

`void` 表示没有返回值。

## 7. 数组

```java
int[] numbers = new int[]{{4, 7, 10}};
```

数组下标从 0 开始，长度使用：

```java
numbers.length
```

练习实现：

```java
public static int max(int[] m)
```

返回非负整数数组中的最大值。

## 8. `for` 循环

```java
for (int i = 0; i < a.length; i += 1) {
    ...
}
```

把 `max` 的 `while` 版本改写为 `for` 版本。

## 9. `break`、`continue` 与增强 for

- `continue`：跳过当前轮剩余代码。
- `break`：结束最内层循环。
- 增强 for：

```java
for (String s : array) {
    ...
}
```

适用于不需要下标的遍历。

## 10. 可选挑战：`windowPosSum`

实现：

```java
windowPosSum(int[] a, int n)
```

若 `a[i]` 为正数，就把它替换为从 `a[i]` 到之后最多 `n` 个元素的和；负数保持不变。到数组末尾时停止，避免越界。

## 完成标准

能独立阅读和编写包含变量、分支、循环、方法与数组的基础 Java 程序。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/hw/hw0/hw0){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
