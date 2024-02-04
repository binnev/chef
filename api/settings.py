import json
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings
from . import utils

BASE = Path.home() / ".sous-chef"
SETTINGS_FILE = BASE / "settings.json"
RECIPES_DIR = BASE / "recipes"
PLANS_DIR = BASE / "plans"


class Settings(BaseSettings):
    recipes_dir: Path = Field(RECIPES_DIR)
    plans_dir: Path = Field(PLANS_DIR)

    def save(self):
        utils.touch(SETTINGS_FILE)
        with open(SETTINGS_FILE, "w") as file:
            json.dump(self.model_dump(), file)

    def load(self):
        utils.touch(SETTINGS_FILE)
        with open(SETTINGS_FILE) as file:
            try:
                settings_dict = json.load(file)
            except json.JSONDecodeError:  # file is empty
                settings_dict = {}

        self.update(**settings_dict)

    def update(self, **kwargs):
        combined = {**self.model_dump(), **kwargs}
        self.__init__(**combined)


settings = Settings()
settings.load()
