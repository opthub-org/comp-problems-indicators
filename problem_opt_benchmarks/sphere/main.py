"""Sphere function minimization problem."""

import json
import logging
import sys
from traceback import format_exc
from typing import cast

import click
import numpy as np

from problem_opt_benchmarks.utils.validation import parse_optima, parse_variable

LOGGER = logging.getLogger(__name__)


def sphere(variable: list[float], optimal: list[list[float]]) -> list[float]:
    """Calculate the sphere function value.

    Args:
        variable (list[float]): decision variable
        optimal (list[list[float]]): optimal value

    Returns:
        list[float]: objective value
    """
    variable_arr = np.array(variable, dtype=float)
    optima_arr = np.array(optimal, dtype=float)
    eval_arr = np.sum((variable_arr - optima_arr) ** 2, axis=1)
    return cast(list[float], eval_arr.tolist())


@click.command(help="Sphere function minimization problem.")
@click.option(
    "-o",
    "--optima",
    type=str,
    envvar="SPHERE_OPTIMA",
    help="Optimal value for the sphere function.",
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO",
    help="Log level.",
)
def main(optima: str, log_level: str) -> None:
    """Evaluate a given solution on a multi-objective unconstrained sphere problem."""
    logging.basicConfig(level=log_level)

    try:
        # Validate the input
        LOGGER.info("Parsing the input...")
        parsed_optima = parse_optima(optima)
        decision_dim = len(parsed_optima[0])
        parsed_variable = parse_variable(input(), decision_dim)
        LOGGER.info("...Parsed.")

        LOGGER.debug("variable: %s", parsed_variable)
        LOGGER.debug("optima: %s", parsed_optima)
        LOGGER.debug("decision_dim: %s", decision_dim)

        # Evaluate variable
        LOGGER.info("Evaluating the variable...")
        objective = sphere(parsed_variable, parsed_optima)
        LOGGER.info("...Evaluated.")

        LOGGER.debug("objective: %s", objective)

        # Output the result
        LOGGER.info("Outputting the result...")
        sys.stdout.write(json.dumps({"objective": objective[0] if len(objective) == 1 else objective}))
        LOGGER.info("...Outputted.")

    except Exception as e:
        LOGGER.exception(format_exc())
        LOGGER.info("Outputting the result...")
        sys.stdout.write(json.dumps({"objective": None, "error": str(e)}))
        LOGGER.info("...Outputted.")


if __name__ == "__main__":
    main()
