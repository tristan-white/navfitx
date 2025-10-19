import typer

from navfitx.fitrep_layout import app as fitrep_app

app = typer.Typer(no_args_is_help=True, add_completion=False)

app.add_typer(fitrep_app)

app()
