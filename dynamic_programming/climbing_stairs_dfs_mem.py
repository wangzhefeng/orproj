# -*- coding: utf-8 -*-

# ***************************************************
# * File        : climbing_stairs_dfs_mem.py
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
from typing import List

# global variable
LOGGING_LABEL = __file__.split('/')[-1][:-3]


def dfs(i: int, mem: List[int]) -> int:
    """
    记忆化搜索

    Args:
        i (int): 目标楼梯阶数
        mem (List[int]): 记录每个子问题的解

    Returns:
        int: 爬楼梯方案数
    """
    # 已知 dp[1] 和 dp[2]，返回
    if i == 1 or i == 2:
        return i
    # 若存在记录 dp[i]，则直接返回
    if mem[i] != -1:
        return mem[i]
    # dp[i] = dp[i-1] + dp[i-2]
    count = dfs(i - 1, mem) + dfs(i - 2, mem)
    # 记录 dp[i]
    mem[i] = count
    
    return count


def climbing_stairs_dfs_mem(n: int) -> int:
    """
    爬楼梯：记忆化搜索

    Args:
        n (int): 目标楼梯阶数

    Returns:
        int: 爬楼梯方案数
    """
    mem = [-1] * (n + 1)

    return dfs(n, mem)


# 测试代码 main 函数
def main():
    res = climbing_stairs_dfs_mem(3)
    print(res)

if __name__ == "__main__":
    main()
