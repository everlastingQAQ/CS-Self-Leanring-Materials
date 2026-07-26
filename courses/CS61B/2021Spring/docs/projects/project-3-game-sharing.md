---
title: "Project 3：游戏共享"
description: "CS61B Spring 2021 Project 3：游戏共享中文学习资料。"
---

# Project 3 扩展：远程游戏共享

> 作者：Boren Tsai<br>
> 原始页面：<https://sp21.datastructur.es/materials/proj/proj3/proj3GameSharing>
>
> 本文件为完整中文说明。类名、方法签名、命令、IP、端口和程序输出保持原样。

## 一、介绍

这一扩展允许两名学生远程玩对方的 BYOW 游戏。主机运行 `BYOWServer`，远程玩家运行 `BYOWClient`。

整体模型类似联网游戏：

- 客户端负责本地显示、音频、UI 和采集用户输入；
- 远程服务器接收并执行输入；
- 服务器把正确游戏状态和画布信息发回客户端；
- 客户端显示服务器计算出的结果。

需要在 `Engine` 中新增：

```java
interactWithRemoteClient
```

## 二、获取 Networking 骨架

重新从 `skeleton` 拉取代码，得到：

```text
Networking/
├── BYOWClient.java
└── BYOWServer.java
```

这两个类已经完整实现，不需要修改。

你只需：

- 在 `Engine.java` 实现 `interactWithRemoteClient`；
- 修改 `Main.main`；
- 使用服务器 API 替代本地输入和画布发送。

`interactWithRemoteClient` 接受的启动参数格式是：

```text
-p [4-digit port number]
```

## 三、修改 `Main`

骨架原先包含：

```java
else if (args.length == 2 && args[0].equals("-p")) {
    System.out.println("Coming soon.");
}
```

需要：

1. 把 `main` 声明为可抛出 `IOException`；
2. 创建 `Engine`；
3. 调用 `interactWithRemoteClient(args[1])`。

参考：

```java
public static void main(String[] args) throws IOException {
    if (args.length > 2) {
        System.out.println("Can only have two arguments - the flag and input string");
        System.exit(0);
    } else if (args.length == 2 && args[0].equals("-s")) {
        Engine engine = new Engine();
        engine.interactWithInputString(args[1]);
        System.out.println(engine.toString());
    } else if (args.length == 2 && args[0].equals("-p")) {
        Engine engine = new Engine();
        engine.interactWithRemoteClient(args[1]);
    } else {
        Engine engine = new Engine();
        engine.interactWithKeyboard();
    }
}
```

## 四、`BYOWServer` 接口

```java
public class BYOWServer {
    public BYOWServer(int port)

    public void sendCanvasConfig(int width, int height)
    public void sendCanvas()

    public boolean clientHasKeyTyped()
    public char clientNextKeyTyped()
    public void stopConnection()
}
```

### 构造函数

创建服务器时传入端口号：

```java
new BYOWServer(4005)
```

端口可以任意选择，建议至少四位，如 `4005`。

实例化时服务器打印：

```text
Server started. Waiting for client to connect…
```

构造函数会阻塞，直到客户端连接。连接成功后打印：

```text
Client connected!
```

### `sendCanvasConfig`

```java
sendCanvasConfig(int width, int height)
```

告诉客户端创建多大的 `StdDraw` 画布。

- 单位为像素；
- 必须与 `TERenderer` 中 `setCanvasSize` 参数一致；
- 默认 StdDraw 画布是 `512 × 512`；
- 每次改变画布大小时准确调用一次。

### `sendCanvas`

```java
sendCanvas()
```

把主机当前 `StdDraw` 画布内容发送给客户端。

每次更新屏幕后调用，包括：

- 调用 `StdDraw.showCanvas()`；
- 调用 `TERenderer.renderFrame(...)`；
- 菜单或 HUD 重绘。

### `clientHasKeyTyped`

```java
clientHasKeyTyped()
```

作用对应：

```java
StdDraw.hasNextKeyTyped()
```

远程模式中使用服务器方法，而不是直接读取主机键盘。

### `clientNextKeyTyped`

```java
clientNextKeyTyped()
```

作用对应：

```java
StdDraw.nextKeyTyped()
```

返回客户端输入的下一个字符。

### `stopConnection`

```java
stopConnection()
```

