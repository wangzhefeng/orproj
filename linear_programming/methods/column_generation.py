# -*- coding: utf-8 -*-

# ***************************************************
# * File        : column_generation.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2024-09-16
# * Version     : 0.1.091619
# * Description : 列生成法示例
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


# ------------------------------
# 列生成法主问题
# ------------------------------
# model
model = grb.Model() 

# vars
z1 = model.addVar(vtype = grb.GRB.CONTINUOUS, name = "z1")
z2 = model.addVar(vtype = grb.GRB.CONTINUOUS, name = "z2")
z3 = model.addVar(vtype = grb.GRB.CONTINUOUS, name = "z3")
z4 = model.addVar(vtype = grb.GRB.CONTINUOUS, name = "z4")

# constr
model.addConstr(6 * z1 >= 25)
model.addConstr(2 * z2 >= 30)
model.addConstr(2 * z3 >= 14)
model.addConstr(z4 >= 8)
model.addConstr(z1 >= 0)
model.addConstr(z2 >= 0)
model.addConstr(z3 >= 0)
model.addConstr(z4 >= 0)

# objective
model.setObjective(z1 + z2 + z3 + z4, grb.GRB.MINIMIZE)

# solve
model.optimize()
# print(f"目标函数值是：{model.objVar}")

# result
for v in model.getVars():
    print(v.varName, "=", v.x)

# 获取约束的对偶变量的值
dual = model.getAttr(grb.GRB.Attr.Pi, model.getConstrs())
print(dual)

# ------------------------------
# 列生成法子问题
# ------------------------------
# model
model = grb.Model()

# vars
a1 = model.addVar(vtype = grb.GRB.INTEGER, name = "a1")
a2 = model.addVar(vtype = grb.GRB.INTEGER, name = "a2")
a3 = model.addVar(vtype = grb.GRB.INTEGER, name = "a3")
a4 = model.addVar(vtype = grb.GRB.INTEGER, name = "a4")

# constr
model.addConstr(3 * a1 + 7 * a2 + 9 * a3 + 16 * a4 <= 20)

# objective
model.setObjective(1 - 0.166 * a1 - 0.5 * a2 - 0.5 * a3 - a4, grb.GRB.MINIMIZE)

# solve
model.optimize()
# print(f"目标函数值是：{model.objVar}")

# result
for v in model.getVars():
    print(v.varName, "=", v.x)




# 测试代码 main 函数
def main():
    pass

if __name__ == "__main__":
    main()
