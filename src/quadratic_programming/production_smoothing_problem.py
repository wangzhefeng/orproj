from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.ModelSolver import Constraint, Objective, OptimizationModel, Variable, run_example_model


def build_model() -> OptimizationModel:
    model = OptimizationModel(
        name="production_smoothing_problem",
        problem_type="MIQP",
        description="Choose two monthly production levels while penalizing deviation from the target output.",
    )
    model.add_variable(Variable("month_1", lb=0, vtype="I", search_ub=8))
    model.add_variable(Variable("month_2", lb=0, vtype="I", search_ub=8))
    model.add_constraint(Constraint("total_demand", {"month_1": 1, "month_2": 1}, "==", 10))
    model.add_constraint(Constraint("capacity_m1", {"month_1": 1}, "<=", 8))
    model.add_constraint(Constraint("capacity_m2", {"month_2": 1}, "<=", 8))
    model.add_objective(Objective(name="smoothing_cost", sense="min", quadratic_expr={("month_1", "month_1"): 1.0, ("month_2", "month_2"): 1.0}, expr={"month_1": -10.0, "month_2": -10.0}, constant=50.0))
    return model


def main(solver_name: str = "scipy") -> None:
    run_example_model(build_model, solver_name=solver_name)


if __name__ == "__main__":
    main()
