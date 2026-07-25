---
title: "Lab 6：Project 2 入门"
description: "CS61B Spring 2021 Lab 6：Project 2 入门中文学习资料。"
hide:
  - toc
---

# Lab 6：Project 2 入门

- 原标题：Lab 6: Getting Started on Project 2
- 原页面：`https://sp21.datastructur.es/materials/lab/lab6/lab6`

> **文档性质**：本文件依据 CS 61B Spring 2021 官方页面，由 ChatGPT 独立阅读后制作中文学习版。  
> 为保留技术准确性，类名、方法名、文件名、命令、报错文本和 API 名称保持英文。本文采用逐节翻译与重述，而不是网页的逐句镜像。

## 实验目标

这是 Gitlet 的关键前置 Lab。你将学习：

1. 从命令行编译、运行 Java，并运行测试。
2. 用 Java 操作文件和目录。
3. 将 Java 对象序列化到文件，并在下次运行时恢复。
4. 用一个小型 `Capers` 程序练习持久化设计。

## 1. 持久化的含义

此前程序状态只存在于进程内，程序退出后全部消失。持久化要求把状态写到磁盘，使下一次运行能继续读取。

Gitlet 的 commit、branch、staging area 都需要持久化；否则每次执行一条命令后仓库状态就会丢失。

## 2. Java 编译与 Make

理解：

```bash
javac ...
java ...
make
make check
```

`Makefile` 把常用编译和测试命令统一成短命令。它不是 Java 的一部分，而是构建自动化工具。

## 3. Current Working Directory

Java 中的相对路径以当前工作目录（CWD）为基准。可用：

```java
System.getProperty("user.dir")
```

查看 CWD。IntelliJ 中需检查 Run Configuration 的 Working Directory，否则命令行与 IDE 运行可能读写到不同位置。

## 4. 绝对路径与相对路径

- 绝对路径从文件系统根开始。
- 相对路径从 CWD 开始。
- 不要用字符串硬拼路径分隔符。
- 使用 `File`、`Paths` 或课程提供的 `Utils.join`。

常用操作包括创建目录、检查文件存在、列出普通文件、读取内容和写入内容。

## 5. Serializable

需要持久化的对象实现 `Serializable`。课程工具提供类似方法：

- `readContents(File file)`
- `writeObject(File file, Serializable obj)`
- `readObject(File file, Class<T> expectedClass)`
- `join(...)`

序列化适合保存对象状态，但必须明确文件存放位置、对象生命周期和更新时机。

## 6. Canine Capers 练习

核心文件通常包括：

- `Main.java`
- `CapersRepository.java`
- `Dog.java`

建议顺序：

1. 定义 `CAPERS_FOLDER`。
2. 定义 `DOG_FOLDER`。
3. 实现 `setUpPersistence`。
4. 在 `Main` 中解析命令并调用仓库方法。
5. 实现 `writeStory`。
6. 实现 `Dog.saveDog` 与 `Dog.fromFile`。
7. 实现 `makeDog`。
8. 实现 `celebrateBirthday`。
9. 运行 `make check`。

命令的典型语义：

- 初始化持久化目录。
- 向故事文件追加文本。
- 创建并保存一只狗。
- 读取某只狗、增长年龄并重新保存。

## 7. 调试持久化程序

持久化 bug 常来自：

- CWD 错误。
- 路径拼接错误。
- 目录未创建。
- 修改对象后忘记重新保存。
- 读错文件。
- 同名对象覆盖规则不一致。
- 测试之间残留旧数据。

调试时应检查磁盘上的实际目录树，而不只盯着 Java 变量。

## 完成标准

- Capers 命令能跨多次进程运行保留状态。
- `make check` 通过。
- 能解释序列化、CWD、相对路径和仓库目录的关系。
- 为 Gitlet 写设计文档前，已经完成本 Lab。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/lab/lab6/lab6){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
