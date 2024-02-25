import pytest
import yaml

from api.ingredient import Ingredient
from api.ingredient import IngredientParseError, parse_ingredient_str
from api.recipe import Recipe
from api.recipe.formats import serialize_yaml
from api.recipe.utils import preprocess_yaml


@pytest.mark.parametrize(
    "recipe_dict, expected",
    [
        pytest.param(
            {
                "name": "foo",
                "author": "bar",
                "ingredients": [{"name": "poopoo"}],
            },
            Recipe(
                name="foo",
                author="bar",
                ingredients=[Ingredient(name="poopoo")],
            ),
            id="minimal inputs",
        ),
        pytest.param(
            {
                "name": "potatoes",
                "author": "me",
                "prep_minutes": 69,
                "cook_minutes": 420,
                "servings": 666,
                "source": "https://source.com",
                "image": "https://image.com",
                "notes": "I am a potato. A potato wrote this recipe.",
                "ingredients": [
                    {
                        "name": "potatoes",
                        "amount": 2,
                        "unit": "kg",
                        "prep": "chopped",
                    }
                ],
                "method": ["put the potatoes in boiling water", "eat them"],
                "equipment": ["big pan", "kitchen sink"],
            },
            Recipe(
                name="potatoes",
                author="me",
                prep_minutes=69,
                cook_minutes=420,
                servings=666,
                source="https://source.com",
                image="https://image.com",
                notes="I am a potato. A potato wrote this recipe.",
                ingredients=[
                    Ingredient(
                        name="potatoes",
                        amount=2,
                        unit="kg",
                        prep="chopped",
                    )
                ],
                method=["put the potatoes in boiling " "water", "eat them"],
                equipment=["big pan", "kitchen sink"],
            ),
            id="full input",
        ),
    ],
)
def test_init_happy(recipe_dict: dict, expected: Recipe):
    assert Recipe(**recipe_dict) == expected


RECIPES = [
    Recipe(name="foo", author="bar", ingredients=[]),
    Recipe(name="baz", author="qux", ingredients=[]),
]


@pytest.mark.parametrize(
    "query, recipes, expected",
    [
        pytest.param("", RECIPES, [], id="empty query"),
        pytest.param("foo", [], [], id="empty recipes"),
        pytest.param("fart", RECIPES, [], id="query not found"),
        pytest.param(
            "foo",
            RECIPES,
            [Recipe(name="foo", author="bar", ingredients=[])],
            id="single term found in single recipe",
        ),
        pytest.param(
            "ba",
            RECIPES,
            RECIPES,
            id="single term was found in multiple recipes",
        ),
        pytest.param(
            "foo qux",
            RECIPES,
            RECIPES,
            id="multiple query terms were found in multiple recipes",
        ),
    ],
)
def test_search(
    query: str,
    recipes: list[Recipe],
    expected: list[Recipe],
):
    assert Recipe.search(query, recipes) == expected


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
        assert str(e.value) == str(expected)

    else:
        assert preprocess_yaml(recipe_dict) == expected


def test_serialize_yaml():
    recipe_dict = {
        "name": "foo",
        "author": "bar",
        "ingredients": [
            {"name": "poopoo"},
            {"name": "train", "amount": 4},
            {"name": "weewee", "amount": 4, "unit": "l"},
        ],
    }
    recipe = Recipe.validate(recipe_dict)
    yaml_str = serialize_yaml(recipe)
    # the order of keys in the yaml string output is not reliable, so we have
    # to parse back to dict
    yaml_dict = yaml.safe_load(yaml_str)
    assert yaml_dict == {
        "name": "foo",
        "author": "bar",
        "ingredients": [
            "poopoo",
            "4, train",
            "4, l, weewee",
        ],
    }
