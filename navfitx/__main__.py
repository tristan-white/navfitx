import typer

from navfitx.fitrep_layout import app as fitrep_app
from navfitx.gui import app as gui_app
from navfitx.overlay import app as overlay_app

# from navfitx.utils import app as utils_app

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.callback()
def callback():
    """
    NAVFITX

    Created by Tristan White
    """
    pass


app.add_typer(fitrep_app)
app.add_typer(overlay_app)
app.add_typer(gui_app)
# app.add_typer(utils_app)


def main():
    app()


if __name__ == "__main__":
    main()
