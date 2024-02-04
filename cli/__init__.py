import inquirer
import typer

from api import recipe, Plan
from api.recipe import Recipe
from api.settings import settings
from cli import new
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
    plan = Plan.current()
    all_recipes = Recipe.load_all()
    matches = Recipe.search(query=query, recipes=all_recipes)

    # they need to be hashable
    choices = {r.name: r for r in all_recipes}
    # if there's only one match, don't bother prompting the user
    if len(matches) == 0:
        typer.secho(f"Couldn't find any recipes for {query}")
        return
    if len(matches) == 1:
        recipe = matches[0]
    else:
        key = inquirer.prompt(
            [
                inquirer.List(
                    "recipe",
                    message="Which recipe did you mean?",
                    choices=choices.keys(),
                )
            ]
        )["recipe"]
        recipe = choices[key]

    plan.add(recipe)
    plan.save()
    typer.secho(f"Added {recipe} to plan. Plan is now: ")
    typer.secho(f"{plan}")
