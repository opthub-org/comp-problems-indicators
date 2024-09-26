"""Test for elliptic evaluator."""

from opthub_problems.rastrigin.evaluator import evaluate

EPS = 1e-6


def test_single_objective_2d() -> None:
    """Test single objective function with 2d solution."""
    optima = [[0.0, 0.0]]
    result = evaluate([1.5, 2.5], optima)
    objective = result["objective"]
    if isinstance(objective, list):
        msg = "Expected float, but got list"
        raise TypeError(msg)
    if abs(objective - 48.5) > EPS:
        msg = f"Expected 48.5, but got {objective}"
        raise ValueError(msg)

    result = evaluate([1.5, 2], optima)
    objective = result["objective"]
    if isinstance(objective, list):
        msg = "Expected float, but got list"
        raise TypeError(msg)
    if abs(objective - 26.25) > EPS:
        msg = f"Expected 26.25, but got {objective}"
        raise ValueError(msg)

    result = evaluate([0, 0], optima)
    objective = result["objective"]
    if isinstance(objective, list):
        msg = "Expected float, but got list"
        raise TypeError(msg)
    if abs(objective - 0) > EPS:
        msg = f"Expected 0, but got {objective}"
        raise ValueError(msg)


def test_single_objective_1d() -> None:
    """Test single objective function with 2d solution."""
    optima = [[0.0]]
    result = evaluate([1.5], optima)
    objective = result["objective"]
    if isinstance(objective, list):
        msg = "Expected float, but got list"
        raise TypeError(msg)
    if abs(objective - 22.25) > EPS:
        msg = f"Expected 22.25, but got {objective}"
        raise ValueError(msg)

    result = evaluate([0], optima)
    objective = result["objective"]
    if isinstance(objective, list):
        msg = "Expected float, but got list"
        raise TypeError(msg)
    if abs(objective - 0) > EPS:
        msg = f"Expected 0, but got {objective}"
        raise ValueError(msg)


def test_multi_objective_2d() -> None:
    """Test multi objective function with 2d solution."""
    optima = [[0.0, 0.0], [1.0, 1.0]]
    dim = 2
    result = evaluate([1.5, 2.5], optima)
    objective = result["objective"]
    if isinstance(objective, float):
        msg = "Expected list, but got float"
        raise TypeError(msg)
    if len(objective) != dim or abs(objective[0] - 48.5) > EPS or abs(objective[1] - 42.5) > EPS:
        msg = f"Expected [48.5, 42.5], but got {result['objective']}"
        raise ValueError(msg)
