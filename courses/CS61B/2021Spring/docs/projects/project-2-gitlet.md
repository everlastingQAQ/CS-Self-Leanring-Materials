---
title: "Project 2：Gitlet"
description: "CS61B Spring 2021 Project 2：Gitlet中文学习资料。"
---

# Project 2：Gitlet

> 截止日期：完整评分器 2021-04-02 23:59；Snaps 2021-04-09 23:59<br>
> 原始页面：<https://sp21.datastructur.es/materials/proj/proj2/proj2>
>
> 本文件为完整中文规格整理。所有命令、参数、文件名、类名、错误消息、输出格式和代码保持原样；说明文字由中文重新表述。

## 一、项目目标

本项目要实现一个简化版版本控制系统 **Gitlet**。它模仿 Git 的核心本地功能：

- 保存文件快照；
- 恢复旧版本；
- 查看提交历史；
- 创建与切换分支；
- 重置分支头；
- 合并两个分支；
- 额外实现远程仓库命令。

Gitlet 不要求保存差异补丁。可以保存文件完整内容，但不能为父提交中完全相同的文件重复保存无意义副本。

本项目重点包括：

- 文件系统与持久化；
- Java 序列化；
- SHA-1 内容寻址；
- 集合、映射和图遍历；
- 命令行程序设计；
- 大型集成测试和调试。

## 二、Gitlet 的总体模型

### 1. 提交与历史

一次 `commit` 保存当前被跟踪文件的一个快照。每个普通提交保存一个父提交引用，因此从当前提交沿父指针向后走，可形成一条历史链。

提交节点一旦创建就不可修改或删除。Gitlet 只能在已有提交图上增加新提交。

### 2. 分支与 HEAD

Gitlet 可以维护多个版本方向。每个分支只是：

- 一个分支名称；
- 指向某个提交 SHA-1 的引用。

当前分支的引用称为 HEAD。提交时，新提交成为当前分支的新头；其他分支不会移动。

由于不同分支可以从同一个提交继续发展，提交结构会从链变成树；出现合并提交后，整个结构成为有向无环图。

### 3. Blob、Commit 与 Tree

真实 Git 中有：

- **blob**：保存文件内容；
- **tree**：目录结构，把名称映射到 blob 或子 tree；
- **commit**：提交消息、时间、作者、tree、父提交等。

Gitlet 进一步简化：

- 不处理子目录；仓库只考虑工作目录中的普通文件；
- tree 信息直接合并进 commit；
- 普通提交一个父提交，合并提交两个父提交；
- 元数据只要求时间戳和日志消息。

因此一个提交至少包含：

- 日志消息；
- 时间戳；
- 文件名到 blob SHA-1 的映射；
- 第一父提交 SHA-1；
- 合并提交的第二父提交 SHA-1。

### 4. 内容寻址与 SHA-1

每个 blob 和 commit 都有一个唯一 ID。Gitlet 使用 SHA-1，把任意字节序列映射为 160 位值，通常显示为 40 位十六进制字符串。

内容寻址意味着：

- 内容完全相同的 blob 应得到同一个 SHA-1；
- 元数据、文件映射和父引用完全相同的 commit 应得到同一个 SHA-1；
- 可以使用 SHA-1 作为 `.gitlet` 内对象文件名；
- 比较两个 blob 的 SHA-1，可视为比较文件内容。

提交 SHA-1 必须纳入全部必要信息：

- 消息；
- 时间戳；
- 父提交；
- 文件名与 blob 引用映射；
- 合并时的第二父提交。

还必须确保 commit 与 blob 的命名空间不会被混淆。可以使用不同目录，也可以在哈希输入中加入不同类型标记。

SHA-1 理论上可能冲突，但概率小到本项目直接忽略。

## 三、程序与仓库结构要求

### 1. 必需类

必须存在：

```text
gitlet.Main
```

并包含 `main` 方法。骨架还建议使用：

- `Commit`
- `Repository`

可以增加、删除或重组其他类，但自动评分器必须能通过 `gitlet.Main` 启动程序。

不要把全部逻辑塞进 `Main`。推荐：

- `Main` 负责解析参数；
- `Repository` 负责命令行为和持久化；
- `Commit` 表示提交对象；
- 其他辅助类负责暂存区、分支、远程等。

### 2. `.gitlet` 目录

