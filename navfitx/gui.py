import sys
import webbrowser

import typer
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QGridLayout, QMainWindow, QPushButton, QWidget

app = typer.Typer(no_args_is_help=True, add_completion=False)


def open_navfitx_github():
    url = "https://github.com/tristan-white/navfitx"
    webbrowser.open(url)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NAVFITX")

        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        new_submenu = file_menu.addMenu("New")
        new_submenu.addAction(QAction("Evaluation", self))
        new_submenu.addAction(QAction("Fitness Report", self))
        new_submenu.addAction(QAction("Chief Evaluation", self))
        new_submenu.addAction(QAction("Folder", self))

        file_menu.addAction(QAction("Create Database", self))
        file_menu.addAction(QAction("Open Database", self))
        file_menu.addAction(QAction("Close Database", self))
        file_menu.addAction(QAction("Export Folder", self))
        file_menu.addAction(QAction("Import Data", self))
        file_menu.addAction(QAction("Exit", self))

        edit_menu = menubar.addMenu("Edit")

        edit_report_submenu = edit_menu.addMenu("Edit Eval/Fitrep")
        edit_report_submenu.addAction(QAction("Edit Folder", self))

        delete_submenu = edit_menu.addMenu("Delete")
        delete_submenu.addAction(QAction("Delete Folder", self))

        # validate_submenu = edit_menu.addMenu("Validate")

        # lookup_tables_submenu = edit_menu.addMenu("Lookup Tables")

        # print_menu = menubar.addMenu("Print")

        help_menu = menubar.addMenu("Help")
        help_menu.addAction(QAction("User Guide", self))
        open_github_action = QAction("About NAVFITX", self)
        help_menu.addAction(open_github_action)

        open_github_action.triggered.connect(open_navfitx_github)

        # self.setLayout(MyWidget().buttons)

        window = MyWidget()

        self.setCentralWidget(window)


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout(self)
        layout.setVerticalSpacing(0)
        # self.buttons.addWidget( QtWidgets.QPushButton("test"), 0, 0)

        layout.addWidget(QPushButton("Create Folder"), 0, 0)
        layout.addWidget(QPushButton("Edit Folder"), 1, 0)
        layout.addWidget(QPushButton("Delete Folder"), 2, 0)
        layout.addWidget(QPushButton("Print Folder"), 3, 0)
        layout.addWidget(QPushButton("Validate Folder Reports"), 4, 0)
        layout.addWidget(QPushButton("Validate Report"), 5, 0)

        layout.addWidget(QPushButton("Create FitRep"), 0, 1)
        layout.addWidget(QPushButton("Create Chief Eval"), 1, 1)
        layout.addWidget(QPushButton("Create Eval"), 2, 1)
        layout.addWidget(QPushButton("Edit Report"), 3, 1)
        layout.addWidget(QPushButton("Delete Report"), 4, 1)

        layout.addWidget(QPushButton("Print Summary"), 0, 2)
        layout.addWidget(QPushButton("Print Report"), 1, 2)
        layout.addWidget(QPushButton("Import Data"), 2, 2)
        layout.addWidget(QPushButton("Export Folder"), 3, 2)
        layout.addWidget(QPushButton("Export Report"), 4, 2)

        # self.text = QLabel("Hello World", alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

        # self.layout = QtWidgets.QVBoxLayout(self)
        # self.layout.addLayout(self.buttons)
        # self.layout.addWidget(self.delete_folder)
        # self.layout.addLayout(self.buttons)

    #     self.create_folder.clicked.connect(self.magic)

    # @QtCore.Slot()
    # def magic(self):
    #     self.text.setText(random.choice(self.hello))


@app.command()
def gui():
    # app = QtWidgets.QApplication([])

    # widget = MyWidget()
    # widget.resize(800, 600)
    # widget.show()

    # sys.exit(app.exec())

    app = QApplication()
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
