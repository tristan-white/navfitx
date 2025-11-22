# import QStackedWidget
import webbrowser
from pathlib import Path

from PySide6 import QtWidgets
from PySide6.QtGui import (
    QAction,
)
from PySide6.QtWidgets import (
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .fitrep import FitrepDialog


def open_dir():
    dir = QFileDialog.getExistingDirectory(None, "Select Directory", options=QFileDialog.Option.ShowDirsOnly)
    if dir:
        path = Path(dir)
        print(path)


def open_navfitx_github():
    url = "https://github.com/tristan-white/navfitx"
    webbrowser.open(url)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NAVFITX")

        # set up menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        new_submenu = file_menu.addMenu("New")
        new_submenu.addAction("Evaluation")
        fitness_report_action = new_submenu.addAction("Fitness Report")
        fitness_report_action.triggered.connect(self.open_fitrep_dialog)
        new_submenu.addAction("Chief Evaluation")
        new_submenu.addAction("Folder")
        create_db_action = file_menu.addAction("Create Database")
        create_db_action.triggered.connect(open_dir)
        file_menu.addAction("Open Database")
        file_menu.addAction("Close Database")
        file_menu.addAction("Export Folder")
        file_menu.addAction("Import Data")
        file_menu.addAction("Exit")

        edit_menu = menubar.addMenu("Edit")

        print_menu = menubar.addMenu("Print")
        print_menu.addAction("Print Folder")

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

        # central widget container
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # index 0
        self.home_page = HomeWidget()
        self.home_page.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.stack.addWidget(self.home_page)

        # index 1
        # self.fitrep_form = FitrepDialog()
        # self.stack.addWidget(self.fitrep_form)

        self.stack.setCurrentIndex(0)

    def open_fitrep_dialog(self):
        # self.stack.setCurrentIndex(1)
        fitrep_form = FitrepDialog(self)
        fitrep_form.exec()
        fitrep_form.print()


class HomeWidget(QWidget):
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

    def create_reports_table(self) -> QGroupBox:
        group_box = QGroupBox("Reports")
        reports_table = QTableWidget()
        headers = ["Rank/Rate", "Full Name", "SSN", "Report", "To Date", "Record ID", "Validated"]
        reports_table.setRowCount(3)
        reports_table.setColumnCount(len(headers))
        reports_table.setHorizontalHeaderLabels(headers)

        row1 = ["CWTC", "DOE, JOHN A", "123-45-6789", "Chief", "15SEP2026", "1", "Yes"]
        row2 = ["LTJG", "DOE, JOHN A", "123-45-6789", "FitRep", "28FEB2026", "2", "Yes"]
        row3 = ["CTI", "DOE, JOHN A", "123-45-6789", "Eval", "30JUN2026", "3", "Yes"]
        for i, row in enumerate([row1, row2, row3]):
            for j, v in enumerate(row):
                reports_table.setItem(i, j, QTableWidgetItem(v))
        reports_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout = QHBoxLayout(group_box)
        layout.addWidget(reports_table)
        return group_box

    def create_buttons_groupbox(self) -> QGroupBox:
        group_box = QGroupBox()

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
        col3_layout.addWidget(print_summary)
        col3_layout.addWidget(print_report)
        col3_layout.addWidget(import_data)
        col3_layout.addWidget(export_folder)
        col3_layout.addWidget(export_report)
        col3_layout.addStretch(1)

        layout = QHBoxLayout(group_box)
        layout.addStretch(1)
        layout.addLayout(col1_layout)
        layout.addLayout(col2_layout)
        layout.addLayout(col3_layout)
        layout.addStretch(1)

        return group_box
