"""Test for the best indicator."""

from sys import float_info
from typing import TYPE_CHECKING

from opthub_indicators.best.scorer import calculate_score

if TYPE_CHECKING:
    from opthub_indicators.best.validator import TrialScored, TrialToScore

WORST_SCORE = float_info.max
EPS = 1e-6


def test_updating_score() -> None:
    """Test the best indicator with updating score."""
    trial_to_score: TrialToScore = {"objective": 0.3, "feasible": True}
    trials_scored: list[TrialScored] = [
        {"score": 1.0},
        {"score": 0.5},
    ]
    score = calculate_score(WORST_SCORE, trial_to_score, trials_scored)
    if abs(score["score"] - 0.3) > EPS:
        msg = f"Expected 0.3, but got {score['score']}"
        raise ValueError(msg)


def test_not_updating_score() -> None:
    """Test the best indicator with not updating score."""
    trial_to_score: TrialToScore = {"objective": 0.8, "feasible": True}
    trials_scored: list[TrialScored] = [
        {"score": 1.0},
        {"score": 0.5},
    ]
    score = calculate_score(WORST_SCORE, trial_to_score, trials_scored)
    if abs(score["score"] - 0.5) > EPS:
        msg = f"Expected 0.5, but got {score['score']}"
        raise ValueError(msg)


def test_with_empty_scored() -> None:
    """Test the best indicator with empty scored."""
    trial_to_score: TrialToScore = {"objective": 0.3, "feasible": True}
    trials_scored: list[TrialScored] = []
    score = calculate_score(WORST_SCORE, trial_to_score, trials_scored)
    if abs(score["score"] - 0.3) > EPS:
        msg = f"Expected 0.3, but got {score['score']}"
        raise ValueError(msg)


def test_with_only_infeasible() -> None:
    """Test the best indicator with only infeasible."""
    trial_to_score: TrialToScore = {"objective": 0.3, "feasible": False}
    trials_scored: list[TrialScored] = []
    score = calculate_score(WORST_SCORE, trial_to_score, trials_scored)
    if abs(score["score"] - WORST_SCORE) > EPS:
        msg = f"Expected {WORST_SCORE}, but got {score['score']}"
        raise ValueError(msg)
