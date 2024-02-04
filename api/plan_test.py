from .ingredient import Ingredient
from .plan import merge_recipes
from .recipe import Recipe

import pytest


def _recipe(ingredient_strings: list[str]) -> Recipe:
    return Recipe(
        name="whatever",
        author="whatever",
        ingredients=[_ing(s) for s in ingredient_strings],
    )


def _ing(s: str) -> Ingredient:
    return Ingredient.from_str(s)


@pytest.mark.parametrize(
    "recipes, expected",
    [
        pytest.param(
            [],
            [],
            id="No recipes -> the shopping list should be empty",
        ),
        pytest.param(
            [_recipe(["poopoo", "peepee"])],
            [_ing("poopoo"), _ing("peepee")],
            id=(
                "Only 1 recipe -> the ingredients list should be the same as "
                "that recipe.ingredients"
            ),
        ),
        # pytest.param(
        #     [
        #         _recipe(["poopoo", "peepee"]),
        #         _recipe(["poopoo", "peepee"]),
        #     ],
        #     [_ing("poopoo"), _ing("peepee")],
        #     id=(
        #         "2 recipes with 'name only' ingredients -> the ingredients "
        #         "should be merged"
        #     ),
        # ),
    ],
)
def test_merge_recipes(recipes: list[Recipe], expected: list[Ingredient]):
    assert merge_recipes(recipes) == expected
