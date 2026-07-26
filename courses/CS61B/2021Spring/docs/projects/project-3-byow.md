---
title: "Project 3：CS61BYoW"
description: "CS61B Spring 2021 Project 3：CS61BYoW中文学习资料。"
---

# Project 3：CS61BYoW 世界生成与探索引擎

> 团队表单截止：2021-03-31 23:59<br>
> Phase 1 世界生成截止：2021-04-16 23:59<br>
> Phase 2 交互截止：2021-04-27 23:59<br>
> 额外分展示截止：2021-04-30<br>
> 原始页面：<https://sp21.datastructur.es/materials/proj/proj3/proj3>
>
> 本文件为完整中文规格整理。类名、方法签名、按键、输入字符串、代码和 API 保持原样。

## 一、项目介绍

Project 3 要与一名搭档共同创建一个可探索世界的引擎。项目从构思、设计、实现、测试一直到展示，尽量模拟完整的软件产品开发周期。

本项目没有唯一正确的世界布局或代码结构，因此评分方式除通用自动评分外，还类似实习或工作中的绩效评审。世界设计可以不同，但必须满足基础规格。

项目需要大量探索和实验。可以查阅网上的技术资料，但不能使用往届项目解决方案。实现过程中经历多次设计迭代是正常且预期的。

核心不是强迫使用某种课堂数据结构，而是软件工程：

- 如何把大问题拆成模块；
- 如何管理少量骨架代码下的复杂度；
- 如何设计稳定接口；
- 如何保证随机系统可复现；
- 如何实现交互、保存和加载；
- 如何与搭档协作。

可以使用 A*、最小生成树、并查集等算法，但只有在真正适合你的设计、且你能正确使用时才采用。

项目开始前必须阅读搭档协作指南并提交搭档表单。Phase 2 和额外分不能使用 slip days，因为它们通过 TA checkoff 或展示评分。Phase 1 和 Lab 12、Lab 13 理论上可晚交，但 Phase 2 依赖它们，实际很难在晚交后仍按时完成。

## 二、总体任务

设计并实现一个二维、基于 tile 的俯视角世界探索引擎。

- 世界是 `TETile[][]` 二维网格；
- 程序根据随机种子生成世界；
- 用户能在世界中移动 avatar；
- avatar 能以某种方式与世界交互；
- 支持键盘模式和输入字符串模式；
- 支持保存和加载；
- 同一种子和同一输入序列必须得到完全相同结果。

世界可以使用骨架的 Unicode tile，也可自定义图形 tile；但必须使用课程提供的 TileEngine 和 `StdDraw` 作为显示基础。

项目分为两阶段：

1. **Phase 1：World Generation**：生成满足要求的随机世界；
2. **Phase 2：Interactivity**：加入菜单、avatar、HUD、交互、保存和加载。

## 三、骨架结构

### `byow.TileEngine`

包含渲染和 tile 基础结构：

- `TERenderer.java`：渲染方法；
- `TETile.java`：世界 tile 类型；
- `Tileset.java`：预置 tile 库。

**不要修改 `TETile.java` 的 `character` 字段或 `character()` 方法**，否则自动评分可能错误。

### `byow.Core`

推荐把项目主要代码放在此包中，但不是强制要求。

骨架提供：

- `RandomUtils.java`：随机数辅助方法；
- `Main.java`：程序入口，根据命令行参数选择 Engine 方法；
- `Engine.java`：包含两种交互方法。

必须实现：

```java
public TETile[][] interactWithInputString(String input)
```

处理一串按键，返回处理完所有输入后的世界状态。

```java
public void interactWithKeyboard()
```

从键盘读取输入，并把每次按键后的结果绘制到屏幕。

Lab 12 介绍 tile 渲染和伪随机；Lab 13 介绍用户输入和 UI。

### `StdDraw`

项目大量使用 `StdDraw`：

- 图形绘制；
- 键盘输入；
- 鼠标位置；
- 文本和菜单。

只允许使用：

- `java.*` 标准库；
- 仓库中 `library-sp21` 或骨架提供的库。

Phase 2 最终提交和 checkoff 不得引入其他外部库。额外分展示视频可以单独使用外部库。

### 禁止事项

- 不要使用非 `final` 的 `static` 变量；
- 不要调用 `System.exit()`，否则自动评分器进程会退出；
- 对 `Core.Main` 只做最少修改，把逻辑委托给其他类；
- 不要让 `interactWithInputString` 打开绘图窗口或播放声音。

