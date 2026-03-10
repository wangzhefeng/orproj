from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.ModelSolver import run_example_model
from src.linear_programming.infeasibility_analysis_problem import build_model


if __name__ == "__main__":
    run_example_model(build_model, solver_name="gurobi", diagnostics=True)
