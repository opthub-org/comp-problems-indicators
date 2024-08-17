"""Elliptic function evaluator."""

import logging
from typing import TypedDict, cast

import numpy as np

LOGGER = logging.getLogger(__name__)


class Evaluation(TypedDict):
    """The type of the solution."""

    objective: list[float] | float


def evaluate(var: list[float] | float, opt: list[list[float]]) -> Evaluation:
    """Calculate the objective value of the elliptic function.

    Args:
        var (list[float]): decision variable
        opt (list[list[float]]): optima of the elliptic function

    Returns:
        list[float]: objective value
    """
    var_arr = np.array(var, dtype=float)
    opt_arr = np.array(opt, dtype=float)
    decision_dim = len(var) if isinstance(var, list) else 1
    exp_arr = 6 * np.arange(decision_dim) / (decision_dim - 1)
    obj_arr = np.sum(10**exp_arr * (var_arr - opt_arr) ** 2, axis=1)
    objective = cast(list[float], obj_arr.tolist())
    return {"objective": objective[0] if len(objective) == 1 else objective}
