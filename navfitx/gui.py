import sys
import sys
from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem
from PySide6.QtWidgets import (QApplication, QTableWidget,
                               QTableWidgetItem)
from PySide6.QtCore import (QDateTime, QDir, QLibraryInfo, QSysInfo, Qt,
                            QTimer, Slot, qVersion)
from PySide6.QtGui import (QCursor, QDesktopServices, QGuiApplication, QIcon,
                           QKeySequence, QShortcut, QStandardItem,
                           QStandardItemModel)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox,
                               QCommandLinkButton, QDateTimeEdit, QDial,
                               QDialog, QDialogButtonBox, QFileSystemModel,
                               QGridLayout, QGroupBox, QHBoxLayout, QLabel,
                               QLineEdit, QListView, QMenu, QPlainTextEdit,
                               QProgressBar, QPushButton, QRadioButton,
                               QScrollBar, QSizePolicy, QSlider, QSpinBox,
                               QStyleFactory, QTableWidget, QTabWidget,
                               QTextBrowser, QTextEdit, QToolBox, QToolButton,
                               QTreeView, QVBoxLayout, QWidget)
import webbrowser

import typer
from PySide6 import QtWidgets
from PySide6.QtGui import (
    QAction,
)
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QTreeWidget,
    QVBoxLayout,
    QWidget,
)

data = {
    "Project A": ["file_a.py", "file_a.txt", "something.xls"],
    "Project B": ["file_b.csv", "photo.jpg"],
    "Project C": [],
}


app = typer.Typer(no_args_is_help=True, add_completion=False)


def open_navfitx_github():
    url = "https://github.com/tristan-white/navfitx"
    webbrowser.open(url)


app = typer.Typer(no_args_is_help=True, add_completion=False)


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
        window.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)

        self.setCentralWidget(window)


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        # self.setWindowIcon(QIcon(/path/to/image))

        layout = QGridLayout(self)
        # layout.setVerticalSpacing(0)
        # self.buttons.addWidget( QtWidgets.QPushButton("test"), 0, 0)

        # self.text = QLabel("Hello World", alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

        # self.layout = QtWidgets.QVBoxLayout(self)
        # self.layout.addLayout(self.buttons)
        # self.layout.addWidget(self.delete_folder)
        # self.layout.addLayout(self.buttons)

        folder_tree = self.create_folder_tree()
        reports_table = self.create_reports_table()
        buttons_groupbox = self.create_buttons_groupbox()
        layout.addWidget(folder_tree)
        layout.addWidget(reports_table)
        layout.addWidget(buttons_groupbox)
    
    def create_folder_tree(self) -> QTreeWidget:
        folder_tree = QTreeWidget()
        folder_tree.setWindowTitle("test")
        folder_tree.setColumnCount(1)
        folder_tree.setHeaderLabels(["Folders"])
        root = QTreeWidgetItem(["Root"])
        child = QTreeWidgetItem(["Child"])
        root.addChild(child)
        folder_tree.insertTopLevelItem(0, root)
        return folder_tree

    def create_reports_table(self) -> QTableWidget:
        reports_table = QTableWidget()
        headers = ["Rank/Rate", "Full Name", "SSN", "Report", "To Date", "Record ID", "Validated"]
        reports_table.setRowCount(3)
        reports_table.setColumnCount(len(headers))
        reports_table.setHorizontalHeaderLabels(headers)

        row1 = ["CWTC", "DOE, JOHN A", "123-45-6789", "Chief", "9/15/2026", "1", "No"]
        row2 = ["LTJG", "DOE, JOHN A", "123-45-6789", "FitRep", "2/28/2026", "2", "No"]
        row3 = ["CTN", "SMITH, TIMMY A", "123-45-6789", "Eval", "2024-06-30", "3", "No"]
        for i, row in enumerate([row1, row2, row3]):
            for j, v in enumerate(row):
                reports_table.setItem(i, j, QTableWidgetItem(v))
        return reports_table

    def create_buttons_groupbox(self) -> QGroupBox:
        group_box = QGroupBox("Buttons")

        create_folder = QPushButton("Create Folder")
        edit_folder = QPushButton("Edit Folder")
        delete_folder = QPushButton("Delete Folder")
        print_folder = QPushButton("Print Folder")
        validate_folder_reports = QPushButton("Validate Folder Reports")
        validate_report = QPushButton("Validate Report")
        col1_layout = QVBoxLayout()
        col1_layout.addWidget(create_folder)
        col1_layout.addWidget(edit_folder)
        col1_layout.addWidget(delete_folder)
        col1_layout.addWidget(print_folder)
        col1_layout.addWidget(validate_folder_reports)
        col1_layout.addWidget(validate_report)
        col1_layout.addStretch(1)

        create_fitrep = QPushButton("Create FitRep")
        create_chief_eval = QPushButton("Create Chief Eval")
        create_eval = QPushButton("Create Eval")
        edit_report = QPushButton("Edit Report")
        delete_report = QPushButton("Delete Report")
        col2_layout = QVBoxLayout()
        col2_layout.addWidget(create_fitrep)
        col2_layout.addWidget(create_chief_eval)
        col2_layout.addWidget(create_eval)
        col2_layout.addWidget(edit_report)
        col2_layout.addWidget(delete_report)
        col2_layout.addStretch(1)

        print_summary = QPushButton("Print Summary")
        print_report = QPushButton("Print Report")
        import_data = QPushButton("Import Data")
        export_folder = QPushButton("Export Folder")
        export_report = QPushButton("Export Report")
        col3_layout = QVBoxLayout()


        layout = QHBoxLayout(group_box)
        layout.addStretch(1)
        layout.addLayout(col1_layout)
        layout.addLayout(col2_layout)
        layout.addStretch(1)

        return group_box


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
