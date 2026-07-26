---
title: "Project 0：2048"
description: "CS61B Spring 2021 Project 0：2048中文学习资料。"
---

# Project 0：2048

> 截止日期：2021-01-29<br>
> 原始页面：<https://sp21.datastructur.es/materials/proj/proj0/proj0>
>
> 本文件为完整中文说明整理。代码、方法签名、类名、测试名和程序输出保持原样。

## 一、项目目的

本项目让你熟悉 Java、IntelliJ 和 JUnit。`proj0` 中虽然有大量文件，但你只需要修改 `Model.java` 中的四个方法：

- `emptySpaceExists`
- `maxTileExists`
- `atLeastOneMoveExists`
- `tilt`

本项目只按功能和提交内容评分，没有隐藏测试，也不单独评分代码风格。不过仍建议遵守课程 Style 61B 规范。

规格较长，骨架代码很多。开始编程前应先读完整份说明，过程中可能需要反复阅读。

## 二、2048 游戏规则

游戏在 `4 × 4` 网格上进行。每个方格为空，或放置一个值为 2 的幂的方块。

游戏开始前，在随机空格中生成一个 `2` 或 `4`：

- `2` 的概率为 75%；
- `4` 的概率为 25%。

玩家用方向键向北、南、东、西倾斜棋盘。所有方块沿该方向滑动，直到不能再前进，并可能发生合并。

### 合并的三条规则

1. 两个值相同的方块合并成一个值为原来两倍的方块。
2. 一次倾斜中，刚由合并产生的方块不能再次合并。
   - `[X, 2, 2, 4]` 向左应得到 `[4, 4, X, X]`，不是 `[8, X, X, X]`。
3. 沿移动方向连续三个相同方块时，最靠前的两个先合并，最后一个不参与该次合并。
   - `[X, 2, 2, 2]` 向左得到 `[4, 2, X, X]`，不是 `[2, 4, X, X]`。

因此四个连续相同方块会形成两组合并：

```text
[4, 4, 4, 4] → [8, 8, X, X]
```

若一次倾斜没有改变棋盘，就不会生成新方块；若棋盘改变，框架会在随机空位生成一个方块。**你不需要编写随机生成方块的代码。**

每次两个方块合并，分数增加新方块的值。游戏在以下任一条件成立时结束：

- 棋盘没有任何有效移动；
- 某个方块达到 2048。

`Max Score` 是当前程序会话中已经完成游戏的最高分，只有游戏结束时才更新。

## 三、程序结构

骨架代码采用了 MVC 和 Observer 设计模式。考试不要求掌握这些模式，但理解结构有助于阅读代码。

### MVC

- **Model**：保存棋盘状态和游戏规则。位于 `Model`、`Side`、`Board`、`Tile`；你只修改 `Model`。
- **View**：向用户显示状态，位于 `GUI` 和 `BoardWidget`。
- **Controller**：把用户操作转换为模型操作，主要位于 `Game`。

Observer 模式让视图注册为模型的观察者；模型改变时，视图获知并重绘。

### `Tile`

表示棋盘上的数字方块。`Tile` 变量为 `null` 表示空格。

你需要使用：

```java
tile.value()
```

它返回方块上的整数。

### `Side`

`Side` 是枚举，只有四种值：

```java
Side.NORTH
Side.SOUTH
Side.EAST
Side.WEST
```

枚举无需 `new`：

```java
Side s = Side.NORTH;
```

### `Model`

表示一局 2048 的完整状态，包括棋盘、分数、游戏结束状态等。

### `Board`

表示方块棋盘。你会用到：

- `setViewingPerspective`
- `tile`
- `move`

可选实验方法：`getRandomNonNullTile`。

> 只能提交和修改 `Model.java`。Gradescope 会用原始骨架替换其他文件，因此修改 `Tile.java`、`Board.java` 等不会生效。

## 四、获取与打开项目

先确保完成 Lab 1，并确认仓库干净：

```bash
git status
```

若有未提交修改，先 `add` 和 `commit`。不要在脏工作区开始新项目。

获取骨架（按课程仓库设置执行相应的 skeleton pull）。如果想把整个 `proj0` 恢复为骨架版本：

