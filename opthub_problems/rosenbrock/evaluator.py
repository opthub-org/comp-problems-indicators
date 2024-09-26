"""Rosenbrock function evaluator."""

import logging
from typing import TypedDict, cast

import numpy as np

LOGGER = logging.getLogger(__name__)


class Evaluation(TypedDict):
    """The type of the solution."""

    objective: list[float] | float


def evaluate(var: list[float] | float, opt: list[list[float]]) -> Evaluation:
    """Calculate the objective value of the rosenbrock function.

    Args:
        var (list[float]): decision variable
        opt (list[list[float]]): optima of the rosenbrock function

    Returns:
        list[float]: objective value
    """
    var_arr = np.array(var, dtype=float)
    opt_arr = np.array(opt, dtype=float)
    diff_arr = opt_arr - 1
    var_arr = var_arr[np.newaxis, :] - diff_arr
    obj_arr = np.sum(
        100 * (var_arr[:, :-1] ** 2 - var_arr[:, 1:]) ** 2 + (var_arr[:, :-1] - 1) ** 2,
        axis=1,
    )
    objective = cast(list[float], obj_arr.tolist())
    return {"objective": objective[0] if len(objective) == 1 else objective}
