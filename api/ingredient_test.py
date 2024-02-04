import pytest
from api.ingredient import ParseError, Ingredient


@pytest.mark.parametrize(
    "s, expected",
    [
        pytest.param(
            "coriander",
            Ingredient(name="coriander", amount=0, unit="", prep=""),
            id="ingredient",
        ),
        pytest.param(
            "coriander;",
            Ingredient(name="coriander", amount=0, unit="", prep=""),
            id="ingredient w trailing semicolon",
        ),
        pytest.param(
            "coriander; chopped",
            Ingredient(name="coriander", amount=0, unit="", prep="chopped"),
            id="ingredient w prep",
        ),
        pytest.param(
            "2, potatoes",
            Ingredient(name="potatoes", amount=2, unit="", prep=""),
            id="amount, ingredient",
        ),
        pytest.param(
            "2, potatoes; peeled",
            Ingredient(name="potatoes", amount=2, unit="", prep="peeled"),
            id="amount, ingredient, prep",
        ),
        pytest.param(
            "2, kg, potatoes",
            Ingredient(name="potatoes", amount=2, unit="kg", prep=""),
            id="amount, unit, ingredient",
        ),
        pytest.param(
            "2, kg, potatoes; chopped",
            Ingredient(name="potatoes", amount=2, unit="kg", prep="chopped"),
            id="amount, unit, ingredient, prep",
        ),
        pytest.param(
            "  2  ,   kg   ,    potatoes   ;  chopped   ",
            Ingredient(name="potatoes", amount=2, unit="kg", prep="chopped"),
            id="padded spaces should be trimmed",
        ),
        pytest.param(
            "",
            ParseError("empty input"),
            id="empty input -> error",
        ),
        pytest.param(
            "       ",
            ParseError("empty input"),
            id="non-empty input but it's just spaces",
        ),
        pytest.param(
            "; chopped",
            ParseError("Got prep but no ingredients"),
            id="no ingredient error",
        ),
        pytest.param(
            "2, kg, potatoes, chopped",
            ParseError("Too many commas"),
            id="too many commas error",
        ),
    ],
)
def test_from_str(s: str, expected: Ingredient | ParseError):
    if isinstance(expected, ParseError):
        with pytest.raises(expected.__class__) as e:
            Ingredient.from_str(s)
        # for some reason `e.value == expected` fails even when they're the same
        assert isinstance(e.value, ParseError)
        assert str(e.value) == str(expected)

    else:
        assert Ingredient.from_str(s) == expected
