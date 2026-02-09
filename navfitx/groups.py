from pathlib import Path
from typing import Annotated

import typer

from navfitx.db import get_fitrep_summary_groups

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.callback()
def callback():
    """
    Tool for working with summary groups in NAVFITX.
    """
    pass


@app.command()
def print(
    db: Annotated[
        Path,
        typer.Option(
            "--db",
            "-d",
            help="The path to the sqlite database file.",
            exists=True,
            dir_okay=False,
            readable=True,
        ),
    ],
):
    """
    Print the summary groups in the database.
    """
    get_fitrep_summary_groups(db)
