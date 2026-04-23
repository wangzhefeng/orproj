---
source_type: web
created_at: 2026-01-01  # default placeholder, actual date unknown
topics: [orproj]
status: summarized
---

﻿# Linear Programming

本目录现在分成两层：

- 按问题命名的新脚本：这是后续推荐继续扩展的主入口。
- 兼容旧文件名的入口脚本：保留原文件名，内部转调到新的问题脚本，避免旧链接或旧习惯失效。

所有建模脚本统一基于 [`src/ModelSolver.py`](E:/operations_research/orproj/src/ModelSolver.py)。

## 主问题脚本

### `product_mix_problem.py`
对应原 `lp_pyomo.py`、`lp_ortools.py` 中表达的两产品生产优化问题。

目标函数：

\[
\max Z = 40x_1 + 30x_2
\]

约束：

\[
\begin{aligned}
x_1 &\le 40 \\
x_1 + x_2 &\le 80 \\
2x_1 + x_2 &\le 100 \\
x_1, x_2 &\ge 0
\end{aligned}
\]

### `transportation_problem.py`
对应原 `transport_pyomo.py` 的运输问题。

目标函数：

\[
\min Z = 4x_{NE} + 6x_{NW} + 5x_{SE} + 3x_{SW}
\]

约束：

\[
\begin{aligned}
x_{NE} + x_{NW} &\le 18 \\
x_{SE} + x_{SW} &\le 12 \\
x_{NE} + x_{SE} &= 10 \\
x_{NW} + x_{SW} &= 20
\end{aligned}
\]

### `resource_allocation_problem.py`
对应原 `lp_docplex.py` 中“带上下界的资源分配型 LP”。原脚本随机生成参数，不利于教学复现，这里改成固定参数版本。

目标函数：

\[
\min Z = 3x_{11} + 2x_{21} + 4x_{31} + 5x_{12}
\]

约束：

\[
\begin{aligned}
2x_{11} + x_{21} + 3x_{31} + 2x_{12} &\le 20 \\
x_{11} + 2x_{21} + x_{31} + 2x_{12} &\le 18
\end{aligned}
\]

并且各变量带有显式上下界。

### `three_variable_linear_problem.py`
对应原 `lp_scipy.py` 的三变量线性规划问题。

目标函数：

\[
\max Z = 2x_1 + 3x_2 - 5x_3
\]

约束：

\[
\begin{aligned}
x_1 + x_2 + x_3 &= 7 \\
2x_1 - 5x_2 + x_3 &\ge 10 \\
x_1 + 3x_2 + x_3 &\le 12 \\
x_1, x_2, x_3 &\ge 0
\end{aligned}
\]

### `infeasibility_analysis_problem.py`
对应原 `lp_gurobipy.py` 的“模型不可行诊断”主题。这里不再依赖外部 `.lp` 文件，而是直接构造一个矛盾约束模型。

目标函数：

\[
\min Z = x + y
\]

约束：

\[
\begin{aligned}
x + y &\ge 8 \\
x + y &\le 5
\end{aligned}
\]

该模型必然不可行，用于说明诊断场景。

## 方法脚本

### `methods/simplex_method.py`
基于 `product_mix_problem` 的结构重写单纯形法演示，展示入基、出基与枢轴运算。

### `methods/interior_point.py`
基于 `product_mix_problem` 的障碍函数形式，展示内点法/牛顿法求解思路。

### `methods/column_generation.py`
保留“列生成”主题，使用统一模型抽象描述一个预设切割模式的主问题，用于教学演示。

## 兼容旧文件名

以下文件仍然保留，但现在都是 `ModelSolver.py` 后端注册中心的适配入口：

- `lp_pyomo.py` -> `ModelSolver.py` 中的 `pyomo` 后端 + `product_mix_problem.py`
- `lp_ortools.py` -> `ModelSolver.py` 中的 `ortools` 后端 + `product_mix_problem.py`
- `lp_docplex.py` -> `ModelSolver.py` 中的 `docplex` 后端 + `resource_allocation_problem.py`
- `lp_scipy.py` -> `ModelSolver.py` 中的 `scipy` 后端 + `three_variable_linear_problem.py`
- `transport_pyomo.py` -> `ModelSolver.py` 中的 `pyomo` 后端 + `transportation_problem.py`
- `lp_gurobipy.py` -> `ModelSolver.py` 中的 `gurobi` 后端 + `infeasibility_analysis_problem.py`

## 运行方式

```bash
.venv\Scripts\python.exe src\linear_programming\product_mix_problem.py
.venv\Scripts\python.exe src\linear_programming\resource_allocation_problem.py
.venv\Scripts\python.exe src\linear_programming\three_variable_linear_problem.py
.venv\Scripts\python.exe src\linear_programming\transportation_problem.py
.venv\Scripts\python.exe src\linear_programming\infeasibility_analysis_problem.py
```


