import json
import shutil
import webbrowser
from pathlib import Path

from platformdirs import user_config_dir
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

from navfitx.constants import APP_AUTHOR, APP_NAME, BUPERSINST_URL, GITHUB_URL
from navfitx.models import Fitrep
from navfitx.utils import add_fitrep_to_db, get_blank_report_path

from .fitrep import FitrepForm


class Home(QMainWindow):
    """
    The main window for the NAVFITX GUI app (ie what is seen when the app is opened).
    """

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

        # Load last-used database path from previous session (if any)
        self.load_last_db()
        if self.db:
            # refresh table and enable create button if DB was restored
            try:
                self.refresh_reports_table()
            except Exception:
                # Avoid crashing the UI if the restored DB is invalid/missing
                pass
            if hasattr(self, "create_fitrep_btn"):
                self.create_fitrep_btn.setDisabled(False)

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
        fitness_report_action.triggered.connect(lambda: self.open_fitrep_dialog(None))

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
        # save_action = file_menu.addAction("Save")
        # save_action.triggered.connect(self.submit_form)

        print_action = file_menu.addAction("Export as PDF")
        print_action.triggered.connect(self.fitrep_form.print)
        close_action = file_menu.addAction("Close")
        close_action.triggered.connect(self.cancel_form)

        tools = self.menuBar().addMenu("Tools")
        validate_action = tools.addAction("Validate Report")
        validate_action.setDisabled(True)  # not implemented yet
        spell_check_action = tools.addAction("Spell Check")
        spell_check_action.setDisabled(True)  # not implemented yet

    def on_stack_index_changed(self, index: int):
        if index == 0:
            self.setWindowTitle("NAVFITX")
            self.build_home_menu()
        elif index == 1:
            self.build_form_menu()
            self.setWindowTitle("FITREP Data Entry")

    def open_fitrep_dialog(self, fitrep: Fitrep | None = None):
        self.fitrep_form = FitrepForm(self.submit_form, self.cancel_form, fitrep)

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
            # persist selection for next session
            try:
                self.save_last_db(self.db)
            except Exception:
                pass
            self.refresh_reports_table()
            self.new_submenu.setDisabled(False)
            self.create_fitrep_btn.setDisabled(False)

    def create_db(self):
        filename, selected_filter = QFileDialog.getSaveFileName(self, "Create Database", "navfitx.db")
        if not filename:
            return
        path = Path(filename)
        if path.exists():
            path.unlink()
        engine = create_engine(f"sqlite:///{path}")
        SQLModel.metadata.create_all(engine)
        self.db = path
        # persist new database location
        try:
            self.save_last_db(self.db)
        except Exception:
            pass
        self.new_submenu.setDisabled(False)
        self.create_fitrep_btn.setDisabled(False)
        self.refresh_reports_table()

    # --- persistence helpers for remembering last-opened DB using platformdirs ---
    def _state_file(self) -> Path:
        """Return the path to the per-user state file used to persist simple UI state.

        Uses platformdirs.user_config_dir so state lives in the OS-appropriate location.
        """
        data_dir = Path(user_config_dir(APP_NAME, APP_AUTHOR))
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir / "state.json"

    def load_last_db(self) -> None:
        """Load the last-used database path from the state file (if present).

        Sets self.db to a Path if the file exists and the path is valid; otherwise leaves it None.
        """
        state_file = self._state_file()
        if not state_file.exists():
            return
        try:
            data = json.loads(state_file.read_text(encoding="utf-8"))
            last = data.get("last_db")
            if last:
                p = Path(last)
                if p.exists():
                    self.db = p
        except Exception:
            # Corrupt/invalid state should not break the app; ignore and continue
            return

    def save_last_db(self, db_path: Path | None) -> None:
        """Persist the provided database path to the state file. If db_path is None the state
        file will be removed.
        """
        state_file = self._state_file()
        if db_path is None:
            try:
                if state_file.exists():
                    state_file.unlink()
            except Exception:
                pass
            return
        payload = {"last_db": str(db_path)}
        state_file.write_text(json.dumps(payload), encoding="utf-8")

    def open_link(self, url: str):
        webbrowser.open(url)

    def submit_form(self, fitrep: Fitrep):
        assert self.db is not None
        add_fitrep_to_db(self.db, fitrep)
        self.refresh_reports_table()
        i = self.stack.currentIndex()
        self.stack.setCurrentIndex(0)
        self.stack.removeWidget(self.stack.widget(i))

    def cancel_form(self):
        i = self.stack.currentIndex()
        self.stack.setCurrentIndex(0)
        self.stack.removeWidget(self.stack.widget(i))

    def print_blank(self, report_type: str):
        filename, selected_filter = QFileDialog.getSaveFileName(
            self, f"Save Blank {report_type.upper()} Report", f"{report_type}.pdf"
        )
        if not filename:
            return
        report_path = get_blank_report_path(report_type)
        shutil.copy(report_path, filename)

    # New: create the home widget here instead of a separate class
    def create_home_widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # folder tree
        # folder_tree = self.create_folder_tree()
        # layout.addWidget(folder_tree)

        # reports table
        self.refresh_reports_table()
        layout.addWidget(QLabel("Reports"))

        # buttons
        buttons_groupbox = self.create_buttons_groupbox()
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

    def edit_fitrep_from_table(self, x: int, y: int):
        item = self.reports_table.item(x, y)
        assert item is not None

        if not self.db:
            return None

        row = item.row()

        # (Assumes Record ID is in column 5 of reports table)
        record_id_item = self.reports_table.item(row, 5)

        assert record_id_item is not None

        record_id = int(record_id_item.text())
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

        self.create_folder_btn = QPushButton("Create Folder")
        self.create_folder_btn.setDisabled(True)
        self.edit_folder_btn = QPushButton("Edit Folder")
        self.edit_folder_btn.setDisabled(True)
        self.delete_folder_btn = QPushButton("Delete Folder")
        self.delete_folder_btn.setDisabled(True)
        self.print_folder_btn = QPushButton("Print Folder")
        self.print_folder_btn.setDisabled(True)
        self.validate_folder_reports_btn = QPushButton("Validate Folder Reports")
        self.validate_folder_reports_btn.setDisabled(True)
        self.validate_report_btn = QPushButton("Validate Report")
        self.validate_report_btn.setDisabled(True)
        col1_layout = QVBoxLayout()
        col1_layout.addWidget(self.create_folder_btn)
        col1_layout.addWidget(self.edit_folder_btn)
        col1_layout.addWidget(self.delete_folder_btn)
        col1_layout.addWidget(self.print_folder_btn)
        col1_layout.addWidget(self.validate_folder_reports_btn)
        col1_layout.addWidget(self.validate_report_btn)
        col1_layout.addStretch(1)

        self.create_fitrep_btn = QPushButton("Create FitRep")
        self.create_fitrep_btn.clicked.connect(self.open_fitrep_dialog)
        self.create_fitrep_btn.setDisabled(True)
        self.create_chief_eval_btn = QPushButton("Create Chief Eval")
        self.create_chief_eval_btn.setDisabled(True)
        self.create_eval_btn = QPushButton("Create Eval")
        self.create_eval_btn.setDisabled(True)
        self.edit_report_btn = QPushButton("Edit Report")
        self.edit_report_btn.setDisabled(True)
        self.delete_report_btn = QPushButton("Delete Report")
        self.delete_report_btn.setDisabled(True)
        col2_layout = QVBoxLayout()
        col2_layout.addWidget(self.create_fitrep_btn)
        col2_layout.addWidget(self.create_chief_eval_btn)
        col2_layout.addWidget(self.create_eval_btn)
        col2_layout.addWidget(self.edit_report_btn)
        col2_layout.addWidget(self.delete_report_btn)
        col2_layout.addStretch(1)

        self.print_summary_btn = QPushButton("Print Summary")
        self.print_summary_btn.setDisabled(True)
        self.print_report_btn = QPushButton("Print Report")
        self.print_report_btn.setDisabled(True)
        self.import_data_btn = QPushButton("Import Data")
        self.import_data_btn.setDisabled(True)
        self.export_folder_btn = QPushButton("Export Folder")
        self.export_folder_btn.setDisabled(True)
        self.export_report_btn = QPushButton("Export Report")
        self.export_report_btn.setDisabled(True)
        col3_layout = QVBoxLayout()
        col3_layout.addWidget(self.print_summary_btn)
        col3_layout.addWidget(self.print_report_btn)
        col3_layout.addWidget(self.import_data_btn)
        col3_layout.addWidget(self.export_folder_btn)
        col3_layout.addWidget(self.export_report_btn)
        col3_layout.addStretch(1)

        layout = QHBoxLayout(group_box)
        layout.addStretch(1)
        layout.addLayout(col1_layout)
        layout.addLayout(col2_layout)
        layout.addLayout(col3_layout)
        layout.addStretch(1)

        return group_box
