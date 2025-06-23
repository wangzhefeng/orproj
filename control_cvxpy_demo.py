# -*- coding: utf-8 -*-

# ***************************************************
# * File        : control_cvxpy_demo.py
# * Author      : Zhefeng Wang
# * Email       : zfwang7@gmail.com
# * Date        : 2025-06-20
# * Version     : 1.0.062015
# * Description : description
# * Link        : https://www.cvxgrp.org/cvx_short_course/docs/intro/notebooks/control.html
# * Requirement : 相关模块版本需求(例如: numpy >= 2.1.0)
# ***************************************************

__all__ = []

# python libraries
import os
import sys
ROOT = str(os.getcwd())
if ROOT not in sys.path:
    sys.path.append(ROOT)
import warnings
warnings.filterwarnings("ignore")
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import cvxpy as cp

# global variable
LOGGING_LABEL = Path(__file__).name[:-3]
os.environ['LOG_NAME'] = LOGGING_LABEL

from utils.log_util import logger


# data
np.random.seed(1)
n = 8  # 状态数
m = 2  # 动作数
T = 50  # 时间步长
alpha = 0.2
beta = 3
A = np.eye(n) - alpha * np.random.rand(n, n)  # 状态矩阵
B = np.random.randn(n, m)  # 动作矩阵
x_0 = beta * np.random.randn(n)  # 状态随机初始化

# 优化变量
x = cp.Variable((n, T + 1))
u = cp.Variable((m, T))

# 目标函数(总成本)
cost = 0
# 约束条件
constr = []
for t in range(T):
    cost += cp.sum_squares(x[:, t + 1]) + cp.sum_squares(u[:, t])
    constr += [
        x[:, t + 1] == A @ x[:, t] + B @ u[:, t], 
        cp.norm(u[:, t], "inf") <= 1
    ]
constr += [
    x[:, T] == 0, 
    x[:, 0] == x_0
]

# 优化问题
problem = cp.Problem(cp.Minimize(cost), constr)

# 优化问题求解
optim_objective = problem.solve()
optim_x = x.value
optim_u = u.value
optim_lagr_multip = constr[0].dual_value
logger.info(f"optim_objective: {optim_objective}")
logger.info(f"optim_x: \n{optim_x}")
logger.info(f"optim_u: \n{optim_u}")
logger.info(f"optim_lagr_multip: \n{optim_lagr_multip}")



f = plt.figure()

# Plot (u_t)_1.
ax = f.add_subplot(411)
plt.plot(u[0, :].value)
plt.ylabel(r"$(u_t)_1$", fontsize=16)
plt.yticks(np.linspace(-1.0, 1.0, 3))
plt.xticks([])

# Plot (u_t)_2.
plt.subplot(4, 1, 2)
plt.plot(u[1, :].value)
plt.ylabel(r"$(u_t)_2$", fontsize=16)
plt.yticks(np.linspace(-1, 1, 3))
plt.xticks([])

# Plot (x_t)_1.
plt.subplot(4, 1, 3)
x1 = x[0, :].value
plt.plot(x1)
plt.ylabel(r"$(x_t)_1$", fontsize=16)
plt.yticks([-10, 0, 10])
plt.ylim([-10, 10])
plt.xticks([])

# Plot (x_t)_2.
plt.subplot(4, 1, 4)
x2 = x[1, :].value
plt.plot(range(51), x2)
plt.yticks([-25, 0, 25])
plt.ylim([-25, 25])
plt.ylabel(r"$(x_t)_2$", fontsize=16)
plt.xlabel(r"$t$", fontsize=16)
plt.tight_layout()
plt.show()



# 测试代码 main 函数
def main():
    pass

if __name__ == "__main__":
    main()
