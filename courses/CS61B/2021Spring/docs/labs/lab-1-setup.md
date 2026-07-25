---
title: "Lab 1 Setup：配置计算机"
description: "CS61B Spring 2021 Lab 1 Setup：配置计算机中文学习资料。"
---

# Lab 1 Setup：配置你的计算机

- 原标题：Lab 1 Setup: Setting Up Your Computer
- 原页面：`https://sp21.datastructur.es/materials/lab/lab1setup/lab1setup`

> **文档性质**：本文件依据 CS 61B Spring 2021 官方页面，由 ChatGPT 独立阅读后制作中文学习版。  
> 为保留技术准确性，类名、方法名、文件名、命令、报错文本和 API 名称保持英文。本文采用逐节翻译与重述，而不是网页的逐句镜像。

## 实验目标

在正式开始 CS 61B 前，完成 Java、Git、终端和 IntelliJ 的基础环境配置。原课程建议尽量在 Lab 1 上课前自行完成；若遇到问题，再去 Lab 或 Office Hours 求助。

## A. 安装文本编辑器（可选）

课程列举了 Sublime Text、Atom 和 Visual Studio Code。文本编辑器的选择并不关键，因为课程大部分时间使用 IDE。你也可以使用 Vim、Emacs 或系统自带编辑器。

## B. 按操作系统配置环境

分别按照 Windows、macOS 或 Linux 指南安装：

- Java 开发工具：确保 `java` 与 `javac` 可用。
- Git：确保 `git` 命令可用。
- 必要的系统 PATH 配置。

Windows 使用 Bash/WSL 时，原课程提醒 Java 可能需要在 Windows 环境和 Bash 环境中分别安装。

## C. 终端基础

需要理解以下命令及概念：

| 命令 | 作用 |
|---|---|
| `cd` | 切换当前目录 |
| `pwd` | 查看当前绝对路径 |
| `.` | 当前目录 |
| `..` | 父目录 |
| `ls` / `ls -l` | 查看目录内容与详细信息 |
| `mkdir` | 创建目录 |
| `rm` / `rm -r` | 删除文件或递归删除目录 |
| `cp` | 复制文件 |
| `mv` | 移动或重命名文件 |

还应熟悉 Tab 自动补全和方向键调出历史命令。对 `rm -r` 必须格外谨慎。

## D. 验证 Git 与 Java

先运行：

```bash
git --version
```

随后创建临时目录和 `HelloWorld.java`，再执行：

```bash
javac HelloWorld.java
java HelloWorld
```

预期结果：

- 编译后出现 `HelloWorld.class`
- 运行时打印 `Hello world!`

如果命令找不到，尝试重新打开终端、重启电脑或重新安装对应工具。

## E. 安装 IntelliJ IDEA

安装 IntelliJ IDEA Community Edition。Windows 安装时，原课程特别要求勾选将启动器目录加入 PATH。若漏选，最稳妥的处理是重新安装并正确勾选。

## F. 安装课程插件

在 IntelliJ 的 Marketplace 中安装：

- `CS 61B`
- `Java Visualizer`

安装后按提示重启 IDE。

## 完成标准

- `git --version` 正常输出版本。
- `javac` 能成功编译 Java 文件。
- `java HelloWorld` 能正常运行。
- IntelliJ 能启动。
- CS 61B 与 Java Visualizer 插件已安装。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/lab/lab1setup/lab1setup){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