所有旧版本文件、提交、blob、分支、暂存区和其他元数据都必须位于当前工作目录的：

```text
.gitlet
```

某目录存在 `.gitlet` 时，才算已经初始化 Gitlet 仓库。

`.gitlet` 外的普通文件称为**工作目录文件**。Gitlet 不处理工作目录中的子目录。

### 3. 语言与库

- 只能使用 Java；
- 除 JUnit 外，不得使用外部代码；
- 可使用 Java 标准库；
- 可使用骨架提供的 `gitlet.Utils`。

### 4. 时间与空间要求

每个命令后面给出了运行时间或空间要求，必须遵守。

可以忽略序列化和反序列化本身的时间，但序列化的对象大小不能随着仓库所有历史文件总量无界增长。例如，不应通过一个对象指针把整棵提交图重复序列化到一个文件中。

### 5. 通用错误处理

错误消息需要**逐字匹配**，包括句末句点。遇到失败条件后：

- 打印指定消息；
- 不进行其他状态修改；
- 退出该命令。

通用失败情况：

```text
Please enter a command.
```

用户没有提供任何参数。

```text
No command with that name exists.
```

命令不存在。

```text
Incorrect operands.
```

参数数量或格式错误。

```text
Not in an initialized Gitlet directory.
```

命令要求已初始化仓库，但当前目录没有 `.gitlet`。

### 6. 危险命令

规格把可能覆盖或删除工作目录普通文件的命令标记为危险，例如：

- `rm`
- `checkout`
- `reset`
- `merge`
- `pull`

测试这些命令时应使用专用临时目录。

## 四、命令完整规格

## 4.1 `init`

### 用法

```bash
java gitlet.Main init
```

### 行为

在当前目录创建 `.gitlet`，并建立初始状态：

- 初始提交不跟踪任何文件；
- 消息必须是：

```text
initial commit
```

- 时间戳为 Unix Epoch：1970-01-01 00:00:00 UTC；
- 创建唯一分支 `master`；
- `master` 指向初始提交；
- 当前分支为 `master`。

因为所有初始提交内容完全相同，所有正确实现都应为它生成相同 SHA-1。

### 复杂度

相对于文件、提交数量等重要度量应为常数时间。

### 失败

若当前目录已有 `.gitlet`：

```text
A Gitlet version-control system already exists in the current directory.
```

不得覆盖原仓库。

---

## 4.2 `add`

### 用法

```bash
java gitlet.Main add [file name]
```

### 行为

把文件**当前内容的副本**加入暂存区，即“暂存以供添加”。

- 若文件已经暂存，新的内容覆盖旧暂存内容；
- 暂存区必须位于 `.gitlet` 中；
- 若工作目录版本与当前提交所跟踪版本完全相同：
  - 不暂存；
  - 若此前已暂存添加，则取消该暂存；
- 若该文件此前被暂存删除，执行 `add` 后取消删除暂存。

真实 Git 可以一次添加多个文件；Gitlet 每次只接受一个文件。

### 复杂度

最坏情况下，相对于文件大小为线性，并允许关于当前提交所跟踪文件数 `N` 的 `lg N` 因子。

### 失败

文件不存在：

```text
File does not exist.
```

---

## 4.3 `commit`

### 用法

```bash
java gitlet.Main commit [message]
```

多词消息必须作为一个命令行参数，例如：

```bash
java gitlet.Main commit "added wug"
```

### 行为

创建一个新提交并保存快照。

默认情况下，新提交继承父提交的全部文件映射。然后应用暂存区变化：

- 暂存添加的文件使用暂存版本；
- 父提交未跟踪、但暂存添加的文件开始被跟踪；
- 暂存删除的文件不再被新提交跟踪；
- 未暂存的工作目录修改一律不进入提交。

重要细节：

- 提交后清空添加暂存区和删除暂存区；
- `commit` 不修改工作目录普通文件；
- 工作目录文件在暂存后又发生变化，不影响本次提交；
- 使用系统 `rm` 删除被跟踪文件，但没有执行 Gitlet `rm`，本次提交仍继承父提交中的版本；
- 新提交成为当前提交；
- 当前分支头移动到新提交；
- 原 HEAD 成为新提交第一父提交；
- 每个提交保存创建日期和时间；
- SHA-1 必须包含消息、时间、父引用、文件/blob 引用等。

### 存储要求

