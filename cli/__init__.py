import asyncio

import typer

from api.settings import settings
from cli import new, routines
from cli import view

app = typer.Typer()
app.add_typer(new.app, name="new", help="new help")
app.add_typer(view.app, name="view", help="view help")


@app.command()
def config(
    foo: str = typer.Option(
        "",
        "--foo",
        help="Dummy value",
    ),
):
    """
    Update and/or view configuration
    """
    typer.secho("todo: config set ")
    if foo:
        typer.secho(f"You passed {foo=}")

    print("config: ")
    for key, val in settings.model_dump().items():
        print(f"\t{key}: {val}".expandtabs(4))


@app.command()
def plan(
    query: list[str] = typer.Argument(help="Search term to find recipes"),
):
    """
    plan <search>
    """
    query = " ".join(query)
    asyncio.run(routines.plan_recipe(query))
