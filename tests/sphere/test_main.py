"""Test for problem_benchmarks/sphere/sphere.py."""

import json
import logging
import subprocess

from opthub_runner.evaluator import Evaluator  # type: ignore[import]

EPS = 1e-6
LOGGER = logging.getLogger(__name__)


def build_image() -> None:
    """Build the image for the sphere function."""
    func = "sphere"
    subprocess.run(["make", f"build-{func}"], check=True)  # Build the image
    subprocess.run(["docker", "image", "prune", "-f"], check=True)  # Delete <none> images


def test_sphere_sofo_dim2() -> None:
    """Test sphere function with single objective function optimization (SOFO) and decision dimension 2."""
    build_image()
    func = "sphere"
    image_name = "opthub/problem-" + func + ":latest"

    # Initialize the evaluator
    environment: dict[str, str] = {"SPHERE_OPTIMA": json.dumps([[1, 1]])}
    evaluator = Evaluator(image_name, environment)

    # Case 1 - Evaluate [1.5, 2.5]
    result = evaluator.run([1.5, 2.5])

    if abs(result["objective"] - 2.5) > EPS:
        msg = f"Expected 2.5, but got {result['objective']}"
        raise ValueError(msg)

    # Case 2 - Evaluate [1.5, 2]
    result = evaluator.run([1.5, 2])

    if abs(result["objective"] - 1.25) > EPS:
        msg = f"Expected 1.25, but got {result['objective']}"
        raise ValueError(msg)

    # Case 3 - Invalid Solution ([1.5])
    try:
        result = evaluator.run([1.5])

        msg = f"Expected RuntimeError, but got {result}"
        raise ValueError(msg)

    except RuntimeError as e:
        msg = f"Test for [1.5]: {e}"
        LOGGER.info(msg)

    # Case 4 - Invalid Solution ([1.5, 2.5, 3.5])
    try:
        result = evaluator.run([1.5, 2.5, 3.5])

        msg = f"Expected RuntimeError, but got {result}"
        raise ValueError(msg)
    except RuntimeError as e:
        msg = f"Test for [1.5, 2.5, 3.5]: {e}"
        LOGGER.info(msg)

    # Case 5 - Invalid Solution (["A", 1])
    try:
        result = evaluator.run(["A", 1])

        msg = f"Expected RuntimeError, but got {result}"
        raise ValueError(msg)
    except RuntimeError as e:
        msg = f"Test for ['A', 1]: {e}"
        LOGGER.info(msg)

    # Case 6 - Invalid Solution ([[1, 2]])
    try:
        result = evaluator.run([[1, 2]])

        msg = f"Expected RuntimeError, but got {result}"
        raise ValueError(msg)
    except RuntimeError as e:
        msg = f"Test for [[1, 2]]: {e}"
        LOGGER.info(msg)

    # Case 7 - Invalid Solution (1.5)
    try:
        result = evaluator.run(1.5)

        msg = f"Expected RuntimeError, but got {result}"
        raise ValueError(msg)
    except RuntimeError as e:
        msg = f"Test for 1.5: {e}"
        LOGGER.info(msg)


def test_sphere_sofo_dim1() -> None:
    """Test sphere function with single objective function optimization (SOFO) and decision dimension 1."""
    build_image()
    func = "sphere"
    image_name = "opthub/problem-" + func + ":latest"

    # Initialize the evaluator
    environment: dict[str, str] = {"SPHERE_OPTIMA": json.dumps([[1]])}
    evaluator = Evaluator(image_name, environment)

    # Case 1 - Evaluate 1.5
    result = evaluator.run(1.5)

    if abs(result["objective"] - 0.25) > EPS:
        msg = f"Expected 0.25, but got {result['objective']}"
        raise ValueError(msg)

    # Case 2 - Evaluate [1]
    result = evaluator.run([1])

    if abs(result["objective"] - 0) > EPS:
        msg = f"Expected 0, but got {result['objective']}"
        raise ValueError(msg)

    # Case 3 - Invalid Solution ([1.5, 2.5])
    try:
        result = evaluator.run([1.5, 2.5])

        msg = f"Expected RuntimeError, but got {result}"
        raise ValueError(msg)

    except RuntimeError as e:
        msg = f"Test for [1.5, 2.5]: {e}"
        LOGGER.info(msg)

    # Case 4 - Invalid Solution (["A"])
    try:
        result = evaluator.run(["A"])

        msg = f"Expected RuntimeError, but got {result}"
        raise ValueError(msg)
    except RuntimeError as e:
        msg = f"Test for ['A']: {e}"
        LOGGER.info(msg)


def test_sphere_mofo_dim2() -> None:
    """Test sphere function with multi objective function optimization (MOFO) and decision dimension 2."""
    build_image()
    func = "sphere"
    image_name = "opthub/problem-" + func + ":latest"

    # Initialize the evaluator
    environment: dict[str, str] = {"SPHERE_OPTIMA": json.dumps([[1, 1], [2, 2]])}
    evaluator = Evaluator(image_name, environment)
    objective_dim = 2

    # Case 1 - Evaluate [1.5, 2.5]
    result = evaluator.run([1.5, 2.5])

    if (
        len(result["objective"]) != objective_dim
        or abs(result["objective"][0] - 2.5) > EPS
        or abs(result["objective"][1] - 0.5) > EPS
    ):
        msg = f"Expected [2.5, 0.5], but got {result['objective']}"
        raise ValueError(msg)

    # Case 2 - Invalid Solution ([1.5, "A"])
    try:
        result = evaluator.run([1.5, "A"])

        msg = f"Expected RuntimeError, but got {result}"
        raise ValueError(msg)
    except RuntimeError as e:
        msg = f"Test for [1.5, 'A']: {e}"
        LOGGER.info(msg)

    # Case 3 - Invalid Solution ([1.5])
    try:
        result = evaluator.run([1.5])

        msg = f"Expected RuntimeError, but got {result}"
        raise ValueError(msg)
    except RuntimeError as e:
        msg = f"Test for [1.5]: {e}"
        LOGGER.info(msg)


def test_sphere_mofo_dim1() -> None:
    """Test sphere function with multi objective function optimization (MOFO) and decision dimension 1."""
    build_image()
    func = "sphere"
    image_name = "opthub/problem-" + func + ":latest"

    # Initialize the evaluator
    environment: dict[str, str] = {"SPHERE_OPTIMA": json.dumps([[1], [2.5]])}
    evaluator = Evaluator(image_name, environment)
    objective_dim = 2

    # Case 1 - Evaluate [1.5]
    result = evaluator.run([1.5])

    if (
        len(result["objective"]) != objective_dim
        or abs(result["objective"][0] - 0.25) > EPS
        or abs(result["objective"][1] - 1) > EPS
    ):
        msg = f"Expected [0.25, 1], but got {result['objective']}"
        raise ValueError(msg)

    # Case 2 - Evaluate 1
    result = evaluator.run(1)

    if (
        len(result["objective"]) != objective_dim
        or abs(result["objective"][0] - 0) > EPS
        or abs(result["objective"][1] - 2.25) > EPS
    ):
        msg = f"Expected [0, 2.25], but got {result['objective']}"
        raise ValueError(msg)
