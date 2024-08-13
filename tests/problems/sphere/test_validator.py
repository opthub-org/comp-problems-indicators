"""Test for sphere validator."""

import json
import logging

import pytest
from jsonschema.exceptions import ValidationError

from opthub_problems.sphere.validator import validate_optima, validate_variable

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def test_optima_valid_1d() -> None:
    """Test for the valid optima (1D)."""
    optima_json = json.dumps([[1.0, 2]])
    optima = json.loads(optima_json)
    validate_optima(optima)


def test_optima_valid_2d() -> None:
    """Test for the valid optima (2D)."""
    optima_json = json.dumps([[1.0, 1], [2.0, 2.0]])
    optima = json.loads(optima_json)
    validate_optima(optima)


def test_optima_invalid_empty() -> None:
    """Test for the invalid optima (empty)."""
    optima_json = json.dumps([])
    optima = json.loads(optima_json)
    with pytest.raises(ValidationError):
        validate_optima(optima)


def test_optima_invalid_1d() -> None:
    """Test for the invalid optima (1D)."""
    optima_json = json.dumps([1.0])
    optima = json.loads(optima_json)
    with pytest.raises(ValidationError):
        validate_optima(optima)


def test_optima_invalid_string() -> None:
    """Test for the invalid optima (String)."""
    optima_json = json.dumps([[1, "B"]])
    optima = json.loads(optima_json)
    with pytest.raises(ValidationError):
        validate_optima(optima)


def test_optima_invalid_nest() -> None:
    """Test for the invalid optima (Nest)."""
    optima_json = json.dumps([[[1, 2]]])
    optima = json.loads(optima_json)
    with pytest.raises(ValidationError):
        validate_optima(optima)


def test_optima_invalid_not_unified_dimension() -> None:
    """Test for the invalid optima (Not unified dimension)."""
    optima_json = json.dumps([[1.0, 2.0], [3.0, 4.0, 5.0]])
    optima = json.loads(optima_json)
    with pytest.raises(ValidationError):
        validate_optima(optima)


def test_variable_valid_1d_float() -> None:
    """Test for the Valid variable (1D float)."""
    variable_json = json.dumps(1.0)
    variable = json.loads(variable_json)
    validate_variable(variable, 1)


def test_variable_valid_1d_int() -> None:
    """Test for the valid variable (1D int)."""
    variable_json = json.dumps(1)
    variable = json.loads(variable_json)
    validate_variable(variable, 1)


def test_variable_valid_1d_float_list() -> None:
    """Test for the valid variable (1D float list)."""
    variable_json = json.dumps([1.0])
    variable = json.loads(variable_json)
    validate_variable(variable, 1)


def test_variable_invalid_1d_string() -> None:
    """Test for the invalid variable (1D string)."""
    variable_json = json.dumps("A")
    variable = json.loads(variable_json)
    with pytest.raises(ValidationError):
        validate_variable(variable, 1)


def test_variable_valid_2d() -> None:
    """Test for the valid variable (2D list)."""
    variable_json = json.dumps([1, 2.0])
    variable = json.loads(variable_json)
    validate_variable(variable, 2)


def test_variable_invalid_empty() -> None:
    """Test for the invalid variable (Empty)."""
    variable_json = json.dumps([])
    variable = json.loads(variable_json)
    with pytest.raises(ValidationError):
        validate_variable(variable, 1)


def test_variable_invalid_2d_with_string() -> None:
    """Test for the invalid variable (2D with string)."""
    variable_json = json.dumps(["A", 1])
    variable = json.loads(variable_json)
    with pytest.raises(ValidationError):
        validate_variable(variable, 2)


def test_variable_invalid_nested() -> None:
    """Test for the invalid variable (Nested)."""
    variable_json = json.dumps([[1, 2]])
    variable = json.loads(variable_json)
    with pytest.raises(ValidationError):
        validate_variable(variable, 2)


def test_variable_invalid_not_matched_dimension() -> None:
    """Test for the invalid variable (Not match dimension)."""
    variable_json = json.dumps([1.0, 2.0, 3.0])
    variable = json.loads(variable_json)
    with pytest.raises(ValidationError):
        validate_variable(variable, 2)
