"""This file defines the schema for the input to the indicator best."""

import json
from typing import Any, TypedDict

import numpy as np
from jsonschema import validate

# Schema to validate the evaluation of the solution to score (used in "current")
SOLUTION_TO_SCORE_JSONSCHEMA = """{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Solution to score",
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

# Schema to validate the evaluation and score of already scored solution (used in "history")
SOLUTIONS_SCORED_JSONSCHEMA = """{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Solutions scored",
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


class SolutionToScore(TypedDict):
    """The type of the solution to score."""

    objective: float | None
    feasible: bool | None


class SolutionScored(TypedDict):
    """The type of the solution scored."""

    score: float


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
        raise ValueError(msg)

    return {"objective": solution["objective"], "feasible": feasible}


def validate_solutions_scored(solutions: list[dict[str, Any]]) -> list[SolutionScored]:
    """Validate the solutions scored.

    Args:
        solutions (list[dict[str, Any]]): solutions scored
    Returns:
        list[SolutionScored]: validated solutions scored
    """
    validate(instance=solutions, schema=json.loads(SOLUTIONS_SCORED_JSONSCHEMA))
    return [{"score": solution["score"]} for solution in solutions]


def is_feasible(solution: dict[str, Any]) -> bool:
    """Test a solution is feasible or not.

    Args:
        solution (dict[str, Any]): solution to test

    Returns:
        bool: True if the solution is feasible, False otherwise
    """
    objective = solution.get("objective")
    constraint = solution.get("constraint")
    return isinstance(objective, float | int) and bool(constraint is None or np.all(np.array(constraint) <= 0.0))
