from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.ModelSolver import Constraint, Objective, OptimizationModel, Variable, run_example_model


def build_model() -> OptimizationModel:
    model = OptimizationModel(
        name="transportation_problem",
        problem_type="LP",
        description="Minimize shipping cost from two plants to two customer regions.",
    )
    for source in ("north", "south"):
        for market in ("east", "west"):
            model.add_variable(Variable(f"x_{source}_{market}", lb=0, vtype="C", step=1.0, search_ub=20))
    model.add_constraint(Constraint("north_supply", {"x_north_east": 1, "x_north_west": 1}, "<=", 18))
    model.add_constraint(Constraint("south_supply", {"x_south_east": 1, "x_south_west": 1}, "<=", 12))
    model.add_constraint(Constraint("east_demand", {"x_north_east": 1, "x_south_east": 1}, "==", 10))
    model.add_constraint(Constraint("west_demand", {"x_north_west": 1, "x_south_west": 1}, "==", 20))
    model.add_objective(Objective(name="cost", sense="min", expr={"x_north_east": 4, "x_north_west": 6, "x_south_east": 5, "x_south_west": 3}))
    return model


def main(solver_name: str = "pyomo") -> None:
    run_example_model(build_model, solver_name=solver_name)


if __name__ == "__main__":
    main()
