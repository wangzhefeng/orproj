from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.ModelSolver import Constraint, Objective, OptimizationModel, Variable, run_example_model


def build_model() -> OptimizationModel:
    model = OptimizationModel(
        name="product_mix_problem",
        problem_type="LP",
        description="Choose two products to maximize production profit under capacity limits.",
    )
    model.add_variable(Variable("x_desks", lb=0, vtype="C"))
    model.add_variable(Variable("x_tables", lb=0, vtype="C"))
    model.add_constraint(Constraint("market_limit", {"x_desks": 1}, "<=", 40, "Demand cap for desks."))
    model.add_constraint(Constraint("carpentry", {"x_desks": 1, "x_tables": 1}, "<=", 80, "Carpentry hours."))
    model.add_constraint(Constraint("finishing", {"x_desks": 2, "x_tables": 1}, "<=", 100, "Finishing hours."))
    model.add_objective(Objective(name="profit", sense="max", expr={"x_desks": 40, "x_tables": 30}))
    return model


def main(solver_name: str = "reference") -> None:
    run_example_model(build_model, solver_name=solver_name)


if __name__ == "__main__":
    main()
