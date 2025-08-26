# -*- coding: utf-8 -*-

# ***************************************************
# * File        : main.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2024-08-28
# * Version     : 0.1.082821
# * Description : description
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


try:
    # 定义模型
    model = grb.Model("mip")
    # 定义整数变量
    x1 = model.addVar(vtype = grb.GRB.INTEGER, name = "x1")
    x2 = model.addVar(vtype = grb.GRB.INTEGER, name = "x2")
    # 定义目标函数
    model.setObjective(3 * x1 + 2 * x2, sense = grb.GRB.MAXIMIZE)
    # 添加约束
    model.addConstr(2 * x1 + 3 * x2 <= 14)
    model.addConstr(4 * x1 + 2 * x2 <= 18)
    model.addConstr(x1 >= 0)
    model.addConstr(x2 >= 0) 
    # 模型求解
    model.optimize()
    # 模型结果打印 
    for v in model.getVars():
        print(f"参数 {v.varName} = {v.x}")
    print(f"目标函数值：{model.objVal}")
except grb.GurobiError as e:
    print(f"Error code {e.errno}: {e}")
except:
    print("Encountered an attribute error")




# 测试代码 main 函数
def main():
    pass

if __name__ == "__main__":
    main()
