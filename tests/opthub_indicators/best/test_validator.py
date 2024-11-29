"""Test for the validator for the best indicator."""

import json

import pytest
from jsonschema.exceptions import ValidationError

from opthub_indicators.best.validator import validate_trial_to_score, validate_trials_scored

EPS = 1e-6


def test_trial_to_score_valid() -> None:
    """Test for the valid trial to score."""
    trial_to_score_json = json.dumps({"objective": 0.3, "feasible": None, "constraint": None})
    trial_to_score = json.loads(trial_to_score_json)
    trial_to_score = validate_trial_to_score(trial_to_score)

    if abs(trial_to_score["objective"] - 0.3) > EPS or not trial_to_score["feasible"]:
        msg = f"Unexpected trial to score: {trial_to_score}"
        raise ValueError(msg)


def test_trial_to_score_invalid_not_enough_keys() -> None:
    """Test for the invalid trial to score."""
    trial_to_score_json = json.dumps({"feasible": True, "constraint": None})
    trial_to_score = json.loads(trial_to_score_json)

    with pytest.raises(ValidationError):
        validate_trial_to_score(trial_to_score)

    trial_to_score_json = json.dumps({"objective": 0.3, "feasible": False})
    trial_to_score = json.loads(trial_to_score_json)

    with pytest.raises(ValidationError):
        validate_trial_to_score(trial_to_score)

    trial_to_score_json = json.dumps({"objective": 0.3, "constraint": None})
    trial_to_score = json.loads(trial_to_score_json)

    with pytest.raises(ValidationError):
        validate_trial_to_score(trial_to_score)


def test_trial_scored_valid() -> None:
    """Test for the valid trial scored."""
    trial_scored_json = json.dumps([{"score": 0.5}, {"score": 0.3}])
    trial_scored = json.loads(trial_scored_json)
    trial_scored = validate_trials_scored(trial_scored)

    if abs(trial_scored[0]["score"] - 0.5) > EPS or abs(trial_scored[1]["score"] - 0.3) > EPS:
        msg = f"Unexpected trials scored: {trial_scored}"
        raise ValueError(msg)


def test_trial_scored_invalid_not_enough_keys() -> None:
    """Test for the invalid trial scored."""
    trial_scored_json = json.dumps([{"score": 0.5}, {}])
    trial_scored = json.loads(trial_scored_json)

    with pytest.raises(ValidationError):
        validate_trials_scored(trial_scored)