```bash
git checkout skeleton/master -- proj0
```

这会丢弃 `proj0` 中所有未提交修改；有需要先提交。

### IntelliJ 设置

1. 在 IntelliJ 中打开学生仓库里的 `proj0` 文件夹；
2. `.idea` 是 IntelliJ 配置目录，可以忽略；
3. `game2048` 是 Java 源代码目录；
4. `javalib` 包含 JUnit 和课程图形库的 `.jar`；
5. `File → Project Structure` 中选择 Java 15；
6. 在 Libraries 中确认 `javalib` 已加入；
7. 右键 `game2048/Main.java`，运行 `Main.main()`。

如果能弹出空白 2048 窗口，说明环境正常。

若代码能运行但 IntelliJ 仍显示错误红线：

```text
File → Invalidate Caches / Restart → Invalidate and Restart
```

不要在配置问题上独自耗费太久，应及时向课程工作人员求助并附上完整错误截图。

## 五、任务总览

推荐依次实现：

1. `emptySpaceExists`
2. `maxTileExists`
3. `atLeastOneMoveExists`
4. `tilt`

前三个用于判定游戏是否结束；`tilt` 负责方向键后的棋盘变化。

## 六、`emptySpaceExists`

```java
public static boolean emptySpaceExists(Board b)
```

若棋盘任一位置的 `Tile` 为 `null`，返回 `true`，否则返回 `false`。

应使用：

- `b.size()`
- `b.tile(int col, int row)`

不要直接访问 `Board` 的私有实例变量，也不要修改 `Board.java`。

实现后，`TestEmptySpace.java` 的全部 8 个测试应通过。

## 七、`maxTileExists`

```java
public static boolean maxTileExists(Board b)
```

如果任一方块值等于获胜值，返回 `true`。

不要硬编码：

```java
if (x == 2048)
```

而要使用：

```java
if (x == MAX_PIECE)
```

硬编码常数常被称为 magic number。使用命名常量可避免不同位置的数值不一致。

实现后应通过 `TestMaxTileExists.java`。

## 八、`atLeastOneMoveExists`

```java
public static boolean atLeastOneMoveExists(Board b)
```

如果存在任意方向的倾斜能让至少一个方块移动或合并，返回 `true`。

存在有效移动只有两种情况：

1. 棋盘至少有一个空格；
2. 至少有两个上下或左右相邻的方块值相同。

有空格的棋盘应返回 `true`：

```text
|   2|    |   2|    |
|   4|   4|   2|   2|
|    |   4|    |    |
|   2|   4|   4|   8|
```

完全填满且无相等相邻项时返回 `false`：

```text
|   2|   4|   2|   4|
|  16|   2|   4|   2|
|   2|   4|   2|   4|
|   4|   2|   4|   2|
```

虽然填满，但有可合并相邻项时返回 `true`：

```text
|   2|   4|  64|  64|
|  16|   2|   4|   8|
|   2|   4|   2|  32|
|   4|   2|   4|  32|
```

实现后应通过 `TestAtLeastOneMoveExists.java`。由于它可能调用 `emptySpaceExists`，应先确保后者全部通过。

## 九、主任务：`tilt`

```java
public boolean tilt(Side side)
```

此方法完成所有方块移动和合并。

例如原棋盘：

```text
|   2|    |   2|    |
|   4|   4|   2|   2|
|    |   4|    |    |
|   2|   4|   4|   8|
```

向上后：

```text
|   2|   8|   4|   2|
|   4|   4|   4|   8|
|   2|    |    |    |
|    |    |    |    |
```

除此之外：

1. 更新 `score`，增加所有新合并方块的值。上例增加 `8 + 4 = 12`；
2. 只要棋盘有任何变化，就把局部变量 `changed` 设为 `true`；
3. 方法最终返回棋盘是否变化；
4. 不要自己调用 `setChanged()`，骨架末尾会根据 `changed` 处理；
5. 所有棋盘读取都必须通过 `board.tile`；
6. 所有移动都必须通过 `board.move`；
7. 一次 `tilt` 中，一个具体 `Tile` 最多调用一次 `move`。

`board.move(c, r, t)` 若目标位置已有同值方块并发生合并，会返回 `true`，可以据此更新分数。

