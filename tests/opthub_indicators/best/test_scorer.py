"""Test for the best indicator."""

from sys import float_info
from typing import TYPE_CHECKING

from opthub_indicators.best.scorer import calculate_score

if TYPE_CHECKING:
    from opthub_indicators.best.validator import SolutionScored, SolutionToScore

WORST_SCORE = float_info.max
EPS = 1e-6


def test_updating_score() -> None:
    """Test the best indicator with updating score."""
    solution_to_score: SolutionToScore = {"objective": 0.3, "feasible": True}
    solutions_scored: list[SolutionScored] = [
        {"score": 1.0},
        {"score": 0.5},
    ]
    score = calculate_score(WORST_SCORE, solution_to_score, solutions_scored)
    if abs(score["value"] - 0.3) > EPS:
        msg = f"Expected 0.3, but got {score['value']}"
        raise ValueError(msg)


def test_not_updating_score() -> None:
    """Test the best indicator with not updating score."""
    solution_to_score: SolutionToScore = {"objective": 0.8, "feasible": True}
    solutions_scored: list[SolutionScored] = [
        {"score": 1.0},
        {"score": 0.5},
    ]
    score = calculate_score(WORST_SCORE, solution_to_score, solutions_scored)
    if abs(score["value"] - 0.5) > EPS:
        msg = f"Expected 0.5, but got {score['value']}"
        raise ValueError(msg)


def test_with_empty_scored() -> None:
    """Test the best indicator with empty scored."""
    solution_to_score: SolutionToScore = {"objective": 0.3, "feasible": True}
    solutions_scored: list[SolutionScored] = []
    score = calculate_score(WORST_SCORE, solution_to_score, solutions_scored)
    if abs(score["value"] - 0.3) > EPS:
        msg = f"Expected 0.3, but got {score['value']}"
        raise ValueError(msg)


def test_with_only_infeasible() -> None:
    """Test the best indicator with only infeasible."""
    solution_to_score: SolutionToScore = {"objective": 0.3, "feasible": False}
    solutions_scored: list[SolutionScored] = []
    score = calculate_score(WORST_SCORE, solution_to_score, solutions_scored)
    if abs(score["value"] - WORST_SCORE) > EPS:
        msg = f"Expected {WORST_SCORE}, but got {score['value']}"
        raise ValueError(msg)
