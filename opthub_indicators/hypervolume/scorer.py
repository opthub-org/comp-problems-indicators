"""Hypervolume indicator scorer."""

from typing import TypedDict

import numpy as np
from pymoo.indicators.hv import HV  # type: ignore[import]
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting  # type: ignore[import]

from opthub_indicators.hypervolume.validator import TrialScored, TrialToScore


class Score(TypedDict):
    """The type of the score."""

    score: float


def calculate_score(
    ref_point: list[float] | None,
    trial_to_score: TrialToScore,
    trials_scored: list[TrialScored],
) -> Score:
    """Calculate the score.

    Args:
        ref_point (Sequence[float | int] | None): reference point
        trial_to_score (TrialToScore): trial to score
        trials_scored (list[TrialScored]): trials scored

    Returns:
        Score: score
    """
    score = 0
    feasible_objectives = [trial["objective"] for trial in trials_scored if trial["feasible"]]

    if trial_to_score["feasible"]:
        feasible_objectives.append(trial_to_score["objective"])

    if len(feasible_objectives) == 0:
        return {"score": 0}

    if len(feasible_objectives) == 1 and ref_point is None:
        return {"score": 0}

    feasible_objectives_array = np.array(feasible_objectives)
    pareto_front_indices = NonDominatedSorting().do(feasible_objectives_array, only_non_dominated_front=True)
    pareto_front_array = feasible_objectives_array[pareto_front_indices]

    ref_point_array = np.max(pareto_front_array, axis=0) if ref_point is None else np.array(ref_point)

    hv = HV(ref_point=ref_point_array)
    score = hv.do(feasible_objectives_array)

    if score is None:
        msg = "Hypervolume calculation failed. HV returned None."
        raise ValueError(msg)

    return {"score": score}
