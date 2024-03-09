from collections import namedtuple

import pytest

from src.api.ingredient import Ingredient
from src.api.recipe import Recipe
from src.api.shopping_list import merge_recipes, Amounts


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


@pytest.mark.better_parametrize(
    testcase := namedtuple("_", "recipes, expected, id"),
    [
        testcase(
            id="empty case",
            recipes=[],
            expected={},
        ),
        testcase(
            id="1 recipe; amountless",
            recipes=[_recipe(["poopoo", "peepee"])],
            expected={
                "poopoo": Amounts(enough_for=["whatever"]),
                "peepee": Amounts(enough_for=["whatever"]),
            },
        ),
        testcase(
            id="1 recipe; mix of units/amounts and amountless",
            recipes=[_recipe(["1, kg, poopoo", "peepee"])],
            expected={
                "poopoo": Amounts(units={"g": 1000}),
                "peepee": Amounts(enough_for=["whatever"]),
            },
        ),
        testcase(
            id="same units should be merged",
            recipes=[
                _recipe(["1, kg, poopoo", "peepee"]),
                _recipe(["69, kg, poopoo", "10, weewee"]),
            ],
            expected={
                "poopoo": Amounts(units={"g": 70000}),
                "peepee": Amounts(enough_for=["whatever"]),
                "weewee": Amounts(unitless=10),
            },
        ),
        testcase(
            id="merge multiple amountless",
            recipes=[
                _recipe(["poopoo", "peepee"]),
                _recipe(["poopoo"], name="second one"),
            ],
            expected={
                "poopoo": Amounts(enough_for=["whatever", "second one"]),
                "peepee": Amounts(enough_for=["whatever"]),
            },
        ),
        testcase(
            id="all types",
            recipes=[
                _recipe(["poopoo", "2, poopoo", "3, kg, poopoo"], name="one"),
                _recipe(["poopoo", "5, poopoo", "500, g, poopoo"], name="two"),
            ],
            expected={
                "poopoo": Amounts(
                    enough_for=["one", "two"],
                    unitless=7,
                    units={"g": 3500},
                ),
            },
        ),
    ],
)
def test_merge_recipes(recipes: list[Recipe], expected: list[Ingredient]):
    assert merge_recipes(recipes) == expected
