from typer.testing import CliRunner
from unittest.mock import patch

from src.api import Settings, Recipe
from src.api.ingredient import Ingredient
from src.cli import app
from src.cli.routines.recipe_wizard import recipe_wizard


@patch("src.cli.routines.recipe_wizard.input")
def test_recipe_wizard(mock_input):
    mock_input.side_effect = [
        "silly pie",  # name
        "forrest gump",  # author
        # ingredients
        "apples",
        "3, kg, potatoes; chopped",
        "",  # exit ingredients
        # method
        "chop it all",
        "",
        # equipment
        "",
        "69",  # prep
        "420",  # cook
        "3",  # servings
        "www.example.com",  # source
        "../images/foo.jpeg",  # image
        "yucky",  # notes
    ]

    recipe = recipe_wizard()
    assert recipe.author == "forrest gump"
    assert recipe.name == "silly pie"
    assert len(recipe.ingredients) == 2
    assert recipe.ingredients[0].name == "apples"
    assert recipe.ingredients[1].name == "potatoes"
    assert len(recipe.method) == 1
    assert recipe.method[0] == "chop it all"
    assert len(recipe.equipment) == 0
    assert recipe.prep_minutes == 69
    assert recipe.cook_minutes == 420
    assert recipe.servings == 3
    assert recipe.source == "www.example.com"
    assert recipe.image == "../images/foo.jpeg"
    assert recipe.notes == "yucky"


@patch("src.cli.routines.recipe_wizard.input")
def test_recipe_wizard__minimal(mock_input):
    mock_input.side_effect = [
        "silly pie",  # name
        "forrest gump",  # author
        "",  # ingredients
        "",  # method
        "",  # equipment
        "",  # prep
        "",  # cook
        "",  # servings
        "",  # source
        "",  # image
        "",  # notes
    ]

    recipe = recipe_wizard()
    assert recipe.author == "forrest gump"
    assert recipe.name == "silly pie"
    assert len(recipe.ingredients) == 0
    assert len(recipe.method) == 0
    assert len(recipe.equipment) == 0
    assert recipe.prep_minutes == 0
    assert recipe.cook_minutes == 0
    assert recipe.servings == 0
    assert recipe.source == ""
    assert recipe.image == ""
    assert recipe.notes == ""


@patch("src.cli.new.recipe_wizard")
@patch("src.cli.new.open")
def test_new_recipe(mock_open, mock_recipe_wizard, mock_open_file):
    mock_file, mock_ctx = mock_open_file
    mock_open.return_value = mock_ctx

    mock_recipe_wizard.return_value = Recipe(
        author="foo",
        name="silly pie",
        ingredients=[Ingredient.from_str("poopoo")],
    )
    runner = CliRunner()
    result = runner.invoke(app, ["new", "recipe"])

    settings = Settings.from_file()
    mock_open.assert_called_with(
        settings.recipe_library / "yaml" / "silly-pie.yaml", "w"
    )
    mock_file.write.assert_called()
    assert result.exit_code == 0
