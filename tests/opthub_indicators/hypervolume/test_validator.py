"""Test for the validation of the hypervolume indicator."""

import pytest
from jsonschema.exceptions import ValidationError

from opthub_indicators.hypervolume.validator import (
    validate_ref_point,
    validate_solution_to_score,
    validate_solutions_scored,
)

EPS = 1e-6


def test_ref_point_valid() -> None:
    """Test the validation of the reference point."""
    ref_point = [1.0, 2.0]

    validated_ref_point = validate_ref_point(ref_point)

    if validated_ref_point != ref_point:
        msg = f"Expected {ref_point}, but got {validated_ref_point}"
        raise ValueError(msg)


def test_ref_point_valid_none() -> None:
    """Test the validation of the reference point."""
    ref_point = None

    validated_ref_point = validate_ref_point(ref_point)

    if validated_ref_point is not None:
        msg = f"Expected None, but got {validated_ref_point}"
        raise ValueError(msg)


def test_ref_point_invalid() -> None:
    """Test the validation of the reference point."""
    ref_point = [1.0, "A"]

    with pytest.raises(ValidationError):
        validate_ref_point(ref_point)


def test_solution_to_score_valid_feasible() -> None:
    """Test the validation of the solution to score."""
    objective = [1.0, 2.0]
    feasible = None
    constraint = None
    solution_to_score = {"objective": objective, "feasible": feasible, "constraint": constraint}

    validated_solution_to_score = validate_solution_to_score(solution_to_score)

    if validated_solution_to_score["objective"] is None:
        msg = "Expected a list of numbers, but got None objective."
        raise ValueError(msg)

    if (
        abs(validated_solution_to_score["objective"][0] - objective[0]) > EPS
        or abs(validated_solution_to_score["objective"][1] - objective[1]) > EPS
        or not validated_solution_to_score["feasible"]
    ):
        msg = f"Expected {solution_to_score}, but got {validated_solution_to_score}"
        raise ValueError(msg)


def test_solution_to_score_valid_infeasible() -> None:
    """Test the validation of the solution to score."""
    objective = [1.0, 2.0]
    feasible = None
    constraint = [1.0, 0.0]
    solution_to_score = {"objective": objective, "feasible": feasible, "constraint": constraint}

    validated_solution_to_score = validate_solution_to_score(solution_to_score)

    if validated_solution_to_score["objective"] is None:
        msg = "Expected a list of numbers, but got None objective."
        raise ValueError(msg)

    if (
        abs(validated_solution_to_score["objective"][0] - objective[0]) > EPS
        or abs(validated_solution_to_score["objective"][1] - objective[1]) > EPS
        or validated_solution_to_score["feasible"]
    ):
        msg = f"Expected {solution_to_score}, but got {validated_solution_to_score}"
        raise ValueError(msg)


def test_solution_to_score_valid_none_objective() -> None:
    """Test the validation of the solution to score."""
    objective = None
    feasible = None
    constraint = None
    solution_to_score = {"objective": objective, "feasible": feasible, "constraint": constraint}

    validated_solution_to_score = validate_solution_to_score(solution_to_score)

    if validated_solution_to_score["objective"] is not None or validated_solution_to_score["feasible"]:
        msg = f"Expected None objective, but got {validated_solution_to_score}"
        raise ValueError(msg)


def test_solution_to_score_invalid_objective() -> None:
    """Test the validation of the solution to score."""
    objective = [1.0, "A"]
    feasible = None
    constraint = None
    solution_to_score = {"objective": objective, "feasible": feasible, "constraint": constraint}

    with pytest.raises(ValidationError):
        validate_solution_to_score(solution_to_score)


def test_solution_to_score_invalid_feasible() -> None:
    """Test the validation of the solution to score."""
    objective = [1.0, 2.0]
    feasible = "A"
    constraint = None
    solution_to_score = {"objective": objective, "feasible": feasible, "constraint": constraint}

    with pytest.raises(ValidationError):
        validate_solution_to_score(solution_to_score)


