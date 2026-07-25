---
title: "Project 2 实作日"
description: "CS61B Spring 2021 Project 2 实作日中文学习资料。"
hide:
  - toc
---

# Lab 栏目节点：Project 2 Workday（截止周）

- 课程日历位置：Week 11
- 性质：项目工作日，没有新的独立 Lab 规格页

> **文档性质**：本文件依据 CS 61B Spring 2021 官方页面，由 ChatGPT 独立阅读后制作中文学习版。  
> 为保留技术准确性，类名、方法名、文件名、命令、报错文本和 API 名称保持英文。本文采用逐节翻译与重述，而不是网页的逐句镜像。

## 当周目标

Project 2 临近截止，重点应从“继续加功能”转为“系统验证”。

### 推荐检查

- 所有命令的 operand 数量错误能输出正确信息。
- 未初始化仓库时行为正确。
- commit ID 缩写能解析，歧义情况得到处理。
- `checkout` 和 `reset` 不会覆盖未跟踪文件。
- branch 指针与 HEAD 更新正确。
- merge 的 split point 计算正确。
- fast-forward 和 ancestor 特殊情况正确。
- merge conflict 文件格式正确。
- `status` 各分类准确。

### 测试策略

使用小型、单目的 `.in` 文件。一次测试只验证一个规则，避免一个超长脚本失败后无法判断根因。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
