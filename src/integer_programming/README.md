---
source_type: web
created_at: 2026-01-01  # default placeholder, actual date unknown
topics: [orproj]
status: summarized
---

﻿# Integer Programming

本目录现在只保留纯整数规划中的 0-1 二元决策示例。相关脚本统一通过 [`src/ModelSolver.py`](E:/operations_research/orproj/src/ModelSolver.py) 运行，并沿用原始 `gurobipy` 示例的后端语义。

## 主问题脚本

### `binary_selection_problem.py`
对应原 `bip.py` 和 `bip_matrix.py`。

设 \(x_1, x_2, x_3 \in \{0,1\}\)，其中 \(x_i = 1\) 表示选择项目 \(i\)。

目标函数：

\[
\max Z = x_1 + x_2 + 2x_3
\]

约束条件：

\[
\begin{aligned}
x_1 + 2x_2 + 3x_3 &\le 4 \\
x_1 + x_2 &\ge 1 \\
x_1, x_2, x_3 &\in \{0,1\}
\end{aligned}
\]

该模型表示在预算限制下选择项目，并要求项目 1 与项目 2 至少有一个被选中。

## 兼容旧文件名

- `bip.py` -> `binary_selection_problem.py`
- `bip_matrix.py` -> `binary_selection_problem.py`

## 运行方式

```bash
.venv\Scripts\python.exe src\integer_programming\binary_selection_problem.py
.venv\Scripts\python.exe src\integer_programming\bip.py
.venv\Scripts\python.exe src\integer_programming\bip_matrix.py
```
