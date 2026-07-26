---
title: "Lab 1 Setup：配置计算机"
description: "CS61B Spring 2021 Lab 1 Setup：配置计算机中文学习资料。"
---

# Lab 1 Setup：配置你的电脑

> 原文：https://sp21.datastructur.es/materials/lab/lab1setup/lab1setup<br>
> 说明：正文由 ChatGPT 直接翻译；命令、文件名和软件名称保持原样。

建议在参加 Lab 1 前尽可能独立完成本配置。如果遇到困难，请参加实验课或 Office Hours。

## A. 安装文本编辑器（可选）

若你还没有常用文本编辑器，建议安装一个。常见 GUI 编辑器包括：

1. Sublime Text（可免费使用，但会提示购买）：https://www.sublimetext.com/
2. Atom（免费）：https://atom.io/
3. Visual Studio Code（免费）：https://code.visualstudio.com/

具体选择并不重要，因为本课程只会少量使用普通文本编辑器，大部分时间使用 IDE。也可以用系统自带编辑器、Vim、Emacs 等其他工具。

## B. 配置操作系统

根据你的操作系统完成官方页面中的对应配置：

- Windows instructions
- macOS instructions
- Linux instructions

完成相应系统说明后再继续。Windows 高级用户也可使用 Bash for Windows，但课程不提供正式指导；若这样做，需要分别在 Bash 环境和 Windows 本体中安装 Java。

## C. 学习使用终端（可选）

若你已经会打开和使用终端，可跳过本节。终端可以运行程序并操作文件，非常强大，也可能因误操作造成数据损失。

### 常用命令

#### `cd`：切换当前目录

```bash
cd hw
```

进入 `hw` 目录。

#### `pwd`：显示当前工作目录

```bash
pwd
```

输出当前目录的绝对路径。

#### `.`：当前目录

```bash
cd .
```

仍停留在当前目录。

#### `..`：父目录

```bash
cd ..
```

若当前位于 `/workspace/day1/`，会进入 `/workspace/`。

#### `ls`：列出目录内容

```bash
ls
ls -l
```

第二种形式还会显示时间戳和文件权限。

#### `mkdir`：创建目录

```bash
mkdir dirname
```

在当前目录创建名为 `dirname` 的目录。

#### `rm`：删除文件或目录

```bash
rm file1
rm -r dir1
```

`rm -r` 会递归删除目录及其全部内容，使用时务必谨慎。

#### `cp`：复制文件

```bash
cp lab1/original lab2/duplicate
```

把 `lab1/original` 复制为 `lab2/duplicate`。

#### `mv`：移动或重命名文件

```bash
mv lab1/original lab2/original
mv lab1/original lab1/newname
```

第一条命令移动文件；第二条在同一目录中重命名。

### 终端技巧

- 输入已有文件或目录名的一部分后按 `Tab`，可以自动补全或显示候选项。
- 按方向键 `↑` 可找回最近执行过的命令。

## D. 测试步骤 B 的配置

### 1. 检查 Git

打开终端并运行：

```bash
git --version
```

应打印 Git 版本。若出现 `git: command not found`，尝试新开终端、重启电脑或重新安装 Git。

### 2. 检查 `javac` 与 `java`

```bash
mkdir ~/temp
cd ~/temp
```

从命令行打开当前目录：

- macOS：`open .`
- Windows：`explorer .`
- Ubuntu：`gnome-open .`
- Linux Mint：`xdg-open .` 或 `mate .`

创建 `HelloWorld.java`：

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello world!");
    }
}
```

然后：

1. 运行 `ls`，确认能看到 `HelloWorld.java`。
2. 运行 `javac HelloWorld.java`。正常情况下不会输出任何内容。
3. 再运行 `ls`，应看到新生成的 `HelloWorld.class`。
4. 运行 `java HelloWorld`，应输出 `Hello world!`。
5. 完成后可删除 `temp` 目录。

## E. 安装 IntelliJ

1. 从 JetBrains 官网下载 IntelliJ Community Edition。
2. 选择与你操作系统匹配的版本并完成下载。
3. 运行安装程序。若已有旧版 IntelliJ，建议卸载后安装新版。
4. Windows 用户必须勾选 **Add launchers dir to the PATH**。如果漏选，最简单的修复方式是卸载后重新安装。

## F. 安装 IntelliJ CS 61B 插件

继续前请确认 IntelliJ 版本至少为 `2020.3.1`。

1. 在欢迎窗口左侧点击 **Plugins**。
2. 打开 **Marketplace**，搜索 `CS 61B`。
3. 点击绿色 **Install**，等待安装完成。
4. 再搜索并安装 `Java Visualizer`。
5. 若出现 **Restart IDE**，点击重启。

## G. 完成

电脑配置已完成，可以继续 Lab 1。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/lab/lab1setup/lab1setup<br){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
