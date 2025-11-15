
import pytest
from pathlib import Path
from click.testing import CliRunner
from compose_to_quadlet.cli import main

@pytest.fixture
def runner():
    """Returns a CliRunner instance for invoking the CLI."""
    return CliRunner()

@pytest.fixture
def compose_file(tmp_path: Path) -> Path:
    """Creates a temporary compose file for testing."""
    content = """
services:
  web:
    image: nginx
    ports:
      - "8080:80"
volumes:
  data: {}
"""
    file_path = tmp_path / "docker-compose.yml"
    file_path.write_text(content)
    return file_path

def test_cli_success(runner: CliRunner, compose_file: Path, tmp_path: Path):
    """Tests successful execution of the CLI."""
    output_dir = tmp_path / "quadlets"
    result = runner.invoke(
        main,
        [
            str(compose_file),
            "--output-dir",
            str(output_dir),
            "--stack-name",
            "test-stack",
        ],
    )
    
    assert result.exit_code == 0
    assert f"Generated into {output_dir}" in result.output
    assert (output_dir / "web.container").exists()
    assert (output_dir / "data.volume").exists()
    assert (output_dir / "test-stack.target").exists()

def test_cli_invalid_yaml(runner: CliRunner, tmp_path: Path):
    """Tests that the CLI fails gracefully with invalid YAML."""
    invalid_compose_file = tmp_path / "invalid.yml"
    invalid_compose_file.write_text("services: { web: { image: nginx,")

    result = runner.invoke(main, [str(invalid_compose_file)])

    assert result.exit_code != 0
    # We expect an exception from the YAML parser or Pydantic
    assert isinstance(result.exception, Exception)

def test_cli_missing_compose_file(runner: CliRunner):
    """Tests that the CLI fails if the compose file does not exist."""
    result = runner.invoke(main, ["non-existent-file.yml"])

    assert result.exit_code != 0
    assert "Error: Invalid value for 'COMPOSE_FILE'" in result.output
    assert "does not exist" in result.output