通知客户端停止显示画布并终止连接。建议游戏退出前调用。

## 五、实现建议

`interactWithRemoteClient` 应与：

```java
interactWithKeyboard
```

行为高度相似。良好设计应复用：

- 菜单状态机；
- 种子输入；
- avatar 移动；
- 世界更新；
- HUD；
- 保存与退出。

差异主要是：

| 本地键盘模式 | 远程模式 |
|---|---|
| `StdDraw.hasNextKeyTyped()` | `server.clientHasKeyTyped()` |
| `StdDraw.nextKeyTyped()` | `server.clientNextKeyTyped()` |
| 本地画布显示 | 每次更新后 `server.sendCanvas()` |
| 本地退出 | 退出前 `server.stopConnection()` |

若现有代码把输入源抽象成接口，通常可以避免大量重复代码。最容易遗漏的是画布每次更新后都要发送。

## 六、`BYOWClient`

`BYOWClient` 已完整实现，直接运行其 `main` 方法。程序会询问：

- `IP address`
- `port`

本机测试填写：

```text
IP Address: localhost
Port: 4005
```

示例输出：

```text
BYOW Client. Please Enter the following information to connect to a server...
IP Address: localhost
Port (this must be a number): 4005
CONFIGURING CANVAS
```

端口必须与服务器启动端口相同。

## 七、本地测试

1. 运行 `Main`，程序参数：

```text
-p 4005
```

2. 再运行 `BYOWClient`；
3. IP 输入：

```text
localhost
```

4. 端口输入：

```text
4005
```

应出现两个 `StdDraw` 窗口：

- 一个服务器窗口；
- 一个客户端窗口。

若实现正确，两者内容应完全同步，客户端按键应驱动服务器游戏。

## 八、支持真正远程连接

确认本地服务器和客户端已经镜像成功后，再配置公网隧道。

原课程推荐使用 `ngrok`。

### 安装并加入 PATH

下载 `ngrok`，把可执行文件加入环境变量：

```bash
export PATH=$PATH:[path to ngrok executable]
```

例如位于 Downloads：

```bash
export PATH=$PATH:~/Downloads/
```

### 开启 TCP 隧道

假设服务器使用端口 `4005`：

```bash
ngrok tcp 4005
```

ngrok 会显示类似：

```text
tcp://2.tcp.ngrok.io:17993 -> localhost:4005
```

其中：

- 客户端 IP：`2.tcp.ngrok.io`
- 客户端端口：`17993`
- 输入 IP 时不要包含 `tcp://`。

### 远程游戏步骤

主机：

1. 用 `-p 4005` 启动 `Main`；
2. 新终端执行 `ngrok tcp 4005`；
3. 把 ngrok 显示的主机名和端口发给朋友。

远程玩家：

1. 运行 `BYOWClient`；
2. 输入主机提供的 ngrok 地址；
3. 输入 ngrok 端口；
4. 连接后即可远程操作主机上的游戏。

主机可以观看玩家操作，也可以进一步扩展成服务器同时修改世界的玩法。

## 九、One Point Bounty

理论上可以制作浏览器客户端。课程当时没有提供实现。

若有人创建能连接 BYOW Server 的网站客户端，课程奖励 **1 个 bonus point**，并可能把它作为以后课程资源。

## 十、免责声明

发送 `StdDraw` 画布会产生额外编码、传输和网络开销，因此远程游戏很可能有明显延迟。这是正常且预期的，不代表实现错误。

## 十一、完成检查清单

- [ ] 已重新拉取 `Networking` 文件夹；
- [ ] 未修改 `BYOWClient` 和 `BYOWServer`；
- [ ] `Main.main` 声明 `throws IOException`；
- [ ] `-p` 分支调用 `interactWithRemoteClient`；
- [ ] 端口字符串正确解析为整数；
- [ ] 远程输入使用 `clientHasKeyTyped` / `clientNextKeyTyped`；
- [ ] 初始化或改变画布时调用 `sendCanvasConfig`；
- [ ] 每次重绘后调用 `sendCanvas`；
- [ ] 退出前调用 `stopConnection`；
- [ ] localhost 测试出现两个同步窗口；
- [ ] 远程测试使用正确 ngrok IP 和端口；
- [ ] 能接受网络延迟属于正常现象。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/proj/proj3/proj3GameSharing){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
