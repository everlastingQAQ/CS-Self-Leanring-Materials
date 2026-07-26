---
title: "Project 1：数据结构"
description: "CS61B Spring 2021 Project 1：数据结构中文学习资料。"
---

# Project 1：数据结构

> 截止日期：2021-02-16<br>
> 原始页面：<https://sp21.datastructur.es/materials/proj/proj1/proj1>
>
> 本文件为中文翻译整理。API、代码、命令、测试名和公式保持原样。

## 一、项目概览

你将分别用链表和数组实现双端队列（Deque），再利用该数据结构完成最大值双端队列和 Karplus-Strong 吉他弦声音合成器。

项目分为：

1. 数据结构部分：
   - `LinkedListDeque.java`
   - `ArrayDeque.java`
   - `Deque.java`
   - `MaxArrayDeque.java`
2. 应用部分：
   - `gh2/GuitarString.java`
   - 使用 `GuitarHeroLite`、`TTFAF` 等客户端播放声音。

你必须独立完成项目，并遵守协作与学术诚信政策。项目会检查 Style 61B，风格不合格会扣分。

原课程安排了 2 月 5 日检查点额外分，正式项目只允许使用最多两天 slip days，因为后续 Lab 4 依赖本项目。

## 二、获取骨架

在学生仓库内运行：

```bash
git pull skeleton master
```

较新 Git 版本如有需要：

```bash
git pull skeleton master --allow-unrelated-histories
```

目录大致为：

```text
proj1/
├── deque/
│   └── LinkedListDequeTest.java
└── gh2/
    ├── GuitarHeroLite.java
    ├── GuitarPlayer.java
    ├── GuitarString.java
    ├── TTFAF.java
    └── TestGuitarString.java
```

如果 Git 报错，停止盲目尝试，阅读课程 Git 指南或求助。**不要使用 force push。**

提供的 `LinkedListDequeTest.java` 只是简单样例，不完整；你必须自行补充测试。

## 三、包（Package）

项目最终有两个包：

- `deque`：双端队列数据结构；
- `gh2`：声音合成程序。

包是一组共同完成某项功能的 Java 类。例如：

```java
org.junit.Assert.assertEquals
```

其中：

- `org.junit` 是包名；
- `Assert` 是类名；
- `assertEquals` 是方法名；
- 完整形式称为 canonical name；
- 单独的 `assertEquals` 称为 simple name。

声明某文件属于 `deque` 包：

```java
package deque;
```

外部使用时可以写：

```java
deque.ArrayDeque
```

或先导入：

```java
import deque.ArrayDeque;
```

包避免不同项目中的同名类冲突，也帮助大型项目分层组织。

## 四、Deque API

Deque（读音类似 deck）是 double-ended queue，可在首尾两端扩张或收缩。

两种实现都必须提供：

```java
public void addFirst(T item)
public void addLast(T item)
public boolean isEmpty()
public int size()
public void printDeque()
public T removeFirst()
public T removeLast()
public T get(int index)
public Iterator<T> iterator()
public boolean equals(Object o)
```

行为要求：

### `addFirst(T item)`

把 `item` 加到队首。可假设 `item` 永不为 `null`。

### `addLast(T item)`

把 `item` 加到队尾。可假设非 `null`。

### `isEmpty()`

空则返回 `true`。

### `size()`

返回当前元素个数。

### `printDeque()`

从首到尾打印，每个元素后以空格分隔，最后换行。泛型对象可直接：

```java
System.out.print(item);
```

Java 会使用对象的 `toString()`。

### `removeFirst()` / `removeLast()`

删除并返回首/尾元素；空队列返回 `null`。

### `get(int index)`

返回从队首开始索引为 `index` 的元素，`0` 为首项。越界返回 `null`。不能改变队列。

### `iterator()`

两种实现都要支持增强型 `for` 循环，因此实现 `Iterable<T>` 并返回 `Iterator<T>`。

> 不要让 `Deque` 接口本身 `extends Iterable`；只让 `LinkedListDeque` 和 `ArrayDeque` 实现 `Iterable<T>`，否则当学期自动评分器会报 API 错误。

### `equals(Object o)`

当且仅当：

- `o` 也是一个 Deque；
- 两者元素数量相同；
- 对应位置元素按照泛型对象的 `equals` 相等；
- 顺序相同；

才返回 `true`。需要使用 `instanceof`。

所有类都必须支持任意泛型对象，而不仅是整数。

## 五、任务 1：`LinkedListDeque`

创建：

```text
proj1/deque/LinkedListDeque.java
```

文件顶部：

```java
package deque;
```

使用链表实现全部 Deque API，并提供：

```java
public LinkedListDeque()
public T getRecursive(int index)
```

其中 `getRecursive` 与 `get` 行为相同，但必须使用递归。

### 性能和内存要求

