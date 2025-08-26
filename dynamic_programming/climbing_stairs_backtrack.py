# -*- coding: utf-8 -*-

# ***************************************************
# * File        : main.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2024-08-30
# * Version     : 0.1.083010
# * Description : 回溯算法（深度优先搜索）
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


def backtrack(choices: List[int], state: int, n: int, res: List[int]) -> int:
    """
    回溯

    Args:
        choices (List[int]): 每一步的选择，可以选择每步向上爬的阶数
        state (int): 当前状态，在第几阶
        n (int): 爬到第几层
        res (List[int]): 使用 res[0] 记录方案数量
    """
    # 当爬到第 n 阶时，方案数量加 1
    if state == n:
        res[0] += 1
    # 遍历所有选择
    for choice in choices:
        # 剪枝：不允许越过第 n 阶
        if state + choice > n:
            continue
        # 尝试：做出选择，更新状态
        backtrack(choices, state + choice, n, res)
        # 回退


def climbing_stairs_backtrack(n: int) -> int:
    """
    爬楼梯：回溯

    Args:
        n (int): 爬到第几层

    Returns:
        int: 爬楼梯到第 n 阶的方案数量
    """
    choices = [1, 2]  # 可以选择向上爬 1 阶或 2 阶
    state = 0  # 从第 0 阶开始爬
    res = [0]  # 使用 res[0] 记录方案数量
    backtrack(choices, state, n, res)

    return res[0]




# 测试代码 main 函数
def main():
    res = climbing_stairs_backtrack(10)
    print(res)
    
if __name__ == "__main__":
    main()
