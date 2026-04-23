---
source_type: web
created_at: 2026-01-01  # default placeholder, actual date unknown
topics: [orproj]
status: summarized
---

# Nonlinear Programming

本目录用于存放非线性规划模型。与线性规划、整数规划、二次规划不同，这类问题的目标函数或约束中包含非线性项，例如分式、指数、对数、变量乘积等。

## `bounded_surface_optimization_problem.py`

该脚本对应原 `src/linear_programming/lp_scipy_func.py` 的 SciPy 示例，现已按模型类型重新归类到非线性规划目录。

目标函数：

\[
\min Z = \frac{2 + x_1}{1 + x_2} - 3x_1 + 4x_3
\]

约束：

\[
0.1 \le x_1, x_2, x_3 \le 0.9
\]

分类说明：
- 该模型含有分式项 \(\frac{2 + x_1}{1 + x_2}\)
- 因此它不是线性规划，也不是标准二次规划
- 在统一模型接口中，其 `problem_type` 标记为 `NLP`

## `lp_scipy_func.py`

该文件作为原始文件名的兼容入口保留，内部调用 `bounded_surface_optimization_problem.py` 的统一模型定义，并通过 `ModelSolver.py` 的 `scipy` 后端运行。

## 运行方式

```bash
.venv\Scripts\python.exe src\nonlinear_programming\bounded_surface_optimization_problem.py
.venv\Scripts\python.exe src\nonlinear_programming\lp_scipy_func.py
```
