# -*- coding: utf-8 -*-

# ***************************************************
# * File        : path_mip.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2024-08-30
# * Version     : 0.1.083016
# * Description : 整数规划求解最短路径问题
# * Link        : link
# * Requirement : 相关模块版本需求(例如: numpy >= 2.1.0)
# ***************************************************

# python libraries
import os
import sys
ROOT = os.getcwd()
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import gurobipy as grb

# global variable
LOGGING_LABEL = __file__.split('/')[-1][:-3]


# 定义边
edge = {
    ("V1", "A"): 0,
    ("A", "B1"): 10,
    ("A", "B2"): 20,
    ("B1", "C1"): 30,
    ("B1", "C2"): 10,
    ("B2", "C1"): 5,
    ("B2", "C2"): 20,
    ("C1", "D"): 20,
    ("C2", "D"): 10,
    ("D", "V2"): 0,
}

# 创建边和边长度的 Gurobi 常量
links, length = grb.multidict(edge)

# 创建模型
m = grb.Model()

# 创建变量
x = m.addVars(links, obj = length, name = "flow")

# 添加约束
for i in ["A", "B1", "B2", "C1", "C2", "D"]:
    if i == "A":
        delta = 1
    elif i == "D":
        delta = -1
    else:
        delta = 0
    
    name = f"C_{i}"
    m.addConstr(
        sum(x[i, j] for i, j in links.select(i, "*")) - sum(x[j, i] for j, i in links.select("*", i)) == delta, 
        name = name
    )
    # m.addConstr(
    #     x.sum(i, "*") - x.sum("*", i) == delta, 
    #     name = name
    # )

# 求解并打印结果
m.optimize()

for i, j in links:
    if (x[i, j].x > 0):
        print(f"{i}->{j}: {edge[(i, j)]}")


# 测试代码 main 函数
def main():
    pass

if __name__ == "__main__":
    main()
