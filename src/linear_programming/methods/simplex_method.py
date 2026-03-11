from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.linear_programming.product_mix_problem import build_model


def build_initial_tableau() -> pd.DataFrame:
    return pd.DataFrame(
        [
            [0.0, 40.0, 30.0, 0.0, 0.0, 0.0],
            [40.0, 1.0, 0.0, 1.0, 0.0, 0.0],
            [80.0, 1.0, 1.0, 0.0, 1.0, 0.0],
            [100.0, 2.0, 1.0, 0.0, 0.0, 1.0],
        ],
        index=["obj", "s1", "s2", "s3"],
        columns=["b", "x1", "x2", "s1", "s2", "s3"],
    )


def simplex_solve(tableau: pd.DataFrame) -> pd.DataFrame:
    while tableau.iloc[0, 1:].max() > 1e-9:
        entering = tableau.iloc[0, 1:].idxmax()
        ratios = []
        for row_name in tableau.index[1:]:
            coeff = tableau.loc[row_name, entering]
            if coeff > 1e-9:
                ratios.append((tableau.loc[row_name, "b"] / coeff, row_name))
        _, leaving = min(ratios)
        pivot = tableau.loc[leaving, entering]
        tableau.loc[leaving, :] = tableau.loc[leaving, :] / pivot
        for row_name in tableau.index:
            if row_name != leaving:
                tableau.loc[row_name, :] = tableau.loc[row_name, :] - tableau.loc[row_name, entering] * tableau.loc[leaving, :]
        names = tableau.index.tolist()
        names[names.index(leaving)] = entering
        tableau.index = names
    return tableau


def main() -> None:
    model = build_model()
    print(f"model: {model.name}")
    tableau = simplex_solve(build_initial_tableau())
    print(tableau)
    print(f"objective = {-tableau.loc['obj', 'b']}")


if __name__ == "__main__":
    main()
