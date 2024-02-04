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
    shopping_list = api.current_plan()
    typer.secho(f"Current plan:\n{shopping_list.recipes}")


@app.command(name="list")
def view_list():
    """
    view_list
    """
    plan = api.current_plan()
    typer.secho(f"Current plan:\n{plan.shopping_list()}")
