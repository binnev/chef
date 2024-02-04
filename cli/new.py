"""
new.py
"""

import typer

import api

app = typer.Typer()


@app.command(name="plan")
def new_plan():
    """
    new_plan
    """
    api.new_plan()
    typer.secho("created new plan")


@app.command(name="recipe")
def new_recipe():
    """
    new_recipe
    """
    # todo
    typer.secho("todo: recipe creation wizard")