<a id="phase-1"></a>

## 四、Phase 1：世界生成

世界必须满足以下全部条件：

1. 是用课程 TileEngine 绘制的二维网格；
2. 使用伪随机生成；
3. 包含明确的房间和走廊，也可包含室外区域；
4. 至少部分房间是矩形，也可支持其他形状；
5. 走廊必须能转弯，或通过相交直走廊实现等价连接；
6. 房间和走廊数量随机；
7. 房间和走廊位置随机；
8. 房间宽度和高度随机；
9. 走廊宽度为 1 或 2 个 tile，长度随机；
10. 墙壁与地板视觉上不同；
11. 墙壁、地板与未使用空间视觉上不同；
12. 房间和走廊必须连续连接，相邻区域地板之间不能出现空隙；
13. 所有房间都必须可达，不能出现无入口的孤立房间；
14. 不同种子生成的世界应显著不同，不能只是同一固定布局加少量可预测变化。

原规格示例中：

- `#` 表示墙；
- `.` 表示地板；
- 金色墙段表示上锁的门；
- 未使用空间为空白。

不要求复制示例布局或一定使用上锁的门，但必须满足上述结构要求。

## 五、默认 Tileset 与渲染

使用 `TETile[][]` 存储世界。常见 tile 可从 `Tileset` 获取，例如：

- `Tileset.NOTHING`
- `Tileset.WALL`
- `Tileset.FLOOR`
- `Tileset.AVATAR`

可以创建自定义 `TETile`。若希望不同 tile 被自动评分器识别为不同，必须保证它们的字符表示不同。

渲染时使用 `TERenderer`。Phase 1 调试可以自己编写 `main`：

1. 创建 renderer；
2. 调用 `interactWithInputString`；
3. 渲染返回数组。

但是自动评分调用 `interactWithInputString` 时，该方法本身不得使用 `StdDraw`、初始化 renderer、打开窗口、画图或播放声音。

## 六、启动程序与输入协议

### `Main.main`

用户通过两种方式启动：

#### 命令行字符串模式

格式：

```bash
-s inputString
```

`Main.main` 应调用：

```java
Engine.interactWithInputString(inputString)
```

#### 键盘模式

不提供命令行参数时，调用：

```java
Engine.interactWithKeyboard()
```

### Phase 1 输入

至少支持：

```text
N#######S
```

其中：

- `N`：创建新世界；
- `#`：任意数量数字，组成种子；
- `S`：种子输入结束并开始生成。

例如：

```text
N3412S
```

表示用种子 `3412` 创建新世界。

字母大小写不敏感：

- `N` 与 `n` 等价；
- `S` 与 `s` 等价；
- 后续 `WASD`、`L`、`Q` 同样大小写不敏感。

种子必须作为 `long` 处理，支持最大正值：

```text
9,223,372,036,854,775,807
```

超过该值的行为不定义。不要用 `Integer.parseInt`，应使用 `Long` 对应解析方法。

### IntelliJ 参数

可在：

```text
Run > Edit Configurations > Program Arguments
```

填写输入字符串。若尚未运行过 `main`，可点击方法旁绿色箭头并选择 `Modify Run Configurations`。

### Phase 1 总结

- `Main.main` 接受 `-s inputString`；
- `interactWithInputString` 返回符合要求的 `TETile[][]`；
- 不同种子应产生视觉上不同的世界；
- 同一种子重复调用应返回完全相同世界；
- 自动评分阶段不包含 avatar 移动；
- 求助前应有最新设计文档。

## 七、键盘主菜单

`interactWithKeyboard()` 启动后，必须显示主菜单，至少包含：

```text
N - New World
L - Load Game
Q - Quit
```

要求：

- 完全可通过键盘操作；
- N、L、Q 大小写不敏感；
- 可增加其他菜单选项；
- 但 N、L、Q 的行为必须与规格完全一致。

按 N 后：

1. 提示输入随机种子；
2. 屏幕实时显示已经输入的数字；
3. 用户按 S 结束种子输入；
4. 生成并显示世界。

可加入角色选择、世界参数等自定义选项，但不能改变标准协议。例如：

```text
N23123S
```

必须直接以种子 `23123` 创建世界，不能再要求自动评分器提供其他输入。

## 八、设计文档

由于骨架少、实现高度开放，必须维护 `proj3/README.md` 设计文档。

