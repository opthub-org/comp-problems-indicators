"""Test for elliptic evaluator."""

from opthub_problems.elliptic.evaluator import evaluate

EPS = 1e-6


def test_single_objective_2d() -> None:
    """Test single objective function with 2d solution."""
    optima = [[1.0, 1.0]]
    result = evaluate([1.5, 2.5], optima)
    objective = result["objective"]
    if isinstance(objective, list):
        msg = "Expected float, but got list"
        raise TypeError(msg)
    if abs(objective - 2250000.25) > EPS:
        msg = f"Expected 2250000.25, but got {objective}"
        raise ValueError(msg)

    result = evaluate([1.5, 2], optima)
    objective = result["objective"]
    if isinstance(objective, list):
        msg = "Expected float, but got list"
        raise TypeError(msg)
    if abs(objective - 1000000.25) > EPS:
        msg = f"Expected 1000000.25, but got {objective}"
        raise ValueError(msg)

    result = evaluate([1, 1], optima)
    objective = result["objective"]
    if isinstance(objective, list):
        msg = "Expected float, but got list"
        raise TypeError(msg)
    if abs(objective - 0) > EPS:
        msg = f"Expected 0, but got {objective}"
        raise ValueError(msg)


def test_multi_objective_2d() -> None:
    """Test multi objective function with 2d solution."""
    optima = [[1.0, 1.0], [2.0, 2.0]]
    dim = 2
    result = evaluate([1.5, 2.5], optima)
    objective = result["objective"]
    if isinstance(objective, float):
        msg = "Expected list, but got float"
        raise TypeError(msg)
    if len(objective) != dim or abs(objective[0] - 2250000.25) > EPS or abs(objective[1] - 250000.25) > EPS:
        msg = f"Expected [2250000.25, 250000.25], but got {result['objective']}"
        raise ValueError(msg)
