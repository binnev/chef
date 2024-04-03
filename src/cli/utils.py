import typing as t
from functools import wraps
from typing import TypeVar

import inquirer
import typer

from src.api import Settings

T = TypeVar("T")


def echo(
    s: str,
    nl: bool = True,
    err: bool = False,
    color: t.Optional[bool] = None,
    **styles: t.Any,
):
    typer.secho(
        s.expandtabs(4),
        nl=nl,
        err=err,
        color=color,
        **styles,
    )


def multiple_choice_menu(prompt: str, choices: dict[str, T]) -> T:
    """
    This syntax is pretty cumbersome and nested, so I'm putting it in a
    function.
    :param prompt: The text that will be displayed to the user
    :param choices: dict of {obj_name: obj} (obj_name will be displayed to user)
    :return: the selected object
    """
    key = inquirer.prompt(
        [
            inquirer.List(
                "_",
                message=prompt,
                choices=choices.keys(),
            )
        ]
    )["_"]
    return choices[key]


INIT_MSG = """
You need to initialise your recipe library by running:

    chef init <path-to-your-recipe-library>
"""


def requires_library_init(func):
    """
    Decorator that checks whether the recipe library has been initialised
    before certain functions can be called.
    """

    @wraps(func)
    def wrapped(*args, **kwargs):
        settings = Settings.load()
        if settings.system.recipe_library is None:
            typer.secho(INIT_MSG)
            raise typer.Exit(1)
        return func(*args, **kwargs)

    return wrapped
