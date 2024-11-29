"""Test for best indicator."""

import json

from tests.utils.docker import build_image, executor

EPS = 1e-6


def test_main() -> None:
    """Test the main function."""
    image_name = build_image("indicator", "best")
    trial_to_score = {"objective": 0.2, "feasible": None, "constraint": None}
    trials_scored = [{"score": 0.5}, {"score": 0.3}]
    std_in = json.dumps(trial_to_score) + "\n" + json.dumps(trials_scored) + "\n"
    environment: dict[str, object] = {}

    std_out = executor(image_name=image_name, environment=environment, std_in=std_in, timeout=10)
    if std_out is None:
        msg = "The stdout is None."
        raise ValueError(msg)
    if abs(std_out["score"] - 0.2) > EPS:
        msg = f"Expected 0.2, but got {std_out['score']}"
        raise ValueError(msg)