设计文档不计分，但若没有最新文档：

- Course Staff 可能无法处理 Gitbug；
- Office Hours 无法快速理解你的实现；
- 特定于个人架构的问题可能得不到帮助。

设计文档应随着代码不断更新，而不是只在开始时写一次。

### 设计文档作用

描述：

- 程序由哪些概念模块组成；
- 使用哪些类和抽象；
- 各类使用的数据结构和算法；
- 模块如何交互；
- 持久化状态存在哪里。

写设计文档可帮助：

- 编码前规划；
- 发现设计缺陷；
- 分解复杂功能；
- 调试跨模块问题；
- 与搭档和 TA 沟通。

### 文档格式

使用 Markdown，写在：

```text
proj3/README.md
```

IntelliJ 可显示 Markdown 预览。

### 第 1 节：Classes and Data Structures

对每个类列出：

- 类的用途；
- 实例变量；
- 每个变量保存什么；
- 为什么需要它。

保持简洁，不需要在这里解释完整算法。

### 第 2 节：Algorithms

对每个类的方法写高层行为：

- 方法完成什么；
- 使用什么步骤或数据结构；
- 处理哪些边界情况；
- 与哪些其他类交互。

不要逐行解释代码，也不要复述规格。要说明**你的实现如何完成规格**。

复杂任务应继续拆分，例如“随机生成不同大小的房间”可分为：

1. 产生尺寸；
2. 产生位置；
3. 检查越界与重叠；
4. 放置地板；
5. 建墙；
6. 与已有区域连接。

不同子任务可放在不同类中。若算法调用其他类的方法，应明确写出依赖。

### 第 3 节：Persistence

Phase 1 完成后再补充。描述：

- 保存哪些状态；
- 使用哪些类和方法；
- 创建哪些 `.txt` 文件；
- 加载时如何恢复世界、avatar、随机状态和其他游戏机制。

规格提供了 Capers Lab 设计文档示例作为参考。

<a id="phase-2"></a>

## 九、Phase 2：交互性

必须加入：

- 可通过 `WASD` 控制的 avatar；
- avatar 与世界的某种交互；
- HUD；
- 保存和加载；
- 字符串模式中的移动与保存加载；
- 完全确定性。

### Avatar 移动

默认按键：

- `W`：上；
- `A`：左；
- `S`：下；
- `D`：右。

按键可同时触发其他机制，例如推动物体，但基础移动必须存在。

若目标 tile 是墙：

- avatar 不移动；
- 程序不得报错。

avatar 可以用 `@` 或任何清楚的 tile 表示。

### 交互要求

avatar 必须能以某种方式和世界互动。规格不限定具体形式，可包括：

- 拾取物品；
- 开门；
- 推动物体；
- 与实体对话；
- 触发地形或事件。

### 确定性

同一个种子和完全相同的按键序列必须每次产生完全相同结果。

`Random` 对同一种子会给出相同伪随机序列。不能使用真实时间驱动世界逻辑，因为时间不会记录在输入字符串里。

可以使用“回合数”：每个按键算一回合，例如世界随步数变暗。也可以允许空格表示等待一回合。

### 保存文件限制

程序可在 `proj3` 目录创建保存文件，但**所有创建文件必须以 `.txt` 结尾**，例如：

```text
savefile.txt
```

其他后缀会造成自动评分问题。

## 十、UI 外观

世界显示后，UI 至少包含：

1. 当前世界的二维 tile 网格；
2. HUD（Heads Up Display）。

HUD 至少要显示鼠标当前指向 tile 的描述，例如：

```text
wall
floor
avatar
```

HUD 必须位于世界 tile 区域之外或清楚分隔的位置。可参考：

```java
TERenderer.initialize(int width, int height, int xOffset, int yOffset)
```

或 Lab 13。

可以添加：

- 生命值；
- 分数；
- 当前任务；
- 操作提示；
- tile 的详细描述或 flavor text；
- 地图名称；
- avatar 名称。

## 十一、UI 行为与 `:Q`

探索过程中，用户输入：

```text
:Q
```

必须立即：

1. 保存当前状态；
2. 完全退出程序。

要求：

- `:q` 也有效；
- 不得再询问“是否确认”；
- 冒号后跟任何其他字符都不做任何事；
- `StdDraw` 不支持组合键，因此 `:Q` 是先按 `:`，再按 `Q`。

`StdDraw` 只能注册产生字符的按键：

