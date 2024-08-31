"""The indicator to calculate the best fitness value."""

import json
import logging
import sys
from sys import float_info
from traceback import format_exc

import click

from opthub_indicators.best.scorer import calculate_score
from opthub_indicators.best.validator import validate_solution_to_score, validate_solutions_scored

LOGGER = logging.getLogger(__name__)


@click.command(help="The indicator to calculate the best fitness value.")
@click.option(
    "-m",
    "--float-max",
    type=float,
    default=float_info.max,
    help="Worst value.",
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO",
    help="Log level.",
)
def main(float_max: float, log_level: str) -> None:
    """Calculate the best fitness value."""
    logging.basicConfig(level=log_level)
    try:
        # Validate the input
        LOGGER.info("Validating the input...")
        solution_to_score = json.loads(input())
        solutions_scored = json.loads(input())
        validated_solution_to_score = validate_solution_to_score(solution_to_score)
        validated_solutions_scored = validate_solutions_scored(solutions_scored)
        LOGGER.info("...Validated.")
        LOGGER.debug("solution_to_score: %s", validated_solution_to_score)
        LOGGER.debug("solutions_scored: %s", validated_solutions_scored)

        # Calculate the score
        LOGGER.info("Calculating the score...")
        score = calculate_score(float_max, validated_solution_to_score, validated_solutions_scored)
        LOGGER.info("...Calculated.")
        LOGGER.debug("score: %s", score)

        # Output the result
        LOGGER.info("Outputting the result...")
        sys.stdout.write(json.dumps(score))
        LOGGER.info("...Outputted.")

    except Exception as e:
        LOGGER.exception(format_exc())
        LOGGER.info("Outputting the result...")
        sys.stdout.write(json.dumps({"objective": None, "error": str(e)}))
        LOGGER.info("...Outputted.")


if __name__ == "__main__":
    main()
