"""Test for elliptic main."""

import json

import pytest
from opthub_runner.evaluator import Evaluator  # type: ignore[import]

from tests.utils.docker import build_image

EPS = 1e-6


def test_elliptic_single_objective() -> None:
    """Test elliptic function with single objective function optimization."""
    image_name = build_image("problem", "elliptic")

    # Initialize the evaluator
    environment: dict[str, str] = {"ELLIPTIC_OPTIMA": json.dumps([[1, 1]])}
    evaluator = Evaluator(image_name, environment)

    # Case 1 - Evaluate [1.5, 2]
    result = evaluator.run([1.5, 2])

    if abs(result["objective"] - 1000000.25) > EPS:
        msg = f"Expected 1000000.25, but got {result['objective']}"
        raise ValueError(msg)

    # Case 2 - Invalid Solution ([1.5])
    with pytest.raises(RuntimeError):
        result = evaluator.run([1.5])

    # Case 3 - Invalid Solution (["A", 1])
    with pytest.raises(RuntimeError):
        result = evaluator.run(["A", 1])

    # Case 4 - Invalid Solution (1.5)
    with pytest.raises(RuntimeError):
        result = evaluator.run(1.5)


def test_elliptic_multi_objective() -> None:
    """Test elliptic function with multi objective function optimization."""
    image_name = build_image("problem", "elliptic")

    # Initialize the evaluator
    environment: dict[str, str] = {"ELLIPTIC_OPTIMA": json.dumps([[1, 1], [0, 0]])}
    evaluator = Evaluator(image_name, environment)
    objective_dim = 2

    # Case 1 - Evaluate [1.5, 2]
    result = evaluator.run([1.5, 2])

    if (
        len(result["objective"]) != objective_dim
        or abs(result["objective"][0] - 1000000.25) > EPS
        or abs(result["objective"][1] - 4000002.25) > EPS
    ):
        msg = f"Expected [1000000.25, 4000002.25], but got {result['objective']}"
        raise ValueError(msg)