创建提交导致 `.gitlet` 增长的文件数据，不得超过当时暂存添加文件的总大小（元数据不计）。不要为从父提交继承而来的相同 blob 再保存完整副本。

不要求只保存 diff，可以按 blob 保存完整文件版本。

### 复杂度

- 相对于提交数量应为常数；
- 相对于提交所跟踪文件总大小不得差于线性。

### 失败

没有任何添加或删除暂存：

```text
No changes added to the commit.
```

消息为空或空白：

```text
Please enter a commit message.
```

工作目录中被跟踪文件缺失或被修改，不属于失败；只根据暂存区和父提交创建快照。

---

## 4.4 `rm`

### 用法

```bash
java gitlet.Main rm [file name]
```

### 行为

- 若文件当前暂存添加，取消添加暂存；
- 若当前提交跟踪该文件：
  - 暂存删除；
  - 若工作目录仍存在该文件，则删除工作目录文件；
- 只有当前提交跟踪的文件才允许被该命令从工作目录删除。

### 复杂度

相对于重要度量应为常数时间。

### 失败

文件既未暂存添加，也未由 HEAD 跟踪：

```text
No reason to remove the file.
```

---

## 4.5 `log`

### 用法

```bash
java gitlet.Main log
```

### 行为

从当前 HEAD 开始，沿**第一父提交**一直向后打印到初始提交。合并提交的第二父提交不在该遍历中。

普通提交格式：

```text
===
commit a0da1ea5a15ab613bf9961fd86f010cf74c7ee48
Date: Thu Nov 9 20:00:05 2017 -0800
A commit message.

```

要求：

- 每个提交前一行 `===`；
- 下一行是完整 40 位提交 SHA-1；
- 再下一行是日期；
- 再下一行是消息；
- 每个条目后有一个空行；
- 最新提交在最前；
- 日期使用当前系统时区，不要求固定 UTC。

合并提交在 `commit` 行下面增加：

```text
Merge: 4975af1 2c1ead1
```

其中：

- 第一个 7 位前缀是第一父提交；
- 第二个 7 位前缀是第二父提交。

完整示例：

```text
===
commit 3e8bf1d794ca2e9ef8a4007275acf3751c7170ff
Merge: 4975af1 2c1ead1
Date: Sat Nov 11 12:30:00 2017 -0800
Merged development into master.

```

### 复杂度

相对于 HEAD 第一父历史中的提交数为线性。

---

## 4.6 `global-log`

### 用法

```bash
java gitlet.Main global-log
```

### 行为

使用与 `log` 相同的条目格式，打印仓库中**曾经创建的所有提交**。顺序不限。

### 复杂度

相对于全部提交数量为线性。

---

## 4.7 `find`

### 用法

```bash
java gitlet.Main find [commit message]
```

### 行为

打印消息完全等于给定消息的所有提交 ID，每行一个。多词消息需加引号。

### 复杂度

相对于提交数量为线性。

### 失败

没有任何匹配提交：

```text
Found no commit with that message.
```

---

## 4.8 `status`

### 用法

```bash
java gitlet.Main status
```

### 输出格式

```text
=== Branches ===
*master
other-branch

=== Staged Files ===
wug.txt
wug2.txt

=== Removed Files ===
goodbye.txt

=== Modifications Not Staged For Commit ===
junk.txt (deleted)
wug3.txt (modified)

=== Untracked Files ===
random.stuff

```

要求：

- 当前分支名前加 `*`；
- 各节之间空一行；
- 整个输出末尾也有空行；
- 每节条目按 Java 字符串比较的字典序排列；
- 分支排序时不把 `*` 计入名称。

### `Modifications Not Staged For Commit`

以下文件列为 `(modified)` 或 `(deleted)`：

1. 当前提交跟踪，工作目录内容变化，但未暂存添加；
2. 已暂存添加，但工作目录内容又与暂存内容不同；
3. 已暂存添加，但工作目录文件被删除；
4. 当前提交跟踪，工作目录文件被删除，但未暂存删除。

### `Untracked Files`

工作目录中存在，但既没有暂存添加，也没有被当前提交跟踪的文件。

也包括：

- 文件已暂存删除；
- 之后用户又在工作目录重新创建同名文件；
- Gitlet 并不知道它应重新被跟踪。

忽略子目录。

最后两节属于 32 分额外分。若不实现，仍必须打印节标题并留空。

