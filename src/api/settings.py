import json
from pathlib import Path

from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings

from . import utils
from .constants import __app_name__

GLOBAL_CONFIG = Path.home() / f".{__app_name__}"
PLANS_DIR = GLOBAL_CONFIG / "plans"
GLOBAL_SETTINGS_FILE = GLOBAL_CONFIG / "settings.json"


class SystemSettings(BaseSettings):
    """
    Global system settings (not editable by user)
    """

    recipe_library: Path | None = Field(
        default=None,
        description=(
            "Path to the user's recipe library. If this is None, it means "
            "that the user still needs to run `chef init`."
        ),
    )

    @property
    def user_config_dir(self) -> Path:
        """
        Returns:
            A path to the hidden configuration folder in the user's
            recipe library
        """
        if self.recipe_library is None:
            raise NotInitialised

        return self.recipe_library / f".{__app_name__}"

    @property
    def project_settings(self):
        return self.user_config_dir / "settings.json"


class ProjectSettings(BaseSettings):
    # project settings
    merge_ingredients: bool = Field(
        default=True,
        description=(
            "If True, try to squash together similar ingredients when making "
            "a shopping list "
            "e.g. `5, g, garlic` + `10, g, garlic` -> `15, g, garlic`"
        ),
    )
    model_config = ConfigDict(extra="ignore")


class Settings(BaseSettings):
    """
    NOTE TO SELF:

    I _do_ want to have separate global and project settings, because I want to
    be able to check the .yes-chef folder into git.
    """

    system: SystemSettings = SystemSettings()
    project: ProjectSettings = ProjectSettings()

    def save(self) -> None:
        """
        Saves the system and project settings to their respective files.

        Raises:
            NotInitialised: if the recipe library is not configured.
        """
        utils.touch(GLOBAL_SETTINGS_FILE)
        with open(GLOBAL_SETTINGS_FILE, "w") as file:
            file.write(self.system.model_dump_json())

        with open(self.system.project_settings, "w") as file:
            file.write(self.project.model_dump_json())

    @classmethod
    def load(cls) -> "Settings":
        """
        Load the system settings and the project settings. Should always
        succeed, even if the recipe library is not initialised. Otherwise the
        program will fail on startup and we won't be able to initialise the
        library.

        Returns:
            Settings object
        """
        system_settings = SystemSettings(
            **get_or_create_json(GLOBAL_SETTINGS_FILE)
        )
        try:
            project_settings = ProjectSettings(
                **get_or_create_json(system_settings.project_settings)
            )
        except NotInitialised:
            project_settings = ProjectSettings()
        return cls(
            system=system_settings,
            project=project_settings,
        )


def get_or_create_json(path: Path) -> dict:
    """
    Reads JSON from a file. Creates the file if it doesn't exist.

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
        utils.touch(path)
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


class NotInitialised(Exception):
    pass
