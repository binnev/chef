from typer.testing import CliRunner

from src.cli import app


def test_version(monkeypatch):
    monkeypatch.setattr("src.cli.api.__version__", "420.69")
    runner = CliRunner()
    result = runner.invoke(app, ["--version"])
    assert result.output == "yes-chef v420.69\n"
    monkeypatch.undo()
