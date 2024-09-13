# -*- coding: utf-8 -*-

# ***************************************************
# * File        : lp_ortools.py
# * Author      : Zhefeng Wang
# * Email       : wangzhefengr@163.com
# * Date        : 2024-09-02
# * Version     : 0.1.090214
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

# 1. 导入所需的库
from ortools.init.python import init
from ortools.linear_solver import pywraplp

# global variable
LOGGING_LABEL = __file__.split('/')[-1][:-3]


def get_solver():
    """
    声明求解器: GLOP
    """
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        print("Could not create solver GLOP")
        return

    return solver


def get_vars(solver):
    """
    创建变量
    """
    # create 0<=x1<=1, 0<=x2<=2
    x1_var = solver.NumVar(0, 1, "x1")
    x2_var = solver.NumVar(0, 2, "x2")
    print(f"Number of variables = {solver.NumVariables()}")

    return solver, x1_var, x2_var


def get_constraint(solver, x1_var, x2_var):
    """
    定义约束条件
    """
    infinity = solver.infinity()
    # create a linear constraint: x1 + x2 <= 2
    constraint = solver.Constraint(-infinity, 2, "ct")
    constraint.SetCoefficient(x1_var, 1)
    constraint.SetCoefficient(x2_var, 1)
    print(f"Number of constraints = {solver.NumConstraints()}")

    return solver


def get_objective(solver, x1_var, x2_var):
    """
    定义目标函数
    """ 
    objective = solver.Objective()
    # create the objective function: 3x1 + x2
    objective.SetCoefficient(x1_var, 3)
    objective.SetCoefficient(x2_var, 1)
    objective.SetMaximization()

    return solver, objective


def solve_problem(solver):
    """
    调用求解器
    """ 
    print(f"Solving with {solver.SolverVersion()}")
    result_status = solver.Solve()
    print(f"Status: {result_status}")
    if result_status != pywraplp.Solver.OPTIMAL:
        print("The problem does not have an optimal solution!")
        if result_status == pywraplp.Solver.FEASIBLE:
            print("A potential suboptimal solution was found.")
        else:
            print("The solver could not solve the problem.")
            return
    
    return solver


def print_res(solver, objective, x1_var, x2_var):
    """
    显示结果
    """ 
    print("-" * 20)
    print("Solution:")
    print("-" * 20)
    print(f"Objective value = {objective.Value()}")
    print(f"x1 = {x1_var.solution_value()}")
    print(f"x2 = {x2_var.solution_value()}")
    print("-" * 20)
    print("Advanced usage:")
    print("-" * 20)
    print(f"Problem solved in {solver.wall_time():d} milliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")


# 测试代码 main 函数
def main():
    # init.CppBridge.init_logging("basic_example.py")
    # cpp_flags = init.CppFlags()
    # cpp_flags.stderrthreshold = True
    # cpp_flags.log_prefix = False
    # init.CppBridge.set_flags(cpp_flags)

    print(f"Google OR-Tools version: {init.OrToolsVersion.version_string()}")
    # 声明求解器: GLOP 后端
    solver = get_solver()
    # 创建变量    
    solver, x1_var, x2_var = get_vars(solver)
    # 定义约束条件
    solver = get_constraint(solver, x1_var, x2_var)
    # 定义目标函数 
    solver, objective = get_objective(solver, x1_var, x2_var)
    # 调用求解器 
    solver = solve_problem(solver)
    # 显示结果
    print_res(solver, objective, x1_var, x2_var)

if __name__ == "__main__":
    main()
