import json
import textwrap
from enum import Enum
from pathlib import Path
from typing import Callable

from pydantic import ValidationError
from PySide6.QtCore import QDate, Qt, Slot
from PySide6.QtGui import QFont, QTextOption
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDialogButtonBox,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from navfitx.constants import DUTIES_DESC_SPACE_FOR_ABBREV
from navfitx.models import (
    BilletSubcategory,
    Eval,
    Fitrep,
    PhysicalReadiness,
    PromotionRecommendation,
    PromotionStatus,
    SummaryGroup,
)


class NoScrollDateEdit(QDateEdit):
    """This is a normal QDateEdit that ignores wheel events to prevent accidental changes when scrolling."""

    def wheelEvent(self, event):
        event.ignore()


class NoScrollComboBox(QComboBox):
    """This is a normal QComboBox that ignores wheel events to prevent accidental changes when scrolling."""

    def wheelEvent(self, event):
        event.ignore()


class EvalForm(QWidget):
    perf_traits = {
        "": None,
        "Not Observed": 0,
        "1 - Below Standards": 1,
        "2 - Progressing": 2,
        "3 - Meets Standards": 3,
        "4 - Above Standards": 4,
        "5 - Greatly Exceeds Standards": 5,
    }
    promotion_recs = {
        "": None,
        "NOB": PromotionRecommendation.NOB.value,
        "Significant Problems": PromotionRecommendation.SIGNIFICANT_PROBLEMS.value,
        "Progressing": PromotionRecommendation.PROGRESSING.value,
        "Promotable": PromotionRecommendation.PROMOTABLE.value,
        "Must Promote": PromotionRecommendation.MUST_PROMOTE.value,
        "Early Promote": PromotionRecommendation.EARLY_PROMOTE.value,
    }

    def __init__(
        self,
        main: QMainWindow,
        on_accept: Callable[[Fitrep], None],
        on_reject: Callable[[], None],
        eval: Eval | None,
    ):
        super().__init__()
        self.eval = eval or Eval()
        self.on_accept = on_accept
        self.on_reject = on_reject

        self.setWindowTitle("EVAL Data Entry")

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        grid_layout = QGridLayout()
        grid_layout.setColumnStretch(0, 0)
        container_widget = QWidget()
        container_widget.setLayout(grid_layout)

        grid_layout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)

        self.name = QLineEdit()
        self.name.setText(self.eval.name)
        self.name.setFont(QFont("Courier"))
        self.name.setPlaceholderText("LAST, FIRST MI Suffix")
        self.name.editingFinished.connect(self.validate_name)
        grid_layout.addWidget(QLabel("Name"), 0, 0)
        grid_layout.addWidget(self.name, 0, 1)

        self.grade = QLineEdit()
        self.grade.setText(self.eval.rate)
        self.grade.setFont(QFont("Courier"))
        self.grade.editingFinished.connect(self.validate_grade)
        grid_layout.addWidget(QLabel("Rank"), 0, 2)
        grid_layout.addWidget(self.grade, 0, 3)

        self.desig = QLineEdit()
        self.desig.setFont(QFont("Courier"))
        self.desig.setText(self.eval.desig)
        grid_layout.addWidget(QLabel("Designator"), 1, 0)
        grid_layout.addWidget(self.desig, 1, 1)

        self.ssn = QLineEdit()
        self.ssn.setFont(QFont("Courier"))
        self.ssn.setText(self.eval.ssn)
        self.ssn.setPlaceholderText("XXX-XX-XXXX")
        self.ssn.editingFinished.connect(self.validate_ssn)
        grid_layout.addWidget(QLabel("SSN"), 1, 2)
        grid_layout.addWidget(self.ssn, 1, 3)

        self.group = NoScrollComboBox()
        # AT/ADSW/265 does not match the ATADSW option in BUPERS, the NAVFIT98 user guide, nor
        # the NAVFIT98 .accdb database, but it is what is shown on paper reports themselves,
        # so it's used here to look the same as the form.
        self.group.addItem("")
        self.group.addItems([member.value for member in SummaryGroup])
        grid_layout.addWidget(QLabel("Group"), 2, 0)
        grid_layout.addWidget(self.group, 2, 1)

        self.uic = QLineEdit()
        self.uic.setFont(QFont("Courier"))
        self.uic.setText(self.eval.uic)
        self.uic.editingFinished.connect(self.validate_uic)
        grid_layout.addWidget(QLabel("UIC"), 2, 2)
        grid_layout.addWidget(self.uic, 2, 3)

        self.station = QLineEdit()
        self.station.setText(self.eval.station)
        self.station.setFont(QFont("Courier"))
        self.station.editingFinished.connect(self.validate_ship_station)
        grid_layout.addWidget(QLabel("Ship/Station"), 3, 0)
        grid_layout.addWidget(self.station, 3, 1)

        self.promotion_status = NoScrollComboBox(currentText=self.eval.promotion_status)
        self.promotion_status.addItem("")
        self.promotion_status.addItems([member.value for member in PromotionStatus])
        self.promotion_status.setCurrentIndex(self.get_idx_for_enum(self.eval.promotion_status))
        grid_layout.addWidget(QLabel("Promotion Status"), 3, 2)
        grid_layout.addWidget(self.promotion_status, 3, 3)

        # Move Date Reported so it appears before Type of Report in the grid
        self.date_reported = NoScrollDateEdit(calendarPopup=True, displayFormat="dd MMMM yyyy")  # type: ignore[call-overload]
        if self.eval.date_reported is not None:
            y = self.eval.date_reported.year
            m = self.eval.date_reported.month
            d = self.eval.date_reported.day
            self.date_reported.setDate(QDate(y, m, d))
        grid_layout.addWidget(QLabel("Date Reported"), 4, 0)
        grid_layout.addWidget(self.date_reported, 4, 1)

        group_box = QGroupBox("Occasion for Report")
        self.periodic = QCheckBox("Periodic")
        self.periodic.setChecked(self.eval.periodic)
        self.periodic.checkStateChanged.connect(self.validate_occasion)
        self.det_indiv = QCheckBox("Detachment of Individual")
        self.det_indiv.setChecked(self.eval.det_indiv)
        self.det_indiv.checkStateChanged.connect(self.validate_occasion)
        self.prom_frock = QCheckBox("Promotion/Frocking")
        self.prom_frock.setChecked(self.eval.prom_frock)
        self.prom_frock.checkStateChanged.connect(self.validate_occasion)
        self.special = QCheckBox("Special")
        self.special.setChecked(self.eval.special)
        self.special.checkStateChanged.connect(self.validate_special)
        vbox = QHBoxLayout()
        vbox.addWidget(self.periodic)
        vbox.addWidget(self.det_indiv)
        vbox.addWidget(self.prom_frock)
        vbox.addWidget(self.special)
        group_box.setLayout(vbox)
        grid_layout.addWidget(group_box, 4, 2, 1, 2)

        self.period_start = NoScrollDateEdit(calendarPopup=True, displayFormat="dd MMMM yyyy")  # type: ignore[call-overload]
        if self.eval.period_start:
            y = self.eval.period_start.year
            m = self.eval.period_start.month
            d = self.eval.period_start.day
            self.period_start.setDate(QDate(y, m, d))
        grid_layout.addWidget(QLabel("Period Start"), 6, 0)
        grid_layout.addWidget(self.period_start, 6, 1)

        self.period_end = NoScrollDateEdit(calendarPopup=True, displayFormat="dd MMMM yyyy")  # type: ignore[call-overload]
        if self.eval.period_end:
            y = self.eval.period_end.year
            m = self.eval.period_end.month
            d = self.eval.period_end.day
            self.period_end.setDate(QDate(y, m, d))
        grid_layout.addWidget(QLabel("Period End"), 6, 2)
        grid_layout.addWidget(self.period_end, 6, 3)

        self.not_observed = QCheckBox()
        self.not_observed.setChecked(self.eval.not_observed)
        grid_layout.addWidget(QLabel("Not Observed Report"), 7, 0)
        grid_layout.addWidget(self.not_observed, 7, 1)

        group_box = QGroupBox("Type of Report")
        self.regular = QCheckBox("Regular")
        self.regular.setChecked(self.eval.regular)

        self.concurrent = QCheckBox("Concurrent")
        self.concurrent.setChecked(self.eval.concurrent)
        self.concurrent.checkStateChanged.connect(self.validate_concurrent)

        # self.ops_cdr = QCheckBox("OpsCdr")
        # self.ops_cdr.setChecked(self.eval.ops_cdr)
        # self.ops_cdr.checkStateChanged.connect(self.validate_ops_cdr)
        # hbox = QHBoxLayout()
        # hbox.addWidget(self.regular)
        # hbox.addWidget(self.concurrent)
        # hbox.addWidget(self.ops_cdr)
        # group_box.setLayout(hbox)
        # grid_layout.addWidget(group_box, 7, 2, 1, 2)

        self.physical_readiness = NoScrollComboBox()
        self.physical_readiness.addItem("")
        self.physical_readiness.addItems([member.value for member in PhysicalReadiness])
        self.physical_readiness.setCurrentIndex(self.get_idx_for_enum(self.eval.physical_readiness))
        grid_layout.addWidget(QLabel("Physical Readiness"), 8, 0)
        grid_layout.addWidget(self.physical_readiness, 8, 1)

        self.billet_subcategory = NoScrollComboBox()
        self.billet_subcategory.addItem("")
        self.billet_subcategory.addItems([member.value for member in BilletSubcategory])
        self.billet_subcategory.setCurrentIndex(self.get_idx_for_enum(self.eval.billet_subcategory))
        grid_layout.addWidget(QLabel("Billet Subcategory"), 8, 2)
        grid_layout.addWidget(self.billet_subcategory, 8, 3)

        self.senior_name = QLineEdit()
        self.senior_name.setFont(QFont("Courier"))
        self.senior_name.setText(self.eval.senior_name)
        self.senior_name.setPlaceholderText("LAST, FI MI")
        grid_layout.addWidget(QLabel("Reporting Senior Name"), 9, 0)
        grid_layout.addWidget(self.senior_name, 9, 1)

        self.senior_grade = QLineEdit()
        self.senior_grade.setFont(QFont("Courier"))
        self.senior_grade.setText(self.eval.senior_grade)
        grid_layout.addWidget(QLabel("Reporting Senior Grade"), 9, 2)
        grid_layout.addWidget(self.senior_grade, 9, 3)

        self.senior_desig = QLineEdit()
        self.senior_desig.setFont(QFont("Courier"))
        self.senior_desig.setText(self.eval.senior_desig)
        grid_layout.addWidget(QLabel("Reporting Senior Designator"), 10, 0)
        grid_layout.addWidget(self.senior_desig, 10, 1)

        self.senior_title = QLineEdit()
        self.senior_title.setFont(QFont("Courier"))
        self.senior_title.setText(self.eval.senior_title)
        grid_layout.addWidget(QLabel("Reporting Senior Title"), 10, 2)
        grid_layout.addWidget(self.senior_title, 10, 3)

        self.senior_uic = QLineEdit()
        self.senior_uic.setFont(QFont("Courier"))
        self.senior_uic.setText(self.eval.senior_uic)
        grid_layout.addWidget(QLabel("Reporting Senior UIC"), 11, 0)
        grid_layout.addWidget(self.senior_uic, 11, 1)

        self.senior_ssn = QLineEdit()
        self.senior_ssn.setFont(QFont("Courier"))
        self.senior_ssn.setText(self.eval.senior_ssn)
        self.senior_ssn.setPlaceholderText("XXX-XX-XXXX")
        grid_layout.addWidget(QLabel("Reporting Senior SSN"), 11, 2)
        grid_layout.addWidget(self.senior_ssn, 11, 3)

        self.job = QTextEdit(tabChangesFocus=True, lineWrapMode=QTextEdit.LineWrapMode.FixedColumnWidth)
        self.job.setFont(QFont("Courier"))
        self.job.setPlaceholderText("Maximum of 3 lines. Excess lines will be trimmed.")
        self.job.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.job.setLineWrapColumnOrWidth(92)
        self.job.setText(self.eval.job)
        line_height = self.job.fontMetrics().lineSpacing()
        self.job.setFixedHeight(int(line_height * 3.6))  # I don't know why, but 4 isn't quite tall enough.
        self.job.setFixedWidth(900)

        self.job_label = QLabel(
            f"Command Employment and\nCommand Achievements\n"
            f"(Line Count: {len(Eval.wrap_text(self.job.toPlainText(), 92).split('\n'))}/3)"
        )
        self.job.textChanged.connect(
            lambda: self.job_label.setText(
                f"Command Employment and\nCommand Achievements\n"
                f"(Line Count: {len(Eval.wrap_text(self.job.toPlainText(), 92).split('\n'))}/3)"
            )
        )

        # grid_layout.addWidget(QLabel("Command Employment and\nCommand Achievements"), 12, 0)
        grid_layout.addWidget(self.job_label, 12, 0)
        grid_layout.addWidget(self.job, 12, 1, 1, 3)

        self.duties_abbreviation = QLineEdit()
        self.duties_abbreviation.setFont(QFont("Courier"))
        self.duties_abbreviation.setPlaceholderText("(14 characters max)")
        self.duties_abbreviation.setMaxLength(14)
        self.duties_abbreviation.setFixedWidth(180)
        self.duties_abbreviation.setText(self.eval.duties_abbreviation)
        grid_layout.addWidget(QLabel("Primary Duty Abbreviation"), 13, 0)
        grid_layout.addWidget(self.duties_abbreviation, 13, 1)

        self.duties_description = QTextEdit(tabChangesFocus=True, lineWrapMode=QTextEdit.LineWrapMode.FixedColumnWidth)
        self.duties_description.setFont(QFont("Courier"))
        self.duties_description.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        if self.duties_description == "":
            self.duties_description.setText(" " * DUTIES_DESC_SPACE_FOR_ABBREV)
        else:
            self.duties_description.setText(f"{' ' * DUTIES_DESC_SPACE_FOR_ABBREV}{self.eval.duties_description}")
        self.duties_description.setLineWrapColumnOrWidth(91)
        line_height = self.duties_description.fontMetrics().lineSpacing()
        self.duties_description.setFixedHeight(
            int(line_height * 4.6)
        )  # I don't know why, but 4 isn't quite tall enough.
        self.duties_description.setFixedWidth(900)
        self.duties_description.setPlaceholderText("Maximum of 4 lines. Excess lines will be trimmed.")
        # self.duties_description.selectionChanged.connect(self.validate_duties_description)

        duties_desc_label = QLabel("Primary/Collateral/Watchstanding Duties")
        duties_desc_label.setToolTip(
            "Maximum of 4 lines, but first line must have 21 leading spaces to leave room for the duties abbreviation box."
        )
        grid_layout.addWidget(duties_desc_label, 14, 0)
        grid_layout.addWidget(self.duties_description, 14, 1, 1, 3)

        self.date_counseled = NoScrollDateEdit(calendarPopup=True, displayFormat="dd MMMM yyyy")  # type: ignore[call-overload]
        if self.eval.date_counseled:
            y = self.eval.date_counseled.year
            m = self.eval.date_counseled.month
            d = self.eval.date_counseled.day
            self.date_counseled.setDate(QDate(y, m, d))
        grid_layout.addWidget(QLabel("Date Counseled"), 15, 0)
        grid_layout.addWidget(self.date_counseled, 15, 1)

        self.counselor = QLineEdit()
        self.counselor.setFont(QFont("Courier"))
        self.counselor.setText(self.eval.counselor)
        grid_layout.addWidget(QLabel("Counselor"), 15, 2)
        grid_layout.addWidget(self.counselor, 15, 3)

        self.pro_knowledge = NoScrollComboBox()
        self.pro_knowledge.addItems([p for p in self.perf_traits.keys()])
        if self.eval.prof_knowledge is not None:
            self.pro_knowledge.setCurrentIndex(self.eval.prof_knowledge + 1)
        grid_layout.addWidget(QLabel("Professional Knowledge"), 16, 0)
        grid_layout.addWidget(self.pro_knowledge, 16, 1)

        self.quality_of_work = NoScrollComboBox()
        self.quality_of_work.addItems([p for p in self.perf_traits.keys()])
        if self.eval.quality_of_work is not None:
            self.quality_of_work.setCurrentIndex(self.eval.quality_of_work + 1)
        grid_layout.addWidget(QLabel("Quality of Work"), 16, 2)
        grid_layout.addWidget(self.quality_of_work, 16, 3)

        self.cmd_climate = NoScrollComboBox()
        self.cmd_climate.addItems([p for p in self.perf_traits.keys()])
        if self.eval.cmd_climate is not None:
            self.cmd_climate.setCurrentIndex(self.eval.cmd_climate + 1)
        grid_layout.addWidget(QLabel("Command or Organizational Climate"), 17, 0)
        grid_layout.addWidget(self.cmd_climate, 17, 1)

        self.bearing_and_character = NoScrollComboBox()
        self.bearing_and_character.addItems([p for p in self.perf_traits.keys()])
        if self.eval.bearing_and_character is not None:
            self.bearing_and_character.setCurrentIndex(self.eval.bearing_and_character + 1)
        grid_layout.addWidget(QLabel("Military Bearing/Character"), 17, 2)
        grid_layout.addWidget(self.bearing_and_character, 17, 3)

        self.initiative = NoScrollComboBox()
        self.initiative.addItems([p for p in self.perf_traits.keys()])
        if self.eval.initiative is not None:
            self.initiative.setCurrentIndex(self.eval.initiative + 1)
        grid_layout.addWidget(QLabel("Personal Job\nAccomplishment/Initiative"), 18, 0)
        grid_layout.addWidget(self.initiative, 18, 1)

        self.teamwork = NoScrollComboBox()
        self.teamwork.addItems([p for p in self.perf_traits.keys()])
        if self.eval.teamwork is not None:
            self.teamwork.setCurrentIndex(self.eval.teamwork + 1)
        grid_layout.addWidget(QLabel("Teamwork"), 18, 2)
        grid_layout.addWidget(self.teamwork, 18, 3)

        self.leadership = NoScrollComboBox()
        self.leadership.addItems([p for p in self.perf_traits.keys()])
        if self.eval.leadership is not None:
            self.leadership.setCurrentIndex(self.eval.leadership + 1)
        grid_layout.addWidget(QLabel("Leadership"), 19, 0)
        grid_layout.addWidget(self.leadership, 19, 1)

        self.career_rec_1 = QTextEdit(tabChangesFocus=True, lineWrapMode=QTextEdit.LineWrapMode.FixedColumnWidth)
        self.career_rec_1.setToolTip("Maximum of 20 characters and two lines.")
        self.career_rec_1.setWordWrapMode(QTextOption.WrapMode.WrapAnywhere)
        self.career_rec_1.setText(self.eval.career_rec_1)
        self.career_rec_1.setLineWrapColumnOrWidth(13)
        self.career_rec_1.setFont(QFont("Courier"))
        line_spacing = self.career_rec_1.fontMetrics().lineSpacing()
        self.career_rec_1.setFixedHeight(int(line_spacing * 2.6))
        # self.career_rec_1.setFixedWidth(900)
        self.career_rec_1.textChanged.connect(self.validate_career_rec1)
        grid_layout.addWidget(QLabel("Career Recommendation 1"), 20, 0)
        grid_layout.addWidget(self.career_rec_1, 20, 1)

        self.career_rec_2 = QTextEdit(tabChangesFocus=True, lineWrapMode=QTextEdit.LineWrapMode.FixedColumnWidth)
        self.career_rec_2.setToolTip("Maximum of 20 characters and two lines.")
        self.career_rec_2.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.career_rec_2.setText(self.eval.career_rec_2)
        self.career_rec_2.setLineWrapColumnOrWidth(13)
        self.career_rec_2.setFont(QFont("Courier"))
        line_height = self.career_rec_2.fontMetrics().lineSpacing()
        self.career_rec_2.setFixedHeight(int(line_height * 2.6))
        # self.career_rec_2.setFixedWidth(900)
        grid_layout.addWidget(QLabel("Career Recommendation 2"), 20, 2)
        grid_layout.addWidget(self.career_rec_2, 20, 3)

        self.comments = QTextEdit(tabChangesFocus=True, lineWrapMode=QTextEdit.LineWrapMode.FixedColumnWidth)
        self.comments.setText(self.eval.comments)
        self.comments.setPlaceholderText("Maximum of 18 lines. Excess lines will be trimmed.")
        self.comments.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.comments.setLineWrapColumnOrWidth(92)
        self.comments.setFont(QFont("Courier"))
        line_height = self.comments.fontMetrics().lineSpacing()
        self.comments.setFixedHeight(int(line_height * 18))
        self.comments.setFixedWidth(900)
        # self.comments.textChanged.connect(self.validate_comments)

        self.comments_label = QLabel(
            f"Comments\n\n(Line Count: {len(Fitrep.wrap_text(self.comments.toPlainText(), 92).split('\n'))}/18)"
        )
        # num_lines = len(Fitrep.format_comments(self.comments.toPlainText()).split())
        self.comments.textChanged.connect(
            lambda: self.comments_label.setText(
                f"Comments\n\n(Line Count: {len(Fitrep.wrap_text(self.comments.toPlainText(), 92).split('\n'))}/18)"
            )
        )

        grid_layout.addWidget(self.comments_label, 22, 0)
        grid_layout.addWidget(self.comments, 22, 1, 1, 3)

        self.indiv_promo_rec = NoScrollComboBox()
        self.indiv_promo_rec.addItems([k for k in self.promotion_recs.keys()])
        if self.eval.indiv_promo_rec is not None:
            self.indiv_promo_rec.setCurrentIndex(self.eval.indiv_promo_rec + 1)
        grid_layout.addWidget(QLabel("Promotion Reccomendation"), 23, 0)
        grid_layout.addWidget(self.indiv_promo_rec, 23, 1)

        self.senior_address = QTextEdit()
        self.senior_address.setText(self.eval.senior_address)
        self.senior_address.setLineWrapMode(QTextEdit.LineWrapMode.FixedColumnWidth)
        self.senior_address.setLineWrapColumnOrWidth(27)
        self.senior_address.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.senior_address.setFont(QFont("Courier"))
        line_height = self.name.fontMetrics().lineSpacing()
        self.senior_address.setFixedHeight(line_height * 5)
        self.senior_address.setFixedWidth(500)
        grid_layout.addWidget(QLabel("Reporting Senior Address"), 24, 0)
        grid_layout.addWidget(self.senior_address, 24, 1, 1, 3)

        # layout = QVBoxLayout()
        # grid_layout.addItem(QSpacerItem(0, 0))
        # grid_layout.setRowStretch(15, 1)

        # ---- buttons ----
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        ok_btn = button_box.button(QDialogButtonBox.StandardButton.Ok)
        ok_btn.setText("Save")
        button_box.accepted.connect(self.submit)
        button_box.rejected.connect(self.on_reject)

        scroll_area.setWidget(container_widget)

        # Set the layout for the secondary window
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        main_layout.addWidget(button_box)

        # Set the layout for the secondary window
        self.setLayout(main_layout)

        # Build the form-specific menu on the provided main window
        self.build_menu(main)

    def build_menu(self, main: QMainWindow) -> None:
        """Attach form-specific menu items to the main window's menu bar."""
        menu_bar = main.menuBar()
        menu_bar.clear()

        file_menu = menu_bar.addMenu("File")
        print_action = file_menu.addAction("Export as PDF")
        print_action.triggered.connect(self.print)
        close_action = file_menu.addAction("Close")

        # Connect close to the provided on_reject callback so Home can handle stack cleanup
        close_action.triggered.connect(self.on_reject)

        tools = menu_bar.addMenu("Tools")
        validate_action = tools.addAction("Validate Report")
        validate_action.triggered.connect(self.validate_report)

        # validate_action.setDisabled(True)  # not implemented yet
        spell_check_action = tools.addAction("Spell Check")
        spell_check_action.setDisabled(True)  # not implemented yet

    def validate_report(self):
        """Perform validation on all fields in the form."""
        try:
            Fitrep.model_validate(self.fitrep.model_dump())
        except ValidationError as err:
            errors = json.loads(err.json())
            # show a list of all validation errors
            error_messages = "\n".join([f"{error['loc'][0]}: {error['msg']}" for error in errors])

            test = QMessageBox()
            test.setWindowModality(Qt.WindowModality.NonModal)
            test.information(self, "Validation", error_messages)
            # test.show()

    @staticmethod
    def get_idx_for_enum(member: Enum | None) -> int:
        """
        Return 1-based index of the enum member within its enum class, or 0 if None/not found.

        Useful for setting QComboBox current index based on enum member.
        """
        if member is None:
            return 0
        return list(type(member).__members__).index(member.name) + 1

    @Slot()
    def validate_special(self, check_state: Qt.CheckState):
        if check_state == Qt.CheckState.Checked:
            self.det_indiv.setChecked(False)
            self.prom_frock.setChecked(False)
            self.periodic.setChecked(False)

    @Slot()
    def validate_occasion(self, check_state: Qt.CheckState):
        if check_state == Qt.CheckState.Checked:
            self.special.setChecked(False)

    @Slot()
    def validate_ops_cdr(self, check_state: Qt.CheckState):
        if check_state == Qt.CheckState.Checked:
            self.concurrent.setChecked(False)

    @Slot()
    def validate_concurrent(self, check_state: Qt.CheckState):
        if check_state == Qt.CheckState.Checked:
            self.concurrent.setChecked(False)

    @Slot()
    def validate_career_rec1(self):
        text = self.career_rec_1.document().toPlainText()
        # width is 13 because that's what navfit98 allows on one line
        wrapped = textwrap.wrap(text, width=13)
        if len(text) > 20:
            QMessageBox.information(
                self,
                "Career Reccomendation Validation",
                "Maximum of 20 characters allowed (including whitespace)",
                QMessageBox.StandardButton.Ok,
            )
            self.career_rec_1.setText(text[:20])
        if len(wrapped) > 2:
            QMessageBox.information(
                self,
                "Career Reccomendation Validation",
                "Carreer Reccomenation may not exceed two lines.",
                QMessageBox.StandardButton.Ok,
            )
            allowed_text = "\n".join(wrapped[:2])
            self.career_rec_1.setText(allowed_text)

    @Slot()
    def validate_ship_station(self):
        if not self.station.text().isalnum() or len(self.station.text()) > 18:
            QMessageBox.information(
                self,
                "Ship/Station Validation",
                "Maximum of 18 characters allowed. Only letters and number are permitted.",
                QMessageBox.StandardButton.Ok,
            )
            self.station.setText("")

    @Slot()
    def validate_name(self):
        self.name.setText(self.name.text().upper())

    @Slot()
    def validate_grade(self):
        if len(self.grade.text()) > 5:
            QMessageBox.information(
                self, "Grade Validation", "Rank/Grade cannot be more than 5 characters.", QMessageBox.StandardButton.Ok
            )
            return
        for char in self.grade.text():
            if not char.isalpha():
                QMessageBox.information(
                    self, "Grade Validation", "Rank/Grade may only contain letters.", QMessageBox.StandardButton.Ok
                )
                return

    @Slot()
    def validate_desig(self):
        if len(self.desig.text()) > 5:
            QMessageBox.information(
                self,
                "Designator Validation",
                "Designator must be less than 12 characters.",
                QMessageBox.StandardButton.Ok,
            )

    @Slot()
    def validate_ssn(self):
        self.ssn.setText(self.ssn.text().strip())
        ssn_text = self.ssn.text()
        if len(ssn_text) != 11 or ssn_text[3] != "-" or ssn_text[6] != "-":
            QMessageBox.information(
                self, "SSN Validation", "SSN must be in the format XXX-XX-XXXX.", QMessageBox.StandardButton.Ok
            )
            return
        for i, char in enumerate(ssn_text):
            if i in [3, 6]:
                continue
            if not char.isdigit():
                QMessageBox.information(
                    self, "SSN Validation", "SSN must be in the format XXX-XX-XXXX.", QMessageBox.StandardButton.Ok
                )
                return

    @Slot()
    def validate_uic(self):
        if len(self.uic.text()) > 5:
            QMessageBox.information(
                self,
                "Block 40 Validation",
                "Block 40 may only have up to 20 alpha-numeric characters.",
                QMessageBox.StandardButton.Ok,
            )
        for char in self.uic.text():
            if not char.isalnum():
                QMessageBox.information(
                    self,
                    "UIC Validation",
                    "UIC may only contain alphanumeric characters.",
                    QMessageBox.StandardButton.Ok,
                )

    @Slot()
    def validate_billet_subcategory(self):
        if "SPECIAL" in self.billet_subcategory.currentData():
            QMessageBox.information(
                self,
                "Billet Subcategory Validation",
                "Note: 'SPECIAL' subcategories are only permitted use with Commander, Navy Personnel Command approval.",
                QMessageBox.StandardButton.Ok,
            )

    @Slot()
    def validate_duties_description(self):
        """
        This block is funky because of the duteis abbreviation block, which takes up some space on the first line.
        I think the best solution that makes for an acceptable UX is to initialize the box with spaces. However,
        the user may delete these, in which case they should be added back so the user sees and accurate line
        count. This function, therefore, is not used to validate the length, but rather strip the text of
        leading/trailing whitespace, then re-add the spaces to the beginning to ensure the line count is accurate.
        """
        self.duties_description.setText(
            f"{' ' * DUTIES_DESC_SPACE_FOR_ABBREV}{self.duties_description.toPlainText().strip()}"
        )

    def print(self):
        self.save_form()
        filename, selected_filter = QFileDialog.getSaveFileName(self, "Export FITREP PDF", "fitrep.pdf")
        if filename:
            # create_fitrep_pdf(self.fitrep, Path(filename))
            self.eval.create_pdf(Path(filename))

    def submit(self):
        self.save_form()
        self.on_accept(self.fitrep)

    def save_form(self):
        """
        Create a Fitrep class from the data input in the GUI Form.
        """
        self.eval.name = self.name.text()
        self.eval.rate = self.grade.text()
        self.eval.desig = self.desig.text()
        self.eval.ssn = self.ssn.text()
        group_text = self.group.currentText()
        self.eval.group = None if group_text == "" else SummaryGroup(group_text)
        self.eval.uic = self.uic.text()
        self.eval.station = self.station.text()
        self.eval.promotion_status = (
            None if self.promotion_status.currentText() == "" else PromotionStatus(self.promotion_status.currentText())
        )
        self.eval.date_reported = self.date_reported.date().toPython()
        self.eval.periodic = self.periodic.isChecked()
        self.eval.det_indiv = self.det_indiv.isChecked()
        self.eval.prom_frock = self.prom_frock.isChecked()
        self.eval.special = self.special.isChecked()
        self.eval.period_start = self.period_start.date().toPython()
        self.eval.period_end = self.period_end.date().toPython()
        self.eval.not_observed = self.not_observed.isChecked()
        self.eval.regular = self.regular.isChecked()
        self.eval.concurrent = self.concurrent.isChecked()

        if self.physical_readiness.currentText() == "":
            self.eval.physical_readiness = None
        else:
            self.eval.physical_readiness = PhysicalReadiness(self.physical_readiness.currentText())

        if self.billet_subcategory.currentText() == "":
            self.eval.billet_subcategory = None
        else:
            self.eval.billet_subcategory = BilletSubcategory(self.billet_subcategory.currentText())

        self.eval.senior_name = self.senior_name.text()
        self.eval.senior_grade = self.senior_grade.text()
        self.eval.senior_desig = self.senior_desig.text()
        self.eval.senior_title = self.senior_title.text()
        self.eval.senior_uic = self.senior_uic.text()
        self.eval.senior_ssn = self.senior_ssn.text()
        self.eval.duties_abbreviation = self.duties_abbreviation.text()
        self.eval.duties_description = self.duties_description.toPlainText().strip()
        self.eval.job = self.job.toPlainText()
        self.eval.date_counseled = self.date_counseled.date().toPython()
        self.eval.counselor = self.counselor.text()
        self.eval.prof_knowledge = self.perf_traits[self.pro_knowledge.currentText()]
        self.eval.quality_of_work = self.perf_traits[self.quality_of_work.currentText()]
        self.eval.cmd_climate = self.perf_traits[self.cmd_climate.currentText()]
        self.eval.bearing_and_character = self.perf_traits[self.bearing_and_character.currentText()]
        self.eval.initiative = self.perf_traits[self.initiative.currentText()]
        self.eval.teamwork = self.perf_traits[self.teamwork.currentText()]
        self.eval.leadership = self.perf_traits[self.leadership.currentText()]
        self.eval.career_rec_1 = Fitrep.validate_career_rec(self.career_rec_1.toPlainText())
        self.eval.career_rec_2 = self.career_rec_2.toPlainText()
        self.eval.comments = Fitrep.validate_comments(self.comments.toPlainText())
        self.eval.indiv_promo_rec = self.promotion_recs[self.indiv_promo_rec.currentText()]
        self.eval.senior_address = self.senior_address.toPlainText()
