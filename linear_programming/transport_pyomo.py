# -*- coding: utf-8 -*-

# ***************************************************
# * File        : transport_pyomo.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2024-10-10
# * Version     : 0.1.101017
# * Description : pyomo 实现运输问题
# * Link        : link
# * Requirement : 相关模块版本需求(例如: numpy >= 2.1.0)
# ***************************************************

# python libraries
import os
import sys
ROOT = os.getcwd()
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from pyomo.environ import (
    ConcreteModel,
    Set, Param,
    Var,
    Constraint,
    Objective,
    minimize,
)

# global variable
LOGGING_LABEL = __file__.split('/')[-1][:-3]


# ------------------------------
# 定义参数
# ------------------------------
# model
model = ConcreteModel()

# 定义生产地和销售地
model.i = Set(initialize = ["seattle", "san-diego"], doc = "Canning plans")
model.j = Set(initialize = ["new-york", "chicago", "topeka"], doc = "Markets")

# 定义生产地的生产量和销售地的需求量
model.a = Param(model.i, initialize = {"seattle": 350, "san-diego": 600}, doc = "Capacity of plant i in cases")
model.b = Param(model.j, initialize = {"new-york": 325, "chicago": 300, "topeka": 275}, doc = "Demand at market j in cases")

# 定义生产地到销售地的距离(千英里)
dtab = {
    ("seattle", "new-york"): 2.5,
    ("seattle", "chicago"): 1.7,
    ("seattle", "topeka"): 1.8,
    ("san-diego", "new-york"): 2.5,
    ("san-diego", "chicago"): 1.8,
    ("san-diego", "topeka"): 1.4,
}
model.d = Param(model.i, model.j, initialize = dtab, doc = "Distance in thousands of miles")

# 费用/千英里
model.f = Param(initialize = 90, doc = "Freight in dollars per case per thousand miles")

# cij 就是产地 i 到销售地 j 的单位运价
def c_init(model, i, j):
    return model.f * model.d[i, j] / 1000
model.c = Param(model.i, model.j, initialize = c_init, doc = "Transport cost in thousands of dollar per case")

# ------------------------------
# 定义变量
# ------------------------------
model.x = Var(model.i, model.j, bounds = (0.0, None), doc = "Shipment quantities in case")

# ------------------------------
# 约束条件
# ------------------------------
def supply_rule(model, i):
    return sum(model.x[i, j] for j in model.j) <= model.a[i]
model.supply = Constraint(model.i, rule = supply_rule, doc = "Observe supply limit at plant i")

def demand_rule(model, j):
    return sum(model.x[i, j] for i in model.i) >= model.b[j]
model.demand = Constraint(model.j, rule = demand_rule, doc = "Satisfy demand at market j")

# ------------------------------
# 目标函数
# ------------------------------
def objective_rule(model):
    return sum(
        model.c[i, j] * model.x[i, j] 
        for i in model.i 
        for j in model.j
    )
model.objective = Objective(rule = objective_rule, sense = minimize, doc = "Define objective function")

# ------------------------------
# 模型求解
# ------------------------------
def pyomo_postprocess(options = None, instance = None, results = None):
    model.x.display()




# 测试代码 main 函数
def main():
    from pyomo.opt import SolverFactory
    import pyomo.environ
    opt = SolverFactory("glpk")
    results = opt.solve(model)

    # sends results to stdout
    results.write()
    print("\nDisplaying Solution\n" + "-" * 60)
    pyomo_postprocess(None, model, results)

if __name__ == "__main__":
    main()
