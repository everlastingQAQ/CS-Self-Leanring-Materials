---
title: "Lab 1：IntelliJ、Java 与 Git"
description: "CS61B Spring 2021 Lab 1：IntelliJ、Java 与 Git中文学习资料。"
---

# Lab 1：IntelliJ、Java 与 Git

> 原文：https://sp21.datastructur.es/materials/lab/lab1/lab1<br>
> 说明：正文由 ChatGPT 直接翻译；命令、代码、仓库名与服务名称保持原样。

## 开始之前

- 先完成 Lab 1 Setup，安装课程所需软件。
- 第一周配置步骤较多，不要因此气馁；卡住时及时在 Ed、Lab 或 Office Hours 求助。
- 本 Lab 较长，尤其遇到环境问题时，一次实验课没做完很正常。
- 可以与同学讨论，但键入代码、命令和实际配置必须由你自己完成。

## GitHub 与 Beacon

CS 61B 使用 Beacon 集中管理成绩和学生信息，并使用私人 GitHub 仓库提交所有编程作业。

1. 注册 GitHub 账号；已有账号无需重建。
2. 进入 Beacon，按指引完成课程仓库注册。Google Form 必须使用 Berkeley 账号登录。
3. 完成后，你会收到课程仓库协作者邀请。请接受发送到 GitHub 账号邮箱的邀请；不要执行 GitHub 自动推荐的初始化命令，后面会给出课程自己的步骤。

### 仓库说明

- 你的私人仓库形如 `sp21-s42`，编号每人不同。
- 只有本人和课程 staff 能查看。私密调试问题可在 Ed 中附仓库代码链接。
- 不得把本课程代码公开，即使课程已经结束也不可以。
- 有 Lab partner 时，可能另有共享实验仓库。
- 你还会收到 `snaps-sp21-sXXX` 仓库邀请，先接受，稍后配置。

## A. 获取 Starter Files

### 1. 配置 Git 身份

```bash
git config --global user.email "you@berkeley.edu"
git config --global user.name "Your Name"
```

邮箱应与 GitHub 注册邮箱一致，不一定非要是 Berkeley 邮箱。

### 2. 克隆个人课程仓库

```bash
cd cs61b
git clone https://github.com/Berkeley-CS61B-Student/sp21-s**.git
cd sp21-s**
```

把 `s**` 替换成你的课程编号。熟悉 SSH 的同学可以自行使用 SSH URL。

### 3. 添加 `skeleton` remote

```bash
git remote add skeleton https://github.com/Berkeley-CS61B/skeleton-sp21.git
git remote -v
```

应同时看到 `origin` 与 `skeleton`。出现 `Not a git repository` 时，确认当前目录是 `sp21-s**`。

### 4. 拉取 Lab 1 Starter Code

```bash
git pull skeleton master
```

该命令会把 skeleton 仓库中的远程文件复制/合并到当前仓库。

若出现 `fatal: refusing to merge unrelated histories`，本次改用：

```bash
git pull --rebase --allow-unrelated-histories skeleton master
```

## B. 在 IntelliJ 中运行代码

IntelliJ 是 IDE，既包含文本编辑器，也包含大量辅助开发功能。

1. 启动 IntelliJ，选择 **Open**。
2. 打开 `lab1` 目录。
3. 左侧应看到 `HelloWorld`、`HelloNumbers`、`Collatz`、`GetEnvironmentVariables` 和 `CheckLabConfig`。若看不到侧栏，打开 **View → Tool Windows → Project**。
4. 首次打开时 IntelliJ 可能需要数分钟建立索引；索引完成前部分功能不可用。
5. 打开 `HelloNumbers`，确认没有红色错误提示。
6. 选择 **Run → Run... → HelloNumbers**。
7. 控制台应打印一组数字。

## C. 配置 Snaps

你有两个仓库：

- 标准仓库 `sp21-s33`：手动提交 commit。
- Snaps 仓库 `snaps-sp21-s33`：由插件自动记录快照。

Snaps 用作额外安全备份和匿名课程工作量分析。staff 不会手工监视仓库，也不会把 Snaps 用于抄袭检测。

### 获取 Snaps 仓库

确认已接受 `snaps-sp21-s***` 协作邀请，然后：

```bash
cd ~
git clone https://github.com/Berkeley-CS61B-Student/snaps-sp21-s***
ls
```

**绝对不要在 Snaps 目录中完成作业。**从该目录提交到 Gradescope 会失败。真正工作目录始终是 `sp21-s***`。

### 设置环境变量

按原页面中你的操作系统说明配置环境变量：

- Windows instructions
- macOS and Linux instructions

### 安装 Snaps 插件

#### macOS / Linux

