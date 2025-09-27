# -*- coding: utf-8 -*-

# ***************************************************
# * File        : network_flow.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2024-09-02
# * Version     : 0.1.090220
# * Description : 在这个网络流的例子中，有两个城市（底特律和丹佛）生产了两种商品（铅笔和钢笔），
# *               必须装运到三个城市的仓库（波士顿、纽约、西雅图），以满足给定的需求。
# *               网络中每一条弧都有其总容量和成本。
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


# ------------------------------
# 两种商品
# ------------------------------ 
commodities = ["Pencils", "Pens"]
print(f"commodities:\n {commodities}")
# ------------------------------
# 两个产地、三个目的地
# ------------------------------ 
nodes = [
    "Detroit",
    "Denver",
    "Boston",
    "New York",
    "Seattle",
]
print(f"nodes:\n {nodes}")

# ------------------------------
# 网络中每条弧的容量(multidict)
# ------------------------------ 
arcs, capacity = grb.multidict({
    ("Detroit", "Boston"): 100,
    ("Detroit", "New York"): 80,
    ("Detroit", "Seattle"): 120,
    ("Denver", "Boston"): 120,
    ("Denver", "New York"): 120,
    ("Denver", "Seattle"): 120,
})
print(f"arcs:\n {arcs}")
print(f"capacity:\n {capacity}")

# ------------------------------
# 商品在不同弧上的运输成本(tupledict)
# ------------------------------ 
cost = {
    ("Pencils", "Detroit", "Boston"): 10,
    ("Pencils", "Detroit", "New York"): 20,
    ("Pencils", "Detroit", "Seattle"): 60,
    ("Pencils", "Denver", "Boston"): 40,
    ("Pencils", "Denver", "New York"): 40,
    ("Pencils", "Denver", "Seattle"): 30,
    ("Pens", "Detroit", "Boston"): 20,
    ("Pens", "Detroit", "New York"): 20,
    ("Pens", "Detroit", "Seattle"): 80,
    ("Pens", "Denver", "Boston"): 60,
    ("Pens", "Denver", "New York"): 70,
    ("Pens", "Denver", "Seattle"): 30,
}
print(f"cost:\n {cost}")

# ------------------------------
# 商品在不同节点的流入量、流出量（需求量），
# 正数表示产地，负数表示需求量(tupledict)
# ------------------------------ 
inflow = {
    ("Pencils", "Detroit"): 50,
    ("Pencils", "Denver"): 60,
    ("Pencils", "Boston"): -50,
    ("Pencils", "New York"): -50,
    ("Pencils", "Seattle"): -10,
    ("Pens", "Detroit"): 60,
    ("Pens", "Denver"): 40,
    ("Pens", "Boston"): -40,
    ("Pens", "New York"): -30,
    ("Pens", "Seattle"): -30,
}
print(f"inflow:\n {inflow}")

# ------------------------------
# 创建模型
# ------------------------------ 
m = grb.Model("netflow")

# ------------------------------
# 创建变量(tupledict) 
# ------------------------------
flow = m.addVars(commodities, arcs, obj = cost, name = "flow")
print(f"flow:\n {flow}\n")

# ------------------------------
# 添加约束
# ------------------------------ 
# 添加容量约束，capacity[i, j] 表示 i->j 的弧的容量，i 是产地，j 是目的地
m.addConstrs(
    (
        flow.sum("*", i, j) <= capacity[i, j] 
        for i, j in arcs
    ), 
    name = "cap"
)
# 添加节点流入=流出的约束
m.addConstrs(
    (
        flow.sum(h, "*", j) + inflow[h, j] == flow.sum(h, j, "*") 
        for h in commodities for j in nodes
    ), 
    name = "node"
)

# ------------------------------
# 求解模型
# ------------------------------ 
m.optimize()

# ------------------------------
# 输出结果
# ------------------------------ 
if m.status == grb.GRB.Status.OPTIMAL:
    solution = m.getAttr("x", flow)
    for h in commodities:
        print(f"\nOptimal flows for {h}")
        for i, j in arcs:
            if solution[h, i, j] > 0:
                print(f"{i} -> {j}: {solution[h, i, j]}")




# 测试代码 main 函数
def main():
    pass

if __name__ == "__main__":
    main()
