"""Rosenbrock function evaluator."""

import logging
from typing import TypedDict, cast

import numpy as np

LOGGER = logging.getLogger(__name__)


class Evaluation(TypedDict):
    """The type of the solution."""

    objective: list[float] | float


def evaluate(var: list[float] | float) -> Evaluation:
    """Calculate the objective value of the rosenbrock function.

    Args:
        var (list[float]): decision variable
        opt (list[list[float]]): optima of the rosenbrock function

    Returns:
        list[float]: objective value
    """
    var_arr = np.array(var, dtype=float)
    obj_arr = np.sum(
        100 * (var_arr[:-1] ** 2 - var_arr[1:]) ** 2 + (var_arr[:-1] - 1) ** 2,
        axis=0,
    )
    objective = cast(list[float], obj_arr.tolist())
    return {"objective": objective}
