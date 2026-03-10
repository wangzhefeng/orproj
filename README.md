<details><summary>目录</summary><p>

- [数学规划模型简介](#数学规划模型简介)
    - [线性规划](#线性规划)
    - [整数规划、混合整数规划](#整数规划混合整数规划)
    - [多目标规划](#多目标规划)
    - [二次规划](#二次规划)
    - [动态规划](#动态规划)
    - [非线性规划](#非线性规划)
    - [路径规划](#路径规划)
    - [广义分隔编程](#广义分隔编程)
    - [微分代数方程](#微分代数方程)
    - [具有平衡约束的数据规划](#具有平衡约束的数据规划)
- [数学规划求解算法](#数学规划求解算法)
    - [线性规划](#线性规划-1)
    - [整数规划、混合整数规划](#整数规划混合整数规划-1)
    - [多目标规划](#多目标规划-1)
    - [动态规划](#动态规划-1)
    - [非线性规划](#非线性规划-1)
    - [路径规划](#路径规划-1)
    - [进化算法](#进化算法)
    - [广义分隔编程](#广义分隔编程-1)
    - [微分代数方程](#微分代数方程-1)
    - [具有平衡约束的数据规划](#具有平衡约束的数据规划-1)
- [最优化算法求解器](#最优化算法求解器)
    - [Pyomo](#pyomo)
- [参考资料](#参考资料)
</p></details><p></p>

# 数学规划模型简介

## 线性规划

* 线性规划(Linear Programming, LP)

## 整数规划、混合整数规划

* 整数规划(Integer Programming, IP)
    - 整数线性规划(Integer Linear Programming, ILP)
* 0-1 整数规划(Binary Integer Programming, BIP)
    - 0-1 整数线性规划(Binary Integer Linear Programming, BILP)
* 混合整数规划(Mix Integer Programming, MIP)
    - 混合整数线性规划(Mix Integer Linear Programming, MILP)
    - 混合整数二次规划(Mix Integer Quadratic Programming, MIQP)
    - 混合整数非线性规划(Mix Integer NonLinear Programming, MINLP)
* 整数随机规划

## 多目标规划

## 二次规划

## 动态规划

## 非线性规划

* 无约束非线性规划
* 带约束非线性规划

## 路径规划


## 广义分隔编程

## 微分代数方程

## 具有平衡约束的数据规划

<!-- ========================================================= -->
# 数学规划求解算法

## 线性规划

* 单纯形法(simplex method)
* 内点法(interior point)
* 列生成法

## 整数规划、混合整数规划

## 多目标规划

## 动态规划

## 非线性规划

## 路径规划

## 进化算法

* 蚁群算法
* 遗传算法
* 粒子群算法
* 模拟退火算法
* ...

## 广义分隔编程

## 微分代数方程

## 具有平衡约束的数据规划


<!-- ========================================================= -->
# 最优化算法求解器

无论是在生产制造领域，还是在金融、保险、交通等其他领域，当实际问题越来越复杂、
问题规模越来越庞大，就需要借助计算机的快速计算能力，求解器的作用就是能简化编程问题，
使得工程师能专注于问题的分析和建模，而不是编程。

一般我们使用 LP/MILP 包来单独建模一个实际的优化问题，例如 GAMS、AMPL、OPL 或其他，
然后使用优化求解器(例如 CPLEX、gu、Mosek、Xpress 等)来解决它，并将最优结果提供给决策者。

算法优化的求解器有很多，其中商用的求解器包括 Gurobi、CPLEX、Xpress 等；
开源的求解器有 SCIP、GLPK、Ortools 等，这些求解器都有 Python 接口，
因此，能够用比较简单的方式对运筹优化问题进行建模。

商用求解器：

* **Gurobi** 是由美国 Gurobi 公司开发的针对算法最优化领域的求解器，可以高效求解算法优化中的建模问题。
    - Python API：`gurobipy`
* **CPLEX** 用于 Python 的 IBM Decision Optimization CPLEX 建模包
    - Python API：`docplex`
* **Xpress**

开源求解器：

* **SCIP**
* **GLPK** 是一个开源的 GNU 线性编程工具包，可在 GNU 通用公共许可证 3 下使用。
  GLPK 是一个单线程单形解算器，通常适用于中小型线性整数规划问题。它是用 C 语言编写的，依赖性很小，
  因此在计算机和操作系统之间具有很高的可移植性。对于许多示例来说，GLPK 通常“足够好”。
  对于较大的问题，用户应该考虑高性能的解决方案，如 `COIN-OR CBC`，它们可以利用多线程处理器。
    - [`GLPK`](https://blog.csdn.net/weixin_42848399/article/details/91654118)
* **Ortools** 是 Google 开源维护的算法优化求解器，针对 Google 的商业场景进行优化，如 VRP 问题，
  对于中小规模的商业场景的使用是个不错的选择。
* **PuLP** 用 Python 编写的 LP/MILP 建模器
    - Python API：`pulp`   
* **Scipy**

其他求解器：

* **Pyomo**
    - Python API: `pyomo`
    - 求解器：[`GLPK`](https://blog.csdn.net/weixin_42848399/article/details/91654118)
* **Geatpy**
    - [geatpy-dev/geatpy](https://github.com/geatpy-dev/geatpy)

## Pyomo

Pyomo 是一个基于 Python 的开源软件包，它支持多种优化功能，用于制定和分析优化模型。
Pyomo 可用于定义符号问题、创建具体的问题实例，并使用标准解决程序解决这些实例。
Pyomo 支持多种问题类型，包括:

* 线性规划
* 二次规划
* 非线性规划
* 整数线性规划
* 混合整数二次规划
* 混合整数非线性规划
* 整数随机规划
* 广义分隔编程
* 微分代数方程
* 具有平衡约束的数学规划

Pyomo 支持全功能编程语言中的分析和脚本编制。此外，Pyomo 还证明了开发高级优化和分析工具的有效框架。
例如，`PySP` 包提供了随机规划的通用求解程序。`PySP` 利用了 Pyomo 的建模对象嵌入在功能全面的高级编程语言中的事实，
这种语言允许使用 Python 并行通信库透明地并行化子问题。

安装 `pyomo` 和 `GLPK`：

```bash
$ pip install pyomo
$ apt-get install -y -qq glpk-utils
```

<!-- ========================================================= -->
# 参考资料

* [PathPlanning](https://github.com/zhm-real/PathPlanning)
* [路径规划五种算法简述及对比](https://zhuanlan.zhihu.com/p/124232080)
* [python运筹优化实践](https://www.zhihu.com/column/c_1060904037507006464)
* [Computational-intelligence](https://github.com/doFighter/Computational-intelligence)
