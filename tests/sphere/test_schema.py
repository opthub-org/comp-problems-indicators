"""This module implements tests for the schema of the sphere function problem."""

import json
import logging

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from problem_opt_benchmarks.sphere.schema import OPTIMA_SCHEMA, VARIABLE_1D_SCHEMA, VARIABLE_ND_SCHEMA

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def test_optima() -> None:
    """Test the schema for the optima of the sphere function."""
    # Case 1 - Valid Optima (1D)
    optima_json = json.dumps([[1.0, 2]])
    optima = json.loads(optima_json)
    validate(instance=optima, schema=json.loads(OPTIMA_SCHEMA))

    # Case 2 - Valid Optima (2D)
    optima_json = json.dumps([[1.0, 1], [2.0, 2.0]])
    optima = json.loads(optima_json)
    validate(instance=optima, schema=json.loads(OPTIMA_SCHEMA))

    # Case 3 - Invalid Optima (Empty)
    optima_json = json.dumps([])
    optima = json.loads(optima_json)
    try:
        validate(instance=optima, schema=json.loads(OPTIMA_SCHEMA))
        msg = "Expected ValidationError, but got None."
        raise ValueError(msg)
    except ValidationError as e:
        msg = f"Test for []: {e}"
        LOGGER.info(msg)

    # Case 4 - Invalid Optima (1D)
    optima_json = json.dumps([1.0])
    optima = json.loads(optima_json)
    try:
        validate(instance=optima, schema=json.loads(OPTIMA_SCHEMA))
        msg = "Expected ValidationError, but got None."
        raise ValueError(msg)
    except ValidationError as e:
        msg = f"Test for [1.0]: {e}"
        LOGGER.info(msg)

    # Case 5 - Invalid Optima with string
    optima_json = json.dumps([[1, "B"]])
    optima = json.loads(optima_json)
    try:
        validate(instance=optima, schema=json.loads(OPTIMA_SCHEMA))
        msg = "Expected ValidationError, but got None."
        raise ValueError(msg)
    except ValidationError as e:
        msg = f"Test for [[1, 'B']]: {e}"
        LOGGER.info(msg)

    # Case 6 - Invalid Optima (2D)
    optima_json = json.dumps([[[1, 2]]])
    optima = json.loads(optima_json)
    try:
        validate(instance=optima, schema=json.loads(OPTIMA_SCHEMA))
        msg = "Expected ValidationError, but got None."
        raise ValueError(msg)
    except ValidationError as e:
        msg = f"Test for [[[1, 2]]]: {e}"
        LOGGER.info(msg)

    # Case 7 - Invalid Optima (Invalid number of items)
    optima_json = json.dumps([[1.0, 2.0], [3.0, 4.0, 5.0]])
    optima = json.loads(optima_json)
    try:
        validate(instance=optima, schema=json.loads(OPTIMA_SCHEMA))
        msg = "Expected ValidationError, but got None."
        raise ValueError(msg)
    except ValidationError as e:
        msg = f"Test for [[1.0, 2.0], [3.0, 4.0, 5.0]]: {e}"
        LOGGER.info(msg)


def test_variable_1d() -> None:
    """Test the schema for the variable of the sphere function with 1 decision dimension."""
    # Case 1 - Valid Variable (number)
    variable_json = json.dumps(1.0)
    variable = json.loads(variable_json)
    validate(instance=variable, schema=json.loads(VARIABLE_1D_SCHEMA))

    # Case 2 - Valid Variable (number)
    variable_json = json.dumps(1)
    variable = json.loads(variable_json)
    validate(instance=variable, schema=json.loads(VARIABLE_1D_SCHEMA))

    # Case 3 - Invalid Variable (list)
    variable_json = json.dumps([1.0])
    variable = json.loads(variable_json)

    try:
        validate(instance=variable, schema=json.loads(VARIABLE_1D_SCHEMA))
        msg = "Expected ValidationError, but got None."
        raise ValueError(msg)
    except ValidationError as e:
        msg = f"Test for [1.0]: {e}"
        LOGGER.info(msg)

    # Case 4 - Invalid Variable with string
    variable_json = json.dumps("A")
    variable = json.loads(variable_json)
    try:
        validate(instance=variable, schema=json.loads(VARIABLE_1D_SCHEMA))
        msg = "Expected ValidationError, but got None."
        raise ValueError(msg)
    except ValidationError as e:
        msg = f"Test for 'A': {e}"
        LOGGER.info(msg)


def test_variable_nd() -> None:
    """Test the schema for the variable of the sphere function with n decision dimensions."""
    LOGGER.info(VARIABLE_ND_SCHEMA.format(items=1))
    # Case 1 - Valid Variable (1D)
    variable_json = json.dumps([1.0])
    variable = json.loads(variable_json)
    validate(instance=variable, schema=json.loads(VARIABLE_ND_SCHEMA.format(items=1)))

    # Case 2 - Valid Variable (2D)
    variable_json = json.dumps([1, 2.0])
    variable = json.loads(variable_json)
    validate(instance=variable, schema=json.loads(VARIABLE_ND_SCHEMA.format(items=2)))

    # Case 3 - Invalid Variable (Empty)
    variable_json = json.dumps([])
    variable = json.loads(variable_json)
    try:
        validate(instance=variable, schema=json.loads(VARIABLE_ND_SCHEMA.format(items=1)))
        msg = "Expected ValidationError, but got None."
        raise ValueError(msg)
    except ValidationError as e:
        msg = f"Test for []: {e}"
        LOGGER.info(msg)

    # Case 4 - Invalid Variable (number)
    variable_json = json.dumps(1.0)
    variable = json.loads(variable_json)
    try:
        validate(instance=variable, schema=json.loads(VARIABLE_ND_SCHEMA.format(items=1)))
        msg = "Expected ValidationError, but got None."
        raise ValueError(msg)
    except ValidationError as e:
        msg = f"Test for 1.0: {e}"
        LOGGER.info(msg)

    # Case 5 - Invalid Variable with string
    variable_json = json.dumps(["A", 1])
    variable = json.loads(variable_json)
    try:
        validate(instance=variable, schema=json.loads(VARIABLE_ND_SCHEMA.format(items=2)))
        msg = "Expected ValidationError, but got None."
        raise ValueError(msg)
    except ValidationError as e:
        msg = f"Test for ['A', 1]: {e}"
        LOGGER.info(msg)

    # Case 6 - Invalid Variable (2D)
    variable_json = json.dumps([[1, 2]])
    variable = json.loads(variable_json)
    try:
        validate(instance=variable, schema=json.loads(VARIABLE_ND_SCHEMA.format(items=2)))
        msg = "Expected ValidationError, but got None."
        raise ValueError(msg)
    except ValidationError as e:
        msg = f"Test for [[[1, 2]]]: {e}"
        LOGGER.info(msg)

    # Case 7 - Invalid Variable (Invalid number of items)
    variable_json = json.dumps([1.0, 2.0, 3.0])
    variable = json.loads(variable_json)
    try:
        validate(instance=variable, schema=json.loads(VARIABLE_ND_SCHEMA.format(items=2)))
        msg = "Expected ValidationError, but got None."
        raise ValueError(msg)
    except ValidationError as e:
        msg = f"Test for [1.0, 2.0, 3.0]: {e}"
        LOGGER.info(msg)
