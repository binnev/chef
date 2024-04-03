from datetime import datetime, timezone
from unittest.mock import patch

import pytest

from src.api import Plan, Recipe
import json

from src.api.ingredient import Ingredient


@patch("src.api.plan.Plan.new", return_value="foo")
def test_current__no_existing_plan(mock_new):
    """
    NOTE: Path.glob is mocked, and returns an empty generator.
    """
    plan = Plan.current()
    assert plan == "foo"


@patch("src.api.plan.open")
def test_current__existing_plans(
    mock_open,
    mock_open_file_ctx,
    mock_path_glob,
):
    mock_path_glob.return_value = ["2024-04-03.json", "2020-01-01.json"]
    mock_open.return_value = mock_open_file_ctx
    mock_open_file_ctx.mock_file.read.return_value = json.dumps(
        {
            "created": "2024-04-03T12:00:00.000000Z",
            "recipes": [
                {
                    "name": "foo",
                    "author": "bar",
                    "ingredients": [{"name": "poopoo"}],
                }
            ],
        }
    )

    plan = Plan.current()
    assert plan.created == datetime(2024, 4, 3, 12, 0, 0, tzinfo=timezone.utc)
    assert plan.recipes == [
        Recipe(
            name="foo",
            author="bar",
            ingredients=[Ingredient(name="poopoo")],
        )
    ]
    mock_open.assert_called_with("2024-04-03.json")  # latest one


@pytest.mark.parametrize(
    "created_time, expected",
    [
        pytest.param(
            datetime(2024, 4, 3, 12, 1, 2, microsecond=69),
            "2024-04-03T12:01:02.json",
            id="with microseconds",
        ),
        pytest.param(
            datetime(2024, 4, 3, 12, 1, 2, microsecond=0),
            "2024-04-03T12:01:02.json",
            id="without microseconds",
        ),
    ],
)
def test_filename(created_time: datetime, expected: str):
    plan = Plan(created=created_time)
    assert plan.filename.name == expected
