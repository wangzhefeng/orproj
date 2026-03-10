from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.ModelSolver import Constraint, Objective, OptimizationModel, Variable, run_example_model


def build_model() -> OptimizationModel:
    model = OptimizationModel(
        name="resource_allocation_problem",
        problem_type="LP",
        description="Allocate continuous activity levels to minimize total cost under resource consumption limits.",
    )
    model.add_variable(Variable("x_1_1", lb=2, ub=6, vtype="C", step=1.0))
    model.add_variable(Variable("x_2_1", lb=0, ub=5, vtype="C", step=1.0))
    model.add_variable(Variable("x_3_1", lb=1, ub=4, vtype="C", step=1.0))
    model.add_variable(Variable("x_1_2", lb=1, ub=5, vtype="C", step=1.0))
    model.add_constraint(Constraint("capacity_1", {"x_1_1": 2, "x_2_1": 1, "x_3_1": 3, "x_1_2": 2}, "<=", 20))
    model.add_constraint(Constraint("capacity_2", {"x_1_1": 1, "x_2_1": 2, "x_3_1": 1, "x_1_2": 2}, "<=", 18))
    model.add_objective(Objective(name="cost", sense="min", expr={"x_1_1": 3, "x_2_1": 2, "x_3_1": 4, "x_1_2": 5}))
    return model


def main(solver_name: str = "docplex") -> None:
    run_example_model(build_model, solver_name=solver_name)


if __name__ == "__main__":
    main()
