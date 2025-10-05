from pathlib import Path

import typer
from typing_extensions import Annotated

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.callback()
def callback():
    """
    NAVFITX: NextGen FITREP Generation Tool.
    """
    pass


@app.command()
def make_pdf(
    b1: Annotated[str, typer.Option(help="Block 1 text")],
):
    """Generate a PDF file."""


@app.command()
def toml_to_pdf():
    """Generate a FITREP PDF from a TOML file."""
    pass


@app.command()
def blank_toml(
    dest: Annotated[Path, typer.Argument(help="Path to output TOML file", exists=True, dir_okay=False, writable=True)],
):
    """Generate a blank FITREP TOML file."""
    pass


if __name__ == "__main__":
    app()
