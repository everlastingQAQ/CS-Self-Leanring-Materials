---
title: "Project 3 实作日"
description: "CS61B Spring 2021 Project 3 实作日中文学习资料。"
hide:
  - toc
---

# Lab 栏目节点：Project 3 Work Day

- 课程日历位置：Week 14
- 性质：项目工作日

> **文档性质**：本文件依据 CS 61B Spring 2021 官方页面，由 ChatGPT 独立阅读后制作中文学习版。  
> 为保留技术准确性，类名、方法名、文件名、命令、报错文本和 API 名称保持英文。本文采用逐节翻译与重述，而不是网页的逐句镜像。

## 当周目标

Phase 2 截止前集中完成：

- 主菜单。
- 键盘控制。
- avatar 移动。
- HUD。
- 保存与加载。
- `interactWithKeyboard` 与 `interactWithInputString` 的行为一致。
- Ambition feature。

## 最关键的架构检查

键盘输入和字符串输入必须复用同一套命令处理逻辑。不要写两套世界模拟代码，否则保存、加载和移动规则很容易不一致。

推荐结构：

```text
输入来源 → 命令解析器 → 游戏状态更新 → 可选渲染
```

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
