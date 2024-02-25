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


def serialize_json(recipe: Recipe) -> str:
    return recipe.model_dump_json()


def serialize_markdown(recipe: Recipe) -> str:
    out =""

    def add_line(s: str):
        nonlocal out
        out += s + "\n"

    add_line(f"# {recipe.name}")
    add_line(f"Author: {recipe.author.title()}")
    if recipe.image:
        add_line(f"![]({recipe.image})")
    if recipe.source:
        add_line(f"From: {recipe.source}")
    if recipe.servings:
        add_line(f"Servings: {recipe.servings}")
    if recipe.prep_minutes:
        add_line(f"Preparation: {recipe.prep_minutes} minutes")
    if recipe.cook_minutes:
        add_line(f"Cooking: {recipe.cook_minutes} minutes")
    if recipe.notes:
        add_line(f"Notes: {recipe.notes}")
    if recipe.equipment:
        add_line("Equipment: ")
        for item in recipe.equipment:
            add_line(f"- {item}")

    add_line("## Ingredients:")
    for ing in recipe.ingredients:
        add_line(f"- [ ] {ing}")

    if recipe.method:
        add_line("## Method:")
        for ii, step in enumerate(recipe.method, start=1):
            add_line(f"{ii}. {step}")

    return out
