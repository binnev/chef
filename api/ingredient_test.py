import pytest
from api.ingredient import (
    IngredientParseError,
    parse_ingredient_str,
)


@pytest.mark.parametrize(
    "s, expected",
    [
        pytest.param(
            "coriander",
            dict(name="coriander"),
            id="ingredient",
        ),
        pytest.param(
            "coriander;",
            dict(name="coriander"),
            id="ingredient w trailing semicolon",
        ),
        pytest.param(
            "coriander; chopped",
            dict(name="coriander", prep="chopped"),
            id="ingredient w prep",
        ),
        pytest.param(
            "2, potatoes",
            dict(name="potatoes", amount=2),
            id="amount, ingredient",
        ),
        pytest.param(
            "2, potatoes; peeled",
            dict(name="potatoes", amount=2, prep="peeled"),
            id="amount, ingredient, prep",
        ),
        pytest.param(
            "2, kg, potatoes",
            dict(name="potatoes", amount=2, unit="kg"),
            id="amount, unit, ingredient",
        ),
        pytest.param(
            "2, kg, potatoes; chopped",
            dict(name="potatoes", amount=2, unit="kg", prep="chopped"),
            id="amount, unit, ingredient, prep",
        ),
        pytest.param(
            "  2  ,   kg   ,    potatoes   ;  chopped   ",
            dict(name="potatoes", amount=2, unit="kg", prep="chopped"),
            id="padded spaces should be trimmed",
        ),
        pytest.param(
            "",
            IngredientParseError("empty input"),
            id="empty input -> error",
        ),
        pytest.param(
            ",",
            IngredientParseError("empty value: name"),
            id="single comma",
        ),
        pytest.param(
            ",apples",
            IngredientParseError("empty value: amount"),
            id="amount is empty str",
        ),
        pytest.param(
            "       ",
            IngredientParseError("empty input"),
            id="non-empty input but it's just spaces",
        ),
        pytest.param(
            "; chopped",
            IngredientParseError("Got prep but no ingredients"),
            id="no ingredient error",
        ),
        pytest.param(
            ";",
            IngredientParseError("Got prep but no ingredients"),
            id="single semicolon",
        ),
        pytest.param(
            "2, kg, potatoes, chopped",
            IngredientParseError("Too many commas"),
            id="too many commas error",
        ),
    ],
)
def test_parse_ingredient_str(s: str, expected: dict | IngredientParseError):
    if isinstance(expected, IngredientParseError):
        with pytest.raises(expected.__class__) as e:
            parse_ingredient_str(s)
        # for some reason `e.value == expected` fails even when they're the same
        assert isinstance(e.value, IngredientParseError)
        assert str(e.value) == str(expected)

    else:
        assert parse_ingredient_str(s) == expected
