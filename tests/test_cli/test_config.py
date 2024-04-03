from typer.testing import CliRunner

from src.cli import app

EXPECTED = """
config: 
    merge_ingredients: True
""".lstrip()


def test_config__list(monkeypatch):
    runner = CliRunner()
    result = runner.invoke(app, ["config"])
    assert result.output == EXPECTED
