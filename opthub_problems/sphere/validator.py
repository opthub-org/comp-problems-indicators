"""This file defines the schema for the sphere function problem."""

# Schema to validate the optima of the sphere function
import json
from typing import Any, cast

from jsonschema import ValidationError, validate

OPTIMA_SCHEMA = """{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Optima of the sphere function.",
    "type": "array",
    "minItems": 1,
    "items": {
        "type": "array",
        "minItems": 1,
        "items": {"type": "number"}
    }
}"""


def validate_optima(optima: Any) -> list[list[float]]:  # noqa: ANN401
    """Validate the optima of the sphere function.

    Args:
        optima (Any): optima environment variable of the sphere function

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


# Schema to validate the variable of the sphere function with n decision dimensions
VARIABLE_ND_SCHEMA = """{{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Variable of the sphere function with n decision dimensions.",
    "type": "array",
    "minItems": {items},
    "maxItems": {items},
    "items": {{"type": "number"}}
}}"""

# Schema to validate the variable of the sphere function with 1 decision dimension
VARIABLE_1D_SCHEMA = """{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Variable of the sphere function with 1 decision dimension.",
    "type": "number"
}"""


def validate_variable(variable: Any, dim: int) -> float | list[float]:  # noqa: ANN401
    """Validate the variable of the sphere function.

    Args:
        variable (Any): variable to be validated
        dim (int): number of decided dimensions

    Raises:
        jsonschema.exceptions.ValidationError: if the variable is invalid
    """
    if dim == 1:
        combined = {
            "anyOf": [json.loads(VARIABLE_1D_SCHEMA), json.loads(VARIABLE_ND_SCHEMA.format(items=1))],
        }
        validate(instance=variable, schema=combined)
    else:
        validate(instance=variable, schema=json.loads(VARIABLE_ND_SCHEMA.format(items=dim)))
    return cast(float | list[float], variable)
