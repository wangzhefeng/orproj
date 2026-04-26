<details><summary>目录</summary><p>

- [项目简介](#项目简介)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [核心架构：ModelSolver.py](#核心架构modelsolver)
- [已实现内容](#已实现内容)
    - [线性规划（LP）](#线性规划lp)
    - [整数规划（IP）](#整数规划ip)
    - [混合整数规划（MIP）](#混合整数规划mip)
    - [二次规划（QP）](#二次规划qp)
    - [非线性规划（NLP）](#非线性规划nlp)
    - [多目标优化（MOIP）](#多目标优化moip)
    - [动态规划（DP）](#动态规划dp)
    - [路径规划](#路径规划)
    - [启发式算法](#启发式算法)
- [待完善内容](#待完善内容)
- [数学规划理论速查](#数学规划理论速查)
- [求解器说明](#求解器说明)
    - [reference](#reference内置教学后端)
    - [SciPy](#scipy)
    - [CVXPY](#cvxpy)
    - [Pyomo + GLPK](#pyomo--glpk)
    - [OR-Tools](#or-tools)
    - [SCIP](#scip)
    - [Gurobi](#gurobi)
    - [CPLEX / DOCPLEX](#cplex--docplex)
    - [PuLP](#pulp)
- [参考资料](#参考资料)

</p></details><p></p>

# 运筹优化工程仓库（orproj）

## 项目简介

本仓库是一个运筹优化**教学工程**项目，目标是：

- 用统一建模接口（[`src/ModelSolver.py`](src/ModelSolver.py)）管理多类型优化问题
- 展示 LP / IP / MIP / QP / NLP / MOIP / DP / 路径规划 / 启发式算法的标准建模与求解方式
- 内置参考后端（`reference`），**无需安装任何商用求解器**即可直接运行所有示例

工作约定见 [AGENTS.md](AGENTS.md)，常用运行命令见 [.codex/RUNBOOK.md](.codex/2026-01-01-RUNBOOK.md)。

---

## 项目结构

```
orproj/
├── src/
│   ├── ModelSolver.py                  # 统一建模与求解器接口（核心）
│   ├── linear_programming/             # LP：5 主问题 + 3 方法脚本
│   ├── integer_programming/            # IP：0-1 二元决策
│   ├── mix_integer_programming/        # MIP：整数批次决策
│   ├── quadratic_programming/          # QP：投资组合、生产平滑
│   ├── nonlinear_programming/          # NLP：分式目标函数
│   ├── multi_objective_optimizaion/    # MOIP：多目标加权聚合
│   ├── dynamic_programming/            # DP：爬楼梯、最短路径、背包
│   ├── path_planning/                  # 路径规划：RRT* 系列 + A*/D* 系列 + 曲线生成
│   └── heuristic_algorithms/           # 进化算法：GA / ACO / PSO / SA
├── .codex/                             # 任务模板、检查清单、运行手册
├── AGENTS.md                           # Codex 工作约定（主规范）
├── CLAUDE.md                           # Claude Code 补充配置
└── pyproject.toml                      # 依赖：numpy / scipy / cvxpy / matplotlib / pandas
```

---

## 快速开始

**环境要求：** Python >= 3.10

```bash
# 安装依赖
pip install -e .

# 运行最简示例（无需任何商用求解器）
python3 src/linear_programming/product_mix_problem.py
```

预期输出：状态 `OPTIMAL`，目标值 `2600.0`，变量 `x_desks=20, x_tables=60`。

---

## 核心架构：ModelSolver

[`src/ModelSolver.py`](src/ModelSolver.py) 是本仓库的工程核心，采用**策略模式 + 工厂模式**实现多求解器统一调用层，设计动机见 [`src/README.md`](src/README.md)。

### 核心数据结构

| 类 | 作用 |
|----|------|
| `Variable` | 决策变量：名称、边界（`lb/ub`）、类型（`C/I/B`） |
| `Constraint` | 约束：线性表达式 + 关系符（`<=` / `==` / `>=`） + 右侧常数 |
| `Objective` | 目标函数：线性项、二次项、非线性函数、方向（`min/max`）、权重 |
| `OptimizationModel` | 完整模型：变量 + 约束 + 目标 + `problem_type` 标签 |
| `SolverConfig` | 求解配置：时间限制、MIP 间隙、线程数 |
| `SolveResult` | 统一结果：状态、目标值、变量值、求解器名称 |

`problem_type` 取值：`LP` / `IP` / `MIP` / `QP` / `MIQP` / `NLP` / `MOIP`

### 支持的求解器后端

| 后端名称 | 说明 |
|---------|------|
| `reference` | **内置教学后端**，顶点枚举法（2D LP）或有限候选集枚举（其他），无需额外安装 |
| `scipy` | SciPy 优化接口 |
| `gurobi` | Gurobi（需商用许可） |
| `cplex` / `docplex` | IBM CPLEX（需商用许可） |
| `ortools` | Google OR-Tools |
| `pyomo` | Pyomo 建模层（可搭配 GLPK 等开源求解器） |
| `scip` | SCIP 开源求解器 |

### 最小使用示例

```python
from src.ModelSolver import (
    OptimizationModel, Variable, Constraint, Objective,
    SolverConfig, run_example_model
)

def build_model():
    return OptimizationModel(
        name="toy",
        problem_type="LP",
        variables=[Variable("x", lb=0, ub=6), Variable("y", lb=0, ub=6)],
        constraints=[Constraint("c1", {"x": 1, "y": 2}, "<=", 14)],
        objective=Objective("obj", "max", {"x": 5, "y": 4}),
        objectives=[],
    )

run_example_model(build_model, solver_name="reference")
```

---

## 已实现内容

### 线性规划（LP）

> 目录：[`src/linear_programming/`](src/linear_programming/)

| 脚本 | 问题名 | 目标函数 |
|------|--------|---------|
| [`product_mix_problem.py`](src/linear_programming/product_mix_problem.py) | 两产品生产优化 | $\max\; 40x_1 + 30x_2$ |
| [`transportation_problem.py`](src/linear_programming/transportation_problem.py) | 运输问题 | $\min\; 4x_{NE} + 6x_{NW} + 5x_{SE} + 3x_{SW}$ |
| [`resource_allocation_problem.py`](src/linear_programming/resource_allocation_problem.py) | 资源分配 | $\min\; 3x_{11} + 2x_{21} + 4x_{31} + 5x_{12}$ |
| [`three_variable_linear_problem.py`](src/linear_programming/three_variable_linear_problem.py) | 三变量 LP | $\max\; 2x_{1} + 3x_{2} - 5x_{3}$ |
| [`infeasibility_analysis_problem.py`](src/linear_programming/infeasibility_analysis_problem.py) | 不可行诊断 | 矛盾约束示例（ $x+y \geq 8$ 且 $x+y \leq 5$ ） |

方法脚本（[`methods/`](src/linear_programming/methods/)）：单纯形法、内点法、列生成（教学演示）

```bash
python src/linear_programming/product_mix_problem.py
python src/linear_programming/transportation_problem.py
```

---

### 整数规划（IP）

> 目录：[`src/integer_programming/`](src/integer_programming/)

| 脚本 | 问题名 | 目标函数 |
|------|--------|---------|
| [`binary_selection_problem.py`](src/integer_programming/binary_selection_problem.py) | 0-1 项目选择 | $\max\; x_{1} + x_{2} + 2x_{3},\quad x_{i} \in \lbrace 0,1 \rbrace$ |

```bash
python src/integer_programming/binary_selection_problem.py
```

---

### 混合整数规划（MIP）

> 目录：[`src/mix_integer_programming/`](src/mix_integer_programming/)

| 脚本 | 问题名 | 目标函数 |
|------|--------|---------|
| [`capital_budgeting_problem.py`](src/mix_integer_programming/capital_budgeting_problem.py) | 生产线批次决策 | $\max\; 3x_1 + 2x_2,\quad x_1, x_2 \in \mathbb{Z}_{\geq 0}$ |

```bash
python src/mix_integer_programming/capital_budgeting_problem.py
```

---

### 二次规划（QP）

> 目录：[`src/quadratic_programming/`](src/quadratic_programming/)

| 脚本 | 问题名 | 目标函数 |
|------|--------|---------|
| [`portfolio_risk_problem.py`](src/quadratic_programming/portfolio_risk_problem.py) | 投资组合均值-方差 | $\min\; 0.05w_{b}^{2} + 0.18w_{s}^{2} + 0.10w_{f}^{2} + \cdots$ |
| [`production_smoothing_problem.py`](src/quadratic_programming/production_smoothing_problem.py) | 生产平滑 | $\min\; (x_1-5)^2 + (x_2-5)^2$ |

```bash
python src/quadratic_programming/portfolio_risk_problem.py
python src/quadratic_programming/production_smoothing_problem.py
```

---

### 非线性规划（NLP）

> 目录：[`src/nonlinear_programming/`](src/nonlinear_programming/)

| 脚本 | 问题名 | 目标函数 |
|------|--------|---------|
| [`bounded_surface_optimization_problem.py`](src/nonlinear_programming/bounded_surface_optimization_problem.py) | 分式目标曲面优化 | $\min\; \frac{2+x_1}{1+x_2} - 3x_1 + 4x_3$ |

```bash
python src/nonlinear_programming/bounded_surface_optimization_problem.py
```

---

### 多目标优化（MOIP）

> 目录：[`src/multi_objective_optimizaion/`](src/multi_objective_optimizaion/)

采用加权聚合法，通过 `Objective.weight` 字段设置各目标权重。

| 脚本 | 问题名 | 目标 |
|------|--------|------|
| [`workforce_balance_problem.py`](src/multi_objective_optimizaion/workforce_balance_problem.py) | 劳动力均衡 | 利润 $\max 8x_{r}+6x_{o}$，加班 $\min x_{o}$，权重 0.7/0.3 |
| [`green_supply_mix_problem.py`](src/multi_objective_optimizaion/green_supply_mix_problem.py) | 绿色供应链 | 成本 $\min 7x_{A}+5x_{B}$，碳排 $\min 2x_{A}+5x_{B}$，权重 0.6/0.4 |

```bash
python src/multi_objective_optimizaion/workforce_balance_problem.py
python src/multi_objective_optimizaion/green_supply_mix_problem.py
```

---

### 动态规划（DP）

> 目录：[`src/dynamic_programming/`](src/dynamic_programming/)　｜　**README 待补**

| 脚本 | 问题 | 方法 |
|------|------|------|
| `climbing_stairs_dp.py` | 爬楼梯 | 动态规划 |
| `climbing_stairs_dfs.py` | 爬楼梯 | DFS 暴力搜索 |
| `climbing_stairs_dfs_mem.py` | 爬楼梯 | DFS + 记忆化 |
| `climbing_stairs_backtrack.py` | 爬楼梯 | 回溯 |
| `path_dp.py` | 最短路径 | 动态规划 |
| `path_mip.py` | 最短路径 | 整数规划建模 |
| `bag_dp.py` | 背包问题 | 动态规划（占位，待实现） |

---

### 路径规划

> 目录：[`src/path_planning/`](src/path_planning/)　｜　**README 待补**

包含 80+ 个脚本，分三大类：

**基于采样的规划（RRT 系列）**

| 子目录 | 算法 |
|--------|------|
| `sampling_based/rrt_2D/` | RRT / RRT-Connect / RRT\* / Informed RRT\* / BIT\* / ABIT\* / FMT\* |
| `sampling_based/rrt_3D/` | 上述算法的三维版本 |

**基于搜索的规划（A\*/D\* 系列）**

| 子目录 | 算法 |
|--------|------|
| `search_based/search_2D/` | Dijkstra / BFS / DFS / A\* / 双向A\* / ARA\* / D\* / D\* Lite / LPA\* / LRTA\* |
| `search_based/search_3D/` | 上述算法的三维版本 |

**曲线生成（`CurvesGenerator/`）**

贝塞尔曲线、B 样条、三次样条、Dubins 路径、四次/五次多项式、Reeds-Shepp 路径

---

### 启发式算法

> 目录：[`src/heuristic_algorithms/`](src/heuristic_algorithms/)　｜　**README 待补**

| 子目录 | 算法 |
|--------|------|
| `genetic_algorithm/` | 遗传算法（单目标 + LP/IP 问题专项） |
| `ant_colony_algorithm/` | 蚁群优化（ACO） |
| `particle_swarm_optimization/` | 粒子群优化（PSO） |
| `simulated_annealing_algorithm/` | 模拟退火（SA） |
| `transport_geatpy/` | 运输问题的 Geatpy 实现 |

---

## 待完善内容

### 文档待补（代码已有）

| 模块 | 说明 | 优先级 |
|------|------|--------|
| `src/dynamic_programming/` | 补写 README，含各脚本的问题说明与运行命令 | 高 |
| `src/path_planning/` | 补写 README，含算法分类说明、依赖环境、运行方式 | 高 |
| `src/heuristic_algorithms/` | 补写 README，含各算法的适用场景与运行命令 | 中 |

### 算法实现待补

| 类型 | 说明 | 优先级 |
|------|------|--------|
| CVXPY 后端对接 | `ModelSolver.py` 中尚无 `cvxpy` 策略实现，需补充 `CvxpySolverStrategy`，适配 LP/QP/NLP 问题 | 高 |
| LP 方法：列生成 | `methods/column_generation.py` 当前为教学示意，需补充完整列生成主问题+子问题迭代逻辑 | 中 |
| MIP 求解算法 | 分支定界法（B&B）、割平面法等尚无实现，仅理论分类 | 中 |
| 多目标方法扩展 | Pareto 前沿可视化、ε-约束法等尚无实现 | 低 |
| 背包问题 | `bag_dp.py` 仅有 `__all__` 占位，核心逻辑待补 | 中 |
| 整数随机规划 | 原 README 提及，当前无任何实现 | 低 |
| 广义分隔编程 / DAE | 原 README 提及，当前无任何实现 | 低 |
| SDP 示例问题 | 新增 `src/semidefinite_programming/` 目录，提供 SDP 建模示例（如 MAX-CUT 松弛），基于 CVXPY + SCS 后端运行 | 中 |

---

## 数学规划理论速查

### 模型类型

| 缩写 | 全名 | 特征 |
|------|------|------|
| LP | Linear Programming | 线性目标 + 线性约束 |
| IP / BIP | Integer / Binary Integer Programming | 决策变量为整数或 0-1 |
| MIP / MILP | Mixed Integer (Linear) Programming | 连续变量 + 整数变量混合 |
| MIQP | Mixed Integer Quadratic Programming | 含二次项的 MIP |
| MINLP | Mixed Integer Nonlinear Programming | 含非线性项的 MIP |
| QP | Quadratic Programming | 二次目标 + 线性约束 |
| NLP | Nonlinear Programming | 含非线性目标或约束 |
| MOIP | Multi-Objective (Integer) Programming | 多个目标函数 |
| DP | Dynamic Programming | 最优子结构递推 |
| SOCP | Second-Order Cone Programming | 约束含二阶锥，是 QP 的推广；可用 CVXPY 建模 |
| SDP | Semidefinite Programming | 变量为对称半正定矩阵，目标为矩阵迹的线性函数；可用 CVXPY 建模 |

**半正定规划（SDP）说明**

SDP 是凸优化中最重要的问题类之一，标准形式为：

$$\min_{X} \; \mathrm{tr}(C^\top X) \quad \text{s.t.} \quad \mathrm{tr}(A_i^\top X) = b_i,\ i=1,\ldots,m,\quad X \succeq 0$$

其中 $X \in \mathbb{S}^{n}$ 为对称半正定矩阵，$\succeq 0$ 表示正半定约束。SDP 是 LP（标量变量）的矩阵推广：LP 对应标量非负约束 $x \geq 0$，SDP 对应矩阵半正定约束 $X \succeq 0$。典型应用场景：

- 组合优化的 SDP 松弛（MAX-CUT、图着色）
- 鲁棒优化与协方差矩阵估计
- 控制系统中的 Lyapunov 稳定性分析
- 信号处理中的波束成形优化

本项目推荐用 **CVXPY** 建模和求解 SDP 问题（内置 SCS 后端，无需额外安装）。

### 经典求解算法

| 类型 | 算法 |
|------|------|
| LP | 单纯形法、内点法、列生成 |
| IP / MIP | 分支定界法、割平面法、分支切割 |
| NLP | 梯度下降、牛顿法、内点法、SQP |
| SDP / SOCP | 内点法（原对偶路径跟踪）、SCS（分裂锥求解器）、MOSEK |
| 路径规划 | Dijkstra、A\*、D\*、RRT、RRT\* |
| 启发式 | 遗传算法、蚁群优化、粒子群优化、模拟退火 |

---

## 求解器说明

### 快速参考

| 类型 | 求解器 | Python 接口 | 适合问题 |
|------|--------|------------|---------|
| **内置** | reference | 本仓库内置 | LP / IP / MIP / QP（教学示意） |
| 开源 | SciPy | `scipy` | LP / NLP（小规模） |
| 开源 | CVXPY | `cvxpy` | LP / QP / SOCP / **SDP**（凸优化建模层） |
| 开源 | GLPK | `pyomo` + GLPK | LP / MIP（中小规模） |
| 开源 | OR-Tools | `ortools` | LP / MIP / VRP / 调度 |
| 开源 | SCIP | `pyscipopt` | MIP / MINLP |
| 商用 | Gurobi | `gurobipy` | LP / MIP / QP（高性能） |
| 商用 | CPLEX | `docplex` | LP / MIP / QP（高性能） |
| 建模层 | Pyomo | `pyomo` | 多类型（可搭配多种后端） |
| 建模层 | PuLP | `pulp` | LP / MIP（默认内置 CBC，语法简洁） |

---

### reference（内置教学后端）

**介绍**：本仓库内置的参考求解后端，不依赖任何外部求解器库。对 2D 连续 LP 采用顶点枚举法，对其他问题采用有限候选集枚举法，多目标通过加权聚合实现。适合教学演示与快速验证，不适合大规模生产问题。

**安装**：随项目依赖安装，无需额外操作。

**Python 接口**：

```python
from src.ModelSolver import run_example_model, SolverEngine

# 使用统一入口运行任意问题
run_example_model(build_model_fn, solver_name="reference")
```

---

### SciPy

**介绍**：Python 科学计算基础库，`scipy.optimize` 模块提供 LP（`linprog`）和通用非线性优化（`minimize`）接口，无需额外求解器，适合小规模 LP 和 NLP 问题。

**安装**：已列入项目依赖，随 `pip install -e .` 自动安装。

```bash
pip install scipy
```

**Python 接口**：

```python
from scipy.optimize import linprog, minimize

# LP：min c^T x，s.t. A_ub x <= b_ub
res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

# NLP：min f(x)，s.t. 约束
res = minimize(fun, x0, method="SLSQP", constraints=constraints, bounds=bounds)
```

---

### CVXPY

**介绍**：专为凸优化设计的 Python 建模层，语法接近数学公式，支持 LP / QP / SOCP / **SDP** 等多类凸优化问题。内置 SCS、ECOS、OSQP 等开源后端，也可搭配 Gurobi、MOSEK 等商用求解器。本项目中 SDP 问题的首选工具。

**安装**：已列入项目依赖，随 `pip install -e .` 自动安装。

```bash
pip install cvxpy
```

**Python 接口**：

```python
import cvxpy as cp

# LP 示例：两产品生产优化
x = cp.Variable(2, nonneg=True)
obj = cp.Maximize(cp.array([40.0, 30.0]) @ x)
constraints = [x[0] <= 40, x[0] + x[1] <= 80, 2*x[0] + x[1] <= 100]
prob = cp.Problem(obj, constraints)
prob.solve()

# SDP 示例：最小化迹，约束半正定
X = cp.Variable((3, 3), symmetric=True)
obj = cp.Minimize(cp.trace(C @ X))
constraints = [cp.trace(A[i] @ X) == b[i] for i in range(m)] + [X >> 0]
prob = cp.Problem(obj, constraints)
prob.solve(solver=cp.SCS)
```

---

### Pyomo + GLPK

**介绍**：Pyomo 是基于 Python 的代数建模语言（AML），支持 LP / MIP / NLP 等多种问题类型，本身不包含求解器，需搭配 GLPK、CBC、CPLEX、Gurobi 等后端。GLPK（GNU Linear Programming Kit）是配套的开源线性规划工具包，单线程单纯形解算器，适合中小规模 LP / MIP。

**安装**：

```bash
pip install pyomo

# GLPK 安装（选其一）
apt-get install -y glpk-utils   # Linux / WSL
brew install glpk                # macOS
```

**Python 接口**：

```python
import pyomo.environ as pyo

model = pyo.ConcreteModel()
model.x = pyo.Var(domain=pyo.NonNegativeReals)
model.y = pyo.Var(domain=pyo.NonNegativeReals)
model.obj = pyo.Objective(expr=40*model.x + 30*model.y, sense=pyo.maximize)
model.c1 = pyo.Constraint(expr=model.x <= 40)

solver = pyo.SolverFactory("glpk")
result = solver.solve(model)
```

---

### OR-Tools

**介绍**：Google 开源维护的组合优化求解器套件，内置 LP（GLOP）、MIP（CP-SAT）、车辆路径（VRP）、调度等求解器。在中小规模路径规划和调度问题上有良好性能，Python 接口友好。

**安装**：

```bash
pip install ortools
```

**Python 接口**：

```python
from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver("GLOP")  # LP
x = solver.NumVar(0, solver.infinity(), "x")
y = solver.NumVar(0, solver.infinity(), "y")
solver.Maximize(40 * x + 30 * y)
solver.Add(x <= 40)
status = solver.Solve()
```

---

### SCIP

**介绍**：Zuse Institute Berlin（ZIB）开发的开源 MIP / MINLP 求解器，在学术与工业界均广泛使用。支持分支定界、割平面、Benders 分解等高级技术，适合复杂整数规划和混合整数非线性规划。

**安装**：

```bash
pip install pyscipopt
```

**Python 接口**：

```python
from pyscipopt import Model

model = Model()
x = model.addVar("x", vtype="I", lb=0)
y = model.addVar("y", vtype="I", lb=0)
model.setObjective(3*x + 2*y, sense="maximize")
model.addCons(2*x + 3*y <= 14)
model.optimize()
```

---

### Gurobi

**介绍**：美国 Gurobi 公司开发的商用高性能求解器，在 LP / MIP / QP / MIQP 等问题上持续保持业界领先性能。提供学术免费许可证（需申请），商业场景需购买许可。本仓库 `ModelSolver.py` 中已注册 `gurobi` 后端占位符。

**安装**：

```bash
pip install gurobipy
# 需在 Gurobi 官网申请并激活许可证（学术版免费）
```

**Python 接口**：

```python
import gurobipy as gp
from gurobipy import GRB

model = gp.Model()
x = model.addVar(name="x", lb=0)
y = model.addVar(name="y", lb=0)
model.setObjective(40*x + 30*y, GRB.MAXIMIZE)
model.addConstr(x <= 40, "c1")
model.optimize()
```

---

### CPLEX / DOCPLEX

**介绍**：IBM 开发的商用高性能求解器，与 Gurobi 并列为业界顶级 MIP 求解器。`docplex` 是其 Python 建模接口，语法较接近自然语言。学术版通过 IBM Academic Initiative 免费申请。本仓库 `ModelSolver.py` 中已注册 `cplex` / `docplex` 后端占位符。

**安装**：

```bash
pip install docplex
# 需在 IBM 官网申请并配置 CPLEX 引擎（学术版免费）
```

**Python 接口**：

```python
from docplex.mp.model import Model

mdl = Model(name="product_mix")
x = mdl.continuous_var(name="x", lb=0)
y = mdl.continuous_var(name="y", lb=0)
mdl.maximize(40*x + 30*y)
mdl.add_constraint(x <= 40, "c1")
solution = mdl.solve()
```

---

### PuLP

**介绍**：PuLP 是用 Python 编写的开源 LP / MIP 建模库，语法简洁直观，内置 CBC（COIN-OR Branch and Cut）求解器，无需额外安装即可求解 LP 和 MIP 问题。也支持调用 GLPK、Gurobi、CPLEX 等外部求解器。相比 Pyomo，PuLP 更轻量，适合快速建模中小规模线性整数规划问题；相比 CVXPY，PuLP 不支持 QP / SDP 等非线性凸优化，但 LP / MIP 的 API 更为简洁。

**安装**：

```bash
pip install pulp
# CBC 求解器随 pulp 自动安装，无需额外操作
```

**Python 接口**：

```python
import pulp

# LP 示例：两产品生产优化
prob = pulp.LpProblem("product_mix", pulp.LpMaximize)

x_desks  = pulp.LpVariable("x_desks",  lowBound=0)
x_tables = pulp.LpVariable("x_tables", lowBound=0)

# 目标函数
prob += 40 * x_desks + 30 * x_tables

# 约束
prob += x_desks <= 40
prob += x_desks + x_tables <= 80
prob += 2 * x_desks + x_tables <= 100

prob.solve(pulp.PULP_CBC_CMD(msg=False))
print(pulp.LpStatus[prob.status])          # Optimal
print(pulp.value(prob.objective))          # 2600.0

# MIP 示例：0-1 整数规划
prob_mip = pulp.LpProblem("binary_selection", pulp.LpMaximize)
x = [pulp.LpVariable(f"x{i}", cat="Binary") for i in range(1, 4)]
prob_mip += x[0] + x[1] + 2*x[2]
prob_mip += x[0] + 2*x[1] + 3*x[2] <= 4
prob_mip += x[0] + x[1] >= 1
prob_mip.solve(pulp.PULP_CBC_CMD(msg=False))
```

**切换外部求解器**：

```python
# 使用 GLPK
prob.solve(pulp.GLPK(msg=False))

# 使用 Gurobi（需已安装 gurobipy 和许可证）
prob.solve(pulp.GUROBI(msg=False))
```

---

## 参考资料

* [多求解器时代的工程设计（ModelSolver.py 来源）](https://mp.weixin.qq.com/s/9z1TfR0XB58CCRAf-ccPxw)
* [PathPlanning](https://github.com/zhm-real/PathPlanning)
* [路径规划五种算法简述及对比](https://zhuanlan.zhihu.com/p/124232080)
* [python 运筹优化实践](https://www.zhihu.com/column/c_1060904037507006464)
* [Computational-intelligence](https://github.com/doFighter/Computational-intelligence)
* [Geatpy](https://github.com/geatpy-dev/geatpy)
* [GLPK 安装说明](https://blog.csdn.net/weixin_42848399/article/details/91654118)