### 复杂度

只能依赖：

- 工作目录数据量；
- 暂存添加和删除的文件数；
- 分支数。

---

## 4.9 `checkout`

`checkout` 有三种语法。

### 用法一：从 HEAD 恢复文件

```bash
java gitlet.Main checkout -- [file name]
```

把 HEAD 提交中的版本写入工作目录，覆盖同名文件。不进行暂存。

失败：HEAD 不包含该文件：

```text
File does not exist in that commit.
```

### 用法二：从指定提交恢复文件

```bash
java gitlet.Main checkout [commit id] -- [file name]
```

把指定提交中的版本写入工作目录，覆盖同名文件。不进行暂存。

失败：提交不存在：

```text
No commit with that id exists.
```

提交存在但不包含文件：

```text
File does not exist in that commit.
```

### 用法三：切换分支

```bash
java gitlet.Main checkout [branch name]
```

行为：

1. 把目标分支头提交跟踪的所有文件写入工作目录；
2. 覆盖已有同名工作目录文件；
3. 当前分支跟踪、而目标分支不跟踪的文件从工作目录删除；
4. 目标分支成为当前分支；
5. 清空暂存区。

### 未跟踪文件保护

切换分支前，若当前工作目录有一个未跟踪文件，而目标分支会写入或覆盖该路径，必须在做任何修改前退出：

```text
There is an untracked file in the way; delete it, or add and commit it first.
```

其他失败：

目标分支不存在：

```text
No such branch exists.
```

目标就是当前分支：

```text
No need to checkout the current branch.
```

此时不清空暂存区。

### 缩写提交 ID

用法二支持提交 ID 的唯一前缀。例如完整 ID：

```text
a0da1ea5a15ab613bf9961fd86f010cf74c7ee48
```

若前缀唯一，可写：

```text
a0da1e
```

缩写查找允许对提交数线性扫描，不作严格时间要求。

### 暂存区差异

只有整分支切换会清空暂存区。两种单文件 checkout 不改变暂存状态。

### 复杂度

- 单文件 checkout：相对于文件大小线性；
- 指定提交 checkout：相对于目标快照文件总大小线性；
- 不得依赖提交总数或分支总数，缩写 ID 查找除外。

---

## 4.10 `branch`

### 用法

```bash
java gitlet.Main branch [branch name]
```

### 行为

创建新分支，并让新分支指向当前 HEAD。**不会自动切换到新分支。**

仓库默认分支名必须是：

```text
master
```

创建分支本质只是创建一个额外提交指针。之后切换分支并提交，才会产生分叉。

### 复杂度

常数时间。

### 失败

同名分支已存在：

```text
A branch with that name already exists.
```

---

## 4.11 `rm-branch`

### 用法

```bash
java gitlet.Main rm-branch [branch name]
```

### 行为

删除分支名称和指针，不删除任何提交或 blob。

### 复杂度

常数时间。

### 失败

分支不存在：

```text
A branch with that name does not exist.
```

试图删除当前分支：

```text
Cannot remove the current branch.
```

---

## 4.12 `reset`

### 用法

```bash
java gitlet.Main reset [commit id]
```

### 行为

1. 把指定提交跟踪的所有文件写入工作目录；
2. 删除当前提交跟踪、但指定提交不跟踪的工作目录文件；
3. 当前分支头移动到指定提交；
4. 清空暂存区。

可使用缩写提交 ID。此命令等价于“对任意提交做硬 checkout，并移动当前分支头”，接近真实 Git 的：

```bash
git reset --hard [commit hash]
```

### 未跟踪文件保护

若 reset 会覆盖未跟踪文件，先退出：

```text
There is an untracked file in the way; delete it, or add and commit it first.
```

### 复杂度

相对于目标提交快照中的文件总大小线性；相对于提交数量必须为常数，缩写查找除外。

### 失败

提交不存在：

```text
No commit with that id exists.
```

---

## 4.13 `merge`

### 用法

```bash
java gitlet.Main merge [branch name]
```

把给定分支合入当前分支。

## 五、合并的分叉点

设：

- 当前分支头为 `current`；
- 给定分支头为 `given`。

**共同祖先**是从两个分支头沿父指针均可到达的提交。

**最新共同祖先**是：不是其他共同祖先之祖先的共同祖先。该提交称为 split point（分叉点）。存在多个候选时，按规格所要求的“latest common ancestor”选择。

