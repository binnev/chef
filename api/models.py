from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    name: str
    amount: int
    unit: str
    prep: str


class Recipe(BaseModel):
    name: str
    author: str
    ingredients: list[Ingredient]
    method: list[str]

    def __str__(self):
        return f"{self.name} by {self.author}"


class ShoppingList(BaseModel):
    recipes: list[Recipe] = Field(default_factory=list)

    def squeeze(self) -> list[Ingredient]:
        """
        Merge the ingredients from self.recipes into one list of ingredients.
        """
        raise NotImplementedError
