"""Sphere function minimization problem."""

import json
import logging
import sys
from traceback import format_exc
from typing import cast

import click
import numpy as np
from jsonschema import validate

from problem_opt_benchmarks.sphere.schema import OPTIMA_SCHEMA, VARIABLE_1D_SCHEMA, VARIABLE_ND_SCHEMA

LOGGER = logging.getLogger(__name__)


def sphere(var: list[float], opt: list[list[float]]) -> list[float]:
    """Calculate the objective value of the sphere function.

    Args:
        var (list[float]): decision variable
        opt (list[list[float]]): optima of the sphere function

    Returns:
        list[float]: objective value
    """
    var_arr = np.array(var, dtype=float)
    opt_arr = np.array(opt, dtype=float)
    obj_arr = np.sum((var_arr - opt_arr) ** 2, axis=1)
    return cast(list[float], obj_arr.tolist())


@click.command(help="Sphere function minimization problem.")
@click.option(
    "-o",
    "--optima",
    type=str,
    envvar="SPHERE_OPTIMA",
    help="Optima of the sphere function.",
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO",
    help="Log level.",
)
def main(optima: str, log_level: str) -> None:
    """Evaluate the given solution on the sphere function minimization problem."""
    logging.basicConfig(level=log_level)

    try:
        # Validate the input
        LOGGER.info("Validating the input...")
        opt = json.loads(optima)
        validate(instance=opt, schema=json.loads(OPTIMA_SCHEMA))

        decision_dim = len(opt[0])
        var = json.loads(input())

        if decision_dim == 1:
            combined = {
                "anyOf": [json.loads(VARIABLE_1D_SCHEMA), json.loads(VARIABLE_ND_SCHEMA.format(items=1))],
            }
            validate(instance=var, schema=combined)
        else:
            validate(instance=var, schema=json.loads(VARIABLE_ND_SCHEMA.format(items=decision_dim)))
        LOGGER.info("...Validated.")

        LOGGER.debug("variable: %s", var)
        LOGGER.debug("optima: %s", opt)
        LOGGER.debug("decision_dim: %s", decision_dim)

        # Evaluate variable
        LOGGER.info("Evaluating the variable...")
        objective = sphere(var, opt)
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
