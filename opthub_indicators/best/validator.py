"""This file defines the schema for the input to the indicator best."""

import json
from typing import Any, TypedDict

import numpy as np
from jsonschema import validate

# Schema to validate the evaluation of the trial to score (used in "current")
SOLUTION_TO_SCORE_JSONSCHEMA = """{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Trial to score",
    "type": "object",
    "properties": {
        "objective": {
            "type": ["number", "null"]
        },
        "feasible": {
            "type": ["boolean", "null"]
        },
        "constraint": {
            "oneOf": [
                {"type": ["number", "null"]},
                {"type": "array", "minItems": 1, "items": {"type": "number"}}
            ]
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
      "score": {
        "type": "number"
      }
    },
    "required": ["score"]
  }
}"""


class TrialToScore(TypedDict):
    """The type of the trial to score."""

    objective: float | None
    feasible: bool | None


class TrialScored(TypedDict):
    """The type of the trial scored."""

    score: float


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
        raise ValueError(msg)

    return {"objective": trial["objective"], "feasible": feasible}


def validate_trials_scored(trials: list[dict[str, Any]]) -> list[TrialScored]:
    """Validate the trials scored.

    Args:
        trials (list[dict[str, Any]]): trials scored
    Returns:
        list[TrialScored]: validated trials scored
    """
    validate(instance=trials, schema=json.loads(SOLUTIONS_SCORED_JSONSCHEMA))
    return [{"score": trial["score"]} for trial in trials]


def is_feasible(trial: dict[str, Any]) -> bool:
    """Test a trial is feasible or not.

    Args:
        trial (dict[str, Any]): trial to test

    Returns:
        bool: True if the trial is feasible, False otherwise
    """
    objective = trial.get("objective")
    constraint = trial.get("constraint")
    return isinstance(objective, float | int) and bool(constraint is None or np.all(np.array(constraint) <= 0.0))
