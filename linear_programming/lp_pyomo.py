# -*- coding: utf-8 -*-


# ***************************************************
# * File        : lp_pyomo.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2023-04-12
# * Version     : 0.1.041223
# * Description : description
# * Link        : https://zhuanlan.zhihu.com/p/125179633
# * Requirement : 相关模块版本需求(例如: numpy >= 2.1.0)
# ***************************************************


# python libraries
import os
import sys

from pyomo.environ import *


# global variable
LOGGING_LABEL = __file__.split('/')[-1][:-3]


# ------------------------------
# Problem
# ------------------------------
# objective: profit = 40x + 30y
# constraint: x <= 40
#             x + y <= 80
#             2x + y <= 100
# ------------------------------


# model
model = ConcreteModel()

# 声明决策变量
model.x = Var(domain = NonNegativeReals)
model.y = Var(domain = NonNegativeReals)

# 声明目标函数
model.profit = Objective(expr = 40 * model.x + 30 * model.y, sense = maximize)

# 声明约束条件
model.demand = Constraint(expr = model.x <= 40)
model.laborA = Constraint(expr = model.x + model.y <= 80)
model.laborB = Constraint(expr = 2 * model.x + model.y <= 100)
model.pprint()

# 模型求解
SolverFactory("glpk", executable = "/usr/local/bin/glpsol").solve(model).write()

# 模型解
print(f"\nProfit = {model.profit()}")

print("\nDecision Variables:")
print(f"x = {model.x()}")
print(f"y = {model.y()}")

print("\nConstraints:")
print(f"Demand = {model.demand()}")
print(f"Labor A = {model.laborA()}")
print(f"Labor B = {model.laborB()}")







# 测试代码 main 函数
def main():
    pass

if __name__ == "__main__":
    main()
