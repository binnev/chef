from datetime import datetime

from pydantic import BaseModel, Field

from .ingredient import Ingredient


class Recipe(BaseModel):
    # metadata
    name: str
    author: str
    # todo:
    #  prep_time
    #  cook_time
    #  serves N
    #  source
    #  image
    #  notes

    # child objects
    ingredients: list[Ingredient]
    method: list[str]
    equipment: list[str]

    def __str__(self):
        return f"{self.name} by {self.author}"


class Plan(BaseModel):
    created: datetime = Field(default_factory=lambda: datetime.utcnow())
    recipes: list[Recipe] = Field(default_factory=list)

    def shopping_list(self) -> list[Ingredient]:
        """
        Merge the ingredients from self.recipes into one list of ingredients.
        """
        raise NotImplementedError
