import pytest

from api.ingredient import Ingredient
from api.recipe import Recipe


@pytest.mark.parametrize(
    "recipe_dict, expected",
    [
        pytest.param(
            {
                "name": "foo",
                "author": "bar",
                "ingredients": [{"name": "poopoo"}],
            },
            Recipe(
                name="foo",
                author="bar",
                ingredients=[Ingredient(name="poopoo")],
            ),
            id="minimal inputs",
        ),
        pytest.param(
            {
                "name": "potatoes",
                "author": "me",
                "prep_minutes": 69,
                "cook_minutes": 420,
                "servings": 666,
                "source": "https://source.com",
                "image": "https://image.com",
                "notes": ["I am a potato"],
                "ingredients": [
                    {
                        "name": "potatoes",
                        "amount": 2,
                        "unit": "kg",
                        "prep": "chopped",
                    }
                ],
                "method": ["put the potatoes in boiling water", "eat them"],
                "equipment": ["big pan", "kitchen sink"],
            },
            Recipe(
                name="potatoes",
                author="me",
                prep_minutes=69,
                cook_minutes=420,
                servings=666,
                source="https://source.com",
                image="https://image.com",
                notes=["I am a potato"],
                ingredients=[
                    Ingredient(
                        name="potatoes",
                        amount=2,
                        unit="kg",
                        prep="chopped",
                    )
                ],
                method=["put the potatoes in boiling " "water", "eat them"],
                equipment=["big pan", "kitchen sink"],
            ),
            id="full input",
        ),
    ],
)
def test_init_happy(recipe_dict: dict, expected: Recipe):
    assert Recipe(**recipe_dict) == expected
