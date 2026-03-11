from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.ModelSolver import FileSolveRequest, solve_model_file


if __name__ == "__main__":
    request_path = sys.argv[1] if len(sys.argv) > 1 else "model.lp"
    diagnostic = solve_model_file(FileSolveRequest(request_path), solver_name="gurobi")
    print(diagnostic.summary)
