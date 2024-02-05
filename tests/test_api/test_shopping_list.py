import pytest

from api.ingredient import Ingredient
from api.recipe import Recipe
from api.shopping_list import merge_recipes, Amounts


def _recipe(
    ingredient_strings: list[str],
    author: str = "whatever",
    name: str = "whatever",
) -> Recipe:
    return Recipe(
        name=name,
        author=author,
        ingredients=[Ingredient.from_str(s) for s in ingredient_strings],
    )


@pytest.mark.parametrize(
    "recipes, expected",
    [
        pytest.param(
            [],
            {},
            id="No recipes -> the shopping list should be empty",
        ),
        pytest.param(
            [_recipe(["poopoo", "peepee"])],
            {
                "poopoo": Amounts(enough_for=["whatever"]),
                "peepee": Amounts(enough_for=["whatever"]),
            },
        ),
        pytest.param(
            [_recipe(["1, kg, poopoo", "peepee"])],
            {
                "poopoo": Amounts(units={"kg": 1}),
                "peepee": Amounts(enough_for=["whatever"]),
            },
        ),
        pytest.param(
            [
                _recipe(["1, kg, poopoo", "peepee"]),
                _recipe(["69, kg, poopoo", "10, weewee"]),
            ],
            {
                "poopoo": Amounts(units={"kg": 70}),
                "peepee": Amounts(enough_for=["whatever"]),
                "weewee": Amounts(unitless=10),
            },
        ),
        pytest.param(
            [
                _recipe(["poopoo", "peepee"]),
                _recipe(["poopoo"], name="second one"),
            ],
            {
                "poopoo": Amounts(enough_for=["whatever", "second one"]),
                "peepee": Amounts(enough_for=["whatever"]),
            },
        ),
        pytest.param(
            [
                _recipe(["poopoo", "2, poopoo", "3, kg, poopoo"], name="one"),
                _recipe(["poopoo", "5, poopoo", "7, kg, poopoo"], name="two"),
            ],
            {
                "poopoo": Amounts(
                    enough_for=["one", "two"],
                    unitless=7,
                    units={"kg": 10},
                ),
            },
        ),
    ],
)
def test_merge_recipes(recipes: list[Recipe], expected: list[Ingredient]):
    assert merge_recipes(recipes) == expected
