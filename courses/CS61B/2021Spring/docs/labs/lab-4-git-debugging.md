---
title: "Lab 4：Git 与调试"
description: "CS61B Spring 2021 Lab 4：Git 与调试中文学习资料。"
---

# Lab 4：Git 与调试

- 原标题：Lab 4: Git and Debugging
- 原页面：`https://sp21.datastructur.es/materials/lab/lab4/lab4`

> **文档性质**：本文件依据 CS 61B Spring 2021 官方页面，由 ChatGPT 独立阅读后制作中文学习版。  
> 为保留技术准确性，类名、方法名、文件名、命令、报错文本和 API 名称保持英文。本文采用逐节翻译与重述，而不是网页的逐句镜像。

## 特别提醒

原实验要求开始前**不要立刻从 skeleton pull**，因为课程故意设计了一次 merge conflict，让学生按指定流程解决。自学时也应保留这个练习目的，不要用强制覆盖绕开冲突。

先确认个人仓库与远程同步：

```bash
git push origin master
```

## 实验目标

- 理解 commit、branch、checkout、merge 和 HEAD。
- 查看历史版本中的文件。
- 亲手处理一次合并冲突。
- 再完成一个调试谜题。

## 1. Git 历史与提交图

使用以下工具观察仓库：

```bash
git status
git log
git log --oneline --graph --all
```

每个 commit 是项目状态的一个快照，并通过父指针形成历史图。分支本质上是指向某个 commit 的可移动名称。

## 2. Checkout 历史提交

实验会创建或使用类似 `lab1commit` 的标签/引用，切换过去后查看旧版 `Collatz.java`：

```bash
git checkout lab1commit
git status
```

此时可能处于 detached HEAD。你可以查看旧代码，但不应直接在这里继续正常开发。

用 `cat` 或编辑器检查历史文件，理解 Git 并没有“只保存差异给人看”，而是能还原某一提交的完整工作树状态。

## 3. 返回当前分支

完成观察后切回主分支：

```bash
git checkout master
```

再次确认文件恢复为当前版本。理解“切换 commit/branch 会改变工作区内容”。

## 4. Merge Conflict

从 skeleton 拉取课程更新时，若本地和远程修改了同一区域，会出现冲突标记：

```text
<<<<<<< HEAD
本地版本
=======
远程版本
>>>>>>> skeleton/master
```

处理流程：

1. 打开冲突文件。
2. 判断最终应保留的内容。
3. 删除冲突标记。
4. 编译和测试。
5. `git add` 标记冲突已解决。
6. 完成 merge commit。

不要使用 `git reset --hard` 或直接删除整个目录来逃避冲突，除非你清楚后果且已备份。

## 5. 调试谜题

实验后半部分要求使用前几次 Lab 学到的工具定位错误。核心流程仍是：

- 先复现。
- 设置断点。
- 找到第一次偏离预期的状态。
- 修复根因。
- 重新运行测试。

## 完成标准

- 能解释 detached HEAD。
- 能查看旧提交中的文件。
- 能切回正确分支。
- 能手动解决 merge conflict。
- 调试题通过，Git 工作区干净。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/lab/lab4/lab4){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
