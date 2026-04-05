from pathlib import Path

import typer
from typing_extensions import Annotated

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command()
def print_accdb(
    accdb: Annotated[
        Path,
        typer.Option(
            help="Path to the Access (.accdb) file to import.",
            exists=True,
            dir_okay=False,
        ),
    ],
):
    """Print info from the .accdb file."""
