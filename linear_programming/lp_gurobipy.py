# -*- coding: utf-8 -*-

# ***************************************************
# * File        : lp_demo.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2024-10-10
# * Version     : 0.1.101017
# * Description : description
# * Link        : https://docs.gurobi.com/projects/examples/en/current/examples/python/lp.html
# * Requirement : 相关模块版本需求(例如: numpy >= 2.1.0)
# ***************************************************

# This example reads an LP model from a file and solves it.
# If the model is infeasible or unbounded, the example turns off
# presolve and solves the model again. If the model is infeasible,
# the example computes an Irreducible Inconsistent Subsystem (IIS),
# and writes it to a file

# python libraries
import os
import sys
ROOT = os.getcwd()
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import gurobipy as grb

# global variable
LOGGING_LABEL = __file__.split('/')[-1][:-3]


# 命令行参数
if len(sys.argv) < 2:
    print("Usage: lp.py filename")
    sys.exit(0)


# read and solve model
model = grb.read(sys.argv[1])
model.optimize()

if model.Status == grb.GRB.INF_OR_UNBD:
    # turn presolve off to determine whether model is infeasible or unbounded
    # 关闭预求解来确定模型是否不可行或无界
    model.setParam(grb.GRB.Param.Presolve, 0)
    model.optimize()

if model.Status == grb.GRB.OPTIMAL:
    print(f"Optimal objective: {model.ObjVal:g}")
    model.write("model.sol")
    sys.exit(0)
elif model.Status != grb.GRB.INFEASIBLE:
    print(f"Optimization was stopped with status {model.Status}")
    sys.exit(0)


# model is infeasible - compute an Irreducible Inconsistent Subsystem(IIS)
print("")
print("Model is infeasible")
model.computeIIS()
model.write("model.ilp")
print("IIS written to file 'model.ilp'")




# 测试代码 main 函数
def main():
    pass

if __name__ == "__main__":
    main()
