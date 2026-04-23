---
source_type: web
created_at: 2026-01-01  # default placeholder, actual date unknown
topics: [orproj]
status: summarized
---

﻿# Multi-Objective Optimization

本目录补充了两个多目标优化案例。统一思路是：在 [`src/ModelSolver.py`](E:/operations_research/orproj/src/ModelSolver.py) 中为同一个模型添加多个目标函数，再用加权方式形成可比较的综合目标。

## `workforce_balance_problem.py`

### 问题描述
企业需要制定周生产计划。常规工时生产利润较高，但加班生产会带来额外管理压力，因此需要在“利润最大化”和“加班最少化”之间做权衡。

### 决策变量
设：

- \(x_r\)：常规工时产量，对应 `regular_units`
- \(x_o\)：加班产量，对应 `overtime_units`

并且 \(x_r, x_o \in \mathbb{Z}_{\ge 0}\)。

### 多目标模型
目标 1：最大化利润

\[
\max f_1 = 8x_r + 6x_o
\]

目标 2：最小化加班使用量

\[
\min f_2 = x_o
\]

约束条件：

\[
\begin{aligned}
x_r + x_o &\ge 30 \\
x_r &\le 40 \\
x_o &\le 20 \\
x_r, x_o &\in \mathbb{Z}_{\ge 0}
\end{aligned}
\]

### 加权聚合
脚本中采用权重 \(0.7\) 和 \(0.3\) 对两个目标进行综合评价，体现“利润优先，但不忽略加班成本”的决策偏好。

## `green_supply_mix_problem.py`

### 问题描述
企业从两个供应商采购总量固定的物料。供应商 A 成本较高但碳排放低，供应商 B 成本较低但碳排放高，需要在成本和环保目标之间折中。

### 决策变量
设：

- \(x_A\)：从供应商 A 采购的数量
- \(x_B\)：从供应商 B 采购的数量

且 \(x_A, x_B \in \mathbb{Z}_{\ge 0}\)。

### 多目标模型
目标 1：最小化采购成本

\[
\min f_1 = 7x_A + 5x_B
\]

目标 2：最小化碳排放

\[
\min f_2 = 2x_A + 5x_B
\]

约束条件：

\[
\begin{aligned}
x_A + x_B &= 20 \\
x_A &\ge 6 \\
x_A, x_B &\in \mathbb{Z}_{\ge 0}
\end{aligned}
\]

### 加权聚合
脚本中使用成本权重 0.6、碳排放权重 0.4。若要改变企业偏好，只需调整目标权重即可。

## 运行方式

```bash
.venv\Scripts\python.exe src\multi_objective_optimizaion\workforce_balance_problem.py
.venv\Scripts\python.exe src\multi_objective_optimizaion\green_supply_mix_problem.py
```

