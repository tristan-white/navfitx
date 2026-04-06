import sys

import typer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from navfitx.utils import get_icon_path

from .home import Home

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command()
def gui():
    """
    Launch the NAVFITX GUI application.
    """
    qt_app = QApplication()
    qt_app.setWindowIcon(QIcon(str(get_icon_path())))
    window = Home()
    # window.resize(800, 600)
    window.setGeometry(200, 200, 1300, 800)
    window.show()
    sys.exit(qt_app.exec())
