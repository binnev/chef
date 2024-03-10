"""
Handles the merging of multiple ingredient lists into one shopping list.
"""

from pydantic import BaseModel, Field

from .recipe import Recipe
from .unit import normalise

Number = int | float
Unit = str
IngredientName = str
RecipeName = str


class MergedIngredient(BaseModel):
    """
    Container class to hold merged Ingredients. Handles a mixture of
    amountless, unitless, and fully populated Ingredients. It is not possible
    to merge a fully populated unit with an amountless unit -- e.g. "2, kg,
    potatoes" and "potatoes". This is why we need the following attributes

    Attributes:
        amountless: for Ingredients without an amount, we just want to keep
            track of which recipes we need them for. So that instead of seeing
            "coriander" in the shopping list, we see "coriander: enough for
            recipes A, B, C"
        unitless: for Ingredients with no units, we can simply add the amounts,
            e.g. "2 apples" + "3 apples" = "5 apples"
        units: a mapping of amounts to units. For units that can't be merged
            like "cm" and "g"
    """

    # from "apples" -> display as "enough for x"
    amountless: list[RecipeName] = []

    # from "4 apples"
    unitless: Number = 0

    # from "4 kg apples"
    units: dict[Unit, Number] = Field(default_factory=dict)


ShoppingList = dict[IngredientName, MergedIngredient]


def merge_recipes(recipes: list[Recipe]) -> ShoppingList:
    """
    Create a combined shopping list by merging the ingredients from multiple
    recipes.

    Args:
        recipes: the list of recipes we want to generate a shopping list for

    Returns:
        the merged shopping list
    """
    shopping_list = {}
    for recipe in recipes:
        for ing in recipe.ingredients:
            merged = shopping_list.get(ing.name, MergedIngredient())
            match [ing.amount, ing.unit]:
                case [0, ""]:
                    merged.amountless.append(recipe.name)
                case [amount, ""]:
                    merged.unitless += amount
                case [amount, unit]:
                    amount, unit = normalise(amount, unit)
                    merged.units[unit] = merged.units.get(unit, 0) + amount
            shopping_list[ing.name] = merged

    return shopping_list
