import json
from pathlib import Path

from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings

from . import utils
from .constants import __app_name__


GLOBAL_CONFIG = Path.home() / f".{__app_name__}"
GLOBAL_SETTINGS_FILE = GLOBAL_CONFIG / "settings.json"
DEFAULT_RECIPE_LIBRARY = Path.home() / "recipes"


class Settings(BaseSettings):
    model_config = ConfigDict(extra="ignore")

    recipe_library: Path = Field(
        default=DEFAULT_RECIPE_LIBRARY,
        description="Path to the user's recipe library",
    )
    merge_ingredients: bool = Field(
        default=True,
        description=(
            "If True, try to squash together similar ingredients when making "
            "a shopping list "
            "e.g. `5, g, garlic` + `10, g, garlic` -> `15, g, garlic`"
        ),
    )

    def save(self) -> None:
        utils.touch(GLOBAL_SETTINGS_FILE)
        with open(GLOBAL_SETTINGS_FILE, "w") as file:
            file.write(self.model_dump_json())

    @classmethod
    def from_file(cls) -> "Settings":
        """
        Load the global settings and the user settings, and merge the two
        such that the user settings override the globals.
        """
        self = cls()
        global_settings = get_or_create_json(GLOBAL_SETTINGS_FILE)
        user_settings = get_or_create_json(self.user_settings)
        combined = global_settings | user_settings
        self.__init__(**combined)
        return self

    @property
    def user_config_dir(self) -> Path:
        """
        Returns:
            A path to the hidden configuration folder in the user's
            recipe library
        """
        return self.recipe_library / f".{__app_name__}"

    @property
    def user_settings(self):
        return self.user_config_dir / "settings.json"

    @property
    def plans_dir(self) -> Path:
        return self.user_config_dir / "plans"


def get_or_create_json(path: Path) -> dict:
    """
    Creates the file if it doesn't exist.

    Args:
        path: the JSON file to open

    Returns:
        A dictionary of native Python data types

    Raises:
        json.JSONDecodeError: if the JSON is not valid
        ValueError: if the JSON starts with a "[" instead of a "{"
    """
    try:
        with open(path) as file:
            json_str = file.read()
    except FileNotFoundError:
        with open(path, "w") as file:
            file.write("{}")
        return {}

    try:
        data = json.loads(json_str)
        assert isinstance(data, dict)
    except AssertionError:
        raise ValueError(f"JSON shouldn't be an array: {json_str[:10]}")
    else:
        return data
