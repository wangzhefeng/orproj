# -*- coding: utf-8 -*-


# ***************************************************
# * File        : Problem.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2023-04-13
# * Version     : 0.1.041301
# * Description : 单目标优化
# * Link        : link
# * Requirement : 相关模块版本需求(例如: numpy >= 2.1.0)
# ***************************************************


# python libraries
import os
import sys

import numpy as np
import geatpy as ea


# global variable
LOGGING_LABEL = __file__.split('/')[-1][:-3]


# ------------------------------
# Problem
# ------------------------------
# 该案例展示了一个带等式约束的连续型决策变量最大化目标的单目标优化问题。
# 该函数存在多个欺骗性很强的局部最优点
# max f = 4*x1 + 2*x2 + x3
# s.t.
#   2*x1 + x2 - 1 <= 0
#   x1 + 2*x3 - 2 <= 0
#   x1 + x2 + x3 - 1 == 0 
#   0 <= x1,x2 <= 1
#   0 < x3 < 2
# ------------------------------


class MyProblem(ea.Problem):

    def __init__(self):
        name = "MyProblem"
        M = 1  # 目标维数
        maxormins = [-1]  # 目标最小、最大化标记列表，1:最小化目标，-1:最大化该目标
        Dim = 3  # 决策变量维数
        varTypes = [0] * Dim  # 决策变量的的类型，元素为 0 表示对应的变量是连续的，1 表示是离散的
        lb = [0, 0, 0]  # 决策变量下界
        ub = [1, 1, 2]  # 决策变量下界
        lbin = [1, 1, 0]  # 是否包含决策变量下边界(0 表示不包含该变量的下边界，1 表示包含)
        ubin = [1, 1, 0]  # 是否包含决策变量上边界(0 表示不包含该变量的上边界，1 表示包含)
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(
            self, name = name, 
            M = M, maxormins = maxormins, 
            Dim = Dim, varTypes = varTypes, 
            lb = lb, ub = ub, lbin = lbin, ubin = ubin
        )
    
    def aimFunc(self, pop):
        """
        目标函数
        """
        # 得到决策变量矩阵
        Vars = pop.Phen
        x1 = Vars[:, [0]]  # 取出第一列得到所有个体组成的列向量
        x2 = Vars[:, [1]]  # 取出第二列得到所有个体组成的列向量
        x3 = Vars[:, [2]]  # 取出第三列得到所有个体组成的列向量
        # 计算目标函数值
        pop.ObjV = 4 * x1 + 2 * x2 + x3
        # 采用可行性法则处理约束
        pop.CV = np.hstack([
            2 * x1 + x2 - 1, 
            x1 + 2 * x3 - 2, 
            np.abs(x1 + x2 + x3 - 1)
        ])
    
    def calReferObjV(self):
        """
        设定目标数参考值
        本问题目标函数参考值设定为理论最优值,这个函数其实可以不要
        """
        referenceObjV = np.array([[2.5]])
        return referenceObjV




# 测试代码 main 函数
def main():
    pass

if __name__ == "__main__":
    main()
