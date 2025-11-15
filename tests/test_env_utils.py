
import pytest
from pathlib import Path
from compose_to_quadlet.env_utils import load_env

def test_load_env_success(tmp_path: Path):
    """Tests that a valid .env file is loaded correctly."""
    env_file = tmp_path / ".env"
    env_file.write_text("KEY1=VALUE1\nKEY2 = VALUE2 \n# This is a comment\n")
    
    env = load_env(env_file)
    
    assert env == {"KEY1": "VALUE1", "KEY2": "VALUE2"}

def test_load_env_with_empty_lines(tmp_path: Path):
    """Tests that empty lines are ignored."""
    env_file = tmp_path / ".env"
    env_file.write_text("\nKEY1=VALUE1\n\nKEY2=VALUE2\n")
    
    env = load_env(env_file)
    
    assert env == {"KEY1": "VALUE1", "KEY2": "VALUE2"}

def test_load_env_value_with_equals(tmp_path: Path):
    """Tests that values can contain the '=' character."""
    env_file = tmp_path / ".env"
    env_file.write_text("URL=postgres://user:pass@host:5432/db?sslmode=require")
    
    env = load_env(env_file)
    
    assert env == {"URL": "postgres://user:pass@host:5432/db?sslmode=require"}

def test_load_env_file_not_found():
    """Tests that a non-existent file returns an empty dict."""
    env = load_env(Path("non-existent-file.env"))
    assert env == {}

def test_load_env_empty_file(tmp_path: Path):
    """Tests that an empty file returns an empty dict."""
    env_file = tmp_path / ".env"
    env_file.touch()
    
    env = load_env(env_file)
    
    assert env == {}

