from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.ModelSolver import Constraint, Objective, OptimizationModel, SolverConfig, SolverEngine, SolverFactory, Variable


def build_master_problem() -> OptimizationModel:
    model = OptimizationModel(name="cutting_stock_master", problem_type="IP")
    model.add_variable(Variable("p1", lb=0, ub=20, vtype="I"))
    model.add_variable(Variable("p2", lb=0, ub=20, vtype="I"))
    model.add_variable(Variable("p3", lb=0, ub=20, vtype="I"))
    model.add_constraint(Constraint("demand_3", {"p1": 6, "p2": 0, "p3": 0}, ">=", 25))
    model.add_constraint(Constraint("demand_7", {"p1": 0, "p2": 2, "p3": 0}, ">=", 30))
    model.add_constraint(Constraint("demand_9", {"p1": 0, "p2": 0, "p3": 2}, ">=", 14))
    model.add_objective(Objective("rolls", "min", {"p1": 1, "p2": 1, "p3": 1}))
    return model


def main() -> None:
    result = SolverEngine(SolverFactory.create("reference")).solve(build_master_problem(), SolverConfig())
    print("master problem result:")
    print(result.variable_values)
    print("note: this demo keeps the column-generation idea but uses predefined patterns under the shared model abstraction.")


if __name__ == "__main__":
    main()
