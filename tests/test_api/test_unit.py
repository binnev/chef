from collections import namedtuple

import pytest

from src.api.unit import (
    normalise,
    CONVERSIONS,
    INTERNAL_UNITS,
    ALIASES,
)


@pytest.mark.better_parametrize(
    testcase := namedtuple("_", "args, expected"),
    [
        testcase(args=(1, "g"), expected=(1, "g")),
        testcase(args=(1, "ml"), expected=(1, "ml")),
        testcase(args=(5, "kg"), expected=(5000, "g")),
        testcase(args=(5, "kilos"), expected=(5000, "g")),
        testcase(args=(10, "fluid ounces"), expected=(300, "ml")),
        testcase(args=(10, "fl oz"), expected=(300, "ml")),
        testcase(args=(2, "L"), expected=(2000, "ml")),
    ],
)
def test_normalise(
    args: tuple[int | float, str],
    expected: tuple[int | float, str],
):
    result = normalise(*args)
    assert result == expected


@pytest.mark.parametrize("unit", ALIASES.keys())
def test_all_units_can_be_converted_to_internal(unit: str):
    """
    Check all the known units can be converted to our internal units
    """
    assert unit in CONVERSIONS
    _, converted_unit = CONVERSIONS[unit]
    assert converted_unit in INTERNAL_UNITS


@pytest.mark.parametrize("_, unit", CONVERSIONS.values())
def test_preferred_denominations_all_point_to_internal_units(_, unit: str):
    assert unit in INTERNAL_UNITS
