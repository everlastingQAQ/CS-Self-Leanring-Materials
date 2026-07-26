---
title: "HW 0：Java 速成"
description: "CS61B Spring 2021 HW 0：Java 速成中文学习资料。"
---

# HW 0：Java 速成教程

## 作业目标

本作业快速介绍 Java 的基础语法。它特别适合以前没有用过 Java、但已经学过至少一学期其他编程语言的同学。

课程讲座不会专门完整讲授这些基础语法，但后续默认你已经理解。可以按自己的节奏阅读，也可以根据已有经验略过熟悉部分。

## 一、一个最基本的程序

在 Lab 1 教你本地运行 Java 前，本作业使用浏览器中的 Java 可视化器。

一个典型程序可能如下：

```java
public class ClassNameHere {
    public static void main(String[] args) {
        int x = 5;
        x = x + 1;
        System.out.println(x);
    }
}
```

暂时不必理解 `public class` 或 `public static void main(String[] args)`。

```java
int x = 5;
```

会创建一个静态类型为 `int` 的变量 `x`，并赋值为 `5`。Java 变量具有静态类型：一旦 `x` 声明为 `int`，就不能存储 `5.3` 这样的实数。

可视化器会显示变量框，帮助你观察程序逐行执行。真实开发中通常看不到程序内部的所有变量，因此这种显示只是教学工具。

建议修改代码并观察编译或运行结果，例如尝试把实数赋给 `int`。

## 二、条件语句

### 基本 `if`

```java
public class ClassNameHere {
    public static void main(String[] args) {
        int x = 5;

        if (x < 10)
            x = x + 10;

        if (x < 10)
            x = x + 10;

        System.out.println(x);
    }
}
```

`if` 会计算圆括号里的布尔条件；如果条件为 `true`，执行紧接着的下一条语句。

### 花括号与代码块

一条条件可以控制多条语句，只需用花括号包围：

```java
public class ConditionalsWithBlocks {
    public static void main(String[] args) {
        int x = 5;

        if (x < 10) {
            System.out.println("I shall increment x by 10.");
            x = x + 10;
        }

        if (x < 10) {
            System.out.println("I shall increment x by 10.");
            x = x + 10;
        }

        System.out.println(x);
    }
}
```

Java 通过花括号而不是缩进决定语句分组。下面代码看起来像是两行都受 `if` 控制，实际只有打印语句受控制：

```java
public class PrintAbsoluteValue {
    public static void main(String[] args) {
        int x = -5;

        if (x < 0)
            System.out.println("I should negate X");
            x = -x;

        System.out.println(x);
    }
}
```

正确写法应使用花括号：

```java
if (x < 0) {
    System.out.println("I should negate X");
    x = -x;
}
```

### 花括号风格

课程采用：

```java
if (condition) {
    statement;
}
```

而不是把左花括号放到下一行。即使某个条件只有一条语句，也建议始终使用花括号，避免将来添加代码时产生隐蔽错误。

## 三、`else`

当条件为假时执行另一段代码：

```java
int x = 9;
if (x - 3 > 8) {
    System.out.println("x - 3 is greater than 8");
} else {
    System.out.println("x - 3 is not greater than 8");
}
```

可以连接多个分支：

```java
int dogSize = 20;
if (dogSize >= 50) {
    System.out.println("woof!");
} else if (dogSize >= 10) {
    System.out.println("bark!");
} else {
    System.out.println("yip!");
}
```

`>=` 表示“大于等于”。

## 四、`while` 循环

`while` 会在条件为真时反复执行代码块：

```java
int bottles = 99;
while (bottles > 0) {
    System.out.println(bottles + " bottles of beer on the wall.");
    bottles = bottles - 1;
}
```

若删除递减语句，条件会一直为真，从而形成无限循环。

程序仍然按顺序逐行执行。如果循环体中间把条件相关变量改成不满足条件，当前这一轮不会立刻中止；它会执行完循环体，之后才重新检查条件：

```java
int bottles = 5;
while (bottles > 0) {
    bottles = -312;
    System.out.println(bottles + " bottles of beer on the wall.");
}
```

因此它仍会打印 `-312 bottles...` 一次。

## 五、`double` 和 `String`

- `double`：存储实数的近似值；
- `String`：存储字符序列。