- Unicode 字符可用；
- 方向键、Escape 等不作为标准输入方案；
- 某些系统不支持持续按住键重复移动。

若自行支持长按，仍必须保证它能被输入字符串等价重放。

## 十二、保存与加载

系统必须保存完整世界状态，并在下一次启动后精确恢复。

加载状态包括但不限于：

- 世界 tile；
- avatar 位置；
- 所有实体和物品状态；
- 当前分数、生命或任务；
- 随机数生成器状态，或足以重建相同状态的输入历史；
- 任何会影响未来行为的信息。

程序结束时变量会消失，因此必须把状态持久化到文件。

当重新运行 `byow.Core.Main` 并按 L 时，世界应与上次 `:Q` 前完全一致。

若用户按 L 但没有任何存档：

- 程序直接退出；
- UI 关闭；
- 不输出错误。

基础规格中，`:Q` 保存后立即终止，所以一个合法输入字符串中的 `:Q` 后不应再有其他字符。继续游戏必须重新运行，以 `L` 开头。

## 十三、输入字符串与 Phase 2

`interactWithInputString` 必须模拟键盘模式，但：

- 不显示菜单；
- 不绘图；
- 不播放声音；
- 最后返回 `TETile[][]`。

例如：

```text
N543SWWWWAA
```

含义：

1. 新建世界；
2. 种子 543；
3. 向上四次；
4. 向左两次。

返回值必须与真实用户在 `interactWithKeyboard` 中输入同样按键后的世界完全一致。

### 字符串保存与加载

```text
N25SDDWD:Q
```

表示：

- 种子 25 新建世界；
- 右、右、上、右；
- 保存并退出；
- 方法返回保存时的 `TETile[][]`。

随后：

```text
LDDDD
```

加载刚才存档，再向右四次，返回移动后的世界。

### 必须等价的调用

以下最终返回世界必须完全相同：

```text
interactWithInputString("N999SDDDWWWDDD")
```

```text
interactWithInputString("N999SDDD:Q")
interactWithInputString("LWWWDDD")
```

```text
interactWithInputString("N999SDDD:Q")
interactWithInputString("LWWW:Q")
interactWithInputString("LDDD:Q")
```

```text
interactWithInputString("N999SDDD:Q")
interactWithInputString("L:Q")
interactWithInputString("L:Q")
interactWithInputString("LWWWDDD")
```

保存和加载本身不得改变世界。

不需要处理一个字符串里多个 `:Q`，例如：

```text
N5SDD:QD:QDD:Q
```

不是合法 replay string，因为程序应在第一次 `:Q` 时结束。

自动评分器提供的字符串可假定：

- 以 `N#S` 开头，其中 `#` 是种子；或
- 以 `L` 开头。

`interactWithInputString` 返回值不应因末尾是否有 `:Q` 而变化。唯一差异是 `:Q` 会产生保存副作用。

## 十四、Ambition Score

项目中 360 分来自自选功能。功能分两类：

- Primary Feature：270 分；
- Secondary Feature：90 分。

要拿满 360 分，至少实现一个 Primary。可以组合：

- 1 个 Primary + 1 个 Secondary；
- 或更高总分，但该类别最多只计 360 分。

实现自选功能不能破坏基础要求。例如加入鼠标移动后，仍必须支持 `WASD`。

### 270 分 Primary Features

任选：

1. **视线系统**：只渲染 avatar 视线内 tile，并能按键开关；可以是拐角视线，也可以是 avatar 周围方形光区。
2. **动态光源**：光源改变世界渲染，至少一个光源能按键开关。
3. **追踪实体**：实体使用课堂搜索算法追逐 avatar 或其他实体，并可切换显示预测路径。
4. **Encounter 系统**：avatar 接触实体时切换到新界面，互动结束后回到原世界，例如 Pokémon。
5. **Replay**：视觉重放自新世界创建以来或最近保存中的全部动作，最终状态必须与正常加载相同。
6. **切换视角**：第一人称、2.5D 等不同视角。

### 90 分 Secondary Features

可选：

