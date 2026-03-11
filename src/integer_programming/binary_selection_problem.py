from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.ModelSolver import Constraint, Objective, OptimizationModel, Variable, run_example_model


def build_model() -> OptimizationModel:
    model = OptimizationModel(
        name="binary_selection_problem",
        problem_type="IP",
        description="Select projects with binary choices under a resource budget.",
    )
    model.add_variable(Variable("x1", lb=0, ub=1, vtype="B"))
    model.add_variable(Variable("x2", lb=0, ub=1, vtype="B"))
    model.add_variable(Variable("x3", lb=0, ub=1, vtype="B"))
    model.add_constraint(Constraint("budget", {"x1": 1, "x2": 2, "x3": 3}, "<=", 4))
    model.add_constraint(Constraint("coverage", {"x1": 1, "x2": 1}, ">=", 1))
    model.add_objective(Objective(name="benefit", sense="max", expr={"x1": 1, "x2": 1, "x3": 2}))
    return model


def main(solver_name: str = "gurobi") -> None:
    run_example_model(build_model, solver_name=solver_name)


if __name__ == "__main__":
    main()