- `addFirst`、`addLast`、`removeFirst`、`removeLast` 不得使用循环或递归，必须为常数时间；
- `get` 必须迭代实现；
- `getRecursive` 必须递归实现；
- `size` 必须常数时间；
- 完整遍历的时间应与元素数量成正比；
- 删除元素后不能继续保留指向它的引用；
- 空间使用必须与当前元素数成正比。

允许添加私有节点类和辅助方法，需写有帮助的 Javadoc。

推荐使用哨兵节点，尤其是循环哨兵结构。禁止使用 Java 内置 `LinkedList` 或任何 `java.util.*` 数据结构；若检测到会直接判零分。

## 六、任务 2：`ArrayDeque`

创建：

```text
proj1/deque/ArrayDeque.java
```

使用数组作为核心存储，实现全部 API，并提供：

```java
public ArrayDeque()
```

### 要求

- 初始数组长度为 `8`；
- 除扩容/缩容外，`add` 与 `remove` 必须常数时间；
- `get` 和 `size` 必须常数时间；
- 建议把底层数组视为循环数组；
- 必须记录队首、队尾或下一可用位置；
- 内存使用应与当前元素数成正比；
- 当底层数组长度至少为 16 时，使用率必须始终至少为 25%。

也就是说，一次删除若会让使用率低于 25%，应缩小数组。长度小于 16 时允许更低使用率。

扩缩容时必须正确重排循环数组中的元素。建议先画图，明确逻辑顺序与物理索引的映射，再编写代码。

## 七、检查点额外分

检查点测试基础功能：

- 两种 `add`；
- 两种 `remove`；
- `size`；
- `isEmpty`；
- `get`。

不测试：

- `equals`；
- `iterator`；
- `ArrayDeque` 扩容（最多放 8 个元素）。

检查点不是必做，但能帮助确认进度。

## 八、测试策略

测试是项目核心目标之一。提供的 `LinkedListDequeTest.java` 只是 sanity check，需取消相应测试和 `@Test` 注释后运行。

不要只依赖自动评分器。正式自动评分器 token 每 8 小时恢复一次，不能累积；截止日前恢复频率会提高。

应把 Lab 3 的测试方式迁移过来：

- 确定性单元测试；
- 随机差分测试：将你的 deque 与可信参考结构执行同一随机操作序列；
- 大规模测试，运行数万或数十万次操作；
- 计时测试，验证 `get`、`size`、首尾操作复杂度；
- 测试空 → 非空 → 空 → 再非空；
- 测试扩容后环绕、缩容后顺序；
- 测试 `equals` 的跨实现比较、`null`、不同类型和不同顺序。

在 `Deque` 接口和全部必需方法实现前，完整自动评分器可能无法编译你的代码，应先使用检查点评分器和本地测试。

## 九、`MaxArrayDeque`

在确认 `ArrayDeque` 正确后，实现：

```java
public class MaxArrayDeque<T> extends ArrayDeque<T>
```

不要复制整份 `ArrayDeque` 代码；本任务强调继承和减少重复。

新增：

```java
public MaxArrayDeque(Comparator<T> c)
public T max()
public T max(Comparator<T> c)
```

- 构造器保存默认比较器；
- `max()` 使用构造器提供的比较器；
- `max(c)` 使用参数比较器；
- 空 deque 返回 `null`；
- 若多个元素并列最大，可返回任意一个；
- 这两个新增方法没有特殊复杂度要求；
- 本类的 `equals` 不测试，可自行选择合理行为。

必须自行编写测试，并创建多个不同 `Comparator<T>`，例如按整数大小、字符串长度或对象字段比较。

`MaxArrayDeque` 与后面的 Guitar Hero 部分相互独立。

## 十、`Deque` 接口

新建：

```text
proj1/deque/Deque.java
```

把 API 方法声明放入泛型接口：

```java
public interface Deque<T> {
    ...
}
```

让实现类声明：

```java
implements Deque<T>
```

若写成 `implements Deque`，可能出现擦除冲突：

```text
The method ... has the same erasure ... but does not override it.
```

给所有重写方法添加 `@Override`。

在接口中为 `isEmpty` 提供默认实现：

```java
default boolean isEmpty() {
    return size() == 0;
}
```

然后可以删除两个实现类中重复的 `isEmpty`。

## 十一、Guitar Hero 与 `GuitarString`

`gh2` 包使用你实现的 `Deque<Double>` 模拟拨动吉他弦。

主要修改：

```text
gh2/GuitarString.java
```

### Karplus-Strong 算法

1. 拨弦时，把缓冲区中的每个值替换为 `[-0.5, 0.5)` 的随机噪声；
2. 每次 `tic`：
   - 删除队首样本；
   - 读取新的队首样本；
   - 计算两者平均值，再乘能量衰减因子 `0.996`；
   - 把新值加到队尾；
3. 客户端播放刚删除的样本，并不断重复。

若队首是 `0.2`，下一项是 `0.4`：

