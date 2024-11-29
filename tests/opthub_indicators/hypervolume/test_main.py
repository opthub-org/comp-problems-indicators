"""Test for the indicators of the hypervolume."""

import json

from tests.utils.docker import build_image, executor

EPS = 1e-6


def test_hypervolume_1() -> None:
    """Test hypervolume indicator."""
    image_name = build_image("indicator", "hypervolume")
    trial_to_score = {"objective": [1, 1], "feasible": None, "constraint": None}
    trials_scored = [
        {"objective": [2, 0], "feasible": None, "constraint": None},
        {"objective": [0, 2], "feasible": None, "constraint": None},
    ]
    std_in = json.dumps(trial_to_score) + "\n" + json.dumps(trials_scored) + "\n"
    environment: dict[str, object] = {"HV_REF_POINT": json.dumps([2, 4])}

    std_out = executor(image_name=image_name, environment=environment, std_in=std_in, timeout=10)
    if std_out is None:
        msg = "The stdout is None."
        raise ValueError(msg)
    if abs(std_out["score"] - 5.0) > EPS:
        msg = f"Expected 5.0, but got {std_out['score']}"
        raise ValueError(msg)


def test_hypervolume_2() -> None:
    """Test hypervolume indicator."""
    image_name = build_image("indicator", "hypervolume")
    trial_to_score = {"objective": [1, 1], "feasible": None, "constraint": [0, 0]}
    trials_scored = [
        {"objective": [2, 0], "feasible": None, "constraint": [0, 0]},
        {"objective": [0, 2], "feasible": None, "constraint": [0, 0]},
        {"objective": [1, 1], "feasible": None, "constraint": [0, 0]},
        {"objective": [0.5, 1], "feasible": None, "constraint": [1, 1]},
        {"objective": [1, 0.5], "feasible": None, "constraint": [1, 1]},
    ]
    std_in = json.dumps(trial_to_score) + "\n" + json.dumps(trials_scored) + "\n"
    environment: dict[str, object] = {}

    std_out = executor(image_name=image_name, environment=environment, std_in=std_in, timeout=10)
    if std_out is None:
        msg = "The stdout is None."
        raise ValueError(msg)
    if abs(std_out["score"] - 1.0) > EPS:
        msg = f"Expected 1.0, but got {std_out['score']}"
        raise ValueError(msg)
