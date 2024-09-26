"""This file defines the schema for the input to the indicator hyper volume."""

import json
from typing import Any, TypedDict

import numpy as np
from jsonschema import validate
from jsonschema.exceptions import ValidationError

# Schema to validate the evaluation of the solution to score (used in "current")
SOLUTION_TO_SCORE_JSONSCHEMA = """{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Solution to score",
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


# Schema to validate the evaluation and score of already scored solution (used in "history")
SOLUTIONS_SCORED_JSONSCHEMA = """{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Solutions scored",
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


class SolutionToScore(TypedDict):
    """The type of the solution to score."""

    objective: list[float] | None
    feasible: bool | None


class SolutionScored(TypedDict):
    """The type of the solution scored."""

    objective: list[float] | None
    feasible: bool | None


def validate_solution_to_score(solution: dict[str, Any]) -> SolutionToScore:
    """Validate the solution to score.

    Args:
        solution (dict[str, Any]): solution to score

    Returns:
        SolutionToScore: validated solution to score
    """
    validate(instance=solution, schema=json.loads(SOLUTION_TO_SCORE_JSONSCHEMA))
    feasible = solution["feasible"] if solution["feasible"] is not None else is_feasible(solution)

    if feasible and solution["objective"] is None:
        msg = "The solution is feasible, but the objective is None."
        raise ValidationError(msg)

    return {"objective": solution["objective"], "feasible": feasible}


def validate_solutions_scored(solutions: list[dict[str, Any]]) -> list[SolutionScored]:
    """Validate the solutions scored.

    Args:
        solutions (list[dict[str, Any]]): solutions scored

    Returns:
        list[SolutionScored]: validated solutions scored
    """
    validate(instance=solutions, schema=json.loads(SOLUTIONS_SCORED_JSONSCHEMA))
    solutions_scored: list[SolutionScored] = [
        {
            "objective": solution["objective"],
            "feasible": solution["feasible"] if solution["feasible"] is not None else is_feasible(solution),
        }
        for solution in solutions
    ]
    return solutions_scored


def is_feasible(solution: dict[str, Any]) -> bool:
    """Test a solution is feasible or not.

    Args:
        solution (dict[str, Any]): solution to test

    Returns:
        bool: True if the solution is feasible, False otherwise
    """
    objective = solution.get("objective")
    constraint = solution.get("constraint")
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