### 两个特殊情况

若分叉点就是给定分支头，什么都不修改并打印：

```text
Given branch is an ancestor of the current branch.
```

若分叉点就是当前分支头，对给定分支执行快进，使当前分支头指向给定分支头，并打印：

```text
Current branch fast-forwarded.
```

当前分支名称不改变。

## 六、合并文件的八类规则

对分叉点、当前分支头和给定分支头中出现的每一个文件进行比较。

### 规则 1

自分叉点后，仅给定分支修改，当前分支未修改：

- 使用给定分支版本覆盖工作目录；
- 自动暂存添加。

### 规则 2

自分叉点后，仅当前分支修改，给定分支未修改：

- 保留当前版本；
- 不作其他操作。

### 规则 3

两个分支以完全相同方式修改：

- 内容变成相同版本，保持不变；
- 两边都删除，保持删除。

若两边都删除，但工作目录后来出现同名普通文件，该文件留在工作目录中，但仍不跟踪、不暂存。

### 规则 4

分叉点没有该文件，只有当前分支新增：

- 保持当前版本。

### 规则 5

分叉点没有该文件，只有给定分支新增：

- checkout 给定版本；
- 暂存添加。

### 规则 6

分叉点有该文件；当前分支未修改；给定分支删除：

- 删除工作目录文件；
- 暂存删除。

### 规则 7

分叉点有该文件；给定分支未修改；当前分支删除：

- 保持缺失。

### 规则 8：冲突

以下都属于两个分支以不同方式修改：

- 两边都修改，但内容不同；
- 一边修改，另一边删除；
- 分叉点没有该文件，两边都新增但内容不同。

冲突文件内容改为：

```text
<<<<<<< HEAD
当前分支文件内容=======
给定分支文件内容>>>>>>>
```

准确结构为：

```text
<<<<<<< HEAD
[contents of file in current branch]=======
[contents of file in given branch]>>>>>>>
```

原规格以换行形式展示：

```text
<<<<<<< HEAD
contents of file in current branch
=======
contents of file in given branch
>>>>>>>
```

处理时直接拼接：

- 若某分支删除文件，把该侧内容视为空字符串；
- 不主动补齐病态文件缺失的末尾换行；
- 生成的冲突文件自动暂存添加。

## 七、合并提交

若不属于两个祖先特殊情况，完成文件处理后自动提交，消息必须是：

```text
Merged [given branch name] into [current branch name].
```

合并提交有两个父提交：

1. 合并前当前分支头；
2. 合并前给定分支头。

若发生冲突，合并提交仍自动创建。然后终端打印：

```text
Encountered a merge conflict.
```

该消息不是提交日志消息的一部分。

若自动提交本身没有任何变化，允许普通 `commit` 的失败消息自然出现。

### 合并复杂度

```text
O(N lg N + D)
```

其中：

- `N` 是两个分支祖先提交的总数；
- `D` 是这些提交下全部相关文件数据量。

### 合并失败

暂存区存在添加或删除：

```text
You have uncommitted changes.
```

给定分支不存在：

```text
A branch with that name does not exist.
```

与自身合并：

```text
Cannot merge a branch with itself.
```

未跟踪文件会被覆盖或删除：

```text
There is an untracked file in the way; delete it, or add and commit it first.
```

未跟踪文件检查必须在任何修改前完成。

### 与真实 Git 的差异

- 真实 Git 只在双方自分叉点后都改动的具体区域插入冲突标记；Gitlet 对整个文件生成冲突内容；
- 真实 Git 选择多重分叉点的规则不同；
- 真实 Git 要求用户解决冲突后再完成合并；Gitlet 先提交冲突版本，再由后续提交修复；
- 真实 Git 还会处理未暂存、即将被合并覆盖的普通修改；本项目不要求测试该情况。

## 八、建议实现规模与顺序

规格给出的参考命令特定代码行数只是帮助估算难度，不要求一致。`merge` 明显比其他命令更长，不应留到最后。

建议顺序：

1. `init`
2. `add`
3. `commit`
4. 两种单文件 `checkout`
5. `log`
6. `rm`
7. `global-log`、`find`、`status`
8. `branch`、整分支 `checkout`、`rm-branch`
9. `reset`
10. `merge`
11. 额外分远程命令

