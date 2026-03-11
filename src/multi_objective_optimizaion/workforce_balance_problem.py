from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.ModelSolver import Constraint, Objective, OptimizationModel, Variable, run_example_model


def build_model() -> OptimizationModel:
    model = OptimizationModel(
        name="workforce_balance_problem",
        problem_type="MOIP",
        description="Trade off operating profit and overtime use in a weekly production plan.",
    )
    model.add_variable(Variable("regular_units", lb=0, vtype="I", search_ub=40))
    model.add_variable(Variable("overtime_units", lb=0, vtype="I", search_ub=20))
    model.add_constraint(Constraint("demand", {"regular_units": 1, "overtime_units": 1}, ">=", 30))
    model.add_constraint(Constraint("regular_capacity", {"regular_units": 1}, "<=", 40))
    model.add_constraint(Constraint("overtime_capacity", {"overtime_units": 1}, "<=", 20))
    model.add_objective(Objective("profit", "max", {"regular_units": 8, "overtime_units": 6}, weight=0.7))
    model.add_objective(Objective("overtime_penalty", "min", {"overtime_units": 1}, weight=0.3))
    return model


def main(solver_name: str = "reference") -> None:
    run_example_model(build_model, solver_name=solver_name)


if __name__ == "__main__":
    main()
