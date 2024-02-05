import pytest

from api.shopping_list import Amounts
from cli.view import _format_ingredient_for_list


@pytest.mark.parametrize(
    "ing_name, amounts, expected",
    [
        pytest.param(
            "apples",
            Amounts(amountless=["apple pie"]),
            "apples: enough for apple pie",
            id="should fit on one line if only amountless",
        ),
        pytest.param(
            "apples",
            Amounts(unitless=4),
            "apples: 4",
            id="should fit on one line if only unitless",
        ),
        pytest.param(
            "apples",
            Amounts(units={"kg": 2.5}),
            "apples: 2.5 kg",
            id="should fit on one line if only one unit",
        ),
        pytest.param(
            "apples",
            Amounts(amountless=["apple pie"], unitless=4),
            "apples:\n\tenough for apple pie\n\t4",
            id="if multiple amount types, print on multiple lines",
        ),
        pytest.param(
            "apples",
            Amounts(amountless=["apple pie", "apple pie"]),
            "apples: enough for apple pie (x2)",
            id="repeated recipes should be squashed",
        ),
        pytest.param(
            "apples",
            Amounts(amountless=["apple pie", "apple pie", "something else"]),
            "apples:\n\tenough for\n\t\tapple pie (x2)\n\t\tsomething else",
            id="if more than one recipe in amountless, should be displayed as new nested list",
        ),
    ],
)
def test__format_ingredient_for_list(
    ing_name: str,
    amounts: Amounts,
    expected: str,
):
    assert _format_ingredient_for_list(ing_name, amounts) == expected
