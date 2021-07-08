"""
The module provides parameter validation functions common across Metron's components. The scope of validation is all
parameters, except validation of YAML config parameters.
"""

import os
import typing


def type_check(variable: typing.Any, expected_type: typing.Any) -> None:
    """
    Validates if given <variable> is type of <expected_type>.

    Args:
        variable (typing.Any): Variable.
        expected_type (typing.Any): Type.

    Returns (None):

    Exceptions:
        TypeError: Raised if <variable> is not type of <expected_type>.
    """
    if not isinstance(variable, expected_type):
        raise TypeError(f"Given variable value `{variable}` does not meet expected type `{expected_type}`.")


def resolution_validity_check(res_width: int, res_height: int) -> None:
    """
    Validates if resolution has valid dimensions.

    Args:
        res_width (int): Resolution width.
        res_height (int): Resolution height.

    Returns (None):

    Exceptions:
        ValueError: If resolution width or height is lower or equal to zero.
    """
    type_check(res_width, int)
    type_check(res_height, int)
    if res_width <= 0:
        raise ValueError(f"Resolution width `{res_width}` is lower or equal to zero.")
    if res_height <= 0:
        raise ValueError(f"Resolution height `{res_height}` is lower or equal to zero.")


def file_existence_check(file_path: str) -> None:
    """
    Validates if file path exists.

    Args:
        file_path (str): File path.

    Returns (None):

    Exceptions:
        OSError: If file does not exist.
    """
    type_check(file_path, str)
    if not os.path.isfile(file_path):
        raise OSError(f"Path `{file_path}` is not a file.")


def parameter_value_in_range(
    param_value: typing.Union[int, float], lower_bound: typing.Union[int, float], upper_bound: typing.Union[int, float]
) -> None:
    """
    Checks if parameter value is in range <<lower_bound>, <upper_bound>>.

    Args:
        param_value (typing.Union[int, float]): Parameter value.
        lower_bound (typing.Union[int, float]): Lower bound of allowed parameter values.
        upper_bound (typing.Union[int, float]): Upper bound of allowed parameter values.

    Returns (None):

    Exceptions:
        ValueError: If value is not in the range.
    """
    type_check(param_value, (int, float))
    type_check(lower_bound, (int, float))
    type_check(upper_bound, (int, float))
    if param_value < lower_bound or param_value > upper_bound:
        raise ValueError(f"Given `{param_value}` is out of the allowed range" f" <{lower_bound}, {upper_bound}>.")
