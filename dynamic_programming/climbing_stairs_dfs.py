# -*- coding: utf-8 -*-

# ***************************************************
# * File        : climbing_stairs_dfs.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2024-08-30
# * Version     : 0.1.083011
# * Description : 暴力搜索（深度优先搜索）
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


def dfs(i: int) -> int:
    """
    搜索

    Args:
        i (int): 目标楼梯阶数

    Returns:
        int: 爬楼梯方案数
    """
    # 已知 dp[1] 和 dp[2]，返回
    if i == 1 or i == 2:
        return i
    # dp[i] = dp[i-1] + dp[i-2]
    count = dfs(i - 1) + dfs(i - 2)

    return count


def climbing_stairs_dfs(n: int) -> int:
    """
    爬楼梯：搜索

    Args:
        n (int): 目标楼梯阶数

    Returns:
        int: 爬楼梯方案数
    """
    return dfs(n)




# 测试代码 main 函数
def main():
    res = climbing_stairs_dfs(10)
    print(res)

if __name__ == "__main__":
    main()
