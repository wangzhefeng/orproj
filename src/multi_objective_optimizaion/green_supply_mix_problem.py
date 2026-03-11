from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.ModelSolver import Constraint, Objective, OptimizationModel, Variable, run_example_model


def build_model() -> OptimizationModel:
    model = OptimizationModel(
        name="green_supply_mix_problem",
        problem_type="MOIP",
        description="Balance purchasing cost and carbon emission across two suppliers.",
    )
    model.add_variable(Variable("supplier_a", lb=0, vtype="I", search_ub=20))
    model.add_variable(Variable("supplier_b", lb=0, vtype="I", search_ub=20))
    model.add_constraint(Constraint("demand", {"supplier_a": 1, "supplier_b": 1}, "==", 20))
    model.add_constraint(Constraint("reliable_supply", {"supplier_a": 1}, ">=", 6))
    model.add_objective(Objective("procurement_cost", "min", {"supplier_a": 7, "supplier_b": 5}, weight=0.6))
    model.add_objective(Objective("carbon_emission", "min", {"supplier_a": 2, "supplier_b": 5}, weight=0.4))
    return model


def main(solver_name: str = "reference") -> None:
    run_example_model(build_model, solver_name=solver_name)


if __name__ == "__main__":
    main()
