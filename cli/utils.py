from typing import TypeVar

import inquirer

T = TypeVar("T")


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
