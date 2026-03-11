from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.ModelSolver import Constraint, Objective, OptimizationModel, Variable, run_example_model


def build_model() -> OptimizationModel:
    model = OptimizationModel(
        name="portfolio_risk_problem",
        problem_type="QP",
        description="Choose portfolio weights to minimize quadratic risk under a return target.",
    )
    model.add_variable(Variable("w_bond", lb=0.0, ub=1.0, vtype="C", step=0.1))
    model.add_variable(Variable("w_stock", lb=0.0, ub=1.0, vtype="C", step=0.1))
    model.add_variable(Variable("w_fund", lb=0.0, ub=1.0, vtype="C", step=0.1))
    model.add_constraint(Constraint("budget", {"w_bond": 1, "w_stock": 1, "w_fund": 1}, "==", 1))
    model.add_constraint(Constraint("return_target", {"w_bond": 0.08, "w_stock": 0.14, "w_fund": 0.11}, ">=", 0.11))
    model.add_objective(Objective(name="risk", sense="min", quadratic_expr={("w_bond", "w_bond"): 0.05, ("w_stock", "w_stock"): 0.18, ("w_fund", "w_fund"): 0.10, ("w_bond", "w_stock"): 0.02, ("w_stock", "w_bond"): 0.02, ("w_bond", "w_fund"): 0.01, ("w_fund", "w_bond"): 0.01, ("w_stock", "w_fund"): 0.03, ("w_fund", "w_stock"): 0.03}))
    return model


def main(solver_name: str = "scipy") -> None:
    run_example_model(build_model, solver_name=solver_name)


if __name__ == "__main__":
    main()
