from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.ModelSolver import Constraint, Objective, OptimizationModel, Variable, run_example_model


def build_model() -> OptimizationModel:
    model = OptimizationModel(
        name="three_variable_linear_problem",
        problem_type="LP",
        description="Solve a three-variable LP with equality and inequality constraints.",
    )
    model.add_variable(Variable("x1", lb=0, vtype="C", step=1.0, search_ub=7))
    model.add_variable(Variable("x2", lb=0, vtype="C", step=1.0, search_ub=7))
    model.add_variable(Variable("x3", lb=0, vtype="C", step=1.0, search_ub=7))
    model.add_constraint(Constraint("balance", {"x1": 1, "x2": 1, "x3": 1}, "==", 7))
    model.add_constraint(Constraint("quality", {"x1": 2, "x2": -5, "x3": 1}, ">=", 10))
    model.add_constraint(Constraint("capacity", {"x1": 1, "x2": 3, "x3": 1}, "<=", 12))
    model.add_objective(Objective("profit", "max", {"x1": 2, "x2": 3, "x3": -5}))
    return model


def main(solver_name: str = "scipy") -> None:
    run_example_model(build_model, solver_name=solver_name)


if __name__ == "__main__":
    main()
