---
title: "Lab 1：IntelliJ、Java 与 Git"
description: "CS61B Spring 2021 Lab 1：IntelliJ、Java 与 Git中文学习资料。"
---

# Lab 1：IntelliJ、Java 与 Git

- 原标题：Lab 1: IntelliJ, Java, git
- 原页面：`https://sp21.datastructur.es/materials/lab/lab1/lab1`

> **文档性质**：本文件依据 CS 61B Spring 2021 官方页面，由 ChatGPT 独立阅读后制作中文学习版。  
> 为保留技术准确性，类名、方法名、文件名、命令、报错文本和 API 名称保持英文。本文采用逐节翻译与重述，而不是网页的逐句镜像。

## 开始前

先完成 Lab 1 Setup。第一次实验配置步骤很多，无法在一次 Lab 时段内完成很正常。可以与同学讨论，但命令、配置和编程必须自己实际操作一遍。

## 1. GitHub、Beacon 与课程仓库

当年课程使用 Beacon 管理学生信息和仓库注册。学生会获得：

- 一个私有课程仓库，如 `sp21-s***`
- 一个 Snaps 备份仓库，如 `snaps-sp21-s***`

课程仓库用于提交代码；Snaps 仓库用于自动保存项目开发快照。课程明确禁止公开发布作业代码。

## 2. 获取 Skeleton

先配置 Git 身份：

```bash
git config --global user.email "你的邮箱"
git config --global user.name "你的名字"
```

克隆个人仓库并进入目录，然后加入课程 skeleton 远程仓库：

```bash
git remote add skeleton https://github.com/Berkeley-CS61B/skeleton-sp21.git
git remote -v
git pull skeleton master
```

如果出现 unrelated histories 错误，当年课程允许首次使用：

```bash
git pull --rebase --allow-unrelated-histories skeleton master
```

获取成功后应出现 `lab1/` 目录，其中包含 `HelloWorld.java`、`HelloNumbers.java`、`Collatz.java` 等文件。

## 3. 在 IntelliJ 中运行代码

用 IntelliJ 打开 `lab1` 目录，等待索引完成。打开并运行 `HelloNumbers`，确认控制台正常输出。

重要概念：

- IntelliJ 是 IDE，不只是文本编辑器。
- 运行 Java 程序时应选择含有 `main` 方法的类。
- 红色标记通常表示编译或配置错误。

## 4. Snaps 配置

Snaps 的目的不是替代正常 Git commit，而是提供自动备份与课程工作量分析。原课程说明不会把 Snaps 用于人工监视或抄袭检测。

主要步骤：

1. 克隆 Snaps 仓库。
2. 配置课程要求的环境变量。
3. 安装 `CS 61B Snaps` IntelliJ 插件。
4. 重启 IntelliJ 和终端。
5. 运行 `CheckLabConfig` 验证配置。

不要在 Snaps 仓库里完成作业，否则 Gradescope 测试会失败。

## 5. Collatz 编程练习

在 `Collatz.java` 中实现 Collatz 序列：

- 若 `n` 为偶数，下一个值为 `n / 2`
- 若 `n` 为奇数，下一个值为 `3n + 1`
- 到 `1` 时结束

重点不是算法难度，而是确认你能在课程目录中编辑、运行和验证 Java 代码。

## 6. 提交 Git 工作流

典型流程：

```bash
git status
git add <文件>
git commit -m "完成 Lab 1"
git push origin master
```

提交前检查：

- 修改的是个人课程仓库，不是 Snaps 仓库。
- 本地更改已经 commit。
- GitHub 远程仓库中能看到最新 commit。
- Gradescope 提交的是正确目录。

## 完成标准

- 能从 skeleton 拉取代码。
- 能用 IntelliJ 运行 Java 类。
- `Collatz.java` 行为正确。
- Snaps 配置测试通过。
- 能 commit、push 并提交 Lab。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/lab/lab1/lab1){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
