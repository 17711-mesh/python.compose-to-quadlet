import click, yaml
from pathlib import Path
from .logging_utils import configure_logging
from .schemas import ComposeFile
from .generator import QuadletGenerator
from . import __version__

@click.command()
@click.version_option(__version__)
@click.argument("compose_file", type=click.Path(exists=True, path_type=Path))
@click.option("--output-dir", default="quadlet-out", type=click.Path(path_type=Path))
@click.option("--template-dir", default=None, type=click.Path(path_type=Path))
@click.option("--stack-name", default=None)
def main(compose_file, output_dir, template_dir, stack_name):
    configure_logging("DEBUG")
    raw=yaml.safe_load(compose_file.read_text())
    compose=ComposeFile.from_raw(raw)
    template_dir=template_dir or (Path(__file__).parent/"templates")
    gen=QuadletGenerator(template_dir)
    gen.generate(compose, output_dir, stack_name)
    print(f"Generated into {output_dir}")

if __name__=="__main__":
    main()
