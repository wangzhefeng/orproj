# -*- coding: utf-8 -*-

# ***************************************************
# * File        : data.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2023-07-29
# * Version     : 0.1.072911
# * Description : description
# * Link        : link
# * Requirement : 相关模块版本需求(例如: numpy >= 2.1.0)
# ***************************************************

import gurobipy as grb

# global variable
LOGGING_LABEL = __file__.split('/')[-1][:-3]


# ------------------------------
# multidict 
# ------------------------------
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


# ------------------------------
# tuplelist
# ------------------------------
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
