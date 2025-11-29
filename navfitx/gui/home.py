# import QStackedWidget
import webbrowser
from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
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
from sqlmodel import SQLModel, create_engine

from navfitx.models import Fitrep, Report
from navfitx.utils import add_report_to_db

from .fitrep import FitrepForm


class Home(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db: Path | None = None

        self.setWindowTitle("NAVFITX")

        # Set up menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        new_submenu = file_menu.addMenu("New")
        # new_submenu.setDisabled(True)

        new_eval_action = new_submenu.addAction("Evaluation")
        new_eval_action.setDisabled(True)  # not implemented yet

        new_chief_action = new_submenu.addAction("Chief Evaluation")
        new_chief_action.setDisabled(True)  # not implemented yet

        fitness_report_action = new_submenu.addAction("Fitness Report")
        fitness_report_action.triggered.connect(self.open_fitrep_dialog)

        new_submenu.addAction("Folder")
        create_db_action = file_menu.addAction("Create Database")
        create_db_action.triggered.connect(self.create_db)
        file_menu.addAction("Open Database")
        self.close_db_action = file_menu.addAction("Close Database")
        self.export_folder_action = file_menu.addAction("Export Folder")
        self.export_folder_action.setDisabled(True)
        self.import_data_action = file_menu.addAction("Import Data")
        self.import_data_action.setDisabled(True)
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        edit_menu = menubar.addMenu("Edit")

        print_menu = menubar.addMenu("Print")
        self.print_folder_action = print_menu.addAction("Print Folder")

        edit_report_submenu = edit_menu.addMenu("Edit Report")
        self.edit_folder_action = edit_report_submenu.addAction("Edit Folder")
        self.edit_folder_action.setDisabled(True)

        delete_submenu = edit_menu.addMenu("Delete")
        self.delete_folder_action = delete_submenu.addAction("Delete Folder")
        self.delete_folder_action.setDisabled(True)

        help_menu = menubar.addMenu("Help")
        self.about_navfitx_action = help_menu.addAction("About NAVFITX")
        self.about_navfitx_action.triggered.connect(self.open_navfitx_github)

        # central widget container
        self.stack = QStackedWidget()
        self.stack.addWidget(HomeWidget())

        # self.home_page.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.setCentralWidget(self.stack)
        # self.stack.addWidget(self.home_page)

        # index 1
        # self.fitrep_form = FitrepDialog()
        # self.stack.addWidget(self.fitrep_form)

        # self.stack.setCurrentIndex(0)

    def open_fitrep_dialog(self):
        self.fitrep = FitrepForm(self.add_fitrep_to_db)
        self.stack.addWidget(self.fitrep)
        self.stack.setCurrentIndex(1)
        # self.fitrep.show()

    def create_db(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        filename, selected_filter = dialog.getSaveFileName(
            None, "Create a File for NAVFITX", filter="SQLite Database (*.sqlite)"
        )
        assert filename
        db_path = Path(f"{filename}.sqlite")
        engine = create_engine(f"sqlite:///{db_path}")
        SQLModel.metadata.create_all(engine)
        self.db = db_path

    def open_navfitx_github(self):
        url = "https://github.com/tristan-white/navfitx"
        webbrowser.open(url)

    def add_report_to_db(self, report: Report):
        assert self.db is not None
        add_report_to_db(self.db, report)

    def add_fitrep_to_db(self, fitrep: Fitrep):
        # assert self.db is not None
        # add_fitrep_to_db(self.db, fitrep)
        self.stack.setCurrentIndex(0)


class HomeWidget(QWidget):
    def __init__(self):
        super().__init__()

        # self.setWindowIcon(QIcon(/path/to/image))

        layout = QVBoxLayout(self)

        self.folder_tree = self.create_folder_tree()

        # reports_group_box = QGroupBox("Reports")
        self.reports_table = self.get_reports_table()
        layout.addWidget(self.reports_table)

        buttons_groupbox = self.create_buttons_groupbox()
        layout.addWidget(self.folder_tree)
        layout.addWidget(QLabel("Reports"))
        layout.addWidget(self.reports_table)
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

    def get_reports_table(self) -> QTableWidget:
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
        return reports_table

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
