---
title: "Lab 5：同伴代码审查"
description: "CS61B Spring 2021 Lab 5：同伴代码审查中文学习资料。"
---

# Lab 5：Project 1 同伴代码审查

> 原文：https://sp21.datastructur.es/materials/lab/lab5/lab5<br>
> 说明：正文由 ChatGPT 直接翻译。

## 简介

本 Lab 与实验课中的 1–3 名同学比较 Project 1 解法。本周必须按时参加；无法参加常规时段可去其他 Lab，确实无法参加任何时段时才填写官方豁免表。

TA 会讲解 Project 1 的部分参考解法。**只有在已经完成 Project 1 最终 Gradescope 提交后才能参加本 Lab**，否则可能因提前接触解法而被认定违反学术诚信。

## LinkedListDeque 概览

TA 先简要介绍 staff 的 `LinkedListDeque` 解法。

## LinkedListDeque 同伴审查

与 1–3 名同学组队比较实现。目标不是评判谁写得“高级”，而是互相学习。不要从头到尾逐行讲解整个实现，而应围绕具体问题讨论：

1. 最麻烦的 bug 是什么？如何修复？是否用了 Debugger、特殊情况，或“改一点然后祈祷 AG 通过”？
2. 是否删除过某些设计，使代码更简单？
3. 代码中有哪些 special cases？
4. 是否使用 private helper methods？
5. 是否存在重复代码？helper 是否能减少重复？
6. 哪些地方复用了已有方法或代码？

讨论后，完成 `self_reflection.txt` 前半部分。

## ArrayDeque 概览与审查

TA 讲解 `ArrayDeque` 参考方案。然后按相同方式再次结组讨论自己的 `ArrayDeque`。建议换一组同学，但保留原组也可以。继续填写 `self_reflection.txt`。

## 自我反思与提交

1. 在 skeleton 提供的 `self_reflection.txt` 中至少回答 4 个问题。
2. 请 TA 检查文件并领取 magic word。
3. 把 magic word 写入 `magic_word.txt`。
4. Push 到 GitHub 并提交 Gradescope。

---

原始来源：[CS61B Spring 2021](https://sp21.datastructur.es/materials/lab/lab5/lab5<br){ target="_blank" rel="noopener" } · 中文整理：everlasting · [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans){ target="_blank" rel="license noopener" }
