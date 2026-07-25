---
title: "Lab 8：HashMap"
description: "CS61B Spring 2021 Lab 8：HashMap中文学习资料。"
---

# Lab 8：HashMap

- 原标题：Lab 8: HashMap
- 原页面：`https://sp21.datastructur.es/materials/lab/lab8/lab8`

> **文档性质**：本文件依据 CS 61B Spring 2021 官方页面，由 ChatGPT 独立阅读后制作中文学习版。  
> 为保留技术准确性，类名、方法名、文件名、命令、报错文本和 API 名称保持英文。本文采用逐节翻译与重述，而不是网页的逐句镜像。

## 实验目标

完成 `MyHashMap`，它实现 `Map61B` 接口。与 Lab 7 不同，本次底层结构是哈希表，并要求实现 `keySet` 与 `iterator`。

## 核心结构

哈希表由 bucket 数组组成。每个 bucket 存放哈希冲突的多个节点。典型节点包含：

```text
key
value
```

核心字段通常包括：

- buckets
- size
- loadFactor
- 默认初始容量
- 最大负载因子

## 索引计算

对 key 计算哈希值，并映射到合法下标。实现时要避免负下标，可使用安全的非负转换或 `Math.floorMod` 思路。

`null` key 是否支持，应严格按课程 skeleton 和测试要求处理，不要自行扩展语义。

## 需要实现的方法

- `clear`
- `containsKey`
- `get`
- `size`
- `put`
- `keySet`
- `iterator`

`remove` 可抛出 `UnsupportedOperationException`。

### `put`

- key 不存在：插入新节点，增加 size。
- key 已存在：只更新 value。
- 插入后或插入前检查负载因子。
- 扩容时必须重新哈希所有现有 key，不能只复制 bucket 下标。

### `keySet` 与 `iterator`

`keySet` 返回所有当前 key。`iterator` 遍历这些 key，顺序不限，但不能漏项或重复。

## Bucket 类型比较

原实验允许改变 bucket 的具体集合类型，再进行速度测试。你需要理解：

- bucket 很短时，链表或简单集合足够。
- 哈希分布差或负载过高时，单个 bucket 会变长。
- 总体性能依赖哈希函数、容量和扩容策略。

## 性能比较

完成后与：

- `ULLMap`
- Java `HashMap`
- 不同 bucket 实现的 `MyHashMap`

进行计时对比。平均情况下哈希表查询接近常数时间，但这依赖良好哈希分布和负载控制。

## 完成标准

- 所有接口方法行为正确。
- 更新已有 key 不增加 size。
- 扩容后所有 key 仍可查询。
- iterator 遍历完整。
- 能解释为什么扩容时必须 rehash。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/lab/lab8/lab8){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
