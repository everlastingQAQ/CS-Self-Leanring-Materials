---
title: "Lab 4：Git 与调试"
description: "CS61B Spring 2021 Lab 4：Git 与调试中文学习资料。"
---

# Lab 4：Git 与调试

> 原文：https://sp21.datastructur.es/materials/lab/lab4/lab4<br>
> 说明：正文由 ChatGPT 直接翻译；命令、代码、commit hash 与工具名称保持原样。

## Lab 前准备

- **先不要从 skeleton 拉取。**这会故意制造 merge conflict，必须在 Lab 指定位置处理。
- 若已经拉取，请联系 TA 获取恢复步骤。
- 本 Lab 要求 Lab 1 Gradescope 满分。
- 先确认本地仓库与 GitHub 同步：

```bash
git push origin master
```

成功即可继续；失败时按课程错误说明修复。

## 简介

本 Lab 深入练习 Git，并再次训练调试。目标包括：

- 本地 Git 工作流：`git add`、`git commit`；
- 用 `git checkout` 在 commit 之间移动或恢复文件；
- detached `HEAD`；
- 远程仓库与 `origin/master`、`skeleton/master`；
- 解决 merge conflict；
- 用 JUnit 和 Debugger 穷举式定位错误。

官方要求先观看六段 Git Intro 视频。不要盲目复制网上或朋友提供的 Git 命令；不确定时询问 TA，因为错误 Git 操作可能使仓库更难恢复。

## Git 练习

现在拉取 starter code：

```bash
git pull skeleton master
```

课程故意在 `lab1/Collatz.java` 中制造冲突。你的 Lab 1 版本原本正确，skeleton 新版本包含下面的错误实现：

```java
/** Buggy implementation of nextNumber! */
public static int nextNumber(int n) {
    if (n == 128) {
        return 1;
    } else if (n == 5) {
        return 3 * n + 1;
    } else {
        return n * 2;
    }
}
```

### Step 1：解决冲突，并保留错误版本

解决 `Collatz.java` 的 merge conflict，使文件能编译，且 `nextNumber` 最终必须是上面的**错误版本**。

运行：

```bash
git log
```

最新 commit 应是你解决冲突产生的 merge commit，第二新的是 “Added Lab 4 Starter Files”。向前找到完成 Lab 1、包含正确 `Collatz` 的 commit，记下其 hash，并把它称为 `lab1commit`。

### Step 2：提交 Part A

提交到 Gradescope 的 **Lab 4A: Git Exercise Part A**。Autograder 会检查：

- merge conflict 已正确解决；
- `Collatz.java` 中保留了指定错误版本。

### Step 3：进入旧 commit（detached HEAD）

Checkout 到 `lab1commit`：

```bash
git checkout <lab1commit>
git status
```

应看到类似：

```text
HEAD detached at 4050fd8
nothing to commit, working tree clean
```

在 detached HEAD 中可以查看旧快照，但不要修改或 commit。查看旧文件：

```bash
cat lab1/Collatz.java
```

应看到完成 Lab 1 时的正确实现，例如：

```java
public class Collatz {
    public static int nextNumber(int n) {
        return n % 2 == 0 ? n / 2 : 3 * n + 1;
    }

    public static void main(String[] args) {
        int n = 5;
        System.out.print(n + " ");
        while (n != 1) {
            n = nextNumber(n);
            System.out.print(n + " ");
        }
    }
}
```

### Step 4：回到最新 commit

Checkout 回 `master`（或课程当时的最新分支）：

```bash
git checkout master
```

再次 `cat lab1/Collatz.java`，确认文件又变回指定错误版本。这说明 checkout commit 会切换整个仓库快照。

### Step 5：只恢复一个文件

当前位于最新 commit，但想让 `Collatz.java` 恢复到 `lab1commit` 中的状态。使用文件 checkout：

```bash
git checkout <lab1commit> -- lab1/Collatz.java
```

`git checkout <commit> -- <file>` 不切换整个仓库，只把指定文件替换成目标 commit 中的版本，并自动 stage。运行 `git status` 应看到：

```text
Changes to be committed:
    modified:   lab1/Collatz.java
```

再次 `cat` 确认已恢复正确实现，然后 commit 并 push。

### Step 6：提交 Part B

提交到 **Lab 4B: Git Exercise Part B**。

### 用 checkout 重启或撤销项目文件

把文件恢复到 skeleton 原始状态：

```bash
git checkout skeleton/master -- proj0/game2048/Model.java
```

通用形式：

```bash
git checkout skeleton/master -- <file>
```

把文件恢复到当前 `master` 最新 commit 状态：

```bash
git checkout master -- proj0/game2048/Model.java
```

通用形式：

```bash
git checkout master -- <file>
```

只要经常 commit，就可以放心尝试重写，再从任意旧 commit 恢复。

## 调试谜题

Flik Enterprises 提供 `Flik.java`，用于判断两个 `Integer` 是否相同。Horrible Steve 报告：他的代码应该打印到 500，却只打印到 128。

任务：判断 bug 位于 `HorribleSteve.java` 还是 `Flik.java`，然后修复。可组合使用：

- 为 Flik 编写 JUnit 测试；新建测试文件并 import JUnit；
- IntelliJ Debugger；特别是条件断点与异常断点；
- print statements；
- 重构 Horrible Steve 的代码，即不改变功能，只改变写法，使其更易理解。

JUnit 可使用：

```java
assertTrue(boolean)
assertTrue(String, boolean)
```

Autograder 使用 Hidden Tests，不会透露 bug。修复后提交 **Lab 4: Debugging**。同时准备一段简短解释：为什么结果在 128 附近出现异常。该问题涉及课程尚未正式讲解的 Java `Integer` 行为，可以查阅可信资料，但不要直接照抄修复命令或答案。

## 提交

本 Lab 有三个 Autograder：

1. **Lab 4A: Git Exercise Part A**：检查冲突解决后的错误版本。
2. **Lab 4B: Git Exercise Part B**：检查从历史恢复正确文件。
3. **Lab 4: Debugging**：检查 Flik bug 修复，并检查代码风格。

每个文件可右击选择 **Check Style**。Beacon 中对 Lab 4 的 extension request 会同时应用于三个 Autograder。

## 回顾

- Git 基础；
- merge conflicts；
- detached HEAD；
- 用 Git checkout 恢复 commit 或单个文件；
- 用 JUnit 调试。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/lab/lab4/lab4<br){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
