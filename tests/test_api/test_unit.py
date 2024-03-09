from collections import namedtuple

import pytest

from src.api.unit import (
    normalise,
    CONVERSIONS,
    INTERNAL_UNITS,
    ALIASES,
)


@pytest.mark.better_parametrize(
    testcase := namedtuple("_", "args, expected, id"),
    [
        testcase(
            id="sanity check",
            args=(1, "g"),
            expected=(1, "g"),
        ),
        testcase(
            id="sanity check",
            args=(1, "ml"),
            expected=(1, "ml"),
        ),
        testcase(
            id="convert denomination",
            args=(5, "kg"),
            expected=(5000, "g"),
        ),
        testcase(
            id="convert denomination and alias",
            args=(5, "kilos"),
            expected=(5000, "g"),
        ),
        testcase(
            id="convert amount",
            args=(10, "fl oz"),
            expected=(300, "ml"),
        ),
        testcase(
            id="convert amount and alias",
            args=(10, "fluid ounces"),
            expected=(300, "ml"),
        ),
        testcase(
            id="handle uppercase -> lowercase automatically",
            args=(2, "L"),
            expected=(2000, "ml"),
        ),
        testcase(
            id="plural to singular",
            args=(3, "sprigs"),
            expected=(3, "sprig"),
        ),
        testcase(
            id="singular to singular shouldn't fail",
            args=(3, "sprig"),
            expected=(3, "sprig"),
        ),
        testcase(
            id="unknown unit should not cause an error",
            args=(420, "foobars"),
            expected=(420, "foobars"),
        ),
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
