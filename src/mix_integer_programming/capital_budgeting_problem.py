from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.ModelSolver import Constraint, Objective, OptimizationModel, Variable, run_example_model


def build_model() -> OptimizationModel:
    model = OptimizationModel(
        name="capital_budgeting_problem",
        problem_type="MIP",
        description="Allocate capital among two production lines using integer decisions.",
    )
    model.add_variable(Variable("x1", lb=0, vtype="I", search_ub=6))
    model.add_variable(Variable("x2", lb=0, vtype="I", search_ub=6))
    model.add_constraint(Constraint("machine_hours", {"x1": 2, "x2": 3}, "<=", 14))
    model.add_constraint(Constraint("labor_hours", {"x1": 4, "x2": 2}, "<=", 18))
    model.add_constraint(Constraint("x1_nonnegative", {"x1": 1}, ">=", 0))
    model.add_constraint(Constraint("x2_nonnegative", {"x2": 1}, ">=", 0))
    model.add_objective(Objective(name="profit", sense="max", expr={"x1": 3, "x2": 2}))
    return model


def main(solver_name: str = "gurobi") -> None:
    run_example_model(build_model, solver_name=solver_name)


if __name__ == "__main__":
    main()
