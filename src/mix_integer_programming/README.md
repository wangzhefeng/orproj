---
source_type: web
created_at: 2026-01-01  # default placeholder, actual date unknown
topics: [orproj]
status: summarized
---

# Mix Integer Programming

本目录用于放置混合整数规划问题。当前示例来自原 `integer_programming` 目录中的 `mip.py`，现已迁移到本目录，并继续通过 [`src/ModelSolver.py`](E:/operations_research/orproj/src/ModelSolver.py) 统一运行。

需要注意：模型中的变量边界严格按照原始数学模型保留。像 `x1 >= 0`、`x2 >= 0` 这类约束仍然通过约束条件体现；如果参考后端为了枚举需要有限搜索范围，则使用 `search_ub`，不会把搜索上界误写成数学模型约束。

## 主问题脚本

### `capital_budgeting_problem.py`
该模型是一个小规模混合整数规划/整数批量决策示例，用来决定两条生产线的生产批次数量。

设：

- $x_1$：生产线 1 的批次数
- $x_2$：生产线 2 的批次数

其中 $x_1, x_2 \in \mathbb{Z}_{\ge 0}$。

目标函数：

$$
\max Z = 3x_1 + 2x_2
$$

约束条件：

$$
\begin{aligned}
2x_1 + 3x_2 &\le 14 \\
4x_1 + 2x_2 &\le 18 \\
x_1 &\ge 0 \\
x_2 &\ge 0
\end{aligned}
$$

这个问题体现的是：在机器工时和人工工时受限的情况下，如何选择整数批次以获得最大利润。

## 运行方式

```bash
.venv\Scripts\python.exe src\mix_integer_programming\capital_budgeting_problem.py
```
