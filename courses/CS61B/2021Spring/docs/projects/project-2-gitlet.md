---
title: "Project 2：Gitlet"
description: "CS61B Spring 2021 Project 2：Gitlet中文学习资料。"
---

# Project 2：Gitlet

- 原标题：Project 2: Gitlet
- 原页面：`https://sp21.datastructur.es/materials/proj/proj2/proj2`
- 原截止时间：2021-04-02

> **文档性质**：本文件依据 CS 61B Spring 2021 官方页面，由 ChatGPT 独立阅读后制作中文学习版。  
> 为保留技术准确性，类名、方法名、文件名、命令、报错文本和 API 名称保持英文。本文采用逐节翻译与重述，而不是网页的逐句镜像。

## 项目目标

实现一个简化版 Git 版本控制系统。Gitlet 是本课程第一次大型、持久化、命令行软件工程项目，核心难点不在单个算法，而在：

- 规格精确实现。
- 持久化数据模型。
- commit 图。
- 工作区、暂存区和仓库状态协调。
- 分支、checkout、reset 与 merge。
- 大量错误条件。
- 集成测试与调试。

## 建议架构

至少区分以下概念：

### Repository

负责当前仓库目录、命令入口、状态读取与保存。

### Commit

通常包含：

- message
- timestamp
- parent commit ID
- merge 时的第二父节点
- 文件名到 blob ID 的映射

Commit ID 由能唯一确定 commit 内容的数据计算 SHA-1。

### Blob

文件内容的不可变快照。相同内容应能共享同一个内容地址，避免每个 commit 重复存储未变化文件。

### Staging Area

记录：

- 待添加或更新的文件
- 待删除的文件

### Branch

分支名指向某个 commit。HEAD 表示当前分支，而不只是某个临时 commit。

## 命令规格

### `init`

在当前目录创建 `.gitlet`。重复初始化应报错。

### `add <file>`

把当前工作区文件内容加入暂存区。若内容与当前 commit 相同，应取消该文件的添加暂存。若此前暂存删除，也要撤销删除标记。

### `commit <message>`

创建新 commit，并让当前分支移动到它。没有暂存变化或 message 为空时，按规格输出错误。不得为未变化文件存储多余副本。

### `rm <file>`

若文件在添加暂存区，取消暂存；若被当前 commit 跟踪，则标记删除并从工作区删除。两种条件都不满足时报错。

### `log`

从当前 HEAD 沿第一父节点向前输出历史。

### `global-log`

输出仓库中所有 commit，顺序不限或按规格处理。

### `find <message>`

找到所有 message 完全匹配的 commit ID。

### `status`

按严格格式输出：

- Branches
- Staged Files
- Removed Files
- Modifications Not Staged For Commit
- Untracked Files

排序与空行必须符合规格。

### `checkout`

有三种形式：

- 从当前 commit 恢复文件。
- 从指定 commit 恢复文件。
- 切换到指定 branch。

切分支时要更新工作区和当前分支，但不能覆盖未跟踪且会被目标版本写入的文件。

### `branch`

创建新分支指针，初始指向当前 commit。

### `rm-branch`

删除分支名，但不删除 commit。不能删除当前分支。

### `reset`

让当前分支指向指定 commit，并把工作区更新为该 commit。仍需保护未跟踪文件。

### `merge`

最复杂的命令。需要：

1. 检查未提交变化与错误条件。
2. 找到 current branch 与 given branch 的 split point。
3. 处理 ancestor 与 fast-forward 特殊情况。
4. 按每个文件在 split/current/given 三方的状态决定：
   - 保持
   - checkout given 版本
   - 删除
   - 冲突
5. 创建带两个 parent 的 merge commit。

冲突文件使用规格要求的标记格式，并打印冲突提示。

## Split Point

commit 图不是普通树，merge commit 有两个父节点。split point 是两个分支历史中的适当共同祖先。不能仅沿一条 parent 链或只比较时间戳。

## 设计文档

实现前应写 Markdown Design Document，包括：

1. Classes and Data Structures
2. Algorithms
3. Persistence

每个类写明字段职责；复杂命令给出高层算法；明确 `.gitlet` 中每类对象如何存放。

## 测试系统

课程提供 Python tester DSL，可：

- 创建和删除文件。
- 执行 `java gitlet.Main ...`。
- 比较输出。
- 检查文件存在性和内容。
- 引用 `.inc` 公共设置脚本。
- 使用正则匹配 commit ID 等动态输出。

命令示例：

```bash
python3 testing/tester.py
make check
make TESTER_FLAGS="--keep --verbose"
```

自己的 `.in` 测试应放在 `testing/student_tests`，不要混进 staff samples。

## 调试策略

- 一条测试只验证一个规则。
- 用 staff solution 验证测试本身。
- 使用 `--keep` 保存失败目录。
- 在保存目录中手动运行下一条命令。
- 检查 `.gitlet` 持久化对象和工作区文件。
- 保持 Design Document 与实现同步。

## 提交前检查

- 所有错误消息精确。
- 输出排序和格式精确。
- abbreviated commit ID 正确。
- untracked file protection 覆盖 checkout、reset、merge。
- merge 特殊情况和冲突正确。
- commit 存储不重复复制所有历史文件。
- Snaps grader 与正式 grader 按当年要求提交。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/proj/proj2/proj2){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