骨架较少。推荐沿用 Lab 6 Capers 的架构：`Main` 只做分派，真正工作交给仓库类。

## 九、设计文档

必须维护设计文档，虽然不单独计分，但：

- Office Hours 求助前必须完整且最新；
- 提交 Gitbug 前必须完整且最新；
- 应描述类、字段、文件布局、算法和对象关系。

规格提供了设计文档指南和 Capers 示例。

## 十、评分器与时间安排

### Checkpoint Grader

截止：2021-03-12 23:59，价值 16 额外分。

测试：

- 编译；
- 骨架 `testing/samples/*.in`；
- 所需命令：
  - `init`
  - `add`
  - `commit`
  - `checkout -- [file]`
  - `checkout [id] -- [file]`
  - `log`

还会提示风格问题但暂不计分。最大 1 个 token，每 20 分钟恢复。

### Full Grader

截止：2021-04-02 23:59，1600 分。

最大 1 个 token，恢复速度：

- 02-20 至 03-19：每 6 小时一次；
- 03-20 至 03-26：每 3 小时一次；
- 03-26 至 04-02：每 20 分钟一次。

只提供英文测试提示，不提供真实 `.in` 文件。必须自行写测试，不能依赖评分器调试。

### Snaps Grader

截止：2021-04-09 23:59。先推送 snaps 仓库：

```bash
cd $SNAPS_DIR
git push
```

再把 snaps 仓库提交到对应 Gradescope 作业。可在主截止日期后最多一周完成；再晚需使用 slip days。

### 额外分

共 `16 + 32 + 64 = 112`：

- 16：Checkpoint；
- 32：`status` 最后两节；
- 64：远程命令。

## 十一、协作规则

可以比平时更紧密地讨论算法，但：

- 在 `gitlet/Main.java` 开头附近注释中感谢所有合作者；
- 不得分享具体代码；
- 每个人必须独立写出自己的实现；
- 可在 Ed megathread 讨论高层设计和测试想法。

## 十二、文件处理

本项目大量读写文件。可使用：

- `java.io.File`
- `java.nio.file.Files`
- `java.io` / `java.nio` 其他类
- `gitlet.Utils`

若大量手写 Reader、Writer、Scanner 或 Stream，通常说明实现复杂化了。先检查 `Utils` 中提供的文件辅助方法。

## 十三、序列化细节

每次进程只执行一个 Gitlet 命令，因此所有状态必须在进程之间持久保存。

Java 序列化会沿对象引用继续序列化。若一个提交对象直接引用父 `Commit` 对象，保存分支头时可能把整棵祖先图和全部 blob 重复写进同一个文件，违反空间要求。

推荐：

- 对 commit 和 blob 使用 SHA-1 字符串引用；
- 运行时需要时再根据 SHA-1 读取对象；
- 不把“SHA 到对象”的完整运行时缓存持久化。

若希望同时保留运行时对象指针，可以声明为：

```java
private transient MyCommitType parent1;
```

`transient` 字段不会被序列化；反序列化后会恢复为默认值，如对象引用为 `null`。读取对象后需要重新填充。

二进制序列化文件不适合直接用文本编辑器检查。骨架提供：

```text
gitlet.DumpObj
```

具体用法见 `DumpObj.java` 的 Javadoc。

## 十四、测试命令

运行全部测试：

```bash
make check
```

显示更详细失败信息：

```bash
make check TESTER_FLAGS="--verbose"
```

运行单个或若干测试：

```bash
cd testing
python3 tester.py --verbose FILE.in ...
```

注意：直接运行 Python 不会重新编译。每次之前先执行：

```bash
make
```

保留临时测试目录：

```bash
python3 tester.py --verbose --keep FILE.in
```

Python 3 命令名为 `python` 的系统：

```bash
make PYTHON=python check
```

额外参数：

```bash
make TESTER_FLAGS="--keep --verbose"
```

## 十五、测试目录

```text
.
├── Makefile
├── student_tests
├── samples
│   ├── test01-init.in
│   ├── test02-basic-checkout.in
│   ├── test03-basic-log.in
│   ├── test04-prev-checkout.in
│   └── definitions.inc
├── src
│   ├── notwug.txt
│   └── wug.txt
├── runner.py
└── tester.py
```

