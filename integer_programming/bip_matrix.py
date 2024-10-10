# -*- coding: utf-8 -*-

# ***************************************************
# * File        : bip_matrix.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2024-10-10
# * Version     : 0.1.101015
# * Description : description
# * Link        : link
# * Requirement : 相关模块版本需求(例如: numpy >= 2.1.0)
# ***************************************************

# This example formulates and solves the following simple MIP model
# using the matrix API:
#  maximize
#        x + y + 2 z
#  subject to
#        x + 2 y + 3 z <= 4
#        x + y         >= 1
#        x, y, z binary

# python libraries
import os
import sys
ROOT = os.getcwd()
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import numpy as np
import scipy.sparse as sp
import gurobipy as grb

# global variable
LOGGING_LABEL = __file__.split('/')[-1][:-3]


try:
    # model
    m = grb.Model("bip_matrix")
    
    # variables
    x = m.addMVar(shape = 3, vtype = grb.GRB.BINARY, name = "x")
    
    # objective
    obj_coef = np.array([1.0, 1.0, 2.0])
    m.setObjective(obj_coef @ x, sense = grb.GRB.MAXIMIZE)
    
    # build constraint matrix(sparse)
    val = np.array([1.0, 2.0, 3.0, -1.0, -1.0])
    row = np.array([0, 0, 0, 1, 1])
    col = np.array([0, 1, 2, 0, 1])
    A = sp.csr_matrix((val, (row, col)), shape = (2, 3))
    # build rsh vector
    rhs = np.array([4.0, -1.0])
    # constraints
    m.addConstr(A @ x <= rhs, name = "c")
    
    # optimize model
    m.optimize()
    
    # print the result of model
    print(x.X)
    print(f"目标函数值：{m.ObjVal:g}")
except grb.GurobiError as e:
    print(f"Error code {e.errno}: {e}")
except AttributeError:
    print("Encountered an attribute error")





# 测试代码 main 函数
def main():
    pass

if __name__ == "__main__":
    main()
