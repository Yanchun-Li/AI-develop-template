import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_template_has_project_metadata() -> None:
    assert Path("pyproject.toml").is_file()


def test_aidd_overlay_template_shape() -> None:
    overlay = ROOT / "templates" / "aidd-overlay"

    assert (overlay / "AGENTS.md").is_file()
    assert (overlay / "CLAUDE.md").is_file()
    assert (overlay / ".aidd" / "RULES.md").is_file()
    assert (overlay / ".aidd" / "docs" / "WORKFLOW.md").is_file()
    assert (overlay / ".aidd" / "docs" / "tasks" / "active" / "README.md").is_file()
    assert (overlay / ".aidd" / "docs" / "tasks" / "completed" / "README.md").is_file()
    assert not (overlay / ".aidd" / "docs" / "architectures").exists()


def test_aidd_init_installs_overlay_without_overwriting_bridges(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True, text=True)

    existing_agents = "existing AGENTS\n"
    (repo / "AGENTS.md").write_text(existing_agents)

    result = subprocess.run(
        ["bash", str(ROOT / "scripts" / "aidd-init.sh"), str(repo)],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "AIDD overlay initialized" in result.stdout
    assert (repo / "AGENTS.md").read_text() == existing_agents
    assert (repo / "CLAUDE.md").is_file()
    assert (repo / ".aidd" / "RULES.md").is_file()
    assert (repo / ".aidd" / "docs" / "tasks" / "active" / "README.md").is_file()
    assert not (repo / ".aidd" / "docs" / "architectures").exists()

    exclude = (repo / ".git" / "info" / "exclude").read_text()
    assert ".aidd/" in exclude
    assert "AGENTS.md" in exclude
    assert "CLAUDE.md" in exclude


def test_aidd_init_does_not_overwrite_existing_overlay_without_force(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True, text=True)

    subprocess.run(
        ["bash", str(ROOT / "scripts" / "aidd-init.sh"), str(repo)],
        check=True,
        capture_output=True,
        text=True,
    )

    custom_rules = "custom local rules\n"
    (repo / ".aidd" / "RULES.md").write_text(custom_rules)

    result = subprocess.run(
        ["bash", str(ROOT / "scripts" / "aidd-init.sh"), str(repo)],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "skip: .aidd already exists" in result.stdout
    assert (repo / ".aidd" / "RULES.md").read_text() == custom_rules


def test_aidd_init_force_refreshes_overlay(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()

    subprocess.run(
        ["bash", str(ROOT / "scripts" / "aidd-init.sh"), str(repo)],
        check=True,
        capture_output=True,
        text=True,
    )
    (repo / ".aidd" / "RULES.md").write_text("custom local rules\n")

    result = subprocess.run(
        ["bash", str(ROOT / "scripts" / "aidd-init.sh"), "--force", str(repo)],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "synced: .aidd" in result.stdout
    assert (repo / ".aidd" / "RULES.md").read_text() != "custom local rules\n"
