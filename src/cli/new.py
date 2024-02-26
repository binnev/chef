"""
new.py
"""

import typer

from .. import api

app = typer.Typer()


@app.command(name="plan")
def new_plan():
    """
    new_plan
    """
    api.Plan.new()
    typer.secho("created new plan\n")


@app.command(name="recipe")
def new_recipe():
    """
    new_recipe
    """
    # todo
    typer.secho("todo: recipe creation wizard")