- 自己的 `.in` 文件放在 `testing/student_tests`；
- 不要放入 `samples`；
- `src` 存放测试用的实际文件内容；
- 每个测试会创建独立临时目录；
- `--keep` 可保留临时目录检查 `.gitlet` 状态。

## 十六、集成测试 DSL

```text
# ...
```

注释，无效果。

```text
I FILE
```

把相对于当前 `.in` 文件的 `FILE` 内容作为测试脚本包含进来。适合复用初始化流程。

```text
C DIR
```

必要时创建并切换到测试主目录下的 `DIR`。省略 `DIR` 时回到默认目录。主要用于设置远程仓库。

```text
T N
```

把后续 Gitlet 命令超时设为 `N` 秒。

```text
+ NAME F
```

把 `src/F` 内容复制到临时目录中的 `NAME`。

```text
- NAME
```

删除临时目录中的 `NAME`。

```text
> COMMAND OPERANDS
LINE1
LINE2
...
<<<
```

运行：

```bash
java gitlet.Main COMMAND OPERANDS
```

并比较输出。若结尾是：

```text
<<<*
```

前面的期望输出按 Python 正则表达式匹配。

```text
= NAME F
```

断言临时目录中的 `NAME` 与 `src/F` 内容完全一致。

```text
* NAME
```

断言 `NAME` 不存在。

```text
E NAME
```

断言文件或目录 `NAME` 存在。

```text
D VAR "VALUE"
```

定义变量 `VAR`，值为经过替换后的 Python raw string。

## 十七、基础测试示例

初始化，无输出：

```text
> init
<<<
```

复制测试文件：

```text
+ wug.txt wug.txt
```

添加、提交：

```text
> add wug.txt
<<<
> commit "added wug"
<<<
```

把工作文件改成另一份内容：

```text
+ wug.txt notwug.txt
```

恢复 HEAD 版本：

```text
> checkout -- wug.txt
<<<
```

断言内容恢复：

```text
= wug.txt wug.txt
```

## 十八、复用测试设置

可把公共设置放入 `.inc` 文件：

```text
# Initialize, add, and commit a file.
> init
<<<
+ a.txt wug.txt
> add a.txt
<<<
> commit "a is a wug"
<<<
```

保存为：

```text
samples/commit_setup.inc
```

测试中使用：

```text
I commit_setup.inc
```

不要给公共片段使用 `.in` 后缀，否则测试器会把它当成独立测试。

## 十九、模式匹配与捕获 SHA

`log` 中 SHA 和时间每次变化，所以使用 `definitions.inc` 中的模式：

```text
I definitions.inc
> log
===
${COMMIT_HEAD}
added wug

===
${COMMIT_HEAD}
initial commit

<<<*
```

`<<<*` 表示正则匹配。

在 `status` 正则中，星号需要转义：

```text
\*master
```

若不用正则，直接写 `*master`。

模式还可以捕获值：

```text
> log
===
${COMMIT_HEAD}
version 2 of wug.txt

===
${COMMIT_HEAD}
version 1 of wug.txt

===
${COMMIT_HEAD}
initial commit

<<<*
```

随后定义变量：

```text
D UID2 "${1}"
D UID1 "${2}"
```

捕获编号从日志顶部的 1 开始，因此当前版本是 `${1}`。之后可执行：

```text
> checkout ${UID1} -- wug.txt
<<<
```

## 二十、调试集成测试

使用 `runner.py` 逐条执行测试。一个测试中会多次启动 Gitlet，最终 `status` 错误不一定说明 `status` 实现错误，也可能是早先 `add`、`commit` 或持久化没有正确记录状态。

调试步骤：

1. 找到最早产生错误状态的那一次程序执行；
2. 每执行一条命令后检查临时目录；
3. 检查 `.gitlet` 中应写入的对象和引用；
4. 序列化对象无法直接阅读时，在序列化前用调试器检查字段；
5. 检查是否忘记写入持久化文件；
6. 保持设计文档最新，再提交 Gitbug。

Office Hours 通常每位学生最多约 10 分钟。复杂问题应提供最小复现测试和充分 Gitbug 信息。

## 二十一、远程命令（64 分额外分）

远程仓库就是另一个 Gitlet 仓库。实现：

- `add-remote`
- `rm-remote`
- `push`
- `fetch`
- `pull`

执行时间不评分。这些命令比真实 Git 明显简化。

## 21.1 `add-remote`

### 用法

