from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.ModelSolver import Objective, OptimizationModel, Variable, run_example_model


def surface_value(values: dict[str, float]) -> float:
    x1 = values["x1"]
    x2 = values["x2"]
    x3 = values["x3"]
    return (2 + x1) / (1 + x2) - 3 * x1 + 4 * x3


def build_model() -> OptimizationModel:
    model = OptimizationModel(
        name="bounded_surface_optimization_problem",
        problem_type="NLP",
        description="Bounded nonlinear surface optimization restored from the original SciPy example.",
    )
    # 原始示例只给出了三个变量的盒约束，没有其他显式约束。
    model.add_variable(Variable("x1", lb=0.1, ub=0.9, vtype="C", step=0.1))
    model.add_variable(Variable("x2", lb=0.1, ub=0.9, vtype="C", step=0.1))
    model.add_variable(Variable("x3", lb=0.1, ub=0.9, vtype="C", step=0.1))
    model.add_objective(
        Objective(
            name="surface_value",
            sense="min",
            nonlinear_expr=surface_value,
            description="min ((2 + x1) / (1 + x2)) - 3*x1 + 4*x3",
        )
    )
    return model


def main(solver_name: str = "scipy") -> None:
    run_example_model(build_model, solver_name=solver_name)


if __name__ == "__main__":
    main()
