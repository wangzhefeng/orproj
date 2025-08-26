# -*- coding: utf-8 -*-

# ***************************************************
# * File        : bag_dp.py
# * Author      : Zhefeng Wang
# * Email       : zfwang7@gmail.com
# * Date        : 2024-09-19
# * Version     : 1.0.091916
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

# global variable
LOGGING_LABEL = __file__.split('/')[-1][:-3]


def dp(weight, count, weights, costs):
    """
    动态规划求解 0-1 背包问题

    Args:
        weight (_type_): _description_
        count (_type_): _description_
        weights (_type_): _description_
        costs (_type_): _description_
    """
    preline, curline = [0] * (weight + 1), [0] * (weight + 1)
    for i in range(count):
        for j in range(weight + 1):
            if weights[i] <= j:
                curline[j] = max(preline[j], costs[i] + preline[j - weights[i]])
        preline = curline[:]
        
    return curline[weight]



# 测试代码 main 函数
def main():
    count = 5  # 物品数量
    weight = 10  # 背包总重量
    costs = [6, 3, 5, 4, 6]  # 每件物品的价值
    weights = [2, 2, 6, 5, 4]  # 每件物品的重量
    print(dp(weight, count, weights, costs))

if __name__ == "__main__":
    main()
