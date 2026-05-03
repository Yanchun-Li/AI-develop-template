from pathlib import Path


def test_template_has_project_metadata() -> None:
    assert Path("pyproject.toml").is_file()
