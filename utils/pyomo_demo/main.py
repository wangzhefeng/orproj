# -*- coding: utf-8 -*-

# ***************************************************
# * File        : main.py
# * Author      : Zhefeng Wang
# * Email       : zfwang7@gmail.com
# * Date        : 2025-09-27
# * Version     : 1.0.092719
# * Description : description
# * Link        : https://zhuanlan.zhihu.com/p/125179633
# *               https://blog.csdn.net/weixin_42848399/article/details/91654118
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
import warnings
warnings.filterwarnings("ignore")

from pyomo.environ import *

# global variable
LOGGING_LABEL = Path(__file__).name[:-3]
os.environ['LOG_NAME'] = LOGGING_LABEL
from utils.log_util import logger


# ##############################
# 定义模型
# max profit=40x+30y
# subjectto:
# x <= 40
# x + y <= 80
# 2x + y <= 100
# ##############################
# model
model = ConcreteModel()

# decision variables
model.x = Var(domain=NonNegativeReals)  # NonNegativeReals 代表非 0 实数
model.y = Var(domain=NonNegativeReals)

# objective
model.profit = Objective(expr = 40 * model.x + 30 * model.y, sense = maximize)

# constraints
model.demand = Constraint(expr = model.x <= 40)
model.laborA = Constraint(expr = model.x + model.y <= 80)
model.laborB = Constraint(expr = 2 * model.x + model.y <= 100)

model.pprint()

# ##############################
# 求解模型
# ##############################
SolverFactory("glpk", executable="C:\glpk-4.65\w64\glpsol").solve(model).write()

# display solution
logger.info(f"Profit = {model.profit()}")
logger.info(f"Decision Variables:")
logger.info(f"x = {model.x()}")
logger.info(f"y = {model.y()}")
logger.info(f"Constraints:")
logger.info(f"Demand = {model.demand()}")
logger.info(f"Labor A = {model.laborA()}")
logger.info(f"Labor B = {model.laborB()}")




# 测试代码 main 函数
def main():
    pass

if __name__ == "__main__":
    main()