```bash
java gitlet.Main add-remote [remote name] [name of remote directory]/.gitlet
```

保存远程名称到远程 `.gitlet` 路径的映射。

示例：

```bash
java gitlet.Main add-remote other ../testing/otherdir/.gitlet
```

命令参数统一使用 `/`。程序应把 `/` 转换为当前平台路径分隔符，可使用：

```java
java.io.File.separator
```

失败：

```text
A remote with that name already exists.
```

不要求在添加时验证远程路径是否真实有效。

## 21.2 `rm-remote`

### 用法

```bash
java gitlet.Main rm-remote [remote name]
```

删除保存的远程名称信息。修改远程配置时，先删除再重新添加。

失败：

```text
A remote with that name does not exist.
```

## 21.3 `push`

### 用法

```bash
java gitlet.Main push [remote name] [remote branch name]
```

### 行为

尝试把当前本地分支的提交追加到远程指定分支。

只有在远程分支头位于当前本地 HEAD 的历史中时才允许 push。此时：

1. 把远程缺少的 commit 和 blob 复制到远程；
2. 将远程分支快进到本地 HEAD。

若远程仓库存在但没有该分支，直接在远程创建分支并指向本地 HEAD。

失败：

远程分支头不在本地 HEAD 历史中：

```text
Please pull down remote changes before pushing.
```

远程 `.gitlet` 不存在：

```text
Remote directory not found.
```

## 21.4 `fetch`

### 用法

```bash
java gitlet.Main fetch [remote name] [remote branch name]
```

### 行为

把远程给定分支中本地缺少的 commit 和 blob 复制到本地，并创建或更新本地分支：

```text
[remote name]/[remote branch name]
```

例如：

```text
origin/master
```

该本地远程跟踪分支指向远程分支头。

失败：

远程没有给定分支：

```text
That remote does not have that branch.
```

远程 `.gitlet` 不存在：

```text
Remote directory not found.
```

## 21.5 `pull`

### 用法

```bash
java gitlet.Main pull [remote name] [remote branch name]
```

依次完成：

1. `fetch [remote name] [remote branch name]`
2. 把 `[remote name]/[remote branch name]` 合入当前分支。

失败情况是 `fetch` 与 `merge` 的全部失败情况之和。

## 二十二、应避免的实现方式

1. `File.list` 和 `File.listFiles` 返回顺序未定义。需要确定顺序时必须显式排序，尤其是 `status`；`global-log` 虽顺序不限，也不要把未定义顺序当成逻辑依赖。
2. 不要硬编码 `/` 或 `\` 拼接路径。使用 `File` 多参数构造、`Paths` 或系统分隔符。
3. 序列化 `HashMap` 时条目顺序不确定，可能导致同内容对象产生不同字节和 SHA。需要确定顺序时使用 `TreeMap` 或自行稳定排序。
4. 不要让一个持久化对象直接引用整个提交历史，导致重复序列化。
5. 不要根据工作目录当前状态偷偷改变 `commit`；提交只应用已经暂存的内容。
6. 不要在执行危险命令的一半后才检查未跟踪文件。必须先验证，确认安全后再修改。
7. 不要依赖自动评分器替代本地集成测试。

## 二十三、完成前检查清单

- [ ] `gitlet.Main` 可从命令行运行；
- [ ] 所有状态位于 `.gitlet`；
- [ ] 初始提交消息、时间和 `master` 正确；
- [ ] blob 与 commit 使用稳定 SHA-1；
- [ ] 暂存添加与暂存删除正确持久化；
- [ ] 普通提交不读取未暂存工作目录修改；
- [ ] `log`、合并日志与空行格式精确；
- [ ] `status` 五节始终出现且排序正确；
- [ ] 三种 checkout 参数格式严格检查；
- [ ] 缩写提交 ID 可解析；
- [ ] 分支操作只移动或删除指针；
- [ ] reset 既恢复文件又移动当前分支头；
- [ ] merge 的分叉点和八种文件情况全部覆盖；
- [ ] 冲突标记和消息精确；
- [ ] 未跟踪文件保护在任何写操作前执行；
- [ ] 所有指定错误消息逐字一致；
- [ ] 路径跨 Windows、macOS、Linux；
- [ ] 自己编写了每条命令的集成测试；
- [ ] 设计文档与当前实现一致。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/proj/proj2/proj2){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
