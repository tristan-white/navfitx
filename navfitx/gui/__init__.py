import sys

import typer
from PySide6.QtWidgets import QApplication

from .home import Home

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command()
def gui():
    app = QApplication()
    window = Home()
    # window.resize(800, 600)
    window.setGeometry(200, 200, 1300, 800)
    window.show()
    sys.exit(app.exec())
