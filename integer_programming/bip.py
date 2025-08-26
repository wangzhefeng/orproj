# -*- coding: utf-8 -*-

# ***************************************************
# * File        : mip1.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2024-10-10
# * Version     : 0.1.101014
# * Description : description
# * Link        : link
# * Requirement : 相关模块版本需求(例如: numpy >= 2.1.0)
# ***************************************************

# This example formulates and solves the following simple MIP model:
#  maximize
#        x + y + 2 z
#  subject to
#        x + 2 y + 3 z <= 4
#        x +   y       >= 1
#        x, y, z binary

# python libraries
import os
import sys
ROOT = os.getcwd()
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import gurobipy as grb

# global variable
LOGGING_LABEL = __file__.split('/')[-1][:-3]


try:
    # model
    m = grb.Model("bip")
    # variables
    x = m.addVar(vtype = grb.GRB.BINARY, name = "x")
    y = m.addVar(vtype = grb.GRB.BINARY, name = "y")
    z = m.addVar(vtype = grb.GRB.BINARY, name = "z")
    # objective 
    m.setObjective(x + y + 2 * z, sense = grb.GRB.MAXIMIZE)
    # constraint
    m.addConstr(x + 2 * y + 3 * z <= 4, name = "c0")
    m.addConstr(x + y >= 1, name = "c1")
    # optimize model
    m.optimize()
    # print optimize result
    for v in m.getVars():
        print(f"参数 {v.VarName} = {v.X:g}")
    print(f"目标函数值: {m.ObjVal:g}")
except grb.GurobiError as e:
    print(f"Error code {e.errno}: {e}")
except AttributeError:
    print("Encountered an attribute error")
    





# 测试代码 main 函数
def main():
    pass

if __name__ == "__main__":
    main()
