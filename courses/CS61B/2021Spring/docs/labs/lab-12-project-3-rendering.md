---
title: "Lab 12：Project 3 入门"
description: "CS61B Spring 2021 Lab 12：Project 3 入门中文学习资料。"
---

# Lab 12：Project 3 入门

> 原文：https://sp21.datastructur.es/materials/lab/lab12/lab12<br>
> 说明：正文由 ChatGPT 直接翻译；API、类名、代码与文件名保持原样。

> IntelliJ 必须从 `proj3` 目录级别导入，否则 package 配置会出问题。

## Lab 前准备

1. 运行 `git pull skeleton master`，获取 Project 3、Lab 12 和 Lab 13 starter files。
2. 观看官方链接中的往届 Project 3 getting-started 视频；名称和 API 略有变化，但整体设计仍适用。
3. 阅读 Project 3 Phase 1 spec。
4. Project 3 是马拉松，不是短跑，不要拖到最后。
5. 提前联系 Project 3 partner，最好共同完成 Lab。
6. 整个 Project 3 必须保持同一个 partner。

## Part I：认识 Tile Rendering Engine

### Boring World

1. 在 IntelliJ 中打开 **`proj3`**，不是 `lab12`。
2. 通过 `pom.xml` 导入。
3. 本节只关注 `byow.lab12` package。
4. 运行 `BoringWorldDemo`。

世界生成分三步：

1. 初始化 `TERenderer`。
2. 生成二维 `TETile[][]`。
3. 调用 renderer 显示数组。

```java
TERenderer ter = new TERenderer();
ter.initialize(width, height);
```

宽高以 tile 数量为单位。每个 tile 为 16×16 像素，例如 `initialize(10,20)` 创建 10×20 tile，即 160×320 像素窗口。

可用 `TETile` 构造方法自行创建 tile，也可使用 `Tileset.java` 预生成 tile。初始化空世界：

```java
TETile[][] world = new TETile[WIDTH][HEIGHT];
for (int x = 0; x < WIDTH; x += 1) {
    for (int y = 0; y < HEIGHT; y += 1) {
        world[x][y] = Tileset.NOTHING;
    }
}
```

覆盖某一区域：

```java
for (int x = 20; x < 35; x += 1) {
    for (int y = 5; y < 10; y += 1) {
        world[x][y] = Tileset.WALL;
    }
}
```

最终显示：

```java
ter.renderFrame(world);
```

修改数组后，只有再次调用 `renderFrame` 才会更新屏幕。尝试替换 `WALL` 和循环边界。Tile 是 immutable，不能写：

```java
world[x][y].character = 'X'; // 非法设计
```

### Random World

运行 `RandomWorldDemo.java`。它展示：

- `java.util.Random` 伪随机数生成器；
- `switch`；
- 把任务分解给方法，而不是把所有逻辑写在 `main`。

```java
Random r = new Random(1000);
System.out.println(r.nextInt());
System.out.println(r.nextInt());
System.out.println(r.nextInt());
```

伪随机序列是确定性的；相同 seed 产生完全相同的序列：

```java
Random r = new Random(82731);
System.out.println(r.nextInt());
System.out.println(r.nextInt());
System.out.println(r.nextInt());
System.out.println(r.nextInt());

r = new Random(82731);
System.out.println(r.nextInt());
System.out.println(r.nextInt());
System.out.println(r.nextInt());
System.out.println(r.nextInt());
```

两组四个数相同。`new Random()` 未提供 seed 时，会用时间等频繁变化的值生成 seed。

Starter 使用固定 seed `2873123`，因此每次生成同一世界。Project 3 必须利用这一确定性，使相同输入能重建同一世界。

最重要的设计原则：把复杂任务不断拆成行为清楚的小方法，并形成抽象层级。

## Part II：使用 Tile Rendering Engine

### Hex World 目标

在 `HexWorld` 中创建随机六边形地形世界，类似六边形棋盘。应支持不同边长 `s`，并使用草地、花、沙漠、森林、山脉等不同 tile。

### 绘制单个六边形

实现类似：

```java
addHexagon(..., int s, ...)
```

把边长 `s` 的六边形画到指定位置。要求：

- 支持 `s = 2, 3, 4, 5...`；
- 最宽的“中间”始终有两行相同长度，这样才能无缝 tessellate；
- 通过 helper methods 拆分绘制和几何计算；
- 可为关键计算 helper 写 JUnit；
- 可以设计 `Hexagon` 类，但要认真决定对象知道什么、能做什么；
- `addHexagon` 的方法签名也是设计任务的一部分。

随机颜色可参考：

```java
TETile.colorVariant(...)
```

这个任务可能占用整节 Lab；做不完没关系，重点是设计思考。

### 绘制六边形镶嵌

在单个六边形完成后，尝试排列为含 **19 个六边形**的目标图案。

严禁把全部工作塞进一个巨大嵌套循环而不写 helper。没有层次化抽象，代码会难以理解、调试，也会让 TA 在有限 Office Hours 时间内无法帮助你。

观看官方 Live Coding Demo，观察 staff 如何逐步拆分问题。

## 进入 Project 3

阅读 Phase 1 spec，并查看 `project3prep.md`。与 partner 或 TA 讨论后填写。世界生成虽然比 Hex World 更复杂，但核心过程相同：确定可测试的小任务，再组合成高层世界生成器。

## 提交

提交填写完成的：

```text
project3prep.md
```

只要完整填写并提交即可获得本 Lab 满分。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/lab/lab12/lab12<br){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
