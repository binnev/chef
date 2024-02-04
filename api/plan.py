import json
from datetime import datetime

from pydantic import BaseModel, Field

from . import utils
from .ingredient import Ingredient
from .recipe import Recipe
from .settings import settings


class Plan(BaseModel):
    created: datetime = Field(default_factory=lambda: datetime.utcnow())
    recipes: list[Recipe] = Field(default_factory=list)

    def __str__(self):
        return f"Plan (created at {self.created})"

    def shopping_list(self) -> list[Ingredient]:
        """
        Merge the ingredients from self.recipes into one list of ingredients.
        """
        return merge_recipes(self.recipes)

    def add(self, recipe: Recipe):
        self.recipes.append(recipe)

    @classmethod
    def new(cls) -> "Plan":
        """
        Create a new plan in the filesystem
        :return: new plan
        """
        plan = cls()
        filename = plan.filename
        utils.touch(filename)
        with open(filename, "w") as file:
            file.write(plan.model_dump_json())
        return plan

    @classmethod
    def current(cls) -> "Plan":
        json_files = settings.plans_dir.glob("*.json")
        latest = max(json_files)  # relying on string comparison here
        with open(latest) as file:
            try:
                return Plan(**json.load(file))
            except json.JSONDecodeError:
                return cls.new_plan()

    def save(self):
        with open(self.filename, "w") as file:
            file.write(self.model_dump_json())

    @property
    def filename(self):
        return settings.plans_dir / f"{self.created.isoformat()}.json"


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