def test_solution_to_score_invalid_constraint() -> None:
    """Test the validation of the solution to score."""
    objective = [1.0, 2.0]
    feasible = None
    constraint = [1.0, "A"]
    solution_to_score = {"objective": objective, "feasible": feasible, "constraint": constraint}

    with pytest.raises(ValidationError):
        validate_solution_to_score(solution_to_score)


def test_solution_to_score_invalid_elements() -> None:
    """Test the validation of the solution to score."""
    objective = [1.0, 2.0]
    feasible = None
    solution_to_score = {"objective": objective, "feasible": feasible}

    with pytest.raises(ValidationError):
        validate_solution_to_score(solution_to_score)


def test_solution_scored_valid() -> None:
    """Test the validation of the solutions scored."""
    objective0 = [1.0, 2.0]
    feasible0 = True
    objective1 = [2.0, 1.0]
    feasible1 = False
    solution_scored = [
        {"objective": objective0, "feasible": feasible0},
        {"objective": objective1, "feasible": feasible1},
    ]

    validated_solutions_scored = validate_solutions_scored(solution_scored)

    if validated_solutions_scored[0]["objective"] is None or validated_solutions_scored[1]["objective"] is None:
        msg = "Expected a list of numbers, but got None objective."
        raise ValueError(msg)
    if not all(isinstance(validated_solutions_scored[0]["objective"][i], int | float) for i in range(2)):
        msg = "Expected a list of numbers, but got None objective."
        raise ValueError(msg)
    if not all(isinstance(validated_solutions_scored[1]["objective"][i], int | float) for i in range(2)):
        msg = "Expected a list of numbers, but got None objective."
        raise ValueError(msg)

    if not all(abs(validated_solutions_scored[0]["objective"][i] - objective0[i]) < EPS for i in range(2)) or not all(
        abs(validated_solutions_scored[1]["objective"][i] - objective1[i]) < EPS for i in range(2)
    ):
        msg = f"Expected {solution_scored}, but got {validated_solutions_scored}"
        raise ValueError(msg)
    if validated_solutions_scored[0]["feasible"] != feasible0 or validated_solutions_scored[1]["feasible"] != feasible1:
        msg = f"Expected {solution_scored}, but got {validated_solutions_scored}"
        raise ValueError(msg)


def test_solution_scored_invalid_objective() -> None:
    """Test the validation of the solutions scored."""
    objective0 = [1.0, "A"]
    feasible0 = True
    objective1 = [2.0, 1.0]
    feasible1 = False
    solution_scored = [
        {"objective": objective0, "feasible": feasible0},
        {"objective": objective1, "feasible": feasible1},
    ]

    with pytest.raises(ValidationError):
        validate_solutions_scored(solution_scored)


def test_solution_scored_invalid_feasible() -> None:
    """Test the validation of the solutions scored."""
    objective0 = [1.0, 2.0]
    feasible0 = "A"
    objective1 = [2.0, 1.0]
    feasible1 = False
    solution_scored: list[dict[str, object]] = [
        {"objective": objective0, "feasible": feasible0},
        {"objective": objective1, "feasible": feasible1},
    ]

    with pytest.raises(ValidationError):
        validate_solutions_scored(solution_scored)


def test_solution_scored_invalid_elements() -> None:
    """Test the validation of the solutions scored."""
    objective0 = [1.0, 2.0]
    feasible0 = True
    objective1 = [2.0, 1.0]
    solution_scored: list[dict[str, object]] = [
        {"objective": objective0, "feasible": feasible0},
        {"objective": objective1},
    ]

    with pytest.raises(ValidationError):
        validate_solutions_scored(solution_scored)


def test_solution_scored_valid_empty() -> None:
    """Test the validation of the solutions scored."""
    solution_scored: list[dict[str, object]] = []

    validated_solutions_scored = validate_solutions_scored(solution_scored)

    if validated_solutions_scored != []:
        msg = f"Expected [], but got {validated_solutions_scored}"
        raise ValueError(msg)
