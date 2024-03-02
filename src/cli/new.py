"""
new.py
"""

import typer

from .routines.recipe_wizard import recipe_wizard
from .. import api

app = typer.Typer()


@app.command(name="plan")
def new_plan():
    """
    Create a new plan
    """
    api.Plan.new()
    typer.secho("created new plan\n")


@app.command(name="recipe")
def new_recipe():
    """
    New recipe wizard
    """
    recipe_file = recipe_wizard()
    print(f"Created recipe {recipe_file}")
