import shutil
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
from sqlmodel import Session, SQLModel, create_engine, select

from navfitx.constants import BUPERSINST_URL, GITHUB_URL
from navfitx.models import Fitrep
from navfitx.utils import add_fitrep_to_db, get_blank_report_path

from .fitrep import FitrepForm


class Home(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db: Path | None = None
        self.reports_table: QTableWidget = QTableWidget()
        headers = ["Rank/Rate", "Full Name", "SSN", "Report", "To Date", "Record ID", "Validated"]
        self.reports_table.setRowCount(0)
        self.reports_table.setColumnCount(len(headers))
        self.reports_table.setHorizontalHeaderLabels(headers)
        self.reports_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.reports_table.cellDoubleClicked.connect(self.edit_fitrep_from_table)

        self.setWindowTitle("NAVFITX")

        # central widget container
        self.stack = QStackedWidget()
        self.stack.currentChanged.connect(self.on_stack_index_changed)
        # create home widget via method (moved from former HomeWidget class)
        self.stack.addWidget(self.create_home_widget())
        self.setCentralWidget(self.stack)

    def build_home_menu(self):
        self.menuBar().clear()
        file_menu = self.menuBar().addMenu("File")
        self.new_submenu = file_menu.addMenu("New")

        if not self.db:
            self.new_submenu.setDisabled(True)

        new_eval_action = self.new_submenu.addAction("Evaluation")
        new_eval_action.setDisabled(True)  # not implemented yet

        new_chief_action = self.new_submenu.addAction("Chief Evaluation")
        new_chief_action.setDisabled(True)  # not implemented yet

        fitness_report_action = self.new_submenu.addAction("Fitness Report")
        fitness_report_action.triggered.connect(self.open_fitrep_dialog)

        self.new_submenu.addAction("Folder")
        create_db_action = file_menu.addAction("Create Database")
        create_db_action.triggered.connect(self.create_db)
        open_db_action = file_menu.addAction("Open Database")
        open_db_action.triggered.connect(self.open_db)

        close_db_action = file_menu.addAction("Close Database")
        close_db_action.setDisabled(True)

        export_folder_action = file_menu.addAction("Export Folder")
        export_folder_action.setDisabled(True)
        import_data_action = file_menu.addAction("Import Data")
        import_data_action.setDisabled(True)
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        edit_menu = self.menuBar().addMenu("Edit")

        print_menu = self.menuBar().addMenu("Print")
        print_folder_action = print_menu.addAction("Print Folder")
        print_folder_action.setDisabled(True)

        print_blank_fitrep_action = print_menu.addAction("Print Blank FITREP")
        print_blank_fitrep_action.triggered.connect(lambda: self.print_blank("fitrep"))

        print_blank_chief = print_menu.addAction("Print Blank Chief Eval")
        print_blank_chief.triggered.connect(lambda: self.print_blank("chief"))

        print_blank_eval = print_menu.addAction("Print Blank Evaluation")
        print_blank_eval.triggered.connect(lambda: self.print_blank("eval"))

        print_blank_summary = print_menu.addAction("Print Blank Summary Letter")
        print_blank_summary.triggered.connect(lambda: self.print_blank("summary"))

        edit_report_submenu = edit_menu.addMenu("Edit Report")
        edit_report_submenu.setDisabled(True)

        edit_folder_action = edit_report_submenu.addAction("Edit Folder")
        edit_folder_action.setDisabled(True)

        delete_submenu = edit_menu.addMenu("Delete")
        delete_submenu.setDisabled(True)
        self.delete_folder_action = delete_submenu.addAction("Delete Folder")
        self.delete_folder_action.setDisabled(True)

        help_menu = self.menuBar().addMenu("Help")
        about_navfitx_action = help_menu.addAction("About NAVFITX")
        about_navfitx_action.triggered.connect(lambda: self.open_link(GITHUB_URL))

        instruction = help_menu.addAction("Instructions (BUPERSINST 1610.10H)")
        instruction.triggered.connect(lambda: self.open_link(BUPERSINST_URL))

    def build_form_menu(self):
        self.menuBar().clear()
        file_menu = self.menuBar().addMenu("File")
        save_action = file_menu.addAction("Save")
        save_action.triggered.connect(self.submit_form)

        print_action = file_menu.addAction("Print")
        print_action.triggered.connect(self.fitrep_form.print)
        close_action = file_menu.addAction("Close")
        close_action.triggered.connect(self.set_index_to_home)

    def on_stack_index_changed(self, index: int):
        if index == 0:
            self.setWindowTitle("NAVFITX")
            self.build_home_menu()
        elif index == 1:
            self.build_form_menu()
            self.setWindowTitle("FITREP Data Entry")

    def open_fitrep_dialog(self, fitrep: Fitrep | None = None):
        self.fitrep_form = FitrepForm(self.submit_form, self.set_index_to_home, fitrep)

        # Menu must be built after form is created so that actions can connect to it
        self.build_form_menu()

        self.stack.addWidget(self.fitrep_form)
        self.stack.setCurrentIndex(1)

    def open_db(self):
        filename, selected_filter = QFileDialog.getOpenFileName(
            self, "Open Database", filter="Database Files (*.db *.sqlite);;All Files (*)"
        )
        # TODO: validate that selected file is a valid navfitx database
        if filename:
            self.db = Path(filename)
            self.refresh_reports_table()
            self.new_submenu.setDisabled(False)

    def create_db(self):
        filename, selected_filter = QFileDialog.getSaveFileName(self, "Create Database", "navfitx.db")
        engine = create_engine(f"sqlite:///{filename}")
        SQLModel.metadata.create_all(engine)
        self.db = Path(filename)
        self.new_submenu.setDisabled(False)

    def open_link(self, url: str):
        webbrowser.open(url)

    def submit_form(self, fitrep: Fitrep):
        assert self.db is not None
        add_fitrep_to_db(self.db, fitrep)
        self.refresh_reports_table()
        i = self.stack.currentIndex()
        self.stack.setCurrentIndex(0)
        self.stack.removeWidget(self.stack.widget(i))

    def set_index_to_home(self):
        self.stack.setCurrentIndex(0)

    def print_blank(self, report_type: str):
        filename, selected_filter = QFileDialog.getSaveFileName(
            self, f"Save Blank {report_type.upper()} Report", f"{report_type}.pdf"
        )

        report_path = get_blank_report_path(report_type)
        shutil.copy(report_path, filename)

    # New: create the home widget here instead of a separate class
    def create_home_widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # folder tree
        folder_tree = self.create_folder_tree()
        # reports table
        self.refresh_reports_table()
        # buttons
        buttons_groupbox = self.create_buttons_groupbox()

        layout.addWidget(folder_tree)
        layout.addWidget(QLabel("Reports"))
        layout.addWidget(self.reports_table)
        layout.addWidget(buttons_groupbox)

        return widget

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

    def edit_fitrep_from_table(self, x: int, y: int) -> Fitrep | None:
        item = self.reports_table.item(x, y)
        assert item is not None

        if not self.db:
            return None

        row = item.row()
        record_id_item = self.reports_table.item(row, 5)  # assuming Record ID is in column 5
        assert record_id_item is not None

        record_id = int(record_id_item.text())
        print(f"record id: {record_id}")
        engine = create_engine(f"sqlite:///{self.db}")
        with Session(engine) as session:
            stmt = select(Fitrep).where(Fitrep.id == record_id)
            fitrep = session.exec(stmt).first()
        self.open_fitrep_dialog(fitrep)

    def refresh_reports_table(self):
        if not self.db:
            return

        self.reports_table.clearContents()

        engine = create_engine(f"sqlite:///{self.db}")
        with Session(engine) as session:
            stmt = select(Fitrep)
            results = list(session.exec(stmt))
            self.reports_table.setRowCount(len(results))
            for i, fitrep in enumerate(results):
                self.reports_table.setItem(i, 0, QTableWidgetItem(fitrep.grade))
                self.reports_table.setItem(i, 1, QTableWidgetItem(fitrep.name))
                self.reports_table.setItem(i, 2, QTableWidgetItem(fitrep.ssn))
                self.reports_table.setItem(i, 3, QTableWidgetItem("FitRep"))
                self.reports_table.setItem(i, 4, QTableWidgetItem(str(fitrep.period_start)))
                self.reports_table.setItem(i, 5, QTableWidgetItem(str(fitrep.id)))
                self.reports_table.setItem(i, 6, QTableWidgetItem("no"))

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
