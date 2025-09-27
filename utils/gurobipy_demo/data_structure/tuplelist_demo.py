# -*- coding: utf-8 -*-

# ***************************************************
# * File        : tuplelist_demo.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2024-10-10
# * Version     : 0.1.101011
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

import gurobipy as grb

# global variable
LOGGING_LABEL = __file__.split('/')[-1][:-3]


t1 = grb.tuplelist([
    (1, 2),
    (1, 3),
    (2, 3),
    (2, 5),
])
print(t1)

# 输出第一个值是 1 的元素
print(t1.select(1, "*"))

# 输出第二个值是 3 的元素
print(t1.select("*", 3))

# 添加一个元素
t1.append((3, 5))
print(t1.select(3, "*"))

# 使用迭代的方式实现 select 功能
print(t1.select(1, "*"))




# 测试代码 main 函数
def main():
    pass

if __name__ == "__main__":
    main()
