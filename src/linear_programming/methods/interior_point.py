from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.linear_programming.product_mix_problem import build_model


def gradient(x1: float, x2: float, t: float) -> np.ndarray:
    return np.array([
        -40 * t + 1 / (40 - x1) + 1 / (80 - x1 - x2) + 2 / (100 - 2 * x1 - x2) - 1 / x1,
        -30 * t + 1 / (80 - x1 - x2) + 1 / (100 - 2 * x1 - x2) - 1 / x2,
    ])


def hessian(x1: float, x2: float) -> np.ndarray:
    return np.array([
        [1 / (40 - x1) ** 2 + 1 / (80 - x1 - x2) ** 2 + 4 / (100 - 2 * x1 - x2) ** 2 + 1 / x1**2,
         1 / (80 - x1 - x2) ** 2 + 2 / (100 - 2 * x1 - x2) ** 2],
        [1 / (80 - x1 - x2) ** 2 + 2 / (100 - 2 * x1 - x2) ** 2,
         1 / (80 - x1 - x2) ** 2 + 1 / (100 - 2 * x1 - x2) ** 2 + 1 / x2**2],
    ])


def main() -> None:
    model = build_model()
    print(f"model: {model.name}")
    x = np.array([10.0, 10.0])
    t = 0.001
    for _ in range(12):
        step = np.linalg.solve(hessian(x[0], x[1]), gradient(x[0], x[1], t))
        x = x - step
        if np.linalg.norm(step) < 1e-6:
            break
    objective = 40 * x[0] + 30 * x[1]
    print({"x_desks": round(float(x[0]), 4), "x_tables": round(float(x[1]), 4), "objective": round(float(objective), 4)})


if __name__ == "__main__":
    main()
