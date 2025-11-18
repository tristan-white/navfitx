import sys

import typer
from PySide6.QtWidgets import QApplication

from .home import MainWindow

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command()
def gui():
    app = QApplication()
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
