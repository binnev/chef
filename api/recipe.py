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


def search_recipe(query: str, recipes: list[Recipe]) -> list[Recipe]:
    """
    :param query: Could be anything -- ingredient, title fragment, author
    :param recipes: the recipes to search
    :return: list of recipes that match the given query term
    """
    if not query or not recipes:
        return []

    # todo: improve this function. Should be able to search specifically for
    #  author, or ingredient. Should be able to pass via flags e.g.
    #       -a --author Robin Neville
    #       -i --ingredient lentils
    #       -e --equipment air fryer
    #       -x --exclude (flips the above logic as if applying `not` to the
    #                     whole query)

    return [
        recipe
        for recipe in recipes
        if any(
            needle.lower() in haystack.lower()
            for needle in query.split()
            for haystack in [recipe.name, recipe.author]
        )
    ]
