# -*- coding: utf-8 -*-

# ***************************************************
# * File        : lp1.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2023-04-12
# * Version     : 0.1.041216
# * Description : description
# * Link        : https://zhuanlan.zhihu.com/p/124422566
# * Requirement : 相关模块版本需求(例如: numpy >= 2.1.0)
# ***************************************************

# python libraries
import os
import json
import random

import pandas as pd
import docplex.mp.model as cpx

# global variable
LOGGING_LABEL = __file__.split('/')[-1][:-3]


# ------------------------------
# Problem:
# ------------------------------
# Objective: `$$min \sum_{i=1}^{n}\sum_{j=1}^{m} c_{ij}x_{ij}$$`
# Constraint: `$$\sum_{i=1}^{n}a_{ij}x_{ij} \leq b_{j}, \forall j$$`
#             `$$x_{ij} \geq l_{ij}, \forall i, j$$`
#             `$$x_{ij} \leq u_{ij}, \forall i,j$$`
# ------------------------------
# ------------------------------
# 决策变量：n * m = 10 * 5
# 输出参数：n, m, c, a, b, l, u
# ------------------------------
n = 10
m = 5
set_I = range(1, n + 1)
set_J = range(1, m + 1)
c = {(i, j): random.normalvariate(0, 1) for i in set_I for j in set_J}
a = {(i, j): random.normalvariate(0, 5) for i in set_I for j in set_J}
b = {j: random.randint(0, 30) for j in set_J}
l = {(i, j): random.randint(0, 10) for i in set_I for j in set_J}
u = {(i, j): random.randint(10, 20) for i in set_I for j in set_J}
print(c)
print("-" * 20)
print(a)
print("-" * 20)
print(json.dumps(b, indent = 4))
print("-" * 20)
print(l)
print("-" * 20)
print(u)

# ------------------------------
# 模型
# ------------------------------
opt_model = cpx.Model(name = "MIP Model")

# ------------------------------
# 决策变量
# ------------------------------
# 决策变量：continuous
x_vars = {
    (i, j): opt_model.continuous_var(
        lb = l[i, j], 
        ub = u[i, j], 
        name = f"x_{i}_{j}"
    )
    for i in set_I for j in set_J
}
print(f"\nVariables:\n {x_vars}")
# 决策变量：binary
# x_vars = {
#     (i, j): opt_model.binary_var(name = f"x_{i}_{j}")
#     for i in set_I for j in set_J
# }
# print(f"\nVariables: {x_vars}")
# 决策变量：integer
# x_vars = {
#     (i, j): opt_model.integer_var(lb = l[i, j], ub = u[i, j], name = f"x_{i}_{j}")
#     for i in set_I for j in set_J
# }
# print(f"\nVariables: {x_vars}")

# ------------------------------
# 约束条件
# ------------------------------
# 小于等于(<=)约束
constraints = {
    j: opt_model.add_constraint(
        ct = opt_model.sum(a[i, j] * x_vars[i, j] for i in set_I) <= b[j], 
        ctname = f"constraint_{j}",
    )
    for j in set_J
}
print(f"\n Constraints:\n {constraints}")
# 大于等于(>=)约束
# constraints = {
#     j: opt_model.add_constraint(
#         ct = opt_model.sum(a[i, j] * x_vars[i, j] for i in set_I) >= b[j],
#         ctname = f"constraint_{j}",
#     )
#     for j in set_J
# }
# print(f"\n Constraints: {constraints}")
# 等于(==)约束
# constraints = {
#     j: opt_model.add_constraint(
#         ct = opt_model.sum(a[i, j] * x_vars[i, j] for i in set_I) == b[j],
#         ctname = f"constraint_{j}",
#     )
#     for j in set_J
# }
# print(f"\n Constraints: {constraints}")

# ------------------------------
# 目标函数
# ------------------------------
# objective
objective = opt_model.sum(x_vars[i, j] * c[i, j] for i in set_I for j in set_J)

# maximization
# opt_model.maximize(objective)

# minimization
opt_model.minimize(objective)

# ------------------------------
# 模型求解
# ------------------------------
# local cplex
opt_model.solve()

# cloud cplex
# opt_model.solve(url = "your_cplex_cloud_url", key = "your_api_key")

# ------------------------------
# 模型求解结果
# ------------------------------
# 决策变量解解析
opt_df = pd.DataFrame.from_dict(x_vars, orient = "index", columns = ["variable_object"])
opt_df.index = pd.MultiIndex.from_tuples(opt_df.index, name = ["column_i", "column_j"])
opt_df.reset_index(inplace = True)
opt_df["solution_value"] = opt_df["variable_object"].apply(lambda item: item.solution_value)
opt_df.drop(columns = ["variable_object"], inplace = True)

# 结果保存
solution_path = "./models/optimization_solution.csv"
if not os.path.exists(solution_path):
    opt_df.to_csv(solution_path)




# 测试代码 main 函数
def main():
    pass

if __name__ == "__main__":
    main()