```text
(0.2 + 0.4) / 2 × 0.996 = 0.2988
```

删除并播放 `0.2`，把 `0.2988` 放到队尾。

构造器必须按频率计算缓冲区容量，并先填满零。`GuitarString` 自己**不播放声音**，播放由客户端负责。

可选择 `ArrayDeque` 或 `LinkedListDeque` 作为内部实现，因为只依赖接口操作。

用 Maven 打开项目，否则 IntelliJ 可能找不到 `StdAudio`。

测试：

- `testPluckTheAString`：应听到 A 音；
- 若失败，先调试 `testTic`；
- 可临时写 `print`/`toString` 观察每次 tic 前后的缓冲区。

## 十二、`GuitarHeroLite` 与 37 键扩展

完成 `GuitarString` 后运行 `GuitarHeroLite`，可用 GUI 交互播放。

不计分扩展：支持 37 个半音，键盘映射：

```java
String keyboard = "q2we4r5ty7u8i9op-[=zxdcfvgbnjmk,.;/' ";
```

第 `i` 个字符频率：

```text
440 × 2^((i - 24) / 12)
```

例如：

- `q`：110 Hz；
- `i`：220 Hz；
- `v`：440 Hz；
- 空格：880 Hz。

不要创建 37 个单独变量或 37 路 `if`。应创建长度 37 的 `GuitarString[]`，并用：

```java
keyboard.indexOf(key)
```

查找按键。无映射按键不能让程序崩溃。

## 十三、趣味扩展

完成后可运行 `TTFAF`，阅读 `GuitarPlayer` 和 `TTFAF`。

其他不计分扩展：

- **竖琴**：在 `tic()` 入队前翻转新值符号，并调整衰减和缓冲区；
- **鼓**：以 0.5 概率翻转符号，衰减可设为 1.0；
- **六根琴弦分组**：拨动一个音时衰减/清空同组其他弦；
- **钢琴延音/制音踏板**：按键状态决定衰减；
- **纯律**：用小整数比率而不是十二平均律设置音程。

## 十四、为什么算法能发声

- 环形缓冲区模拟能量在两端固定的弦上往返；缓冲区长度决定基频；
- 反馈加强基频及其整数倍谐波；
- `0.996` 模拟每次往返的能量损耗；
- 平均操作是温和的低通滤波器，使高频谐波逐渐减弱，接近真实拨弦音色。

## 十五、提交与评分

提交步骤：

1. `git add`、`git commit`；
2. 推送学生仓库；
3. 在 Gradescope 提交；
4. 最终提交后推送 snaps 仓库：

```bash
cd $SNAPS_DIR
git push
```

5. 在对应 Snaps Gradescope 作业中提交 snaps 仓库，否则分数不会同步到 Beacon。

正式项目总分 640：

- `deque/LinkedListDeque`：230；
- `deque/ArrayDeque`：230；
- `deque/MaxArrayDeque`：80；
- `gh2/GuitarString`：80。

额外分共 48：

- 检查点：16；
- 自制自动评分器：32。

## 十六、FAQ

### 泛型元素如何打印？

直接：

```java
System.out.print(item);
```

会调用对象的 `toString()`。

### 不能创建泛型数组

使用：

```java
T[] a = (T[]) new Object[1000];
```

会产生 unchecked cast 警告，这是 Java 泛型设计限制。

### 引用能指向对象的某个字段吗？

不能。Java 引用指向整个对象，不会指向数组中间或对象某字段；课堂图中的箭头只是表示对象关系。

### `class file contains wrong class`

检查文件顶部包声明，并确保 `gh2` 包文件实际位于 `gh2` 目录。

### “没有重写抽象方法”

通常是拼写或签名错误。使用 `@Override` 让编译器定位问题。

### “No runnable methods”

确认测试和 `@Test` 注解已取消注释。

### `K#1` 与 `K#2` 不兼容

内部类不要重新声明一个新的泛型参数。例如：

```java
private class MapWizard<Z> implements Iterator<Z>
```

若 `Z` 本应使用外层泛型，应删除内部类上的 `<Z>`。

### GuitarString 自动评分异常

`GuitarString` 只模拟弦，不应直接调用声音播放。播放应由客户端完成。

## 十七、实现建议

- 一小步一小步实现和测试，避免一次写大量代码；
- 必要时删掉失败设计重来，每个类的正确实现并不特别长；
- `ArrayDeque` 可先在不扩容的情况下验证基础逻辑，再加入扩缩容；
- 先在纸上画节点、哨兵、循环数组和索引；
- 重点测试空队列的边界转换；
- 循环哨兵和循环数组会显著简化代码；
- 可编写 `plusOne`、`minusOne` 等索引辅助函数；
- 用 IntelliJ Java Visualizer 和调试器观察引用关系；
- 不要为了通过测试导入禁止的数据结构或复制别人的实现。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/proj/proj1/proj1){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
