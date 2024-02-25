import yaml

from api.recipe.base import Recipe


def serialize_yaml(recipe: Recipe) -> str:
    recipe_dict = recipe.model_dump()
    recipe_dict = {key: value for key, value in recipe_dict.items() if value}
    # make sure the ingredients are displayed in their yaml format
    recipe_dict["ingredients"] = [
        ing.to_yaml_str() for ing in recipe.ingredients
    ]
    return yaml.safe_dump(recipe_dict)
