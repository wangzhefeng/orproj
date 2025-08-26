# -*- coding: utf-8 -*-

# ***************************************************
# * File        : path_dp.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2024-08-30
# * Version     : 0.1.083016
# * Description : 用动态规划求解最短路径问题
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

import numpy as np
import pandas as pd

# global variable
LOGGING_LABEL = __file__.split('/')[-1][:-3]


def dp(df_from, df_to):
    """
    从 df_from 阶段到 df_to 阶段的动态规划求解

    Args:
        df_from (_type_): _description_
        df_to (_type_): _description_
        start (list, optional): 初始状态. Defaults to [df1].
        cv (List): 存储路径

    Returns:
        _type_: _description_
    """
    from_node = df_to.index
    f = pd.Series()
    g = []
    for j in from_node:
        m1 = df_to.loc[j]
        m2 = m1 + df_from
        m3 = m2.sort_values()
        f[j] = m3[0]
        g.append(m3.index[0])
    
    dc = pd.DataFrame()
    dc["v"] = f.values
    dc["n"] = g
    dc.index = f.index
    cv.append(dc)
    
    if len(start) > 0:
        df = start.pop()
        t = dp(dc["v"], df)
    else:
        return dc


# 测试代码 main 函数
def main():
    # 前后两个阶段的节点距离，使用 pd.DataFrame 存储
    # A->B 距离
    df1 = pd.DataFrame(
        np.array([[10, 20]]),
        index = ["A"],
        columns = ["B1", "B2"],
    )
    # B->C 距离
    df2 = pd.DataFrame(
        np.array([[30, 10], [5, 20]]),
        index = ["B1", "B2"],
        columns = ["C1", "C2"],
    )
    # C->D 距离
    df3 = pd.DataFrame(
        np.array([[20], [10]]),
        index = ["C1", "C2"],
        columns = ["D"],
    )
    
    global start  # 初始状态
    start = [df1]
    global cv  # 存储路径
    cv = []
    t1 = df3["D"]  # 初始状态
    h1 = dp(t1, df2)
    
    # 打印路径
    for m in range(len(cv)):
        xc = cv.pop()
        x1 = xc.sort_values(by = "v")
        print(x1["n"].values[0], end = "->")

if __name__ == "__main__":
    main()
