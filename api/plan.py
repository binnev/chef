from datetime import datetime

from pydantic import BaseModel, Field

from .ingredient import Ingredient
from .recipe import Recipe


class Plan(BaseModel):
    created: datetime = Field(default_factory=lambda: datetime.utcnow())
    recipes: list[Recipe] = Field(default_factory=list)

    def shopping_list(self) -> list[Ingredient]:
        """
        Merge the ingredients from self.recipes into one list of ingredients.
        """
        return merge_recipes(self.recipes)


def merge_recipes(recipes: list[Recipe]) -> list[Ingredient]:
    """
    This is the magic.
    :param recipes:
    :return:
    """
    shopping_list = []
    for recipe in recipes:
        shopping_list.extend(recipe.ingredients)

    return shopping_list