- 多个存档槽，通过菜单和新快捷键访问，同时保留默认存取行为；
- 不关闭程序即可创建新世界；
- 菜单中修改 avatar 外观；
- 给 avatar 命名并显示在 HUD；
- 选择或随机决定世界主题/环境；
- 菜单切换 UI 语言，默认英文且能切回；
- 主菜单支持鼠标点击完成全部键盘操作；
- 使用图片而非 Unicode 字符渲染；
- 菜单/探索音乐和交互音效；
- 显示完整地图与 avatar 的 minimap；
- 旋转世界 90 度，并相应调整移动键；
- HUD 显示真实日期时间；
- 点击可见格子自动寻路移动；
- 双人同时交互，两个 avatar 和不同控制方案；
- 撤销移动，包括跨保存加载前的移动；撤销命令仍应加入 replay string，不能简单删除历史字符。

## 十五、基础要求汇总

以下清单不能代替完整规格：

- [ ] 键盘模式有 N、L、Q 菜单，大小写不敏感；
- [ ] 新世界输入整数种子并按 S；
- [ ] 输入种子时 UI 显示已输入数字；
- [ ] 世界按种子伪随机生成，不同种子不同；
- [ ] 世界满足 Phase 1 房间、走廊、连接、墙地板等全部要求；
- [ ] 用户可用 `WASD` 移动；
- [ ] `:Q` 保存并退出；
- [ ] 下次按 L 精确恢复；
- [ ] 所有随机事件对同一种子和输入是确定的；
- [ ] `interactWithInputString` 与键盘模式除输入/绘制外行为一致；
- [ ] `interactWithInputString` 返回处理最后字符后的 `TETile[][]`；
- [ ] 字符串模式支持保存和加载；
- [ ] 使用课程 TileEngine 与 `StdDraw`；
- [ ] 有 HUD；
- [ ] HUD 鼠标悬停显示 tile 描述；
- [ ] 不使用真实时间驱动任何世界变化；
- [ ] Ambition 功能共 360 分，至少一个 Primary。

## 十六、额外分：把世界做成游戏

额外分要求：

1. 世界有明确胜利或失败条件；
2. 加入至少 3 个“creative mechanics”；
3. 至少 2 个机制必须由团队自己原创；
4. 制作公开 YouTube 视频展示：
   - 创意机制；
   - 胜负条件；
   - 实际游戏效果；
5. 一名搭档提交表单即可。

游戏不要求作者本人一定能通关，难度可以很高。

原规格给出的机制灵感中，最多只有一个能计入要求的三个机制：

- 菜单中可阅读世界观和故事；
- 每个 tile 有 flavor text，鼠标悬停时和名称一起显示；
- 彩蛋或作弊码，如 Konami Code；
- 会游荡并破坏 tile 的实体；
- 多屏幕、楼层、楼梯或滚动地图；
- 与 avatar 互动的 NPC，例如追逐玩家的幽灵；
- 传送门；
- 排行榜或高分榜，至少显示前十名和名称；
- 动画；
- 可收集并改变分数或能力的物品；
- inventory；
- health 机制。

<a id="submission"></a>

## 十七、提交与评分

### Gradescope

必须把搭档添加为 group member。

除 Gradescope 外，还要提交 Project 3 Checkoff Form。若不提交表单，checkoff 部分得 0 分。只需一名搭档提交，但应共同填写。

### 分数

自动评分：200 分：

- Phase 1：100；
- Phase 2：100。

Partner Review：160 分：

- Phase 1：80；
- Phase 2：80。

Checkoff Demo：1240 分：

- Ambition：360；
- 基础 Phase 1/2 规格：880。

额外分：32 分。

### 选择评分 Commit

提交表单前：

1. 用 `git log` 找到希望评分的 commit SHA；
2. 最好与 Gradescope 提交版本一致；
3. 允许为了自动评分临时注释某些 checkoff 功能，并在 checkoff commit 中恢复，但务必实际运行确认；
4. commit 必须在截止时间前，否则有 50% 迟交惩罚；
5. 把 SHA 准确粘贴到表单；
6. 若 SHA 无效，默认可能评分 `origin/HEAD`，可能导致错误版本或迟交惩罚。

### Checkoff Form

表单要求说明：

- 尝试了哪些 Ambition 功能；
- 怎样操作；
- 已知 quirks；
- 评分 commit SHA。

说明应简洁清楚。若功能需要很复杂的操作说明，应考虑简化 UI。

提交前确认：

1. 项目完成；
2. 再读一遍全部规格；
3. 已确定评分 commit；
4. 只用 `library-sp21` 或 `java.*`；
5. 所有文件路径跨操作系统。

不要硬编码：

```java
String pathToImage = "images/image1.jpg";
```

