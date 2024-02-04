import yaml
from pydantic import BaseModel

from .ingredient import Ingredient
from .loading import preprocess_yaml
from .settings import settings


class Recipe(BaseModel):
    # metadata
    name: str
    author: str
    prep_minutes: int = 0
    cook_minutes: int = 0
    servings: int = 0
    source: str = ""
    image: str = ""
    notes: str = ""

    # child objects
    ingredients: list[Ingredient]

    # for something like a salsa or a spice mix, the "method" is just:
    # combine all the ingredients. So method should not be mandatory.
    method: list[str] = []
    equipment: list[str] = []

    def __str__(self):
        return f"{self.name} by {self.author}"

    @staticmethod
    def search(query: str, recipes: list["Recipe"]) -> list["Recipe"]:
        """
        :param query: Could be anything -- ingredient, title fragment, author
        :param recipes: the recipes to search
        :return: list of recipes that match the given query term
        """
        # todo: improve this function. Should be able to search specifically for
        #  author, or ingredient. Should be able to pass via flags e.g.
        #       -a --author Robin Neville
        #       -i --ingredient lentils
        #       -e --equipment air fryer
        #       -x --exclude (flips the above logic as if applying `not` to the
        #                     whole query)

        if not query or not recipes:
            return []

        return [
            recipe
            for recipe in recipes
            if any(
                needle.lower() in haystack.lower()
                for needle in query.split()
                for haystack in [recipe.name, recipe.author]
            )
        ]

    @classmethod
    def load_all(cls) -> list["Recipe"]:
        """
        Load all the recipes from yaml
        :return:
        """
        # todo: make this async
        filenames = settings.recipes_dir.glob("*.yaml")
        recipe_dicts = []
        for filename in filenames:
            with open(filename) as file:
                recipe_dict = yaml.safe_load(file)
                recipe_dict = preprocess_yaml(recipe_dict)
                recipe_dicts.append(recipe_dict)
        recipes = [cls(**recipe_dict) for recipe_dict in recipe_dicts]
        return recipes
