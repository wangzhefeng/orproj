# -*- coding: utf-8 -*-

# ***************************************************
# * File        : multidict_demo.py
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


student, chinese, math, english = grb.multidict({
    "student1": [1, 2, 3],
    "student2": [2, 3, 4],
    "student3": [3, 4, 5],
    "student4": [4, 5, 6],
})
# 字典的键
print(student)
# 语文成绩的字典
print(chinese)
# 数学成绩的字典
print(math)
# 英语成绩的字典
print(english)




# 测试代码 main 函数
def main():
    pass

if __name__ == "__main__":
    main()
