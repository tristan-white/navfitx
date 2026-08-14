import json
import shutil
import tomllib
import webbrowser
from datetime import date
from pathlib import Path

from platformdirs import user_config_dir
from PySide6.QtCore import QPoint, Qt, Slot
from PySide6.QtGui import QResizeEvent, QShowEvent
from PySide6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMenu,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)
from sqlmodel import Session, SQLModel, create_engine, select

from navfitx import __version__
from navfitx.constants import APP_AUTHOR, APP_NAME, BUPERSINST_URL, FEEDBACK_URL, SITE_URL
from navfitx.db import add_fitrep_to_db
from navfitx.models import Eval, Fitrep, Report
from navfitx.utils import get_blank_report_path

from .eval import EvalForm
from .fitrep import FitrepForm


class Home(QMainWindow):
    """
    The main window for the NAVFITX GUI app (ie what is seen when the app is opened).
    """

    REPORT_LIST_NAME_COLUMN = 1
    REPORT_LIST_MIN_NAME_COLUMN_WIDTH = 180
    REPORT_LIST_DEFAULT_COLUMN_WIDTHS = {
        0: 120,  # Rank/Rate
        1: 280,  # Full Name (adjusted dynamically)
        2: 130,  # SSN
        3: 100,  # Report
        4: 140,  # Period End
        5: 90,  # Report ID
    }

    def setup_reports_table_context_menu(self):
        self.reports_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.reports_table.customContextMenuRequested.connect(self.show_reports_table_context_menu)

    @Slot(int, int, int)
    def on_report_list_column_resized(self, column: int, old_size: int, new_size: int) -> None:
        if self._is_updating_report_list_columns:
            return
        if old_size == new_size:
            return

        if column != self.REPORT_LIST_NAME_COLUMN:
            return
        if new_size >= self.REPORT_LIST_MIN_NAME_COLUMN_WIDTH:
            return

        self._is_updating_report_list_columns = True
        try:
            self.reports_table.setColumnWidth(self.REPORT_LIST_NAME_COLUMN, self.REPORT_LIST_MIN_NAME_COLUMN_WIDTH)
        finally:
            self._is_updating_report_list_columns = False

    def configure_report_list_column_fill_mode(self) -> None:
        header = self.reports_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.sectionResized.connect(self.on_report_list_column_resized)

        self._is_updating_report_list_columns = True
        try:
            for column, width in self.REPORT_LIST_DEFAULT_COLUMN_WIDTHS.items():
                self.reports_table.setColumnWidth(column, width)
        finally:
            self._is_updating_report_list_columns = False

        self.update_report_list_name_column_width()

    def update_report_list_name_column_width(self) -> None:
        if self.reports_table.columnCount() <= self.REPORT_LIST_NAME_COLUMN:
            return

        viewport_width = self.reports_table.viewport().width()
        if viewport_width <= 0:
            return

        other_columns_width = 0
        for i in range(self.reports_table.columnCount()):
            if i == self.REPORT_LIST_NAME_COLUMN:
                continue
            other_columns_width += self.reports_table.columnWidth(i)

        name_column_width = max(self.REPORT_LIST_MIN_NAME_COLUMN_WIDTH, viewport_width - other_columns_width)
        self._is_updating_report_list_columns = True
        try:
            self.reports_table.setColumnWidth(self.REPORT_LIST_NAME_COLUMN, name_column_width)
        finally:
            self._is_updating_report_list_columns = False

    @Slot(QPoint)
    def show_reports_table_context_menu(self, pos):
        menu = QMenu(self)
        edit_action = menu.addAction("Edit Report")
        delete_action = menu.addAction("Delete Report")
        action = menu.exec(self.reports_table.viewport().mapToGlobal(pos))
        selected_row = self.reports_table.currentRow()
        if selected_row < 0:
            return
        if action == edit_action:
            # Simulate double-click to edit
            self.edit_report_from_table(selected_row, 0)
        elif action == delete_action:
            report_id_item = self.reports_table.item(selected_row, 5)
            report_type_item = self.reports_table.item(selected_row, 3)
            if report_id_item and report_type_item:
                report_id = int(report_id_item.text())
                report_type = report_type_item.text()
                self.delete_report_by_id(report_id, report_type)
                self.refresh_reports_table()

    def delete_report_by_id(self, report_id: int, report_type: str):
        if not self.db:
            return
        engine = create_engine(f"sqlite:///{self.db}")
        with Session(engine) as session:
            if report_type.lower() == "fitrep":
                fitrep = session.exec(select(Fitrep).where(Fitrep.id == report_id)).first()
                if fitrep:
                    session.delete(fitrep)
                    session.commit()
                    return
            elif report_type.lower() == "eval":
                eval = session.exec(select(Eval).where(Eval.id == report_id)).first()
                if eval:
                    session.delete(eval)
                    session.commit()
                    return

    def __init__(self) -> None:
        super().__init__()

        self.db: Path | None = None
        self.sort_column = 4
        self.sort_ascending = False
        self._reports_cache: list[Report] = []
        self._is_updating_report_list_columns = False

        # Load last-used database path from previous session (if any)
        self.load_last_db()
        if self.db:
            # refresh table and enable create button if DB was restored
            try:
                self.refresh_reports_table()
            except Exception:
                # Avoid crashing the UI if the restored DB is invalid/missing
                pass
            # if hasattr(self, "create_fitrep_btn"):
            #     self.create_fitrep_btn.setDisabled(False)
            # if hasattr(self, "create_eval_btn"):
            #     self.create_eval_btn.setDisabled(False)

        # if self.db is not None:
        #     left_label = QLabel(f"NAVFITX Database: {self.db}")
        #     left_label.setToolTip("This file contains saved reports.")
        #     self.statusBar().addWidget(left_label)
        # right_label = QLabel("Right text")
        # self.statusBar().addPermanentWidget(right_label) # Bottom right

        self.reports_table: QTableWidget = QTableWidget()
        self.setup_reports_table_context_menu()
        # self.reports_table.setToolTip("Double click a Report to edit it.")
        self.reports_table.setToolTip("Right click a Report to see options.")
        headers = ["Rank/Rate", "Full Name", "SSN", "Report", "Period End", "Report ID"]
        self.reports_table.setRowCount(0)
        self.reports_table.setColumnCount(len(headers))
        self.reports_table.setHorizontalHeaderLabels(headers)
        self.reports_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.reports_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        header = self.reports_table.horizontalHeader()
        header.setSectionsClickable(True)
        header.setSortIndicatorShown(True)
        header.sectionClicked.connect(self.sort_reports_by_column)
        self.configure_report_list_column_fill_mode()
        self.update_sort_indicator()

        self.reports_table.cellDoubleClicked.connect(self.edit_report_from_table)

        self.setWindowTitle(f"NAVFITX v{__version__}")

        # Central widget container
        self.stack = QStackedWidget()
        self.stack.currentChanged.connect(self.on_stack_index_changed)

        # Create home widget via method (moved from former HomeWidget class)
        self.stack.addWidget(self.create_home_widget())
        self.setCentralWidget(self.stack)

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        self.update_report_list_name_column_width()

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.update_report_list_name_column_width()

    def build_home_menu(self):
        self.menuBar().clear()
        file_menu = self.menuBar().addMenu("File")
        self.new_submenu = file_menu.addMenu("New")

        # import_menu = file_menu.addMenu("Import")
        # import_toml_action = import_menu.addAction("Import Report from TOML")
        # import_toml_action.triggered.connect(self.import_toml_report)

        if not self.db:
            self.new_submenu.setDisabled(True)
            # import_menu.setDisabled(True)

        new_eval_action = self.new_submenu.addAction("Evaluation")
        new_eval_action.setDisabled(False)
        new_eval_action.triggered.connect(lambda: self.open_eval_dialog(Eval()))

        new_chief_action = self.new_submenu.addAction("Chief Evaluation")
        new_chief_action.setDisabled(True)  # not implemented yet

        fitness_report_action = self.new_submenu.addAction("Fitness Report")
        fitness_report_action.triggered.connect(lambda: self.open_fitrep_dialog(Fitrep()))

        folder_action = self.new_submenu.addAction("Folder")
        folder_action.setDisabled(True)  # not implemented yet
        create_db_action = file_menu.addAction("Create Database")
        create_db_action.triggered.connect(self.create_db)
        open_db_action = file_menu.addAction("Open Database")
        open_db_action.triggered.connect(self.open_db)

        close_db_action = file_menu.addAction("Close Database")
        close_db_action.triggered.connect(self.close_db)
        # close_db_action.setDisabled(True)

        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        print_menu = self.menuBar().addMenu("Print")

        print_blank_eval = print_menu.addAction("Blank Evaluation")
        print_blank_eval.triggered.connect(lambda: self.print_blank("eval"))

        print_blank_chief = print_menu.addAction("Blank Chief Eval")
        print_blank_chief.triggered.connect(lambda: self.print_blank("chief"))

        print_blank_fitrep_action = print_menu.addAction("Blank Fitness Report")
        print_blank_fitrep_action.triggered.connect(lambda: self.print_blank("fitrep"))

        print_blank_summary = print_menu.addAction("Blank Summary Letter")
        print_blank_summary.triggered.connect(lambda: self.print_blank("summary"))

        help_menu = self.menuBar().addMenu("Help")

        instruction = help_menu.addAction("Instructions (BUPERSINST 1610.10H)")
        instruction.triggered.connect(lambda: self.open_link(BUPERSINST_URL))

        feedback_action = help_menu.addAction("Give Feedback")
        feedback_action.triggered.connect(lambda: self.open_link(FEEDBACK_URL))

        about_navfitx_action = help_menu.addAction("About NAVFITX")
        about_navfitx_action.triggered.connect(lambda: self.open_link(SITE_URL))

    def open_eval_dialog(self, eval: Eval):
        # self.statusBar().hide()
        self.eval_form = EvalForm(self, self.submit_form, self.cancel_form, eval)
        idx = self.stack.addWidget(self.eval_form)
        self.stack.setCurrentIndex(idx)
        self.setWindowTitle("EVAL")

    def open_fitrep_dialog(self, fitrep: Fitrep):
        # self.statusBar().hide()
        self.fitrep_form = FitrepForm(self, self.submit_form, self.cancel_form, fitrep)
        idx = self.stack.addWidget(self.fitrep_form)
        self.stack.setCurrentIndex(idx)

    @Slot(int)
    def on_stack_index_changed(self, index: int):
        """Handle stack index changes: restore home menu on index 0, set form title on index 1."""
        if index == 0:
            # self.statusBar().show()
            self.setWindowTitle(f"NAVFITX v{__version__}")
            self.build_home_menu()
        elif index == 1:
            # FitrepForm constructs its own menu when created.
            self.setWindowTitle("FITREP")

    @Slot()
    def close_db(self):
        self.db = None
        self.refresh_reports_table()
        self.new_submenu.setDisabled(True)
        self.reports_table_label.setText("Reports (No database open)")
        # self.create_fitrep_btn.setDisabled(True)
        # self.create_eval_btn.setDisabled(True)
        # remove persisted last DB since there is no open DB now
        try:
            self.save_last_db(None)
        except Exception:
            pass

    @Slot()
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
            # self.create_fitrep_btn.setDisabled(False)
            # self.create_eval_btn.setDisabled(False)
            self.reports_table_label.setText(f"Reports ({self.db})")

    @Slot()
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
        # self.create_fitrep_btn.setDisabled(False)
        # self.create_eval_btn.setDisabled(False)
        self.refresh_reports_table()
        self.reports_table_label.setText(f"Reports ({self.db})")

    def import_toml_report(self):
        filename, selected_filter = QFileDialog.getOpenFileName(
            self, "Import Report from TOML", filter="TOML Files (*.toml);;All Files (*)"
        )
        if not filename:
            return
        path = Path(filename)
        if not path.exists():
            return
        try:
            # check if it's a toml file by trying to parse it with tomllib
            content = path.read_text(encoding="utf-8")
            data = tomllib.loads(path.read_text(encoding="utf-8"))
            if "doc_type" not in data:
                # not a valid report toml if doc_type is missing
                print("Invalid report TOML: missing doc_type")
                return
        except Exception:
            # if parsing fails, it's not a valid toml file
            # TODO: add error message box
            return

        # add report to DB
        try:
            if data["doc_type"] == "fitrep":
                report = Fitrep.from_toml(content)
            # elif data["doc_type"] == "eval":
            #     report = Eval.from_toml(content)
            else:
                print("Unknown doc_type in TOML")
                return
            self.submit_form(report)
        except Exception as e:
            print(f"Failed to import report TOML: {e}")

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

    def submit_form(self, report: Report):
        assert self.db is not None
        add_fitrep_to_db(self.db, report)
        self.refresh_reports_table()
        i = self.stack.currentIndex()
        self.stack.setCurrentIndex(0)
        widget = self.stack.widget(i)
        if widget is not None:
            # i == 0 when importing reports on the home screen
            if i != 0:
                self.stack.removeWidget(widget)

    @Slot()
    def cancel_form(self):
        i = self.stack.currentIndex()
        self.stack.setCurrentIndex(0)
        w = self.stack.widget(i)
        if w is None:
            raise Exception("No widget found at current stack index during cancel_form")
        self.stack.removeWidget(w)

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

        db_path_str = f"{self.db}" if self.db else "No database open"
        self.reports_table_label = QLabel(f"Reports ({db_path_str})")
        layout.addWidget(self.reports_table_label)

        layout.addWidget(self.reports_table, 1)

        # Uncomment to add buttons below the table
        # buttons_groupbox = self.create_buttons_groupbox()
        # layout.addWidget(buttons_groupbox)

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

    @Slot(int, int)
    def edit_report_from_table(self, x: int, y: int):
        item = self.reports_table.item(x, y)
        assert item is not None
        if not self.db:
            return None
        row = item.row()

        # Assumes Record ID is col 5 and type is row 3
        record_id_item = self.reports_table.item(row, 5)
        assert record_id_item is not None

        report_type_item = self.reports_table.item(row, 3)
        assert report_type_item is not None

        record_id = int(record_id_item.text())
        report_type = report_type_item.text()

        engine = create_engine(f"sqlite:///{self.db}")
        with Session(engine) as session:
            match report_type.lower():
                case "fitrep":
                    stmt = select(Fitrep).where(Fitrep.id == record_id)
                    report = session.exec(stmt).first()
                    assert report is not None
                    self.open_fitrep_dialog(report)
                case "eval":
                    stmt = select(Eval).where(Eval.id == record_id)
                    report = session.exec(stmt).first()
                    assert report is not None
                    self.open_eval_dialog(report)
                case _:
                    print("unknown report type")
                    return

    @Slot(int)
    def sort_reports_by_column(self, column: int) -> None:
        if self.sort_column == column:
            self.sort_ascending = not self.sort_ascending
        else:
            self.sort_column = column
            self.sort_ascending = True
        self.render_reports_table()

    def update_sort_indicator(self) -> None:
        sort_order = Qt.SortOrder.AscendingOrder if self.sort_ascending else Qt.SortOrder.DescendingOrder
        self.reports_table.horizontalHeader().setSortIndicator(self.sort_column, sort_order)

    def get_report_id_for_sort(self, report: Report) -> int:
        if report.id is None:
            return -1
        return report.id

    def get_period_end_for_sort(self, report: Report) -> date | None:
        period_end = report.period_end
        if isinstance(period_end, date):
            return period_end
        if isinstance(period_end, str):
            try:
                return date.fromisoformat(period_end)
            except ValueError:
                return None
        return None

    def get_sorted_reports(self) -> list[Report]:
        reports = list(self._reports_cache)
        if self.sort_column == 4:

            def period_end_key(report: Report) -> tuple[bool, date | int, int]:
                period_end = self.get_period_end_for_sort(report)
                report_id = self.get_report_id_for_sort(report)
                if self.sort_ascending:
                    return (period_end is None, period_end or date.min, -report_id)
                return (period_end is None, -(period_end or date.min).toordinal(), -report_id)

            return sorted(reports, key=period_end_key)

        if self.sort_column == 5:
            return sorted(
                reports,
                key=lambda report: self.get_report_id_for_sort(report),
                reverse=not self.sort_ascending,
            )
        if self.sort_column == 3:
            return sorted(
                reports,
                key=lambda report: report.doc_type.casefold(),
                reverse=not self.sort_ascending,
            )
        if self.sort_column == 2:
            return sorted(
                reports,
                key=lambda report: report.ssn.casefold(),
                reverse=not self.sort_ascending,
            )
        if self.sort_column == 1:
            return sorted(
                reports,
                key=lambda report: report.name.casefold(),
                reverse=not self.sort_ascending,
            )
        return sorted(
            reports,
            key=lambda report: report.rate.casefold(),
            reverse=not self.sort_ascending,
        )

    def render_reports_table(self) -> None:
        self.reports_table.clearContents()
        sorted_reports = self.get_sorted_reports()
        self.reports_table.setRowCount(len(sorted_reports))
        for i, report in enumerate(sorted_reports):
            self.reports_table.setItem(i, 0, QTableWidgetItem(report.rate))
            self.reports_table.setItem(i, 1, QTableWidgetItem(report.name))
            self.reports_table.setItem(i, 2, QTableWidgetItem(report.ssn))
            self.reports_table.setItem(i, 3, QTableWidgetItem(report.doc_type.upper()))
            period_end = self.get_period_end_for_sort(report)
            self.reports_table.setItem(i, 4, QTableWidgetItem(str(period_end) if period_end else ""))
            self.reports_table.setItem(i, 5, QTableWidgetItem(str(report.id) if report.id is not None else ""))
        self.update_sort_indicator()

    def refresh_reports_table(self):
        self.reports_table.clearContents()
        self.reports_table.setRowCount(0)
        self._reports_cache = []
        if not self.db:
            return

        engine = create_engine(f"sqlite:///{self.db}")
        with Session(engine) as session:
            stmt = select(Fitrep)
            results: list[Report] = list(session.exec(stmt))
            stmt = select(Eval)
            results.extend(list(session.exec(stmt)))
            self._reports_cache = results
            self.render_reports_table()

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

        self.create_fitrep_btn = QPushButton("Create FITREP")
        self.create_fitrep_btn.clicked.connect(lambda: self.open_fitrep_dialog(Fitrep()))
        self.create_fitrep_btn.setDisabled(True)
        self.create_chief_eval_btn = QPushButton("Create CHIEFEVAL")
        self.create_chief_eval_btn.setDisabled(True)
        self.create_eval_btn = QPushButton("Create EVAL")
        self.create_eval_btn.clicked.connect(lambda: self.open_eval_dialog(Eval()))
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
