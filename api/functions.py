import json

from . import utils
from .plan import Plan
from .settings import settings


def new_plan() -> Plan:
    shopping_list = Plan()
    utils.touch(settings.shopping_list_path)
    with open(settings.shopping_list_path, "w") as file:
        file.write(shopping_list.model_dump_json())
    return shopping_list


def current_plan() -> Plan:
    with open(settings.shopping_list_path) as file:
        try:
            list_data = json.load(file)
        except json.JSONDecodeError:
            return new_plan()

    return Plan(**list_data)
