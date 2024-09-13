# -*- coding: utf-8 -*-

# ***************************************************
# * File        : interior_point.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2024-09-13
# * Version     : 0.1.091320
# * Description : 内点法
# * Link        : link
# * Requirement : 相关模块版本需求(例如: numpy >= 2.1.0)
# ***************************************************

# python libraries
import os
import sys
ROOT = os.getcwd()
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
import time
import numpy as np

# global variable
LOGGING_LABEL = __file__.split('/')[-1][:-3]


def gradient(x1, x2, t):
    """
    计算目标函数在 x 处的一阶导数（雅可比矩阵 ）

    Args:
        x1 (_type_): _description_
        x2 (_type_): _description_
        t (_type_): _description_
    """
    j1 = -70*t + 3/(-3*x1 - 9*x2 + 540) \
               + 5/(-5*x1 - 5*x2 + 450) \
               + 9/(-9*x1 - 3*x2 + 720) \
               - 1/x1
    j2 = -30*t + 9/(-3*x1 - 9*x2 + 540) \
               + 5/(-5*x1 - 5*x2 + 450) \
               + 3/(-9*x1 - 3*x2 + 720) \
               - 1/x2

    return np.asmatrix([j1, j2]).T


def hessian(x1, x2):
    """
    计算目标函数在 x 处的二阶导数（黑塞矩阵）

    Args:
        x1 (_type_): _description_
        x2 (_type_): _description_
    """
    x1, x2 = float(x1), float(x2)
    h11 = 9/(3*x1 + x2 - 240)**2 + (x1 + 3*x2 - 180)**(-2) + (x1 + x2 - 90)**(-2) + x1**(-2)
    h12 = 3/(3*x1 + x2 - 240)**2 + 3/(x1 + 3*x2 - 180)**2 + (x1 + x2 - 90)**(-2)
    h21 = 3/(3*x1 + x2 - 240)**2 + 3/(x1 + 3*x2 - 180)**2 + (x1 + x2 - 90)**(-2)
    h22 = (3*x1 + x2 - 240)**(-2) + 9/(x1 + 3*x2 - 180)**2 + (x1 + x2 - 90)**(-2) + x2**(-2)
    
    return np.asmatrix([[h11, h12], [h21, h22]])


def invertible(H):
    """
    求黑塞矩阵的逆矩阵

    Args:
        H (_type_): _description_
    """
    H_inv = np.linalg.inv(H)

    return H_inv


def run():
    # 牛顿法的初始迭代值
    x = np.asmatrix(np.array([10, 10])).T
    # 指数函数中的 t
    t = 0.00001
    # 迭代停止的误差
    eps = 0.01
    # 记录迭代的次数
    iter_cnt = 0
    while iter_cnt < 20:
        iter_cnt += 1
        J = gradient(x[0, 0], x[1, 0], t)
        H = hessian(x[0, 0], x[1, 0])
        H_inv = invertible(H)
        # 牛顿法
        x_new = x - H_inv * J
        # 求二范数，判断迭代效果
        error = np.linalg.norm(x_new - x)
        print(f"迭代次数是：{iter_cnt}, x1={x_new[0, 0]:.2f}, x2={x_new[1, 0]:.2f}, 误差是: {error}")
        x = x_new
        if error < eps:
            break
        time.sleep(1)
    # 打印结果
    print(f"目标函数值是：{70*x[0, 0] + 30*x[1, 0]:.2f}")





# 测试代码 main 函数
def main():
    run()

if __name__ == "__main__":
    main()
