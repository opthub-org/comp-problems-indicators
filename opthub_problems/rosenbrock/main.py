"""Rosenbrock function minimization problem."""

import json
import logging
import sys
from traceback import format_exc

import click

from opthub_problems.rosenbrock.evaluator import evaluate
from opthub_problems.rosenbrock.validator import validate_optima, validate_variable

LOGGER = logging.getLogger(__name__)


@click.command(help="Rosenbrock function minimization problem.")
@click.option(
    "-o",
    "--optima",
    type=str,
    envvar="Rosenbrock_OPTIMA",
    help="Optima of the rosenbrock function.",
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO",
    help="Log level.",
)
def main(optima: str, log_level: str) -> None:
    """Evaluate the given solution on the rosenbrock function minimization problem."""
    logging.basicConfig(level=log_level)

    try:
        # Validate the input
        LOGGER.info("Validating the environment variables...")
        optima = json.loads(optima)
        validated_optima = validate_optima(optima)
        decision_dim = len(validated_optima[0])
        LOGGER.info("Validated.")
        LOGGER.debug("optima: %s", validated_optima)
        LOGGER.debug("decision_dim: %s", decision_dim)

        LOGGER.info("Validating the solution variable.")
        variable = json.loads(input())
        validated_variable = validate_variable(variable, decision_dim)
        LOGGER.info("Validated.")
        LOGGER.debug("variable: %s", validated_variable)

        # Evaluate variable
        LOGGER.info("Evaluating the variable...")
        result = evaluate(validated_variable, validated_optima)
        LOGGER.info("...Evaluated.")

        LOGGER.debug("result: %s", result)

        # Output the result
        LOGGER.info("Outputting the result...")
        sys.stdout.write(json.dumps(result))
        LOGGER.info("...Outputted.")

    except Exception as e:
        LOGGER.exception(format_exc())
        LOGGER.info("Outputting the result...")
        sys.stdout.write(json.dumps({"objective": None, "error": str(e)}))
        LOGGER.info("...Outputted.")


if __name__ == "__main__":
    main()
