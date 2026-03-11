from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.ModelSolver import Constraint, Objective, OptimizationModel, Variable, run_example_model


def build_model() -> OptimizationModel:
    model = OptimizationModel(
        name="infeasibility_analysis_problem",
        problem_type="LP",
        description="An intentionally infeasible LP used to demonstrate model diagnostics.",
    )
    model.add_variable(Variable("x", lb=0, vtype="C", step=1.0, search_ub=10))
    model.add_variable(Variable("y", lb=0, vtype="C", step=1.0, search_ub=10))
    model.add_constraint(Constraint("low_requirement", {"x": 1, "y": 1}, ">=", 8))
    model.add_constraint(Constraint("high_limit", {"x": 1, "y": 1}, "<=", 5))
    model.add_objective(Objective("cost", "min", {"x": 1, "y": 1}))
    return model


def main(solver_name: str = "gurobi", diagnostics: bool = True) -> None:
    run_example_model(build_model, solver_name=solver_name, diagnostics=diagnostics)


if __name__ == "__main__":
    main()
