# -*- coding: utf-8 -*-


# ***************************************************
# * File        : main.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2023-04-13
# * Version     : 0.1.041307
# * Description : description
# * Link        : link
# * Requirement : 相关模块版本需求(例如: numpy >= 2.1.0)
# ***************************************************


# python libraries
import os
import sys

import numpy as np
import geatpy as ea
from Myproblem import MyProblem


# global variable
LOGGING_LABEL = __file__.split('/')[-1][:-3]


# 实例化问题对象
problem = MyProblem()

# 种群设置
Encoding = 'RI'  # 编码方式
NIND = 100  # 种群规模
Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
population = ea.Population(Encoding, Field, NIND)  # 实例化种群对象

# 算法参数设置
myAlgorithm = ea.soea_DE_rand_1_L_templet(problem, population)  # 实例化一个算法模板对象
myAlgorithm.MAXGEN = 500  # 最大进化代数
myAlgorithm.mutOper.F = 0.5  # 差分进化中的参数F
myAlgorithm.recOper.XOVR = 0.7  # 重组概率

# 调用算法模板进行种群进化
res = ea.optimize(
    algorithm = myAlgorithm,
    verbose = True,
    drawing = True,
    outputMsg = True,
    drawLog = True,
    saveFlag = True,
    dirName = "./models/",
)
print(res)




# 测试代码 main 函数
def main():
    pass

if __name__ == "__main__":
    main()
