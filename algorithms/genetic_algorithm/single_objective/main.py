# -*- coding: utf-8 -*-

# ***************************************************
# * File        : main.py
# * Author      : Zhefeng Wang
# * Email       : zfwang7@gmail.com
# * Date        : 2024-10-01
# * Version     : 1.0.100117
# * Description : description
# * Link        : link
# * Requirement : 相关模块版本需求(例如: numpy >= 2.1.0)
# * TODO        : 1.
# ***************************************************

__all__ = []

# python libraries
import os
import sys
ROOT = os.getcwd()
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import geatpy as ea

from MyProblem import MyProblem

# global variable
LOGGING_LABEL = __file__.split('/')[-1][:-3]


# 实例化问题对象
problem = MyProblem()

# 种群设置
Encoding = 'RI'  # 编码方式

population = ea.Population(
    Encoding = "RI",  # 编码方式
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders), # 创建区域描述器
    NIND = 100,  # 种群规模
) # 实例化种群对象(此时种群还没被初始化，仅仅是完成种群对象的实例化)

# 算法参数设置
myAlgorithm = ea.soea_DE_rand_1_L_templet(
    problem = problem, 
    population = population,
)  # 实例化一个算法模板对象
myAlgorithm.MAXGEN = 300  # 最大进化代数
myAlgorithm.mutOper.F = 0.5  # 差分进化中的参数 F
myAlgorithm.recOper.XOVR = 0.7  # 重组概率

# 调用算法模板进行种群进化
res = ea.optimize(
    myAlgorithm,
    verbose = True,
    drawing = 1,
    outputMsg = True,
    drawLog = False,
    saveFlag = True,
)
print(res)




# 测试代码 main 函数
def main():
    pass

if __name__ == "__main__":
    main()
