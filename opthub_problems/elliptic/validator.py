"""This file defines the schema for the elliptic function problem."""

import json
from typing import Any, cast

from jsonschema import ValidationError, validate

# Schema to validate the optima of the elliptic function
OPTIMA_SCHEMA = """{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Optima of the elliptic function.",
    "type": "array",
    "minItems": 1,
    "items": {
        "type": "array",
        "minItems": 2,
        "items": {"type": "number"}
    }
}"""


def validate_optima(optima: Any) -> list[list[float]]:  # noqa: ANN401
    """Validate the optima of the elliptic function.

    Args:
        optima (Any): optima environment variable of the elliptic function

    Raises:
        jsonschema.exceptions.ValidationError: if the optima is invalid
    """
    validate(instance=optima, schema=json.loads(OPTIMA_SCHEMA))
    first_vector_length = len(optima[0])
    for vector in optima:
        if len(vector) != first_vector_length:
            message = "All vectors must have the same length."
            raise ValidationError(message)
    return cast(list[list[float]], optima)


# Schema to validate the variable of the elliptic function with n decision dimensions
VARIABLE_ND_SCHEMA = """{{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Variable of the elliptic function with n decision dimensions.",
    "type": "array",
    "minItems": {items},
    "maxItems": {items},
    "items": {{"type": "number"}}
}}"""


def validate_variable(variable: Any, dim: int) -> list[float]:  # noqa: ANN401
    """Validate the variable of the elliptic function.

    Args:
        variable (Any): variable to be validated
        dim (int): number of decided dimensions

    Raises:
        jsonschema.exceptions.ValidationError: if the variable is invalid
    """
    if dim == 1:
        msg = "The elliptic function requires at least 2 decision dimensions."
        raise ValidationError(msg)
    validate(instance=variable, schema=json.loads(VARIABLE_ND_SCHEMA.format(items=dim)))
    return cast(list[float], variable)
