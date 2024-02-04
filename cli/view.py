"""
view.py
"""

import typer

import api
from api.ingredient import Ingredient

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
        typer.secho(f"\t{_format_ingredient_for_list(ing)}")


def _format_ingredient_for_list(ing: Ingredient) -> str:
    s = f"{ing.name}"
    match [ing.amount, ing.unit]:
        case [amount, ""]:
            s += f": {amount}"
        case [amount, unit]:
            s += f": {amount} {unit}"

    if ing.prep:
        s += f"; {ing.prep}"

    return s