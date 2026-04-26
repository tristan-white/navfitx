import json
import textwrap
from enum import Enum
from pathlib import Path
from typing import Callable

from pydantic import ValidationError
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QCheckBox, QFileDialog, QHBoxLayout, QLayout, QMainWindow, QMessageBox

from navfitx.constants import DUTIES_DESC_SPACE_FOR_ABBREV
from navfitx.models import (
    Fitrep,
)

from .report import BaseReportForm


class FitrepForm(BaseReportForm[Fitrep]):
    def build_fields(self):
        super().build_fields()

    def __init__(
        self,
        main: QMainWindow,
        on_accept: Callable[[Fitrep], None],
        on_reject: Callable[[], None],
        report: Fitrep,
    ):
        super().__init__(
            main=main,
            on_accept=on_accept,
            on_reject=on_reject,
            report=report,
        )

        self.det_rs = QCheckBox("Detachment of Reporting Senior")

        occasion_layout = self.occasion_box.layout()
        assert isinstance(occasion_layout, QHBoxLayout)
        occasion_layout.insertWidget(2, self.det_rs)

        type_layout = self.type_box.layout()
        assert isinstance(type_layout, QLayout)
        self.ops_cdr = QCheckBox("OpsCdr")
        type_layout.addWidget(self.ops_cdr)

        self.add_label("Professional Expertise", 16, 0)
        self.add_label("Command or Organizational Climate", 16, 2)
        self.add_label("Military Bearing/Character", 17, 0)
        self.add_label("Teamwork", 17, 2)
        self.add_label("Mission Accomplishment and Initiative", 18, 0)
        self.add_label("Leadership", 18, 2)
        self.add_label("Tactical Performance", 19, 0)

        # label = QLabel("Normal text <a href='https://example.com'>link</a><br>", openExternalLinks=True)

        # self.setWindowTitle("FITREP Data Entry")

    #     self.ssn = QLineEdit()
    #     self.ssn.setFont(QFont("Courier"))
    #     self.ssn.setText(self.report.ssn)
    #     self.ssn.setInputMask("000-00-0000;_")
    #     grid_layout.addWidget(QLabel("SSN"), 1, 2)
    #     grid_layout.addWidget(self.ssn, 1, 3)

    #     self.group = NoScrollComboBox()
    #     # AT/ADSW/265 does not match the ATADSW option in BUPERS, the NAVFIT98 user guide, nor
    #     # the NAVFIT98 .accdb database, but it is what is shown on paper reports themselves,
    #     # so it's used here to look the same as the form.
    #     self.group.addItem("")
    #     self.group.addItems([member.value for member in SummaryGroup])
    #     if self.report.group is not None:
    #         self.group.setCurrentIndex(self.get_idx_for_enum(self.report.group))
    #     grid_layout.addWidget(QLabel("Group"), 2, 0)
    #     grid_layout.addWidget(self.group, 2, 1)

    #     self.uic = QLineEdit()
    #     self.uic.setFont(QFont("Courier"))
    #     self.uic.setText(self.report.uic)
    #     validator = QRegularExpressionValidator(QRegularExpression(r"[A-Za-z0-9]{0,5}"))
    #     self.uic.setValidator(validator)
    #     grid_layout.addWidget(QLabel("UIC"), 2, 2)
    #     grid_layout.addWidget(self.uic, 2, 3)

    #     self.station = QLineEdit()
    #     self.station.setText(self.report.station)
    #     self.station.setFont(QFont("Courier"))
    #     self.station.editingFinished.connect(self.validate_ship_station)
    #     grid_layout.addWidget(QLabel("Ship/Station"), 3, 0)
    #     grid_layout.addWidget(self.station, 3, 1)

    #     self.promotion_status = NoScrollComboBox(currentText=self.report.promotion_status)
    #     self.promotion_status.addItem("")
    #     self.promotion_status.addItems([member.value for member in PromotionStatus])
    #     self.promotion_status.setCurrentIndex(self.get_idx_for_enum(self.report.promotion_status))
    #     grid_layout.addWidget(QLabel("Promotion Status"), 3, 2)
    #     grid_layout.addWidget(self.promotion_status, 3, 3)

    #     # Move Date Reported so it appears before Type of Report in the grid
    #     # self.date_reported = NoScrollDateEdit(calendarPopup=True, displayFormat="dd MMMM yyyy")  # type: ignore[call-overload]
    #     self.date_reported = NoScrollDateEdit()
    #     self.date_reported.setCalendarPopup(True)
    #     self.date_reported.setDisplayFormat("dd MMMM yyyy")
    #     if self.report.date_reported is not None:
    #         y = self.report.date_reported.year
    #         m = self.report.date_reported.month
    #         d = self.report.date_reported.day
    #         self.date_reported.setDate(QDate(y, m, d))
    #     grid_layout.addWidget(QLabel("Date Reported"), 4, 0)
    #     grid_layout.addWidget(self.date_reported, 4, 1)

    #     group_box = QGroupBox("Occasion for Report")
    #     self.periodic = QCheckBox("Periodic")
    #     self.periodic.setChecked(self.report.periodic)
    #     self.periodic.checkStateChanged.connect(self.validate_occasion)
    #     self.det_indiv = QCheckBox("Detachment of Individual")
    #     self.det_indiv.setChecked(self.report.det_indiv)
    #     self.det_indiv.checkStateChanged.connect(self.validate_occasion)
    #     self.det_rs = QCheckBox("Detachment of Reporting Senior")
    #     self.det_rs.setChecked(self.report.det_rs)
    #     self.det_rs.checkStateChanged.connect(self.validate_occasion)
    #     self.special = QCheckBox("Special")
    #     self.special.setChecked(self.report.special)
    #     self.special.checkStateChanged.connect(self.validate_special)
    #     vbox = QHBoxLayout()
    #     vbox.addWidget(self.periodic)
    #     vbox.addWidget(self.det_indiv)
    #     vbox.addWidget(self.det_rs)
    #     vbox.addWidget(self.special)
    #     group_box.setLayout(vbox)
    #     grid_layout.addWidget(group_box, 4, 2, 1, 2)

    #     # self.period_start = NoScrollDateEdit(calendarPopup=True, displayFormat="dd MMMM yyyy")  # type: ignore[call-overload]
    #     self.period_start = NoScrollDateEdit()
    #     self.period_start.setCalendarPopup(True)
    #     self.period_start.setDisplayFormat("dd MMMM yyyy")
    #     if self.report.period_start:
    #         y = self.report.period_start.year
    #         m = self.report.period_start.month
    #         d = self.report.period_start.day
    #         self.period_start.setDate(QDate(y, m, d))
    #     grid_layout.addWidget(QLabel("Period Start"), 6, 0)
    #     grid_layout.addWidget(self.period_start, 6, 1)

    #     # self.period_end = NoScrollDateEdit(calendarPopup=True, displayFormat="dd MMMM yyyy")  # type: ignore[call-overload]
    #     self.period_end = NoScrollDateEdit()
    #     self.period_end.setCalendarPopup(True)
    #     self.period_end.setDisplayFormat("dd MMMM yyyy")
    #     if self.report.period_end:
    #         y = self.report.period_end.year
    #         m = self.report.period_end.month
    #         d = self.report.period_end.day
    #         self.period_end.setDate(QDate(y, m, d))
    #     grid_layout.addWidget(QLabel("Period End"), 6, 2)
    #     grid_layout.addWidget(self.period_end, 6, 3)

    #     self.not_observed = QCheckBox()
    #     self.not_observed.setChecked(self.report.not_observed)
    #     grid_layout.addWidget(QLabel("Not Observed Report"), 7, 0)
    #     grid_layout.addWidget(self.not_observed, 7, 1)

    #     group_box = QGroupBox("Type of Report")
    #     self.regular = QCheckBox("Regular")
    #     self.regular.setChecked(self.report.regular)

    #     self.concurrent = QCheckBox("Concurrent")
    #     self.concurrent.setChecked(self.report.concurrent)
    #     self.concurrent.checkStateChanged.connect(self.validate_concurrent)

    #     self.ops_cdr = QCheckBox("OpsCdr")
    #     self.ops_cdr.setChecked(self.report.ops_cdr)
    #     self.ops_cdr.checkStateChanged.connect(self.validate_ops_cdr)
    #     hbox = QHBoxLayout()
    #     hbox.addWidget(self.regular)
    #     hbox.addWidget(self.concurrent)
    #     hbox.addWidget(self.ops_cdr)
    #     group_box.setLayout(hbox)
    #     grid_layout.addWidget(group_box, 7, 2, 1, 2)

    #     self.physical_readiness = NoScrollComboBox()
    #     self.physical_readiness.addItem("")
    #     self.physical_readiness.addItems([member.value for member in PhysicalReadiness])
    #     self.physical_readiness.setCurrentIndex(self.get_idx_for_enum(self.report.physical_readiness))
    #     grid_layout.addWidget(QLabel("Physical Readiness"), 8, 0)
    #     grid_layout.addWidget(self.physical_readiness, 8, 1)

    #     self.billet_subcategory = NoScrollComboBox()
    #     self.billet_subcategory.addItem("")
    #     self.billet_subcategory.addItems([member.value for member in BilletSubcategory])
    #     self.billet_subcategory.setCurrentIndex(self.get_idx_for_enum(self.report.billet_subcategory))
    #     grid_layout.addWidget(QLabel("Billet Subcategory"), 8, 2)
    #     grid_layout.addWidget(self.billet_subcategory, 8, 3)

    #     self.senior_name = QLineEdit()
    #     self.senior_name.setFont(QFont("Courier"))
    #     self.senior_name.setText(self.report.senior_name)
    #     self.senior_name.setPlaceholderText("LAST, FI MI")
    #     grid_layout.addWidget(QLabel("Reporting Senior Name"), 9, 0)
    #     grid_layout.addWidget(self.senior_name, 9, 1)

    #     self.senior_grade = QLineEdit()
    #     self.senior_grade.setFont(QFont("Courier"))
    #     self.senior_grade.setText(self.report.senior_grade)
    #     grid_layout.addWidget(QLabel("Reporting Senior Grade"), 9, 2)
    #     grid_layout.addWidget(self.senior_grade, 9, 3)

    #     self.senior_desig = QLineEdit()
    #     self.senior_desig.setFont(QFont("Courier"))
    #     self.senior_desig.setText(self.report.senior_desig)
    #     grid_layout.addWidget(QLabel("Reporting Senior Designator"), 10, 0)
    #     grid_layout.addWidget(self.senior_desig, 10, 1)

    #     self.senior_title = QLineEdit()
    #     self.senior_title.setFont(QFont("Courier"))
    #     self.senior_title.setText(self.report.senior_title)
    #     grid_layout.addWidget(QLabel("Reporting Senior Title"), 10, 2)
    #     grid_layout.addWidget(self.senior_title, 10, 3)

    #     self.senior_uic = QLineEdit()
    #     self.senior_uic.setFont(QFont("Courier"))
    #     self.senior_uic.setText(self.report.senior_uic)
    #     grid_layout.addWidget(QLabel("Reporting Senior UIC"), 11, 0)
    #     grid_layout.addWidget(self.senior_uic, 11, 1)

    #     self.senior_ssn = QLineEdit()
    #     self.senior_ssn.setFont(QFont("Courier"))
    #     self.senior_ssn.setText(self.report.senior_ssn)
    #     self.senior_ssn.setInputMask("000-00-0000;_")
    #     grid_layout.addWidget(QLabel("Reporting Senior SSN"), 11, 2)
    #     grid_layout.addWidget(self.senior_ssn, 11, 3)

    #     self.job = QTextEdit(tabChangesFocus=True, lineWrapMode=QTextEdit.LineWrapMode.FixedColumnWidth)
    #     self.job.setFont(QFont("Courier"))
    #     self.job.setPlaceholderText("Maximum of 3 lines. Excess lines will be trimmed.")
    #     self.job.setWordWrapMode(QTextOption.WrapMode.WordWrap)
    #     self.job.setLineWrapColumnOrWidth(92)
    #     self.job.setText(self.report.job)
    #     line_height = self.job.fontMetrics().lineSpacing()
    #     self.job.setFixedHeight(int(line_height * 3.6))  # I don't know why, but 4 isn't quite tall enough.
    #     self.job.setFixedWidth(900)

    #     self.job_label = QLabel(
    #         f"Command Employment and\nCommand Achievements\n"
    #         f"(Line Count: {len(Fitrep.wrap_text(self.job.toPlainText(), 92).split('\n'))}/3)"
    #     )
    #     # num_lines = len(Fitrep.format_comments(self.comments.toPlainText()).split())
    #     self.job.textChanged.connect(
    #         lambda: self.job_label.setText(
    #             f"Command Employment and\nCommand Achievements\n"
    #             f"(Line Count: {len(Fitrep.wrap_text(self.job.toPlainText(), 92).split('\n'))}/3)"
    #         )
    #     )

    #     # grid_layout.addWidget(QLabel("Command Employment and\nCommand Achievements"), 12, 0)
    #     grid_layout.addWidget(self.job_label, 12, 0)
    #     grid_layout.addWidget(self.job, 12, 1, 1, 3)

    #     self.duties_abbreviation = QLineEdit()
    #     self.duties_abbreviation.setFont(QFont("Courier"))
    #     self.duties_abbreviation.setPlaceholderText("(14 characters max)")
    #     self.duties_abbreviation.setMaxLength(14)
    #     self.duties_abbreviation.setFixedWidth(180)
    #     self.duties_abbreviation.setText(self.report.duties_abbreviation)
    #     grid_layout.addWidget(QLabel("Primary Duty Abbreviation"), 13, 0)
    #     grid_layout.addWidget(self.duties_abbreviation, 13, 1)

    #     self.duties_description = QTextEdit(tabChangesFocus=True, lineWrapMode=QTextEdit.LineWrapMode.FixedColumnWidth)
    #     self.duties_description.setFont(QFont("Courier"))
    #     self.duties_description.setWordWrapMode(QTextOption.WrapMode.WordWrap)
    #     if self.duties_description == "":
    #         self.duties_description.setText(" " * DUTIES_DESC_SPACE_FOR_ABBREV)
    #     else:
    #         self.duties_description.setText(f"{' ' * DUTIES_DESC_SPACE_FOR_ABBREV}{self.report.duties_description}")
    #     self.duties_description.setLineWrapColumnOrWidth(91)
    #     line_height = self.duties_description.fontMetrics().lineSpacing()
    #     self.duties_description.setFixedHeight(
    #         int(line_height * 4.6)
    #     )  # I don't know why, but 4 isn't quite tall enough.
    #     self.duties_description.setFixedWidth(900)
    #     self.duties_description.setPlaceholderText("Maximum of 4 lines. Excess lines will be trimmed.")
    #     # self.duties_description.selectionChanged.connect(self.validate_duties_description)

    #     duties_desc_label = QLabel("Primary/Collateral/Watchstanding Duties")
    #     duties_desc_label.setToolTip(
    #         "Maximum of 4 lines, but first line must have 21 leading spaces to leave room for the duties abbreviation box."
    #     )
    #     grid_layout.addWidget(duties_desc_label, 14, 0)
    #     grid_layout.addWidget(self.duties_description, 14, 1, 1, 3)

    #     # self.date_counseled = NoScrollDateEdit(calendarPopup=True, displayFormat="dd MMMM yyyy")  # type: ignore[call-overload]
    #     self.date_counseled = NoScrollDateEdit()
    #     self.date_counseled.setCalendarPopup(True)
    #     self.date_counseled.setDisplayFormat("dd MMMM yyyy")
    #     if self.report.date_counseled:
    #         y = self.report.date_counseled.year
    #         m = self.report.date_counseled.month
    #         d = self.report.date_counseled.day
    #         self.date_counseled.setDate(QDate(y, m, d))
    #     grid_layout.addWidget(QLabel("Date Counseled"), 15, 0)
    #     grid_layout.addWidget(self.date_counseled, 15, 1)

    #     self.counselor = QLineEdit()
    #     self.counselor.setFont(QFont("Courier"))
    #     self.counselor.setText(self.report.counselor)
    #     grid_layout.addWidget(QLabel("Counselor"), 15, 2)
    #     grid_layout.addWidget(self.counselor, 15, 3)

    #     # h = self.counselor.sizeHint().height()
    #     # w = self.counselor.sizeHint().width()
    #     # grid_layout.addItem(QSpacerItem(0, h), 13, 0)

    #     self.pro_expertise = NoScrollComboBox()
    #     self.pro_expertise.addItems([p for p in self.perf_traits.keys()])
    #     if self.report.pro_expertise is not None:
    #         self.pro_expertise.setCurrentIndex(self.report.pro_expertise + 1)
    #     grid_layout.addWidget(QLabel("Professional Expertise"), 16, 0)
    #     grid_layout.addWidget(self.pro_expertise, 16, 1)

    #     self.cmd_climate = NoScrollComboBox()
    #     self.cmd_climate.addItems([p for p in self.perf_traits.keys()])
    #     if self.report.cmd_climate is not None:
    #         self.cmd_climate.setCurrentIndex(self.report.cmd_climate + 1)
    #     grid_layout.addWidget(QLabel("Command or Organizational Climate"), 16, 2)
    #     grid_layout.addWidget(self.cmd_climate, 16, 3)

    #     self.bearing_and_character = NoScrollComboBox()
    #     self.bearing_and_character.addItems([p for p in self.perf_traits.keys()])
    #     if self.report.bearing_and_character is not None:
    #         self.bearing_and_character.setCurrentIndex(self.report.bearing_and_character + 1)
    #     grid_layout.addWidget(QLabel("Military Bearing/Character"), 17, 0)
    #     grid_layout.addWidget(self.bearing_and_character, 17, 1)

    #     self.teamwork = NoScrollComboBox()
    #     self.teamwork.addItems([p for p in self.perf_traits.keys()])
    #     if self.report.teamwork is not None:
    #         self.teamwork.setCurrentIndex(self.report.teamwork + 1)
    #     grid_layout.addWidget(QLabel("Teamwork"), 17, 2)
    #     grid_layout.addWidget(self.teamwork, 17, 3)

    #     self.accomp_and_initiative = NoScrollComboBox()
    #     self.accomp_and_initiative.addItems([p for p in self.perf_traits.keys()])
    #     if self.report.accomp_and_initiative is not None:
    #         self.accomp_and_initiative.setCurrentIndex(self.report.accomp_and_initiative + 1)
    #     grid_layout.addWidget(QLabel("Mission Accomplishment and Initiative"), 18, 0)
    #     grid_layout.addWidget(self.accomp_and_initiative, 18, 1)

    #     self.leadership = NoScrollComboBox()
    #     self.leadership.addItems([p for p in self.perf_traits.keys()])
    #     if self.report.leadership is not None:
    #         self.leadership.setCurrentIndex(self.report.leadership + 1)
    #     grid_layout.addWidget(QLabel("Leadership"), 18, 2)
    #     grid_layout.addWidget(self.leadership, 18, 3)

    #     self.tactical_performance = NoScrollComboBox()
    #     self.tactical_performance.addItems([p for p in self.perf_traits.keys()])
    #     if self.report.tactical_performance is not None:
    #         self.tactical_performance.setCurrentIndex(self.report.tactical_performance + 1)
    #     grid_layout.addWidget(QLabel("Tactical Performance"), 19, 0)
    #     grid_layout.addWidget(self.tactical_performance, 19, 1)

    #     self.career_rec_1 = QTextEdit(tabChangesFocus=True, lineWrapMode=QTextEdit.LineWrapMode.FixedColumnWidth)
    #     self.career_rec_1.setToolTip("Maximum of 20 characters and two lines.")
    #     self.career_rec_1.setWordWrapMode(QTextOption.WrapMode.WrapAnywhere)
    #     self.career_rec_1.setText(self.report.career_rec_1)
    #     self.career_rec_1.setLineWrapColumnOrWidth(13)
    #     self.career_rec_1.setFont(QFont("Courier"))
    #     line_spacing = self.career_rec_1.fontMetrics().lineSpacing()
    #     self.career_rec_1.setFixedHeight(int(line_spacing * 2.6))
    #     # self.career_rec_1.setFixedWidth(900)
    #     self.career_rec_1.textChanged.connect(self.validate_career_rec1)
    #     grid_layout.addWidget(QLabel("Career Recommendation 1"), 20, 0)
    #     grid_layout.addWidget(self.career_rec_1, 20, 1)

    #     self.career_rec_2 = QTextEdit(tabChangesFocus=True, lineWrapMode=QTextEdit.LineWrapMode.FixedColumnWidth)
    #     self.career_rec_2.setToolTip("Maximum of 20 characters and two lines.")
    #     self.career_rec_2.setWordWrapMode(QTextOption.WrapMode.WordWrap)
    #     self.career_rec_2.setText(self.report.career_rec_2)
    #     self.career_rec_2.setLineWrapColumnOrWidth(13)
    #     self.career_rec_2.setFont(QFont("Courier"))
    #     line_height = self.career_rec_2.fontMetrics().lineSpacing()
    #     self.career_rec_2.setFixedHeight(int(line_height * 2.6))
    #     # self.career_rec_2.setFixedWidth(900)
    #     grid_layout.addWidget(QLabel("Career Recommendation 2"), 20, 2)
    #     grid_layout.addWidget(self.career_rec_2, 20, 3)

    #     self.comments = QTextEdit(tabChangesFocus=True, lineWrapMode=QTextEdit.LineWrapMode.FixedColumnWidth)
    #     self.comments.setText(self.report.comments)
    #     self.comments.setPlaceholderText("Maximum of 18 lines. Excess lines will be trimmed.")
    #     self.comments.setWordWrapMode(QTextOption.WrapMode.WordWrap)
    #     self.comments.setLineWrapColumnOrWidth(92)
    #     self.comments.setFont(QFont("Courier"))
    #     line_height = self.comments.fontMetrics().lineSpacing()
    #     self.comments.setFixedHeight(int(line_height * 18))
    #     self.comments.setFixedWidth(900)
    #     # self.comments.textChanged.connect(self.validate_comments)

    #     self.comments_label = QLabel(
    #         f"Comments\n\n(Line Count: {len(Fitrep.wrap_text(self.comments.toPlainText(), 92).split('\n'))}/18)"
    #     )
    #     # num_lines = len(Fitrep.format_comments(self.comments.toPlainText()).split())
    #     self.comments.textChanged.connect(
    #         lambda: self.comments_label.setText(
    #             f"Comments\n\n(Line Count: {len(Fitrep.wrap_text(self.comments.toPlainText(), 92).split('\n'))}/18)"
    #         )
    #     )

    #     grid_layout.addWidget(self.comments_label, 22, 0)
    #     grid_layout.addWidget(self.comments, 22, 1, 1, 3)

    #     self.indiv_promo_rec = NoScrollComboBox()
    #     self.indiv_promo_rec.addItems([k for k in self.promotion_recs.keys()])
    #     if self.report.indiv_promo_rec is not None:
    #         self.indiv_promo_rec.setCurrentIndex(self.report.indiv_promo_rec + 1)
    #     grid_layout.addWidget(QLabel("Promotion Reccomendation"), 23, 0)
    #     grid_layout.addWidget(self.indiv_promo_rec, 23, 1)

    #     self.senior_address = QTextEdit()
    #     self.senior_address.setText(self.report.senior_address)
    #     self.senior_address.setLineWrapMode(QTextEdit.LineWrapMode.FixedColumnWidth)
    #     self.senior_address.setLineWrapColumnOrWidth(27)
    #     self.senior_address.setWordWrapMode(QTextOption.WrapMode.WordWrap)
    #     self.senior_address.setFont(QFont("Courier"))
    #     line_height = QLineEdit().fontMetrics().lineSpacing()
    #     self.senior_address.setFixedHeight(line_height * 5)
    #     self.senior_address.setFixedWidth(500)
    #     grid_layout.addWidget(QLabel("Reporting Senior Address"), 24, 0)
    #     grid_layout.addWidget(self.senior_address, 24, 1, 1, 3)

    #     # layout = QVBoxLayout()
    #     # grid_layout.addItem(QSpacerItem(0, 0))
    #     # grid_layout.setRowStretch(15, 1)

    #     # scroll_area.setWidget(form_widget)
    #     scroll_area.setWidget(container_widget)

    #     # Set the layout for the secondary window
    #     main_layout = QVBoxLayout()
    #     main_layout.addWidget(scroll_area)

    #     # Set the layout for the secondary window
    #     self.setLayout(main_layout)

    #     # Build the form-specific menu on the provided main window
    #     # self.build_menu(main)

    def validate_report(self):
        """Perform validation on all fields in the form."""
        # TODO: save form before validating
        try:
            Fitrep.model_validate(self.report.model_dump())
        except ValidationError as err:
            errors = json.loads(err.json())
            # show a list of all validation errors
            err_msgs = ""
            for error in errors:
                python_field_name = error["loc"][0]
                err_msgs += f"{Fitrep.model_fields[python_field_name].title}: {error['msg']}\n"
            test = QMessageBox()
            test.setWindowModality(Qt.WindowModality.NonModal)
            test.warning(self, "Validation", err_msgs)
            return
        QMessageBox.information(self, "Validation", "No validation errors found. Report is valid.")

    @staticmethod
    def get_idx_for_enum(member: Enum | None) -> int:
        """
        Return 1-based index of the enum member within its enum class, or 0 if None/not found.

        Useful for setting QComboBinox current index based on enum member.
        """
        if member is None:
            return 0
        return list(type(member).__members__).index(member.name) + 1

    @Slot()
    def validate_special(self, check_state: Qt.CheckState):
        if check_state == Qt.CheckState.Checked:
            self.det_indiv.setChecked(False)
            self.det_rs.setChecked(False)
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
            self.ops_cdr.setChecked(False)

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
        if len(self.station.text()) > 18:
            QMessageBox.information(
                self,
                "Ship/Station Validation",
                "Maximum of 18 characters allowed.",
                QMessageBox.StandardButton.Ok,
            )
            self.station.setText("")

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

        try:
            Fitrep.model_validate(self.report)
            # validation_failed = False
            # err_msgs = ""
        except ValidationError as err:
            # validation_failed = True
            errors = json.loads(err.json())
            err_msgs = ""
            for error in errors:
                python_field_name = error["loc"][0]
                err_msgs += f"{Fitrep.model_fields[python_field_name].title}: {error['msg']}\n"

            # if validation_failed:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Validation Error")
            msg_box.setText(
                f"Validation errors found. The report is invalid and may print incorrectly. Fix the following errors to correct the report:\n\n{err_msgs}"
            )
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg_box.button(QMessageBox.StandardButton.Yes).setText("Ignore and Print")
            msg_box.button(QMessageBox.StandardButton.No).setText("Cancel")
            result = msg_box.exec()
            if result != QMessageBox.StandardButton.Yes:
                return

        filename, selected_filter = QFileDialog.getSaveFileName(self, "Export FITREP PDF", "fitrep.pdf")
        if filename:
            self.report.create_pdf(Path(filename))

    def export_json(self):
        self.save_form()
        filename, selected_filter = QFileDialog.getSaveFileName(self, "Export FITREP JSON", "fitrep.json")
        if filename:
            json_str = self.report.model_dump_json(indent=4)
            with open(filename, "w") as f:
                f.write(json_str)

    def export_toml(self):
        self.save_form()
        filename, selected_filter = QFileDialog.getSaveFileName(self, "Export FITREP TOML", "fitrep.toml")
        if filename:
            toml_str = self.report.model_dump_toml()
            with open(filename, "w") as f:
                f.write(toml_str)

    def submit(self):
        self.save_form()
        self.on_accept(self.report)

    def save_form(self):
        """
        Create a Fitrep class from the data input in the GUI Form.
        """
        super().save_form()
        self.report.det_rs = self.det_rs.isChecked()
        self.report.ops_cdr = self.ops_cdr.isChecked()
