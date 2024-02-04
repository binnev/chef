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
    typer.secho(f"\trecipes:")
    typer.secho(f"\t\t{plan.recipes}")


@app.command(name="list")
def view_list():
    """
    view_list
    """
    plan = api.Plan.current()
    typer.secho(f"Current plan:\n{plan.shopping_list()}")
