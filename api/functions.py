import json

from . import utils
from .models import ShoppingList
from .settings import settings


def new_shopping_list() -> ShoppingList:
    shopping_list = ShoppingList()
    utils.touch(settings.shopping_list_path)
    with open(settings.shopping_list_path, "w") as file:
        file.write(shopping_list.model_dump_json())
    return shopping_list


def current_shopping_list() -> ShoppingList:
    with open(settings.shopping_list_path) as file:
        try:
            list_data = json.load(file)
        except json.JSONDecodeError:
            return new_shopping_list()

    return ShoppingList(**list_data)
