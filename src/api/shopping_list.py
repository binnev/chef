from pydantic import BaseModel, Field

from .recipe import Recipe
from .unit import normalise

Number = int | float
Unit = str
IngredientName = str
RecipeName = str


class Amounts(BaseModel):
    # from "apples" -> display as "enough for x"
    enough_for: list[RecipeName] = []

    # from "4 apples"
    unitless: Number = 0

    # from "4 kg apples"
    units: dict[Unit, Number] = Field(default_factory=dict)


ShoppingList = dict[IngredientName, Amounts]


def merge_recipes(recipes: list[Recipe]) -> ShoppingList:
    """
    Create a combined shopping list by merging the ingredients from all
    multiple recipes.

    Args:
        recipes: the list of recipes we want to generate a shopping list for

    Returns:
        the merged shopping list
    """
    shopping_list = {}
    for recipe in recipes:
        for ing in recipe.ingredients:
            amounts = shopping_list.get(ing.name, Amounts())
            match [ing.amount, ing.unit]:
                case [0, ""]:
                    amounts.enough_for.append(recipe.name)
                case [amount, ""]:
                    amounts.unitless += amount
                case [amount, unit]:
                    amount, unit = normalise(amount, unit)
                    amounts.units[unit] = amounts.units.get(unit, 0) + amount
            shopping_list[ing.name] = amounts

    return shopping_list
