
import pytest
from pathlib import Path
from compose_to_quadlet.generator import QuadletGenerator
from compose_to_quadlet.schemas import ComposeFile

@pytest.fixture
def template_dir():
    """Returns the path to the project's templates directory."""
    return Path(__file__).parent.parent / "compose_to_quadlet" / "templates"

@pytest.fixture
def generator(template_dir):
    """Returns a QuadletGenerator instance."""
    return QuadletGenerator(template_dir)

@pytest.fixture
def simple_compose_file():
    """Returns a simple ComposeFile object for testing."""
    raw_data = {
        "services": {
            "web": {
                "image": "nginx:latest",
                "environment": {"VAR1": "value1"},
                "deploy": {
                    "resources": {
                        "limits": {"cpus": "1", "memory": "1G"}
                    }
                }
            }
        },
        "volumes": {
            "data": {"driver": "local"}
        },
        "networks": {
            "frontend": {"driver": "bridge", "ipam_subnet": "10.0.0.0/24"}
        }
    }
    return ComposeFile.from_raw(raw_data)

def test_generate_creates_files(generator, simple_compose_file, tmp_path):
    """Tests that generate() creates the expected files."""
    output_dir = tmp_path / "quadlets"
    generator.generate(simple_compose_file, output_dir, stack_name="my-stack")

    assert (output_dir / "web.container").exists()
    assert (output_dir / "data.volume").exists()
    assert (output_dir / "frontend.network").exists()
    assert (output_dir / "my-stack.target").exists()

def test_container_file_content(generator, simple_compose_file, tmp_path):
    """Tests the content of a generated .container file."""
    output_dir = tmp_path / "quadlets"
    generator.generate(simple_compose_file, output_dir, stack_name=None)

    content = (output_dir / "web.container").read_text()
    assert "[Unit]" in content
    assert "Description=web" in content
    assert "[Container]" in content
    assert "Image=nginx:latest" in content
    assert "Environment=VAR1=value1" in content
    assert "PodmanArgs=--memory=1G" in content
    assert "PodmanArgs=--cpus=1" in content

def test_volume_file_content(generator, simple_compose_file, tmp_path):
    """Tests the content of a generated .volume file."""
    output_dir = tmp_path / "quadlets"
    generator.generate(simple_compose_file, output_dir, stack_name=None)

    content = (output_dir / "data.volume").read_text()
    assert "[Volume]" in content
    assert "Driver=local" in content

def test_network_file_content(generator, simple_compose_file, tmp_path):
    """Tests the content of a generated .network file."""
    output_dir = tmp_path / "quadlets"
    generator.generate(simple_compose_file, output_dir, stack_name=None)

    content = (output_dir / "frontend.network").read_text()
    assert "[Network]" in content
    assert "Driver=bridge" in content
    assert "Subnet=10.0.0.0/24" in content

def test_stack_target_file_content(generator, simple_compose_file, tmp_path):
    """Tests the content of a generated .target file for a stack."""
    output_dir = tmp_path / "quadlets"
    generator.generate(simple_compose_file, output_dir, stack_name="my-stack")

    content = (output_dir / "my-stack.target").read_text()
    assert "[Unit]" in content
    assert "Description=my-stack stack" in content
    # Check that it wants the container service, using the podman- prefix
    assert "Wants=podman-web.service" in content
    assert "After=network-online.target" in content

def test_generator_with_command(generator, tmp_path):
    """Tests that the Exec= line is correctly rendered when a command is present."""
    raw_data = {
        "services": {
            "worker": {
                "image": "ubuntu",
                "command": "/bin/bash -c 'echo hello'"
            }
        }
    }
    compose_file = ComposeFile.from_raw(raw_data)
    output_dir = tmp_path / "quadlets"
    generator.generate(compose_file, output_dir, stack_name=None)

    content = (output_dir / "worker.container").read_text()
    assert "Exec=/bin/bash -c 'echo hello'" in content
