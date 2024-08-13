"""Sphere function evaluator."""

from typing import TypedDict, cast

import numpy as np


class Evaluation(TypedDict):
    """The type of the solution."""

    objective: list[float] | float


def evaluate(var: list[float] | float, opt: list[list[float]]) -> Evaluation:
    """Calculate the objective value of the sphere function.

    Args:
        var (list[float]): decision variable
        opt (list[list[float]]): optima of the sphere function

    Returns:
        list[float]: objective value
    """
    var_arr = np.array(var, dtype=float)
    opt_arr = np.array(opt, dtype=float)
    obj_arr = np.sum((var_arr - opt_arr) ** 2, axis=1)
    objective = cast(list[float], obj_arr.tolist())
    return {"objective": objective[0] if len(objective) == 1 else objective}
