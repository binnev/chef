"""
view.py
"""

import typer

import api

app = typer.Typer()


@app.command(name="plan")
def view_plan():
    """
    view_plan
    """
    plan = api.Plan.current()
    typer.secho(f"Current plan:")
    typer.secho(f"\tcreated: {plan.created.isoformat()}")
    if plan.recipes:
        typer.secho(f"\trecipes:")
        for recipe in plan.recipes:
            typer.secho(f"\t\t{recipe}")


@app.command(name="list")
def view_list():
    """
    view_list
    """
    plan = api.Plan.current()
    ingredients = plan.shopping_list()
    ingredients = sorted(ingredients, key=lambda ing: ing.name)
    typer.secho("Current shopping list:")
    for ing in ingredients:
        typer.secho(f"\t{ing}")

