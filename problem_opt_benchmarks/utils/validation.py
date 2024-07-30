"""Validate the variable."""

import json
from typing import cast


def parse_optima(optima: str) -> list[list[float]]:
    """Parse and validate optima. Optima must be a list of lists of floats.

    Args:
        optima (str): optima

    Returns:
        list[list[float]]: optima
    """
    if not optima:
        msg = "Optima must be provided."
        raise ValueError(msg)

    opt = json.loads(optima)

    if not isinstance(opt, list):
        msg = "Type of optima is invalid. Must be list[list[float | int]]."
        raise TypeError(msg)

    if not isinstance(opt[0], list):
        msg = "Type of optima is invalid. Must be list[list[float | int]]."
        raise TypeError(msg)

    decision_dim = len(opt[0])

    for arr in opt:
        if not isinstance(arr, list):
            msg = "Type of optima is invalid. Must be list[list[float | int]]."
            raise TypeError(msg)
        if len(arr) != decision_dim:
            msg = "Dimension of optima is invalid. All optima must have the same dimension."
            raise ValueError(msg)
        if not all(isinstance(val, int | float) for val in arr):
            msg = "All elements of optima must be int or float."
            raise ValueError(msg)

    return cast(list[list[float]], opt)


def parse_variable(variable: str, decision_dim: int) -> list[float]:
    """Parse and validate variable. Variable must be a list of floats.

    Args:
        variable (str): variable
        objective_dim (int): objective dimension
        decision_dim (int): decision dimension

    Returns:
        list[float]: variable
    """
    if not variable:
        msg = "Variable must be provided."
        raise ValueError(msg)

    var = json.loads(variable)

    if decision_dim == 1 and isinstance(var, float | int):
        var = [float(var)]

    if not isinstance(var, list):
        msg = "Type of variable is invalid. Must be list[float | int]."
        raise TypeError(msg)

    if len(var) != decision_dim:
        msg = "Dimension of variable is invalid. Must be equal to decision_dim."
        raise ValueError(msg)

    if not all(isinstance(v, float | int) for v in var):
        msg = "Type of variable is invalid. Must be list[float | int]."
        raise TypeError(msg)

    return cast(list[float], var)
