"""Test for elliptic evaluator."""

from opthub_problems.rosenbrock.evaluator import evaluate

EPS = 1e-6


def test_single_objective_2d() -> None:
    """Test single objective function with 2d solution."""
    result = evaluate([1.5, 2.5])
    objective = result["objective"]
    if isinstance(objective, list):
        msg = "Expected float, but got list"
        raise TypeError(msg)
    if abs(objective - 6.5) > EPS:
        msg = f"Expected 6.5, but got {objective}"
        raise ValueError(msg)

    result = evaluate([0.5, 1])
    objective = result["objective"]
    if isinstance(objective, list):
        msg = "Expected float, but got list"
        raise TypeError(msg)
    if abs(objective - 56.5) > EPS:
        msg = f"Expected 56.5, but got {objective}"
        raise ValueError(msg)

    result = evaluate([1, 1])
    objective = result["objective"]
    if isinstance(objective, list):
        msg = "Expected float, but got list"
        raise TypeError(msg)
    if abs(objective - 0) > EPS:
        msg = f"Expected 0, but got {objective}"
        raise ValueError(msg)
