---
title: "Project 0：2048"
description: "CS61B Spring 2021 Project 0：2048中文学习资料。"
hide:
  - toc
---

# Project 0：2048

- 原标题：Project 0: 2048
- 原页面：`https://sp21.datastructur.es/materials/proj/proj0/proj0`
- 原截止时间：2021-01-29

> **文档性质**：本文件依据 CS 61B Spring 2021 官方页面，由 ChatGPT 独立阅读后制作中文学习版。  
> 为保留技术准确性，类名、方法名、文件名、命令、报错文本和 API 名称保持英文。本文采用逐节翻译与重述，而不是网页的逐句镜像。

## 项目目标

在提供的 2048 图形程序中补全游戏逻辑。项目重点是：

- 阅读既有代码库。
- 理解类之间的职责。
- 编写小型辅助判断。
- 实现最核心的 `tilt`。
- 使用 JUnit 和 Debugger 验证行为。

## 代码结构

### `Tile`

表示一个数字方块及其位置和值。

### `Side`

表示观察或倾斜方向。项目设计允许把不同方向统一转换成“向北”视角，从而减少四套重复逻辑。

### `Model`

保存分数、游戏状态并实现移动逻辑。你的主要修改集中在这里。

### `Board`

保存棋盘上的 tile，并提供查询和移动操作。应使用它提供的 API，而不是破坏封装直接重写内部结构。

## 开始项目

先确保工作区干净：

```bash
git status
git pull skeleton master
```

需要重新开始时，可从 skeleton 恢复 `proj0`，但该操作会覆盖未提交修改，因此必须先 commit。

## 任务 1：`emptySpaceExists`

```java
public static boolean emptySpaceExists(Board b)
```

只判断棋盘是否存在空格。遍历所有坐标，只要有一个位置为 `null` 就返回 true。

## 任务 2：`maxTileExists`

```java
public static boolean maxTileExists(Board b)
```

只检查是否存在目标最大 tile。不要混入“还有没有合法移动”等其他逻辑。

## 任务 3：`atLeastOneMoveExists`

```java
public static boolean atLeastOneMoveExists(Board b)
```

存在以下任一情况即可继续：

- 有空格。
- 水平相邻 tile 值相同。
- 垂直相邻 tile 值相同。

注意边界，避免重复或越界访问。

## 主任务：`tilt(Side side)`

`tilt` 必须完成：

1. 所有 tile 朝指定方向尽可能移动。
2. 相同值 tile 按 2048 规则合并。
3. 每个 tile 每次 tilt 最多参与一次合并。
4. 更新 score。
5. 棋盘有变化时返回 true，并触发模型更新。

最稳妥的设计是把棋盘视角设为指定方向，使逻辑统一按“向北”处理，再恢复视角。

### 容易出错的合并

例如一列 `[2, 2, 2, 2]` 向上应得到 `[4, 4, 0, 0]`，而不是 `[8, 0, 0, 0]`。已经合并生成的新 tile 本轮不能再次合并。

## 测试

原项目提供测试组：

- `TestEmptySpace`
- `TestMaxTileExists`
- `TestAtLeastOneMoveExists`
- `TestUpOnly`
- `TestModel`

建议按此顺序完成。先确保辅助方法通过，再调试 `tilt`。

## 提交前检查

- 四个方向都正确。
- 不合法的合并不会发生。
- score 只增加合并值。
- 无变化时 `tilt` 返回 false。
- 没有修改禁止修改的 skeleton 文件。
- Git 工作区已 commit 并 push。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/proj/proj0/proj0){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
