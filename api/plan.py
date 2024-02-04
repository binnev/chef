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
        raise NotImplementedError