下面模拟 Achilles 与 Tortoise 的追赶：

```java
String a = "Achilles";
String t = "Tortoise";
double aPos = 0;
double tPos = 100;
double aSpeed = 20;
double tSpeed = 10;
double totalTime = 0;
while (aPos < tPos) {
    System.out.println("At time: " + totalTime);
    System.out.println("    " + a + " is at position " + aPos);
    System.out.println("    " + t + " is at position " + tPos);

    double timeToReach = (tPos - aPos) / aSpeed;
    totalTime = totalTime + timeToReach;
    aPos = aPos + timeToReach * aSpeed;
    tPos = tPos + timeToReach * tSpeed;
}
```

字符串与其他值可使用 `+` 拼接。

## 六、创意练习 1a：绘制三角形

使用循环打印：

```text
*
**
***
****
*****
```

不能直接写五条打印语句。

你可能会用到：

```java
System.out.print(...);
```

它与 `println` 的区别是不会自动换行。

保存这份代码，后面的练习会再次使用。

## 七、定义函数（方法）

下面四种语言的程序都定义“返回两个数中较大值”的函数。

### Python

```python
def max(x, y):
    if x > y:
        return x
    return y

print(max(5, 15))
```

### MATLAB

```matlab
function m = max(x, y)
    if (x > y)
        m = x
    else
        m = y
    end
end

disp(max(5, 15))
```

### Scheme

```scheme
(define max (lambda (x y) (if (> x y) x y)))
(display (max 5 15)) (newline)
```

### Java

```java
public static int max(int x, int y) {
    if (x > y) {
        return x;
    }
    return y;
}

public static void main(String[] args) {
    System.out.println(max(10, 15));
}
```

Java 中的函数通常称为**方法**。

```java
public static int max(int x, int y)
```

是方法签名的一部分，包含：

- 修饰符：`public static`；
- 返回类型：`int`；
- 方法名：`max`；
- 参数及其类型：`int x, int y`。

本作业中的方法都使用 `public static`，其含义会在后续课程解释。

## 八、创意练习 1b：`drawTriangle`

创建：

```java
public static void drawTriangle(int N)
```

- 返回类型为 `void`，表示不返回值；
- 参数名为 `N`；
- 打印一个高度为 `N` 的星号三角形。

修改 `main`，调用：

```java
drawTriangle(10);
```

## 九、数组

Java 数组与 Python 列表、Scheme 向量、MATLAB 数组在入门用途上相似。

### Python

```python
numbers = [4, 7, 10]
print(numbers[1])
```

### MATLAB

```matlab
numbers = [4 7 10]
disp(numbers(2))
```

### Scheme

```scheme
(define numbers #(4 7 10))
(display (vector-ref numbers 1)) (newline)
```

### Java

```java
int[] numbers = new int[3];
numbers[0] = 4;
numbers[1] = 7;
numbers[2] = 10;
System.out.println(numbers[1]);
```

数组字面量简写：

```java
int[] numbers = new int[]{4, 7, 10};
System.out.println(numbers[1]);
```

数组长度：

```java
System.out.println(numbers.length);
```

注意数组使用字段 `.length`，不是方法 `.length()`。

## 十、练习 2：数组最大值

实现：

```java
public static int max(int[] m)
```

它返回整数数组中的最大值。可假设所有数字都大于等于零。

骨架：

```java
public class ClassNameHere {
    /** Returns the maximum value from m. */
    public static int max(int[] m) {
        return 0;
    }

    public static void main(String[] args) {
        int[] numbers = new int[]{9, 2, 15, 2, 22, 10, 6};
    }
}
```

修改 `main` 调用方法并打印结果；正确输出是 `22`。

## 十一、`for` 循环

使用 `while` 求数组和：

```java
public static int whileSum(int[] a) {
    int i = 0;
    int sum = 0;
    while (i < a.length) {
        sum = sum + a[i];
        i = i + 1;
    }
    return sum;
}
```

相同逻辑的 `for` 写法：

```java
public static int sum(int[] a) {
    int sum = 0;
    for (int i = 0; i < a.length; i = i + 1) {
        sum = sum + a[i];
    }
    return sum;
}
```

一般语法：

```java
for (initialization; termination; increment) {
    statement(s)
}
```