1. 完成环境变量配置后，关闭并重新打开 IntelliJ 和所有终端。
2. 回到 IntelliJ 欢迎页（必要时 **File → Close Project**）。
3. **Plugins → Marketplace** 搜索 `CS 61B Snaps` 并安装。
4. 按提示重启 IDE。
5. 无论刚才是否重启，都再次完全退出 IntelliJ。
6. 在终端运行 `idea` 启动 IntelliJ，不要从 Finder 等 GUI 启动。

#### Windows

1. 重启 IntelliJ 和所有终端。
2. 在欢迎页安装 `CS 61B Snaps` 插件。
3. 按提示重启后，再完全退出并重新打开一次 IntelliJ。

### 测试环境变量

打开 `lab1` 项目，运行 `CheckLabConfig`。若设置正确，应看到确认 Lab 1 setup 完成的消息。

## D. 编程练习：Collatz 序列

打开 `Collatz.java`。程序目标是打印从指定数字开始的 Collatz 序列：

- `n` 为偶数：下一个数是 `n / 2`。
- `n` 为奇数：下一个数是 `3n + 1`。
- `n == 1`：序列结束。

从 `5` 开始时，序列为：

```text
5 16 8 4 2 1
```

### 任务 1：实现 `nextNumber`

```java
public static int nextNumber(int n)
```

返回序列中的下一个数，例如 `nextNumber(5)` 返回 `16`。Gradescope 会直接测试此方法。

为方法编写 `/** ... */` 格式的 Javadoc。课程只强制要求项目中使用 `@source` 标注重要外部帮助，但 Lab/HW 也推荐养成引用来源的习惯。

Java 提示：

- `%` 是取余运算符。
- `==` 比较两个值是否相等。

### 任务 2：完成 `main`

让程序从 `n = 5` 开始，打印完整 Collatz 序列。末尾多一个空格可以接受。

> 背景：人们猜测任意正整数的 Collatz 序列最终都会到达 1，但目前尚未证明。

## E. 把工作推送到 GitHub

进入标准课程仓库，而不是 Snaps 仓库。确认 `ls` 能看到 `lab1`。

### 1. 检查状态

```bash
git status
```

应看到类似：

```text
On branch master
Changes not staged for commit:
  modified:   lab1/Collatz.java
```

若只显示 `Collatz.java` 而不是 `lab1/Collatz.java`，说明当前目录太深，应 `cd ..` 回到仓库根目录。

### 2. Stage 文件

```bash
git add lab1/*
git status
```

此时文件应出现在 `Changes to be committed` 下。

### 3. Commit

```bash
git commit -m "done with Collatz"
```

Commit 会把当前版本和说明保存到本地 Git 历史。

### 4. 再次检查

```bash
git status
```

应看到：

```text
nothing to commit, working tree clean
```

### 5. Push

```bash
git push origin master
```

刷新 GitHub 页面后，应能看到代码和 commit message。

日常真正必需的三条命令是：

```bash
git add lab1/*
git commit -m "done with Collatz"
git push origin master
```

### 三条命令分别做什么

- `git add`：标记哪些文件要进入下一次备份。
- `git commit`：在本机创建带说明的版本记录。
- `git push`：把本地 commit 上传到远端，避免电脑损坏造成丢失。

查看历史可用 `git log`；恢复旧版本可用 `git checkout`，后续 Lab 会详细讲解。

## F. 提交 Lab 1

1. 登录 Gradescope；通常已通过 Berkeley 邮箱加入课程。
2. 打开 **Lab 1: Welcome to Java**。
3. 首次提交时连接 GitHub。
4. 选择你的 `sp21-s***` 仓库和 `master` 分支。
5. 点击 **Upload**。

强烈建议频繁 commit。课程前几周之后，未使用版本控制不会成为代码丢失的免责理由。

## G. 验证 Snaps 安装

```bash
cd $SNAPS_DIR
git push
```

在 Gradescope 打开 **Lab 1A: Snaps Checkoff**，提交方式选择 GitHub，然后选择 `snaps-sp21-s***`（不是标准仓库）。通过检查即说明 Snaps 配置正确。只有课程明确要求时才提交 Snaps 仓库，其他作业均提交标准仓库。

## 回顾

1. 本学期用 IntelliJ 运行 Java 代码。
2. Git 用 commit 跟踪文件历史。
3. 频繁 commit，并写清楚 commit message。
4. 从 `skeleton` remote 拉取作业 starter code。
5. 用 Gradescope 提交 Lab、Homework 和 Project。

## 可选：Josh Hug 配色

可从原页面下载 `hug_sunburst`，在 IntelliJ 中通过 **File → Manage IDE Settings → Import Settings** 导入。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/lab/lab1/lab1<br){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
