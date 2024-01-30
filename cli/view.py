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
    shopping_list = api.current_shopping_list()
    typer.secho(f"Current plan:\n{shopping_list.recipes}")


@app.command(name="list")
def view_list():
    """
    view_list
    """
    shopping_list = api.current_shopping_list()
    typer.secho(f"Current plan:\n{shopping_list.squeeze()}")
