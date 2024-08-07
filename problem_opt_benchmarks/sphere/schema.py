"""This file defines the schema for the sphere problem."""

# Schema to validate the optima of the sphere function
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
