# -*- coding: utf-8 -*-

# ***************************************************
# * File        : ols_cvxpy_demo.py
# * Author      : Zhefeng Wang
# * Email       : zfwang7@gmail.com
# * Date        : 2025-06-20
# * Version     : 1.0.062013
# * Description : description
# * Link        : link
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


# Problem data
m = 30
n = 20
np.random.seed(1)
A = np.random.randn(m, n)
b = np.random.randn(m)
logger.info(f"A: \n{A}")
logger.info(f"b: \n{b}")

# Construct the problem
# 决策变量
x = cp.Variable(n)
# 目标函数
objective = cp.Minimize(cp.sum_squares(A @ x - b))
# 约束条件
constraints = [0 <= x, x <= 1]
# 优化问题
prob = cp.Problem(objective, constraints)
# 优化问题求解
optim_objective = prob.solve()
optim_x = x.value
optim_lagr_multip = constraints[0].dual_value
logger.info(f"optim_objective: {optim_objective}")
logger.info(f"optim_x: \n{optim_x}")
logger.info(f"optim_lagr_multip: \n{optim_lagr_multip}")




# 测试代码 main 函数
def main():
    pass

if __name__ == "__main__":
    main()
