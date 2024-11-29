"""This file defines the schema for the input to the indicator hyper volume."""

import json
from typing import Any, TypedDict

import numpy as np
from jsonschema import validate
from jsonschema.exceptions import ValidationError

# Schema to validate the evaluation of the trial to score (used in "current")
SOLUTION_TO_SCORE_JSONSCHEMA = """{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Trial to score",
    "type": "object",
    "properties": {
        "objective": {
            "oneOf": [
                {"type": "null"},
                {"type": "array", "minItems": 2, "items": {"type": "number"}}
            ]
        },
        "constraint": {
            "oneOf": [
                {"type": ["number", "null"]},
                {"type": "array", "minItems": 2, "items": {"type": "number"}}
            ]
        },
        "feasible": {
            "type": ["boolean", "null"]
        }
    },
    "required": ["objective", "feasible", "constraint"]
}"""


# Schema to validate the evaluation and score of already scored trial (used in "history")
SOLUTIONS_SCORED_JSONSCHEMA = """{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Trials scored",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "objective": {
                "oneOf": [
                    {"type": "null"},
                    {"type": "array", "minItems": 2, "items": {"type": "number"}}
                ]
            },
            "constraint": {
                "oneOf": [
                    {"type": ["number", "null"]},
                    {"type": "array", "minItems": 2, "items": {"type": "number"}}
                ]
            },
            "feasible": {
                "type": ["boolean", "null"]
            }
        },
        "required": ["objective", "feasible"]
    }
}"""


# Schema to validate the reference point for the hypervolume
REF_POINT_JSONSCHEMA = """{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Reference point for Hypervolume",
  "oneOf": [
    {"type": "null"},
    {"type": "array", "minItems": 2, "items": {"type": "number"}}
  ]
}"""


class TrialToScore(TypedDict):
    """The type of the trial to score."""

    objective: list[float] | None
    feasible: bool | None


class TrialScored(TypedDict):
    """The type of the trial scored."""

    objective: list[float] | None
    feasible: bool | None


def validate_trial_to_score(trial: dict[str, Any]) -> TrialToScore:
    """Validate the trial to score.

    Args:
        trial (dict[str, Any]): trial to score

    Returns:
        TrialToScore: validated trial to score
    """
    validate(instance=trial, schema=json.loads(SOLUTION_TO_SCORE_JSONSCHEMA))
    feasible = trial["feasible"] if trial["feasible"] is not None else is_feasible(trial)

    if feasible and trial["objective"] is None:
        msg = "The trial is feasible, but the objective is None."
        raise ValidationError(msg)

    return {"objective": trial["objective"], "feasible": feasible}


def validate_trials_scored(trials: list[dict[str, Any]]) -> list[TrialScored]:
    """Validate the trials scored.

    Args:
        trials (list[dict[str, Any]]): trials scored

    Returns:
        list[TrialScored]: validated trials scored
    """
    validate(instance=trials, schema=json.loads(SOLUTIONS_SCORED_JSONSCHEMA))
    trials_scored: list[TrialScored] = [
        {
            "objective": trial["objective"],
            "feasible": trial["feasible"] if trial["feasible"] is not None else is_feasible(trial),
        }
        for trial in trials
    ]
    return trials_scored


def is_feasible(trial: dict[str, Any]) -> bool:
    """Test a trial is feasible or not.

    Args:
        trial (dict[str, Any]): trial to test

    Returns:
        bool: True if the trial is feasible, False otherwise
    """
    objective = trial.get("objective")
    constraint = trial.get("constraint")
    return isinstance(objective, list) and bool(constraint is None or np.all(np.array(constraint) <= 0.0))


def validate_ref_point(ref_point: object | None) -> list[float] | None:
    """Validate the reference point for the hypervolume.

    Args:
        ref_point (Any): reference point

    Returns:
        list[float] | None: validated reference point
    """
    if not (isinstance(ref_point, list) or ref_point is None):
        msg = "The reference point must be a list of numbers or None."
        raise ValidationError(msg)

    validate(instance=ref_point, schema=json.loads(REF_POINT_JSONSCHEMA))

    return ref_point
