# -*- coding: utf-8 -*-

# ***************************************************
# * File        : simplex_method.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2024-08-26
# * Version     : 0.1.082616
# * Description : 线性规划单纯形法
# * Link        : link
# * Requirement : 相关模块版本需求(例如: numpy >= 2.1.0)
# ***************************************************

# python libraries
import numpy as np
import pandas as pd

# global variable
LOGGING_LABEL = __file__.split('/')[-1][:-3]


# 定义线性规划求解函数
def lp_solver(matrix: pd.DataFrame):
    """
    输入线性规划的矩阵，根据单纯形法求解线性规划模型
    max cx
    s.t. ax <= b

    Args:
        matrix (pd.DataFrame): 
            b      x1    x2    x3   x4   x5
        obj 0.0    70.0  30.0  0.0  0.0  0.0
        x3  540.0  3.0   9.0   1.0  0.0  0.0
        x4  450.0  5.0   5.0   0.0  1.0  0.0
        x5  720.0  9.0   3.0   0.0  0.0  1.0

        - 第 1 行是目标函数的系数
        - 第 2~4 行是约束方程的系数
        - 第 1 列是约束方程的常数项
        - obj-b 交叉，即第 1 行第 1 列的元素是目标函数的负值
        - x3,x4,x5 既是松弛变量，也是初始可行解
    """
    # 检验数是否大于 0
    c = matrix.iloc[0, 1:]
    # TODO
    while c.max() > 0:
        # ------------------------------
        # 选择入基变量 
        # ------------------------------
        # 目标函数系数最大的变量入基
        c = matrix.iloc[0, 1:]
        print(c)
        in_x = c.idxmax()
        print(in_x)
        # in_x_v = c[in_x]  # 入基变量的系数
        # print(in_x_v)
        print("-" *40)
        # ------------------------------
        # 选择出基变量
        # ------------------------------
        # 选择正的最小比值对应的变量出基 min(b列/入基变量列)
        b = matrix.iloc[1:, 0]
        print(b)
        in_x_a = matrix.iloc[1:][in_x]  # 选择入基变量对应的列
        print(in_x_a)
        out_x = (b / in_x_a).idxmin()  # 得到出基变量
        print(out_x)
        # out_x_v = b[out_x]  # 出基变量的系数
        # print(out_x_v)
        print("-" * 40)
        # ------------------------------
        # 旋转操作
        # ------------------------------
        matrix.loc[out_x, :] = matrix.loc[out_x, :] / matrix.loc[out_x, in_x]
        # print(matrix)
        # print("-" * 40)
        for idx in matrix.index: 
            if idx != out_x:
                matrix.loc[idx, :] = matrix.loc[idx, :] - matrix.loc[out_x, :] * matrix.loc[idx, in_x]
        # print(matrix)
        # print("-" * 40)
        # 索引替换（入基与出基变量名称替换）
        matrix_index = matrix.index.tolist()
        i = matrix_index.index(out_x)
        print(matrix_index)
        print(in_x, out_x)
        print(i)
        matrix_index[i] = in_x
        print(matrix_index)
        print("-" * 40)
        matrix.index = matrix_index 
    # 打印结果
    print("最终的最优单纯形法是：")
    print(matrix)
    print(f"目标函数值是：{-matrix.iloc[0, 0]}")
    print("最优决策变量是：")
    x_count = (matrix.shape[1] - 1) - (matrix.shape[0] - 1)
    X = matrix.iloc[0, 1:].index.tolist()[:x_count]
    for xi in X:
        print(f"{xi} = {matrix.loc[xi, 'b']}")




# 测试代码 main 函数
def main():
    # 约束方程系数矩阵，包含常数项
    matrix = pd.DataFrame(
        np.array([
            [0.0, 70.0, 30.0, 0.0, 0.0, 0.0],
            [540.0, 3.0, 9.0, 1.0, 0.0, 0.0],
            [450.0, 5.0, 5.0, 0.0, 1.0, 0.0],
            [720.0, 9.0, 3.0, 0.0, 0.0, 1.0],
        ]),
        index = ["obj", "x3", "x4", "x5"],
        columns = ["b", "x1", "x2", "x3", "x4", "x5"]
    )
    print(matrix)
    print("-" * 40)
    # 调用前面定义的函数求解
    lp_solver(matrix)

if __name__ == "__main__":
    main()