三部分用分号分隔。可以在初始化区使用逗号写多个表达式：

```java
for (int i = 0, j = 10; i < j; i += 1) {
    System.out.println(i + j);
}
```

但应少用这种复杂形式。

## 十二、练习 3：使用 `for` 求最大值

重写练习 2：

```java
public class ClassNameHere {
    /** Returns the maximum value from m using a for loop. */
    public static int forMax(int[] m) {
        return 0;
    }

    public static void main(String[] args) {
        int[] numbers = new int[]{9, 2, 15, 2, 22, 10, 6};
    }
}
```

要求使用 `for` 循环。

## 十三、`break` 与 `continue`

- `continue`：跳过当前迭代剩余代码，直接进入增量步骤/下一轮；
- `break`：立刻终止最内层循环。

### `continue` 示例

下面程序跳过所有包含 `"horse"` 的字符串，其余字符串打印三次：

```java
public class ContinueDemo {
    public static void main(String[] args) {
        String[] a = {"cat", "dog", "laser horse", "ketchup", "horse", "horbse"};

        for (int i = 0; i < a.length; i += 1) {
            if (a[i].contains("horse")) {
                continue;
            }
            for (int j = 0; j < 3; j += 1) {
                System.out.println(a[i]);
            }
        }
    }
}
```

### `break` 示例

包含 `"horse"` 的字符串只打印一次，其他打印三次：

```java
public class BreakDemo {
    public static void main(String[] args) {
        String[] a = {"cat", "dog", "laser horse", "ketchup", "horse", "horbse"};

        for (int i = 0; i < a.length; i += 1) {
            for (int j = 0; j < 3; j += 1) {
                System.out.println(a[i]);
                if (a[i].contains("horse")) {
                    break;
                }
            }
        }
    }
}
```

二者也适用于 `while` 和 `do-while`。

## 十四、可选练习 4：窗口正数和

实现：

```java
windowPosSum(int[] a, int n)
```

对于每个正数 `a[i]`，把它替换为从 `a[i]` 到 `a[i+n]` 的和；若数组剩余元素不足，就只加到数组结尾。若 `a[i]` 为负，不修改它。

例如：

```java
a = {1, 2, -3, 4, 5, 4};
n = 3;
```

执行后：

```java
{4, 8, -3, 13, 9, 4}
```

解释：

- `a[0] = 1 + 2 + (-3) + 4 = 4`；
- `a[1] = 2 + (-3) + 4 + 5 = 8`；
- `a[2]` 为负，不变；
- `a[3] = 4 + 5 + 4 = 13`；
- `a[4] = 5 + 4 = 9`；
- `a[5]` 后面无元素，保持 `4`。

另一个例子：

```java
{1, -1, -1, 10, 5, -1}, n = 2
```

结果：

```java
{-1, -1, -1, 14, 4, -1}
```

骨架：

```java
public class BreakContinue {
    public static void windowPosSum(int[] a, int n) {
        /** your code here */
    }

    public static void main(String[] args) {
        int[] a = {1, 2, -3, 4, 5, 4};
        int n = 3;
        windowPosSum(a, n);

        // Should print 4, 8, -3, 13, 9, 4
        System.out.println(java.util.Arrays.toString(a));
    }
}
```

提示：

1. 使用两个 `for` 循环；
2. 用 `continue` 跳过负数；
3. 用 `break` 防止索引越过数组结尾。

## 十五、增强型 `for` 循环

当不需要索引，只需要依次访问元素时，可以写：

```java
for (String s : a) {
    ...
}
```

示例：

```java
public class EnhancedForBreakDemo {
    public static void main(String[] args) {
        String[] a = {"cat", "dog", "laser horse", "ketchup", "horse", "horbse"};

        for (String s : a) {
            for (int j = 0; j < 3; j += 1) {
                System.out.println(s);
                if (s.contains("horse")) {
                    break;
                }
            }
        }
    }
}
```

变量 `s` 会依次引用 `a[0]` 到 `a[a.length - 1]`。这种循环适合只读遍历；如果需要元素下标，或需要通过下标修改数组，则普通 `for` 循环更合适。

---

原始页面：[https://sp21.datastructur.es/materials/hw/hw0/hw0](https://sp21.datastructur.es/materials/hw/hw0/hw0)
