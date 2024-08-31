"""Test for the validator for the best indicator."""

import json

import pytest
from jsonschema.exceptions import ValidationError

from opthub_indicators.best.validator import validate_solution_to_score, validate_solutions_scored

EPS = 1e-6


def test_solution_to_score_valid() -> None:
    """Test for the valid solution to score."""
    solution_to_score_json = json.dumps({"objective": 0.3, "feasible": None, "constraint": None})
    solution_to_score = json.loads(solution_to_score_json)
    solution_to_score = validate_solution_to_score(solution_to_score)

    if abs(solution_to_score["objective"] - 0.3) > EPS or not solution_to_score["feasible"]:
        msg = f"Unexpected solution to score: {solution_to_score}"
        raise ValueError(msg)


def test_solution_to_score_invalid_not_enough_keys() -> None:
    """Test for the invalid solution to score."""
    solution_to_score_json = json.dumps({"feasible": True, "constraint": None})
    solution_to_score = json.loads(solution_to_score_json)

    with pytest.raises(ValidationError):
        validate_solution_to_score(solution_to_score)

    solution_to_score_json = json.dumps({"objective": 0.3, "feasible": False})
    solution_to_score = json.loads(solution_to_score_json)

    with pytest.raises(ValidationError):
        validate_solution_to_score(solution_to_score)

    solution_to_score_json = json.dumps({"objective": 0.3, "constraint": None})
    solution_to_score = json.loads(solution_to_score_json)

    with pytest.raises(ValidationError):
        validate_solution_to_score(solution_to_score)


def test_solution_scored_valid() -> None:
    """Test for the valid solution scored."""
    solution_scored_json = json.dumps([{"score": 0.5}, {"score": 0.3}])
    solution_scored = json.loads(solution_scored_json)
    solution_scored = validate_solutions_scored(solution_scored)

    if abs(solution_scored[0]["score"] - 0.5) > EPS or abs(solution_scored[1]["score"] - 0.3) > EPS:
        msg = f"Unexpected solutions scored: {solution_scored}"
        raise ValueError(msg)


def test_solution_scored_invalid_not_enough_keys() -> None:
    """Test for the invalid solution scored."""
    solution_scored_json = json.dumps([{"score": 0.5}, {}])
    solution_scored = json.loads(solution_scored_json)

    with pytest.raises(ValidationError):
        validate_solutions_scored(solution_scored)
