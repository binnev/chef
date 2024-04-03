"""
new.py
"""

import typer

from .utils import requires_library_init
from .routines.recipe_wizard import recipe_wizard
from .. import api
from ..api import RecipeSerializer, Settings
from ..api.recipe.serializer import Format
from ..api.utils import clean_filename

app = typer.Typer()


@app.command(name="plan")
@requires_library_init
def new_plan():
    """
    Create a new plan
    """
    api.Plan.new()
    typer.secho("created new plan\n")


@app.command(name="recipe")
@requires_library_init
def new_recipe():
    """
    New recipe wizard
    """
    recipe = recipe_wizard()
    yaml_str = RecipeSerializer().serialize(recipe, Format.YAML)
    settings = Settings.load()
    filename = clean_filename(
        settings.system.recipe_library / "yaml" / f"{recipe.name}.yaml"
    )
    with open(filename, "w") as file:
        file.write(yaml_str)

    print(f"Created recipe {filename}")
