# -*- coding: utf-8 -*-

# ***************************************************
# * File        : main.py
# * Author      : Zhefeng Wang
# * Email       : zfwang7@gmail.com
# * Date        : 2025-09-27
# * Version     : 1.0.092719
# * Description : description
# * Link        : https://zhuanlan.zhihu.com/p/124422566
# * Requirement : 相关模块版本需求(例如: numpy >= 2.1.0)
# ***************************************************

__all__ = []

# python libraries
import os
import sys
from pathlib import Path
ROOT = str(Path.cwd())
if ROOT not in sys.path:
    sys.path.append(ROOT)
import random
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import docplex.mp.model as cpx

# global variable
LOGGING_LABEL = Path(__file__).name[:-3]
os.environ['LOG_NAME'] = LOGGING_LABEL
from utils.log_util import logger


# ##############################
# 定义问题
# min sum_{i=1}^{n}sum_{j=1}^{m}(c_{ij}x_{ij})
# s.t.
# sum_{i=1}^{n}a_{ij}x_{ij} <= b_{j}, \forall j
# x_{ij} >= l_{ij}, \forall i, j
# x_{ij} <= u_{ij}, \forall i, j
# ##############################
# parameters
n = 10
m = 5
set_I = range(1, n+1)
set_J = range(1, m+1)
c = {(i, j): random.normalvariate(0, 1) for i in set_I for j in set_J}
a = {(i, j): random.normalvariate(0, 5) for i in set_I for j in set_J}
l = {(i, j): random.randint(0, 10)      for i in set_I for j in set_J}
u = {(i, j): random.randint(10, 20)     for i in set_I for j in set_J}
b = {j:      random.randint(0, 30)      for j in set_J}
logger.info(f"set_I: {set_I}")
logger.info(f"set_J: {set_J}")
logger.info(f"c: {c}")
logger.info(f"a: {a}")
logger.info(f"l: {l}")
logger.info(f"u: {u}")
logger.info(f"b: {b}")

# ##############################
# model
# ##############################
# model
opt_model = cpx.Model(name="MIP Model")

# ##############################
# 决策变量
# ##############################
# if x is continuous
x_vars = {
    (i, j): opt_model.continuous_var(lb=l[i,j], ub=u[i,j], name=f"x_{i}_{j}")
    for i in set_I for j in set_J
}
# if x is binary
# x_vars = {
#     (i, j): opt_model.binary_var(name=f"x_{i}_{j}")
#     for i in set_I for j in set_J
# }
# if x is integer
# x_vars= {
#     (i, j): opt_model.integer_var(lb=l[i, j], ub=u[i, j], name=f"x_{i}_{j}")
#     for i in set_I for j in set_J
# }
logger.info(f"x_vars: \n{x_vars}")

# ##############################
# 约束条件
# ##############################
# <= constraints, 小于等于
constraints = {
    j: opt_model.add_constraint(
        ct=opt_model.sum(a[i, j] * x_vars[i, j] for i in set_I) <= b[j], 
        ctname=f"constraint_{j}"
    ) for j in set_J
}
# >= constraints, 大于等于
# constraints = {
#     j: opt_model.add_constraint(
#         ct=opt_model.sum(a[i, j] * x_vars[i, j] for i in set_I) >= b[j], 
#         ctname=f"constraint_{j}"
#     ) for j in set_J
# }
# == constraints, 等于
# constraints = {
#     j: opt_model.add_constraint(
#         ct=opt_model.sum(a[i, j] * x_vars[i, j] for i in set_I) == b[j], 
#         ctname=f"constraint_{j}"
#     ) for j in set_J
# }
logger.info(f"constraints: \n{constraints}")

# ##############################
# 目标函数
# ##############################
objective = opt_model.sum(
    x_vars[i, j] * c[i, j] 
    for i in set_I 
    for j in set_J
)
# for maximization
opt_model.maximize(objective)
# for minimization
# opt_model.minimize(objective)

# ##############################
# 模型求解
# ##############################
# solving with local cplex
opt_model.solve()

# solving with cplex cloud
# opt_model.solve(url="your_cplex_cloud_url", key="your_api_key")

# ##############################
# 模型求解
# ##############################
opt_df = pd.DataFrame.from_dict(
    x_vars, 
    orient="index", 
    columns = ["variable_object"]
)
opt_df.index = pd.MultiIndex.from_tuples(
    opt_df.index, 
    names=["column_i", "column_j"]
)
opt_df.reset_index(inplace=True)
logger.info(f"opt_df: \n{opt_df}")

# CPLEX
opt_df["solution_value"] = opt_df["variable_object"].apply(lambda item: item.solution_value)
opt_df.drop(columns=["variable_object"], inplace=True)
opt_df.to_csv("./results/cplex_demo/optimization_solution.csv")




# 测试代码 main 函数
def main():
    pass

if __name__ == "__main__":
    main()
