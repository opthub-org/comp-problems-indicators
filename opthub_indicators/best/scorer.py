"""Best Indicator Scorer."""

from typing import TypedDict

from opthub_indicators.best.validator import SolutionScored, SolutionToScore


class Score(TypedDict):
    """The type of the score."""

    value: float


def calculate_score(
    float_max: float,
    solution_to_score: SolutionToScore,
    solution_scored: list[SolutionScored],
) -> Score:
    """Calculate the score.

    Args:
        float_max (float): maximum float value (worst score)S
        solution_to_score (SolutionToScore): solution to score
        solution_scored (list[SolutionScored]): solutions scored

    Returns:
        Score: score
    """
    if solution_to_score["feasible"]:
        objective = solution_to_score["objective"]
        if objective is None:
            msg = "The solution is feasible, but the objective is None."
            raise ValueError(msg)
        score = min(objective, solution_scored[-1]["score"]) if solution_scored else objective
    else:
        score = solution_scored[-1]["score"] if solution_scored else float_max

    return {"value": score}
