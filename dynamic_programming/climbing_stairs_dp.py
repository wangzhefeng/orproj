# -*- coding: utf-8 -*-

# ***************************************************
# * File        : climbing_stairs_dp.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2024-08-30
# * Version     : 0.1.083015
# * Description : description
# * Link        : link
# * Requirement : 相关模块版本需求(例如: numpy >= 2.1.0)
# ***************************************************

# python libraries
import os
import sys
ROOT = os.getcwd()
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

# global variable
LOGGING_LABEL = __file__.split('/')[-1][:-3]


def climbing_stairs_dp(n: int) -> int:
    """
    爬楼梯：动态规划

    Args:
        n (int): 目标楼梯阶数

    Returns:
        int: 爬楼梯方案数
    """
    if n == 1 or n == 2:
        return n
    # 初始化 dp 表，用于存储子问题的解
    dp = [0] * (n + 1)
    # 初始状态：预设最小子问题的解
    dp[1], dp[2] = 1, 2
    # 状态转移：从较小子问题逐步求解较大子问题
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]


def climbing_stairs_dp_comp(n: int) -> int:
    """
    爬楼梯：空间优化后的动态规划

    Args:
        n (int): _description_

    Returns:
        int: _description_
    """
    if n == 1 or n == 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    
    return b


# 测试代码 main 函数
def main():
    res = climbing_stairs_dp(3)
    print(res)

if __name__ == "__main__":
    main()