### 只先处理向上

先只考虑：

```java
side == Side.NORTH
```

使用 `TestUpOnly`：

- `testUpNoMerge`
- `testUpBasicMerge`
- `testUpTripleMerge`
- `testUpTrickyMerge`

处理一列时，最上方第 3 行不动。可以按从上到下的顺序考虑其他方块，先确定每块方块的最终目标行。

建议在纸上模拟大量例子，并编写辅助方法，例如：

- 处理一列；
- 计算某个方块最终行；
- 记录本列上一次合并位置。

### 每块方块只能移动一次

错误方式：

```java
Tile t = board.tile(3, 0);
board.move(3, 1, t);
board.move(3, 2, t);
board.move(3, 3, t);
```

正确思想是先算出最终位置，再一次移动：

```java
Tile t = board.tile(3, 0);
board.move(3, 3, t);
```

GUI 假设一次倾斜中同一方块只发生一次动画移动。

### 使用视角转换支持四个方向

不要为四个方向复制四份近似代码。`Board` 提供：

```java
board.setViewingPerspective(side);
```

它让指定方向在 `tile` 和 `move` 看来像 `NORTH`。

流程通常是：

1. `board.setViewingPerspective(side)`；
2. 用统一的“向北”逻辑处理；
3. 在返回前执行：

```java
board.setViewingPerspective(Side.NORTH);
```

**必须恢复 `Side.NORTH`，否则后续绘制和操作会异常。**

## 十、测试

课程提供完整测试，没有隐藏测试。

测试文件：

- `TestEmptySpace`
- `TestMaxTileExists`
- `TestAtLeastOneMoveExists`
- `TestUpOnly`
- `TestModel`

前三类和 `TestUpOnly` 主要是单元测试；`TestModel` 把多个方法放在一起，是集成测试。

正确调试顺序：

1. `TestEmptySpace`
2. `TestMaxTileExists`
3. `TestAtLeastOneMoveExists`
4. `TestUpOnly`
5. `TestModel`

不要在前面的测试尚未通过时调试 `TestModel`。

### 阅读失败信息

`TestEmptySpace`、`TestMaxTileExists` 和 `TestAtLeastOneMoveExists` 会显示棋盘和期望布尔值。

`TestUpOnly` 会显示：

- 倾斜方向；
- 倾斜前棋盘；
- 期望棋盘；
- 实际棋盘；
- 分数。

如果 `testUpTrickyMerge` 得到一个 `8` 而不是两个 `4`，通常说明违反了“合并生成的方块不能在同一倾斜中再次合并”。

先识别违反了三条规则中的哪一条，再用纸笔跟踪代码执行，最后重构，而不是盲目修改。

`TestModel` 还会测试：

- `gameOver`；
- 三个游戏结束辅助方法的协作；
- 连续多次 `tilt`。

不要求修改测试代码，但可以阅读 Javadoc 了解测试目的。

## 十一、评分

通过全部公开单元测试即可满分。

大致完成度对应：

1. 只实现 `emptySpaceExists` 或 `maxTileExists`：约 27%；
2. 除 `tilt` 外全部实现：约 47%；
3. `tilt` 只支持向上：约 68%；
4. 除合并外全部实现：约 64%；
5. 除合并规则 2 外全部实现：约 93%。

规则 2 虽难，但只占约 7%。

原课程提供提前一天激活最终 Gradescope 提交的 2 分额外加分。

## 十二、提交与版本控制

频繁提交。建议完成一个小里程碑或通过一组新测试就提交：

```bash
git status
git add <filepath>
git commit -m "Commit message"
git push
```

Git 只有在你真的提交时才能帮助恢复版本。提交信息应说明做了什么。

最终确认 Gradescope 激活的提交是你希望评分的版本，并检查只修改、提交了允许提交的 `Model.java`。

## 十三、获取帮助

遇到问题时：

- 先读测试 Javadoc 和失败棋盘；
- 缩小到具体规则和最小例子；
- 用调试器或纸笔跟踪；
- 在 Ed/Office Hours 求助时提供：错误信息、截图、已尝试的方法和最小失败测试；
- 不要公开贴出完整解答。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/proj/proj0/proj0){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
