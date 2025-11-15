import typer

from navfitx.fitrep_layout import app as fitrep_app
from navfitx.gui import app as gui_app
from navfitx.overlay import app as overlay_app

app = typer.Typer(no_args_is_help=True, add_completion=False)

app.add_typer(fitrep_app)
app.add_typer(overlay_app)
app.add_typer(gui_app)

app()
