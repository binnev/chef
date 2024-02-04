from pydantic import BaseModel

from .ingredient import Ingredient


class Recipe(BaseModel):
    # metadata
    name: str
    author: str
    prep_minutes: int = 0
    cook_minutes: int = 0
    servings: int = 0
    source: str = ""
    image: str = ""

    # child objects
    ingredients: list[Ingredient]

    # for something like a salsa or a spice mix, the "method" is just:
    # combine all the ingredients. So method should not be mandatory.
    method: list[str] = []
    equipment: list[str] = []
    notes: list[str] = []

    def __str__(self):
        return f"{self.name} by {self.author}"
