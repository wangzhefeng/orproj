---
source_type: web
created_at: 2026-01-01  # default placeholder, actual date unknown
topics: [orproj]
status: summarized
---

# Quadratic Programming

本目录包含标准二次规划示例，统一基于 [`src/ModelSolver.py`](E:/operations_research/orproj/src/ModelSolver.py) 中的线性项与 `quadratic_expr` 进行建模。

## `portfolio_risk_problem.py`

投资组合均值-方差问题：

$$
\min Z =
0.05w_b^2 + 0.18w_s^2 + 0.10w_f^2
+ 0.04w_bw_s + 0.02w_bw_f + 0.06w_sw_f
$$

约束：

$$
\begin{aligned}
w_b + w_s + w_f &= 1 \\
0.08w_b + 0.14w_s + 0.11w_f &\ge 0.11
\end{aligned}
$$

## `production_smoothing_problem.py`

平滑生产问题：

$$
\min Z = (x_1 - 5)^2 + (x_2 - 5)^2
$$

约束：

$$
\begin{aligned}
x_1 + x_2 &= 10 \\
x_1 &\le 8 \\
x_2 &\le 8
\end{aligned}
$$

## 运行方式

```bash
.venv\Scripts\python.exe src\quadratic_programming\portfolio_risk_problem.py
.venv\Scripts\python.exe src\quadratic_programming\production_smoothing_problem.py
```
