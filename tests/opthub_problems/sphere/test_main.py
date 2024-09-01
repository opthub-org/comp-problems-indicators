"""Test for sphere main."""

import json

import pytest
from opthub_runner.evaluator import Evaluator  # type: ignore[import]

from tests.utils.docker import build_image

EPS = 1e-6


def test_sphere_single_objective_2d() -> None:
    """Test sphere function with single objective function optimization and decision dimension 2."""
    image_name = build_image("problem", "sphere")

    # Initialize the evaluator
    environment: dict[str, str] = {"SPHERE_OPTIMA": json.dumps([[1, 1]])}
    evaluator = Evaluator(image_name, environment)

    # Case 1 - Evaluate [1.5, 2.5]
    result = evaluator.run([1.5, 2.5])

    if abs(result["objective"] - 2.5) > EPS:
        msg = f"Expected 2.5, but got {result['objective']}"
        raise ValueError(msg)

    # Case 2 - Evaluate [1.5, 2]
    result = evaluator.run([1.5, 2])

    if abs(result["objective"] - 1.25) > EPS:
        msg = f"Expected 1.25, but got {result['objective']}"
        raise ValueError(msg)

    # Case 3 - Invalid Solution ([1.5])
    with pytest.raises(RuntimeError):
        result = evaluator.run([1.5])

    # Case 4 - Invalid Solution ([1.5, 2.5, 3.5])
    with pytest.raises(RuntimeError):
        result = evaluator.run([1.5, 2.5, 3.5])

    # Case 5 - Invalid Solution (["A", 1])
    with pytest.raises(RuntimeError):
        result = evaluator.run(["A", 1])

    # Case 6 - Invalid Solution ([[1, 2]])
    with pytest.raises(RuntimeError):
        result = evaluator.run([[1, 2]])

    # Case 7 - Invalid Solution (1.5)
    with pytest.raises(RuntimeError):
        result = evaluator.run(1.5)


def test_sphere_single_objective_1d() -> None:
    """Test sphere function with single objective function optimization and decision dimension 1."""
    image_name = build_image("problem", "sphere")

    # Initialize the evaluator
    environment: dict[str, str] = {"SPHERE_OPTIMA": json.dumps([[1]])}
    evaluator = Evaluator(image_name, environment)

    # Case 1 - Evaluate 1.5
    result = evaluator.run(1.5)

    if abs(result["objective"] - 0.25) > EPS:
        msg = f"Expected 0.25, but got {result['objective']}"
        raise ValueError(msg)

    # Case 2 - Evaluate [1]
    result = evaluator.run([1])

    if abs(result["objective"] - 0) > EPS:
        msg = f"Expected 0, but got {result['objective']}"
        raise ValueError(msg)

    # Case 3 - Invalid Solution ([1.5, 2.5])
    with pytest.raises(RuntimeError):
        result = evaluator.run([1.5, 2.5])

    # Case 4 - Invalid Solution (["A"])
    with pytest.raises(RuntimeError):
        result = evaluator.run(["A"])


def test_sphere_multi_objective_dim2() -> None:
    """Test sphere function with multi objective function optimization with decision dimension 2."""
    image_name = build_image("problem", "sphere")

    # Initialize the evaluator
    environment: dict[str, str] = {"SPHERE_OPTIMA": json.dumps([[1, 1], [2, 2]])}
    evaluator = Evaluator(image_name, environment)
    objective_dim = 2

    # Case 1 - Evaluate [1.5, 2.5]
    result = evaluator.run([1.5, 2.5])

    if (
        len(result["objective"]) != objective_dim
        or abs(result["objective"][0] - 2.5) > EPS
        or abs(result["objective"][1] - 0.5) > EPS
    ):
        msg = f"Expected [2.5, 0.5], but got {result['objective']}"
        raise ValueError(msg)

    # Case 2 - Invalid Solution ([1.5, "A"])
    with pytest.raises(RuntimeError):
        result = evaluator.run([1.5, "A"])

    # Case 3 - Invalid Solution ([1.5])
    with pytest.raises(RuntimeError):
        result = evaluator.run([1.5])


def test_sphere_multi_objective_dim1() -> None:
    """Test sphere function with multi objective function optimization with decision dimension 1."""
    image_name = build_image("problem", "sphere")

    # Initialize the evaluator
    environment: dict[str, str] = {"SPHERE_OPTIMA": json.dumps([[1], [2.5]])}
    evaluator = Evaluator(image_name, environment)
    objective_dim = 2

    # Case 1 - Evaluate [1.5]
    result = evaluator.run([1.5])

    if (
        len(result["objective"]) != objective_dim
        or abs(result["objective"][0] - 0.25) > EPS
        or abs(result["objective"][1] - 1) > EPS
    ):
        msg = f"Expected [0.25, 1], but got {result['objective']}"
        raise ValueError(msg)

    # Case 2 - Evaluate 1
    result = evaluator.run(1)

    if (
        len(result["objective"]) != objective_dim
        or abs(result["objective"][0] - 0) > EPS
        or abs(result["objective"][1] - 2.25) > EPS
    ):
        msg = f"Expected [0, 2.25], but got {result['objective']}"
        raise ValueError(msg)