可使用 Project 2 `Utils.join`：

```java
import java.nio.file.Paths;

/** Return the concatentation of FIRST and OTHERS into a File designator,
 *  analogous to the {@link java.nio.file.Paths#get(String, String...)}
 *  method. */
static File join(String first, String... others) {
    return Paths.get(first, others).toFile();
}
```

## 十八、自动评分器

### Phase 1 Grader

截止：2021-04-16 23:59，100 分。

测试：

- `interactWithInputString` 返回世界；
- 相同种子多次生成相同世界；
- 不同种子生成不同世界。

不会测试移动。

### Phase 2 Grader

截止：2021-04-27 23:59，100 分。

测试：

- 相同种子和相同移动得到相同世界；
- 不同种子和不同移动产生不同世界；
- 输入中穿插保存和加载，最终仍与连续输入完全一致。

提交时记得添加搭档为 group member。

## 十九、Office Hours 求助要求

由于项目开放，Staff 难以像小项目一样直接定位错误：

- 每位学生约最多 10 分钟；
- 设计文档必须反映当前实现；
- 所有自写方法都应按 style guide 写文档；
- 调试问题必须能说明具体错误；
- 必须准备可重复触发的测试或输入；
- 若没有写测试、没有尝试调试器，Staff 可能不提供调试帮助；
- Staff 可能只给高层重构建议，而不会在混乱、脆弱代码中逐行找 bug。

## 二十、FAQ

### 可以做室外世界或洞穴，不只做房间吗？

可以，但必须仍满足基础房间和走廊要求。可让种子先生成一个符合要求的 starter house，avatar 能离开并探索室外或洞穴。

### 可以支持滚动地图或多个楼层吗？

可以。`interactWithInputString` 应返回处理最后一个字符时屏幕当前可见的那一部分世界。

### 可以在建世界前自定义角色吗？

可以，但应增加第四个菜单选项。标准 API 不得改变：

```text
N23123S
```

必须始终直接用种子 23123 创建新世界，不得要求额外输入。

### 为什么出现两个 StdDraw 窗口？

确认导入：

```java
edu.princeton.cs.introcs.StdDraw
```

而不是：

```java
edu.princeton.cs.algs4.StdDraw
```

### Phase 1 自动评分器报 `Could not initialize class edu.princeton.cs.introcs.StdDraw`

`interactWithInputString` 内部某处使用了 `StdDraw`，例如调用 `TERenderer.initialize()`。字符串模式不得打开任何窗口。某些代码可能只对特定种子渲染，要逐条检查。

### `Integer.parseInt` 导致 `NumberFormatException`

种子可能超过 `int`，`Random` 接受 `long`。使用 `Long` 解析。

### 自动评分器说不同种子世界不 distinct，但肉眼看不同

检查每种 tile 是否使用不同字符。若两个自定义 tile 的 character 相同，评分器可能把世界视为相同。

### 自定义类实例应该相等，但 `equals` 或 HashMap 查找失败

同时重写：

```java
equals(Object o)
hashCode()
```

相等对象必须有相同 hash code。

### 使用 `InputDemo` 后 HUD 不更新

`InputDemo` 只是演示。`KeyboardSource.getNextKey` 是阻塞式：没有按键时不会返回，因此主循环无法刷新鼠标 HUD。需要修改输入架构，使没有键盘输入时也能继续刷新界面。

## 二十一、完成检查清单

- [ ] 与搭档共同维护设计文档；
- [ ] 没有非 final static 状态；
- [ ] 没有 `System.exit()`；
- [ ] `interactWithInputString` 不使用 StdDraw；
- [ ] 世界全部连通并满足房间/走廊规格；
- [ ] 同种子同输入完全确定；
- [ ] 菜单 N/L/Q 大小写不敏感；
- [ ] 支持最大正 `long` 种子；
- [ ] `WASD`、墙碰撞和 avatar 交互正常；
- [ ] HUD 鼠标悬停信息正常；
- [ ] `:Q` 立即保存退出；
- [ ] 无存档时 L 安静退出；
- [ ] 连续输入与多次保存加载结果等价；
- [ ] 只创建 `.txt` 保存文件；
- [ ] 文件路径跨平台；
- [ ] Ambition 共 360 分且含 Primary；
- [ ] 自动评分 commit 与 checkoff commit 已验证；
- [ ] 提交了 Gradescope group 和 checkoff form。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/proj/proj3/proj3){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
