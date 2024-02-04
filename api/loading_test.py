import pytest
from .loading import preprocess_yaml
from .ingredient import IngredientParseError, parse_ingredient_str


@pytest.mark.parametrize(
    "recipe_dict, expected",
    [
        pytest.param(
            {},
            {},
            id=(
                "If ingredients are missing from the input, then the output "
                "should also not contain them"
            ),
        ),
        pytest.param(
            {"ingredients": []},
            {"ingredients": []},
            id="If ingredients are empty, output should be unchanged",
        ),
        pytest.param(
            {"ingredients": ["apples"]},
            {"ingredients": [parse_ingredient_str("apples")]},
            id="Input is populated; output should contain parsed ingredients",
        ),
    ],
)
def test_preprocess_yaml(
    recipe_dict: dict,
    expected: dict | IngredientParseError,
):
    if isinstance(expected, IngredientParseError):
        with pytest.raises(expected.__class__) as e:
            preprocess_yaml(recipe_dict)
        assert isinstance(e.value, IngredientParseError)
        assert str(e.value) == str(expected)

    else:
        assert preprocess_yaml(recipe_dict) == expected
