from importlib.metadata import version

import typer
from typing_extensions import Annotated

from navfitx.gui import app as gui_app

app = typer.Typer(add_completion=False)


def version_callback(value: bool):
    if value:
        print(f"{version('navfitx')}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def callback(
    ctx: typer.Context,
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-v",
            help="Show the version information and exit.",
            is_eager=True,
            show_default=False,
            callback=version_callback,
        ),
    ] = False,
):
    """
    NAVFITX

    Created by Tristan White
    """
    # With no args, launch the GUI
    if ctx.invoked_subcommand is None:
        gui_app()


app.add_typer(gui_app)


def main():
    app()


if __name__ == "__main__":
    main()
