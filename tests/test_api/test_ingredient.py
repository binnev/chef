import pytest
from src.api.ingredient import (
    ParseIngredientError,
    parse_ingredient_str,
    Ingredient,
    _parse_number,
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
            "2.5, potatoes",
            dict(name="potatoes", amount=2.5),
            id="amount (float), ingredient",
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
            "0.25, cup, cabbage;  shredded",
            dict(name="cabbage", amount=0.25, unit="cup", prep="shredded"),
            id="this one gave me trouble in the wild",
        ),
        pytest.param(
            "",
            ParseIngredientError("empty input"),
            id="empty input -> error",
        ),
        pytest.param(
            ",",
            ParseIngredientError("empty value: name"),
            id="single comma",
        ),
        pytest.param(
            ",apples",
            ParseIngredientError("empty value: amount"),
            id="amount is empty str",
        ),
        pytest.param(
            "       ",
            ParseIngredientError("empty input"),
            id="non-empty input but it's just spaces",
        ),
        pytest.param(
            "; chopped",
            ParseIngredientError("Got prep but no ingredients"),
            id="no ingredient error",
        ),
        pytest.param(
            ";",
            ParseIngredientError("Got prep but no ingredients"),
            id="single semicolon",
        ),
        pytest.param(
            "2, kg, potatoes, chopped",
            ParseIngredientError("Too many commas"),
            id="too many commas error",
        ),
    ],
)
def test_parse_ingredient_str(s: str, expected: dict | ParseIngredientError):
    if isinstance(expected, ParseIngredientError):
        with pytest.raises(expected.__class__) as e:
            parse_ingredient_str(s)
        # for some reason `e.value == expected` fails even when they're the same
        assert str(e.value).startswith(str(expected))

    else:
        assert parse_ingredient_str(s) == expected


@pytest.mark.parametrize(
    "s, expected",
    [
        ("", 0),
        ("0", 0),
        ("1", 1),
        ("1.2", 1.2),
        ("0.25", 0.25),
        ("1,2", ParseIngredientError("invalid number: '1,2'")),
        ("aaa", ParseIngredientError("invalid number: 'aaa'")),
    ],
)
def test__parse_number(s: str, expected: int | float | ParseIngredientError):
    if isinstance(expected, ParseIngredientError):
        with pytest.raises(expected.__class__) as e:
            _parse_number(s)
        assert str(e.value) == str(expected)

    else:
        assert _parse_number(s) == expected


@pytest.mark.parametrize(
    "ingredient, expected",
    [
        (Ingredient(name="apples"), "apples"),
        (Ingredient(name="apples", prep="chopped"), "apples, chopped"),
        (Ingredient(name="apples", amount=2), "2 apples"),
        (
            Ingredient(name="apples", amount=2, prep="chopped"),
            "2 apples, chopped",
        ),
        (Ingredient(name="apples", amount=2.5), "2.5 apples"),
        (Ingredient(name="apples", amount=2, unit="kg"), "2 kg apples"),
        (
            Ingredient(name="apples", amount=2, unit="kg", prep="chopped"),
            "2 kg apples, chopped",
        ),
    ],
)
def test_str(ingredient: Ingredient, expected: str):
    assert str(ingredient) == expected
