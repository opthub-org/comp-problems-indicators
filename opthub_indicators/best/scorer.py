"""Best Indicator Scorer."""

from typing import TypedDict

from opthub_indicators.best.validator import TrialScored, TrialToScore


class Score(TypedDict):
    """The type of the score."""

    score: float


def calculate_score(
    float_max: float,
    trial_to_score: TrialToScore,
    trial_scored: list[TrialScored],
) -> Score:
    """Calculate the score.

    Args:
        float_max (float): maximum float value (worst score)S
        trial_to_score (TrialToScore): trial to score
        trial_scored (list[TrialScored]): trials scored

    Returns:
        Score: score
    """
    if trial_to_score["feasible"]:
        objective = trial_to_score["objective"]
        if objective is None:
            msg = "The trial is feasible, but the objective is None."
            raise ValueError(msg)
        score = min(objective, trial_scored[-1]["score"]) if trial_scored else objective
    else:
        score = trial_scored[-1]["score"] if trial_scored else float_max

    return {"score": score}
