# -*- coding: utf-8 -*-


# ***************************************************
# * File        : linear_programming_demo.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2023-04-13
# * Version     : 0.1.041300
# * Description : description
# * Link        : link
# * Requirement : 相关模块版本需求(例如: numpy >= 2.1.0)
# ***************************************************

# python libraries
import numpy as np
from scipy import optimize as op

# global variable
LOGGING_LABEL = __file__.split('/')[-1][:-3]


'''
线性规划

问题：
    max z = 2x1 + 3x2 - 5x3
    s.t. x1 + x2 + x3 = 7
         2x1 - 5x2 + x3 >= 10
         x1 + 3x2 + x3 <= 12
         x1, x2, x3 >= 0

API：
    scipy.optimize.linprog(
        c, 
        A_ub = None, 
        b_ub = None, 
        A_eq = None, 
        b_eq = None, 
        bounds = None, 
        method = 'simplex', 
        callback = None, 
        options = None
    )

参数：
    * c 函数系数数组, 最大化参数为c, 最小化为-c, 函数默认计算最小化. 
    * A_ub 不等式未知量的系数, 默认转成 <= , 如果原式是 >= 系数乘负号. 
    * B_ub 对应A_ub不等式的右边结果
    * A_eq 等式的未知量的系数
    * B_eq 等式的右边结果
    * bounds 每个未知量的范围
'''


# 目标函数
c = np.array([2, 3, -5])

A_ub = np.array([[-2, 5, -1], [1, 3, 1]])
B_ub = np.array([-10, 12])
A_eq = np.array([[1, 1, 1]])
B_eq = np.array([7])
x1 = (0, 7)
x2 = (0, 7)
x3 = (0, 7)
res = op.linprog(-c, A_ub, B_ub, A_eq, B_eq, bounds = (x1, x2, x3))
print(res)




# 测试代码 main 函数
def main():
    pass

if __name__ == "__main__":
    main()
