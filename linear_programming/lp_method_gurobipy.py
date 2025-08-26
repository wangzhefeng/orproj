# -*- coding: utf-8 -*-

# ***************************************************
# * File        : lp_method_gurobipy.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2024-10-10
# * Version     : 0.1.101017
# * Description : description
# * Link        : link
# * Requirement : 相关模块版本需求(例如: numpy >= 2.1.0)
# ***************************************************

# Solve a model with different values of the Method parameter;
# show which value gives the shortest solve time.

# python libraries
import os
import sys
ROOT = os.getcwd()
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import gurobipy as grb

# global variable
LOGGING_LABEL = __file__.split('/')[-1][:-3]


if len(sys.argv) < 2:
    print("Usage: lpmethod.py filename")
    sys.exit(0)


# read model
m = grb.read(sys.argv[1])

# solve the model with different values of method
bestTime = m.Params.TimeLimit
bestMethod = -1
for i in range(3):
    m.reset()
    m.Params.Method = i
    m.optimize()
    if m.Status == grb.GRB.OPTIMAL:
        bestTime = m.Runtime
        bestMethod = i
        # reduce the TimeLimit parameter to save time with other methods
        m.Params.TimeLimit = bestTime

# report which method was fastest
if bestMethod == -1:
    print("Unable to solve this model")
else:
    print(f"Solved in {bestTime:g} seconds with Method {bestMethod}")




# 测试代码 main 函数
def main():
    pass

if __name__ == "__main__":
    main()
