from importlib.metadata import version

import typer
from typing_extensions import Annotated

from navfitx.gui import app as gui_app

# from navfitx.utils import app as utils_app

app = typer.Typer(no_args_is_help=True, add_completion=False)


def version_callback(value: bool):
    if value:
        print(f"{version('navfitx')}")
        raise typer.Exit()


@app.callback()
def callback(
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
    pass


app.add_typer(gui_app)


def main():
    app()


if __name__ == "__main__":
    main()
