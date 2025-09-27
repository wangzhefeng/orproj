# -*- coding: utf-8 -*-

# ***************************************************
# * File        : tupledict_demo.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2024-10-10
# * Version     : 0.1.101011
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


model = grb.Model()

# 定义变量的下标
t1 = [
    (1, 1), (1, 2), (1, 3),
    (2, 1), (2, 2), (2, 3),
    (3, 1), (3, 2), (3, 3),
]
vars = model.addVars(t1, name = "x")
model.update()
print(vars)

# 对第一行求和(两种方法)
print(sum(vars.select(1, "*")))
print(vars.sum(1, "*"))

# 创建一个系数矩阵，用 tupledict 格式存储
coeff = grb.tupledict([
    (1, 1),
    (1, 2),
    (1, 3),
])
print(coeff)
coeff[(1, 1)] = 1
coeff[(1, 2)] = 0.3
coeff[(1, 3)] = 0.4
print(coeff)
print(vars.prod(coeff, 1, "*"))


# tupledict 类型的变量快速创建约束条件
m = grb.Model()
x = m.addVars(3, 4, vtype = grb.GRB.BINARY, name = "x")
m.addConstrs((x.sum(i, "*") <= 1 for i in range(3)), name = "con")
m.update()
m.write("./gurobipy_demo/tupledict_vars.lp")



# 测试代码 main 函数
def main():
    pass

if __name__ == "__main__":
    main()
