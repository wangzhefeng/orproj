# -*- coding: utf-8 -*-


# ***************************************************
# * File        : lp_transportation_geatpy.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2023-04-13
# * Version     : 0.1.041307
# * Description : description
# * Link        : link
# * Requirement : 相关模块版本需求(例如: numpy >= 2.1.0)
# ***************************************************


# python libraries
import os
import sys
import numpy as np
import geatpy as ea


# global variable
LOGGING_LABEL = __file__.split('/')[-1][:-3]


# ------------------------------
# 定义参数
# ------------------------------
# 定义生产地和销售地
I = ["seattle", "san-diego"]
J = ["new-york", "chicago", "topeka"]

# 定义生产地的生产量和销售地的需求量
a = {"seattle": 350, "san-diego": 600}
b = {"new-york": 325, "chicago": 300, "topeka": 275}

# 定义生产地到销售地的距离(千英里)
dtab = {
    ("seattle", "new-york"): 2.5,
    ("seattle", "chicago"): 1.7,
    ("seattle", "topeka"): 1.8,
    ("san-diego", "new-york"): 2.5,
    ("san-diego", "chicago"): 1.8,
    ("san-diego", "topeka"): 1.4,
}

# 费用/千英里
f = 90

# cij 就是生产地 i 到销售地 j 的单位运价
def c_init(i, j):
    return f * dtab[i, j] / 100
c = {}
for i in I:
    for j in J:
        c[i, j] = c_init(i, j)

# ------------------------------
# 约束条件
# ------------------------------
def supply_rule(x, i):
    return sum(x[i, j] for j in J) - a[i]

def demand_rule(x, j):
    return (-1) * sum(x[i, j] for i in I) + b[j]

# ------------------------------
# 目标函数
# ------------------------------
def objective_rule(c, x):
    return sum(c[i, j] * x[i, j] for i in I for j in J)

# ------------------------------
# 问题定义
# ------------------------------
class MyProblem(ea.Problem):
    
    def __init__(self):
        name = "MyProblem"
        M = 1
        maxormins = [1]
        Dim = 6
        varTypes = [0] * Dim
        lb = [0] * Dim
        ub = [10000] * Dim
        lbin = [1] * Dim
        ubin = [1] * Dim
        ea.Problem.__init__(
            self, name, M, 
            maxormins, Dim, varTypes, 
            lb, ub, lbin, ubin
        )

    def aimFunc(self, pop):
        """
        目标函数
        """
        Vars = pop.Phen
        cnt = 0
        x = {}
        for i in I:
            for j in J:
                x[i, j] = Vars[:, [cnt]]
                cnt += 1
        pop.ObjV = objective_rule(c, x)

        for i in I:
            pop.CV = np.hstack([supply_rule(x, i)])

        for j in J:
            pop.CV = np.hstack([pop.CV, demand_rule(x, j)])




# 测试代码 main 函数
def main():
    pass

if __name__ == "__main__":
    main()
