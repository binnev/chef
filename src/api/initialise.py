from pathlib import Path

from .settings import Settings
from .constants import __app_name__


def init_library(path: Path):
    settings = Settings()
    settings.recipe_library = path
    settings.save()

    for p in [
        path,
        path / "yaml",
        path / "md",
        path / f".{__app_name__}",
    ]:
        Path.mkdir(p, parents=True, exist_ok=True)  # ensure the dir exists

    if not settings.user_settings.exists():
        with open(settings.user_settings, "w") as file:
            file.write("{}")  # empty json
