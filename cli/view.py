"""
view.py
"""

import typer

import api
from api.shopping_list import Amounts
from cli.utils import echo

app = typer.Typer()


@app.command(name="plan")
def view_plan():
    """
    view_plan
    """
    plan = api.Plan.current()
    echo("Current plan:")
    echo(f"\tcreated: {plan.created.isoformat()}")
    if plan.recipes:
        echo("\trecipes:")
        for recipe in plan.recipes:
            echo(f"\t\t{recipe}")


@app.command(name="list")
def view_list():
    """
    view_list
    """
    plan = api.Plan.current()
    ingredients = plan.shopping_list()
    echo("Current shopping list:")
    width = max(map(len, ingredients))
    for ing_name in sorted(ingredients):
        amounts = ingredients[ing_name]
        echo(_format_ingredient_for_list(ing_name, amounts, width))


def _format_ingredient_for_list(
    ing_name: str,
    amounts: Amounts,
    width: int = 0,
) -> str:
    result = f"{ing_name}:".ljust(width)
    match [amounts.amountless, amounts.unitless, amounts.units]:
        case [[], 0, __] if not __:  # guard for empty
            print(f"apparently this is empty: {amounts.units}")
            raise ValueError("empty Amounts!")

        # single line cases
        case [amountless, 0, __] if not __:
            recipe_strings = _foo(amountless)
            result += f" enough for {recipe_strings}"
        case [[], unitless, __] if not __:
            result += f" {unitless}"
        case [[], 0, units] if len(units) == 1:
            if len(units) == 1:
                unit = next(iter(units))
                amount = units[unit]
                result += f" {amount} {unit}"

        # multi line cases
        case [amountless, unitless, units]:
            if amountless:
                recipe_strings = _foo(amountless)
                result += f"\n\tenough for {recipe_strings}"
            if unitless:
                result += f"\n\t{unitless}"
            for unit, amount in units.items():
                result += f"\n\t{amount} {unit}"

    return result


def _foo(recipe_names: list[str]) -> str:
    counts = {}
    for name in recipe_names:
        counts[name] = counts.get(name, 0) + 1

    return ", ".join(
        name if count == 1 else f"{name} (x{count})"
        for name, count in counts.items()
    )
