import pytest
import yaml

from src.api.ingredient import Ingredient
from src.api.ingredient import IngredientParseError, parse_ingredient_str
from src.api.recipe import Recipe
from src.api.recipe.formats import serialize_yaml, serialize_markdown
from src.api.recipe.utils import preprocess_yaml


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
                "notes": "I am a potato. A potato wrote this recipe.",
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
                notes="I am a potato. A potato wrote this recipe.",
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


RECIPES = [
    Recipe(name="foo", author="bar", ingredients=[]),
    Recipe(name="baz", author="qux", ingredients=[]),
]


@pytest.mark.parametrize(
    "query, recipes, expected",
    [
        pytest.param("", RECIPES, [], id="empty query"),
        pytest.param("foo", [], [], id="empty recipes"),
        pytest.param("fart", RECIPES, [], id="query not found"),
        pytest.param(
            "foo",
            RECIPES,
            [Recipe(name="foo", author="bar", ingredients=[])],
            id="single term found in single recipe",
        ),
        pytest.param(
            "ba",
            RECIPES,
            RECIPES,
            id="single term was found in multiple recipes",
        ),
        pytest.param(
            "foo qux",
            RECIPES,
            RECIPES,
            id="multiple query terms were found in multiple recipes",
        ),
    ],
)
def test_search(
    query: str,
    recipes: list[Recipe],
    expected: list[Recipe],
):
    assert Recipe.search(query, recipes) == expected


@pytest.mark.parametrize(
    "recipe_dict, expected",
    [
        pytest.param(
            {},
            {},
            id=(
                "If ingredients are missing from the input, then the output "
                "should also not contain them"
            ),
        ),
        pytest.param(
            {"ingredients": []},
            {"ingredients": []},
            id="If ingredients are empty, output should be unchanged",
        ),
        pytest.param(
            {"ingredients": ["apples"]},
            {"ingredients": [parse_ingredient_str("apples")]},
            id="Input is populated; output should contain parsed ingredients",
        ),
    ],
)
def test_preprocess_yaml(
    recipe_dict: dict,
    expected: dict | IngredientParseError,
):
    if isinstance(expected, IngredientParseError):
        with pytest.raises(expected.__class__) as e:
            preprocess_yaml(recipe_dict)
        assert str(e.value) == str(expected)

    else:
        assert preprocess_yaml(recipe_dict) == expected


def test_serialize_yaml():
    recipe_dict = {
        "name": "foo",
        "author": "bar",
        "ingredients": [
            {"name": "poopoo"},
            {"name": "train", "amount": 4},
            {"name": "weewee", "amount": 4, "unit": "l"},
        ],
    }
    recipe = Recipe.model_validate(recipe_dict)
    yaml_str = serialize_yaml(recipe)
    # the order of keys in the yaml string output is not reliable, so we have
    # to parse back to dict
    yaml_dict = yaml.safe_load(yaml_str)
    assert yaml_dict == {
        "name": "foo",
        "author": "bar",
        "ingredients": [
            "poopoo",
            "4, train",
            "4, l, weewee",
        ],
    }


def test_serialize_markdown():
    yaml_input = """name: Neelam Bajwa's chicken madras
author: Neelam Bajwa
source: https://www.youtube.com/watch?v=43yWAafyFMQ 
notes: In this recipe we make the base curry sauce and the madras in one go. 

ingredients: 
  # base curry sauce
  - 2, tbsp, ghee or veg oil
  - 2, onions
  - 3, cloves, garlic
  - 1, inch,  ginger
  - 1, carrot
  - 0.25, cup, cabbage; shredded
  - 1, red bell pepper
  - 2, tomatoes
  - 1, pinch,  turmeric
  - 1, tbsp, cumin powder
  - 1, tbsp, coriander powder
  - 1.5, tsp, ground methi seeds
  - fresh coriander

method: 
  - Prepare the gravy spice mix; pinch of turmeric powder, 1 tsp cumin powder, 1tsp coriander powder and 1.5 tsp ground fenugreek seeds.
  - Prepare the madras spice mix; 4 cardamoms, 1 tsp turmeric powder, 1 tbsp coriander powder, 1 tbsp cumin powder, 2 tbsp red chilli powder.
  - In a saucepan heat ghee and add onions, carrots, bell peppers, tomatoes, garlic, ginger and cabbage.
  - Mix well and add gravy spice mix.
  - Add water and cook.
  - Transfer in a mixer/grinder and make a puree of it.
  - In a saucepan heat ghee and add Kashmiri red chillies, ginger-garlic paste, tomato puree, madras spice mix, slit green chillies, salt and stir well.
  - Add the chicken and cook in the madras spice paste for a few minutes. Add the base curry sauce and cook on high flame.
  - Then add the madras curry powder and water.
  - Garnish with coriander leaves.
"""

    expected_markdown = """# Neelam Bajwa's chicken madras

Author: Neelam Bajwa

From: https://www.youtube.com/watch?v=43yWAafyFMQ

Notes: In this recipe we make the base curry sauce and the madras in one go.

## Ingredients:
- [ ] 2 tbsp ghee or veg oil
- [ ] 2 onions
- [ ] 3 cloves garlic
- [ ] 1 inch ginger
- [ ] 1 carrot
- [ ] 0.25 cup cabbage, shredded
- [ ] 1 red bell pepper
- [ ] 2 tomatoes
- [ ] 1 pinch turmeric
- [ ] 1 tbsp cumin powder
- [ ] 1 tbsp coriander powder
- [ ] 1.5 tsp ground methi seeds
- [ ] fresh coriander

## Method:
1. Prepare the gravy spice mix; pinch of turmeric powder, 1 tsp cumin powder, 1tsp coriander powder and 1.5 tsp ground fenugreek seeds.
2. Prepare the madras spice mix; 4 cardamoms, 1 tsp turmeric powder, 1 tbsp coriander powder, 1 tbsp cumin powder, 2 tbsp red chilli powder.
3. In a saucepan heat ghee and add onions, carrots, bell peppers, tomatoes, garlic, ginger and cabbage.
4. Mix well and add gravy spice mix.
5. Add water and cook.
6. Transfer in a mixer/grinder and make a puree of it.
7. In a saucepan heat ghee and add Kashmiri red chillies, ginger-garlic paste, tomato puree, madras spice mix, slit green chillies, salt and stir well.
8. Add the chicken and cook in the madras spice paste for a few minutes. Add the base curry sauce and cook on high flame.
9. Then add the madras curry powder and water.
10. Garnish with coriander leaves."""
    recipe_dict = yaml.safe_load(yaml_input)
    recipe = Recipe.model_validate(preprocess_yaml(recipe_dict))
    out = serialize_markdown(recipe)
    assert out == expected_markdown
