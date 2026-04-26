from __future__ import annotations

import json
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Generic, TypeVar

from pydantic import ValidationError
from PySide6.QtCore import QDate, QRegularExpression
from PySide6.QtGui import QFont, QRegularExpressionValidator, QTextOption
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
from navfitx.models import BilletSubcategory, PromotionRecommendation, PromotionStatus, Report, SummaryGroup

TReport = TypeVar("TReport", bound=Report)


class NoScrollDateEdit(QDateEdit):
    """QDateEdit that ignores wheel events to prevent accidental changes."""

    def wheelEvent(self, event):  # noqa: N802
        event.ignore()


class NoScrollComboBox(QComboBox):
    """QComboBox that ignores wheel events to prevent accidental changes."""

    def wheelEvent(self, event):  # noqa: N802
        event.ignore()


class BaseReportForm(QWidget, Generic[TReport]):
    """Shared Qt scaffolding for report data-entry forms."""

    window_title = "Report Data Entry"
    pdf_default_name = "report.pdf"
    trait_options = {
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

    def __init__(self, main: QMainWindow, on_accept, on_reject, report) -> None:
        super().__init__()
        self.main = main
        self.on_accept: Callable = on_accept
        self.on_reject: Callable = on_reject
        self.report: TReport = report

        self.setWindowTitle(self.window_title)

        self.form = QGridLayout()
        self.form.setColumnStretch(0, 0)
        self.form.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)

        self.container = QWidget()
        self.container.setLayout(self.form)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_area.setWidget(self.container)

        self.button_box = self.build_button_box()

        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.button_box)

        self.build_fields()
        self.build_menu()

    @property
    def report_type(self) -> type[TReport]:
        return type(self.report)

    # @abstractmethod
    def build_fields(self) -> None:
        """Create widgets and connect per-form signals."""
        self.name = self.add_line_edit(
            row=0,
            col=0,
            label="Name",
            text=self.report.name,
            placeholder="LAST, FIRST MI",
        )
        self.rate = self.add_line_edit(
            row=0,
            col=2,
            label="Rank",
            text=self.report.rate,
            validator=QRegularExpressionValidator(QRegularExpression(r"[A-Za-z0-9]{0,5}$")),
        )
        self.desig = self.add_line_edit(
            row=1,
            col=0,
            label="Designator",
            text=self.report.desig,
        )
        self.ssn = self.add_line_edit(
            row=1,
            col=2,
            label="SSN",
            input_mask="000-00-0000;_",
            text=self.report.ssn,
        )
        self.group = self.add_enum_combo(
            row=2,
            col=0,
            label="Group",
            enum_cls=SummaryGroup,
            value=self.report.group,
        )
        self.uic = self.add_line_edit(
            row=2,
            col=2,
            label="UIC",
            text=self.report.uic,
        )
        self.station = self.add_line_edit(
            row=3,
            col=0,
            label="Ship/Station",
            text=self.report.station,
        )
        self.promotion_status = self.add_enum_combo(
            row=3,
            col=2,
            label="Promotion Status",
            enum_cls=PromotionStatus,
            value=self.report.promotion_status,
        )
        self.date_reported = self.add_date_edit(
            row=4,
            col=0,
            label="Date Reported",
            value=self.report.date_reported,
        )

        self.occasion_box = QGroupBox("Occasion for Report")
        hbox_layout = QHBoxLayout()
        self.occasion_box.setLayout(hbox_layout)
        self.form.addWidget(self.occasion_box, 4, 2, 1, 2)

        self.periodic = QCheckBox("Periodic")
        self.periodic.setChecked(self.report.periodic)
        hbox_layout.addWidget(self.periodic)
        self.det_indiv = QCheckBox("Detachment of Individual")
        self.det_indiv.setChecked(self.report.det_indiv)
        hbox_layout.addWidget(self.det_indiv)
        self.special = QCheckBox("Special")
        self.special.setChecked(self.report.special)
        hbox_layout.addWidget(self.special)

        self.period_start = self.add_date_edit(
            row=5,
            col=0,
            label="Period Start",
            value=self.report.period_start,
        )
        self.period_end = self.add_date_edit(
            row=5,
            col=2,
            label="Period End",
            value=self.report.period_end,
        )
        self.not_observed = self.add_checkbox(
            row=6,
            col=0,
            label="Not Observed",
            checked=self.report.not_observed,
        )

        self.type_box = QGroupBox("Type of Report")
        hbox_layout = QHBoxLayout()
        self.type_box.setLayout(hbox_layout)
        self.form.addWidget(self.type_box, 6, 2, 1, 2)

        self.regular = QCheckBox("Regular")
        self.regular.setChecked(self.report.regular)
        hbox_layout.addWidget(self.regular)
        self.concurrent = QCheckBox("Concurrent")
        self.concurrent.setChecked(self.report.concurrent)
        hbox_layout.addWidget(self.concurrent)

        self.physical_readiness = self.add_line_edit(
            row=7,
            col=0,
            label="Physical Readiness",
            text=self.report.physical_readiness,
        )
        self.billet_subcategory = self.add_enum_combo(
            row=7,
            col=2,
            label="Billet Subcategory",
            enum_cls=BilletSubcategory,
            value=self.report.billet_subcategory,
        )
        self.senior_name = self.add_line_edit(
            row=8,
            col=0,
            label="Reporting Senior Name",
            text=self.report.senior_name,
            placeholder="LAST, FI MI",
        )
        self.senior_grade = self.add_line_edit(
            row=8,
            col=2,
            label="Reporting Senior Grade",
            text=self.report.senior_grade,
            validator=QRegularExpressionValidator(QRegularExpression(r"[A-Za-z0-9]{0,5}$")),
        )
        self.senior_desig = self.add_line_edit(
            row=9,
            col=0,
            label="Reporting Senior Designator",
            text=self.report.senior_desig,
        )
        self.senior_title = self.add_line_edit(
            row=9,
            col=2,
            label="Reporting Senior Title",
            text=self.report.senior_title,
        )
        self.senior_uic = self.add_line_edit(
            row=10,
            col=0,
            label="Reporting Senior UIC",
            text=self.report.senior_uic,
        )
        self.senior_ssn = self.add_line_edit(
            row=10,
            col=2,
            label="Reporting Senior SSN",
            input_mask="000-00-0000;_",
            text=self.report.senior_ssn,
        )

        self.job = QTextEdit(tabChangesFocus=True, lineWrapMode=QTextEdit.LineWrapMode.FixedColumnWidth)
        self.job.setFont(QFont("Courier"))
        self.job.setPlaceholderText("Maximum of 3 lines. Excess lines will be trimmed.")
        self.job.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.job.setLineWrapColumnOrWidth(92)
        self.job.setText(self.report.job)
        line_height = self.job.fontMetrics().lineSpacing()
        self.job.setFixedHeight(int(line_height * 3.6))  # I don't know why, but 4 isn't quite tall enough.
        # self.job.setFixedWidth(900)
        self.job_label = QLabel(
            f"Command Employment and\nCommand Achievements\n"
            f"(Line Count: {len(self.report_type.wrap_text(self.job.toPlainText(), 92).split('\n'))}/3)"
        )
        self.job.textChanged.connect(
            lambda: self.job_label.setText(
                f"Command Employment and\nCommand Achievements\n"
                f"(Line Count: {len(self.report_type.wrap_text(self.job.toPlainText(), 92).split('\n'))}/3)"
            )
        )
        self.form.addWidget(self.job_label, 11, 0)
        self.form.addWidget(self.job, 11, 1, 1, 3)

        self.duties_abbreviation = QLineEdit(
            text=self.report.duties_abbreviation,
            maxLength=14,  # constraint from NAVFIT98 User Manual
        )
        self.duties_abbreviation.setFont(QFont("Courier"))
        self.duties_abbreviation.setFixedWidth(180)
        self.add_label("Primary Duty Abbreviation", 12, 0)
        self.form.addWidget(self.duties_abbreviation, 12, 1)

        self.duties_description = QTextEdit(tabChangesFocus=True, lineWrapMode=QTextEdit.LineWrapMode.FixedColumnWidth)
        self.duties_description.setFont(QFont("Courier"))
        self.duties_description.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        if self.duties_description == "":
            self.duties_description.setText(" " * DUTIES_DESC_SPACE_FOR_ABBREV)
        else:
            self.duties_description.setText(f"{' ' * DUTIES_DESC_SPACE_FOR_ABBREV}{self.report.duties_description}")
        self.duties_description.setLineWrapColumnOrWidth(91)
        line_height = self.duties_description.fontMetrics().lineSpacing()
        self.duties_description.setFixedHeight(
            int(line_height * 4.6)
        )  # I don't know why, but 4 isn't quite tall enough.
        self.duties_description.setFixedWidth(900)
        self.duties_description.setPlaceholderText("Maximum of 4 lines. Excess lines will be trimmed.")
        # self.duties_description.selectionChanged.connect(self.validate_duties_description)

        duties_desc_label = QLabel("Primary/Collateral/Watchstanding\nDuties")
        duties_desc_label.setToolTip(
            "Maximum of 4 lines, but first line must have 21 leading spaces to leave room for the duties abbreviation box."
        )
        self.form.addWidget(duties_desc_label, 14, 0)
        self.form.addWidget(self.duties_description, 14, 1, 1, 3)

        self.date_counseled = self.add_date_edit(
            row=15,
            col=0,
            label="Date Counseled",
            value=self.report.date_counseled,
        )
        self.counselor = self.add_line_edit(
            row=15,
            col=2,
            label="Counselor Name",
            text=self.report.counselor,
        )

        self.trait1 = self.create_trait_combo(self.report.trait1)
        self.form.addWidget(self.trait1, 16, 1)
        self.trait2 = self.create_trait_combo(self.report.trait2)
        self.form.addWidget(self.trait2, 16, 3)
        self.trait3 = self.create_trait_combo(self.report.trait3)
        self.form.addWidget(self.trait3, 17, 1)
        self.trait4 = self.create_trait_combo(self.report.trait4)
        self.form.addWidget(self.trait4, 17, 3)
        self.trait5 = self.create_trait_combo(self.report.trait5)
        self.form.addWidget(self.trait5, 18, 1)
        self.trait6 = self.create_trait_combo(self.report.trait6)
        self.form.addWidget(self.trait6, 18, 3)
        self.trait7 = self.create_trait_combo(self.report.trait7)
        self.form.addWidget(self.trait7, 19, 1)

        self.career_rec_1 = QTextEdit(tabChangesFocus=True, lineWrapMode=QTextEdit.LineWrapMode.FixedColumnWidth)
        self.career_rec_1.setPlaceholderText("Maximum of 20 characters and two lines.")
        self.career_rec_1.setWordWrapMode(QTextOption.WrapMode.WrapAnywhere)
        self.career_rec_1.setText(self.report.career_rec_1)
        self.career_rec_1.setLineWrapColumnOrWidth(13)
        self.career_rec_1.setFont(QFont("Courier"))
        line_spacing = self.career_rec_1.fontMetrics().lineSpacing()
        self.career_rec_1.setFixedHeight(int(line_spacing * 2.6))
        # self.career_rec_1.setFixedWidth(900)
        # self.career_rec_1.textChanged.connect(self.validate_career_rec1)
        self.form.addWidget(QLabel("Career Recommendation 1"), 20, 0)
        self.form.addWidget(self.career_rec_1, 20, 1)

        self.career_rec_2 = QTextEdit(tabChangesFocus=True, lineWrapMode=QTextEdit.LineWrapMode.FixedColumnWidth)
        self.career_rec_1.setPlaceholderText("Maximum of 20 characters and two lines.")
        self.career_rec_2.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.career_rec_2.setText(self.report.career_rec_2)
        self.career_rec_2.setLineWrapColumnOrWidth(13)
        self.career_rec_2.setFont(QFont("Courier"))
        line_height = self.career_rec_2.fontMetrics().lineSpacing()
        self.career_rec_2.setFixedHeight(int(line_height * 2.6))
        self.form.addWidget(QLabel("Career Recommendation 2"), 20, 2)
        self.form.addWidget(self.career_rec_2, 20, 3)

        self.comments = QTextEdit(tabChangesFocus=True, lineWrapMode=QTextEdit.LineWrapMode.FixedColumnWidth)
        self.comments.setText(self.report.comments)
        self.comments.setPlaceholderText("Maximum of 18 lines. Excess lines will be trimmed.")
        self.comments.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.comments.setLineWrapColumnOrWidth(92)
        self.comments.setFont(QFont("Courier"))
        line_height = self.comments.fontMetrics().lineSpacing()
        self.comments.setFixedHeight(int(line_height * 18))
        self.comments.setFixedWidth(900)
        # self.comments.textChanged.connect(self.validate_comments)
        self.comments_label = QLabel(
            f"Comments\n\n(Line Count: {len(self.report_type.wrap_text(self.comments.toPlainText(), 92).split('\n'))}/18)"
        )
        # num_lines = len(Fitrep.format_comments(self.comments.toPlainText()).split())
        self.comments.textChanged.connect(
            lambda: self.comments_label.setText(
                f"Comments\n\n(Line Count: {len(self.report_type.wrap_text(self.comments.toPlainText(), 92).split('\n'))}/18)"
            )
        )

        self.form.addWidget(self.comments_label, 22, 0)
        self.form.addWidget(self.comments, 22, 1, 1, 3)

        combo = NoScrollComboBox()
        combo.addItems([p for p in BaseReportForm.promotion_recs.keys()])
        if p := self.report.indiv_promo_rec is not None:
            combo.setCurrentIndex(p + 1)
        self.indiv_promo_rec = combo
        self.form.addWidget(QLabel("Promotion Recommendation"), 23, 0)
        self.form.addWidget(self.indiv_promo_rec, 23, 1)

        self.senior_address = QTextEdit()
        self.senior_address.setText(self.report.senior_address)
        self.senior_address.setLineWrapMode(QTextEdit.LineWrapMode.FixedColumnWidth)
        self.senior_address.setLineWrapColumnOrWidth(27)
        self.senior_address.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.senior_address.setFont(QFont("Courier"))
        line_height = QLineEdit().fontMetrics().lineSpacing()
        self.senior_address.setFixedHeight(line_height * 5)
        self.senior_address.setFixedWidth(500)
        self.form.addWidget(QLabel("Reporting Senior Address"), 24, 0)
        self.form.addWidget(self.senior_address, 24, 1, 1, 3)

    def create_trait_combo(self, trait: int | None) -> NoScrollComboBox:
        combo = NoScrollComboBox()
        combo.addItems([p for p in BaseReportForm.trait_options.keys()])
        if trait is not None:
            combo.setCurrentIndex(trait + 1)
        return combo

    def save_to_report(self) -> None:
        """Copy widget state back into self.report."""
        self.save_form()

    def build_button_box(self) -> QDialogButtonBox:
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        ok_btn = button_box.button(QDialogButtonBox.StandardButton.Ok)
        if ok_btn is not None:
            ok_btn.setText("Save")
        button_box.accepted.connect(self.submit)
        button_box.rejected.connect(self.on_reject)
        return button_box

    def build_menu(self) -> None:
        menu_bar = self.main.menuBar()
        menu_bar.clear()

        file_menu = menu_bar.addMenu("File")
        export_action = file_menu.addAction("Export as PDF")
        export_action.triggered.connect(self.export_pdf)

        close_action = file_menu.addAction("Close")
        close_action.triggered.connect(self.on_reject)

        tools = menu_bar.addMenu("Tools")
        validate_action = tools.addAction("Validate Report")
        validate_action.triggered.connect(self.validate_report)

    def submit(self) -> None:
        self.save_to_report()
        self.on_accept(self.report)

    def validate_report(self) -> None:
        self.save_to_report()
        try:
            self.report_type.model_validate(self.report.model_dump())
        except ValidationError as err:
            self.show_validation_errors(err)
            return
        QMessageBox.information(self, "Validation", "No validation errors found. Report is valid.")

    def export_pdf(self) -> None:
        self.save_to_report()
        if not self.confirm_invalid_print():
            return

        filename, _ = QFileDialog.getSaveFileName(self, "Export PDF", self.pdf_default_name)
        if filename:
            self.report.create_pdf(Path(filename))

    def show_validation_errors(self, err: ValidationError) -> None:
        errors = json.loads(err.json())
        lines = []
        for error in errors:
            field_name = error["loc"][0]
            title = self.field_title(field_name)
            lines.append(f"{title}: {error['msg']}")
        QMessageBox.warning(self, "Validation", "\n".join(lines))

    def confirm_invalid_print(self) -> bool:
        try:
            self.report_type.model_validate(self.report)
            return True
        except ValidationError as err:
            errors = json.loads(err.json())
            lines = []
            for error in errors:
                field_name = error["loc"][0]
                title = self.field_title(field_name)
                lines.append(f"{title}: {error['msg']}")

            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Validation Error")
            msg_box.setText(
                "Validation errors found. The report is invalid and may print incorrectly. "
                "Fix the following errors to correct the report:\n\n" + "\n".join(lines)
            )
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            yes_btn = msg_box.button(QMessageBox.StandardButton.Yes)
            no_btn = msg_box.button(QMessageBox.StandardButton.No)
            if yes_btn is not None:
                yes_btn.setText("Ignore and Print")
            if no_btn is not None:
                no_btn.setText("Cancel")
            return msg_box.exec() == QMessageBox.StandardButton.Yes

    def field_title(self, field_name: str) -> str:
        field = self.report_type.model_fields.get(field_name)
        if field is None:
            return field_name
        return field.title or field_name

    def add_label(self, text: str, row: int, col: int = 0) -> QLabel:
        label = QLabel(text)
        self.form.addWidget(label, row, col)
        return label

    def add_line_edit(
        self,
        row: int,
        col: int,
        label: str,
        *,
        text: str = "",
        placeholder: str = "",
        font: QFont | None = QFont("Courier"),
        input_mask: str | None = None,
        validator=None,
        max_length: int | None = None,
    ) -> QLineEdit:
        widget = QLineEdit()
        widget.setText(text)
        if font:
            widget.setFont(font)
        if placeholder:
            widget.setPlaceholderText(placeholder)
        if input_mask is not None:
            widget.setInputMask(input_mask)
        if validator is not None:
            widget.setValidator(validator)
        if max_length is not None:
            widget.setMaxLength(max_length)
        self.add_label(label, row, col)
        self.form.addWidget(widget, row, col + 1)
        return widget

    def add_date_edit(self, row: int, label: str, col: int, value=None) -> NoScrollDateEdit:
        widget = NoScrollDateEdit()
        widget.setCalendarPopup(True)
        widget.setDisplayFormat("dd MMMM yyyy")
        if value is not None:
            widget.setDate(QDate(value.year, value.month, value.day))
        self.add_label(label, row, col)
        self.form.addWidget(widget, row, col + 1)
        return widget

    def add_enum_combo(
        self,
        row: int,
        col: int,
        label: str,
        enum_cls: type[Enum],
        *,
        value: Enum | None = None,
        allow_blank: bool = True,
    ) -> NoScrollComboBox:
        widget = NoScrollComboBox()
        if allow_blank:
            widget.addItem("", None)
        for member in enum_cls:
            widget.addItem(member.value, member)
        if value is not None:
            idx = widget.findData(value)
            if idx >= 0:
                widget.setCurrentIndex(idx)
        self.add_label(label, row, col)
        self.form.addWidget(widget, row, col + 1)
        return widget

    def add_value_combo(
        self,
        row: int,
        col: int,
        label: str,
        values: dict[str, Any],
        *,
        value: Any = None,
    ) -> NoScrollComboBox:
        widget = NoScrollComboBox()
        for text, data in values.items():
            widget.addItem(text, data)
        idx = widget.findData(value)
        if idx >= 0:
            widget.setCurrentIndex(idx)
        self.add_label(label, row, col)
        self.form.addWidget(widget, row, col + 1)
        return widget

    def add_text_edit(
        self,
        row: int,
        label: str,
        col: int,
        *,
        text: str = "",
        placeholder: str = "",
        width: int | None = None,
        height: int | None = None,
        tab_changes_focus: bool = False,
        line_wrap_column: int | None = None,
        word_wrap_mode=None,
    ) -> QTextEdit:
        widget = QTextEdit()
        widget.setText(text)
        widget.setTabChangesFocus(tab_changes_focus)
        widget.setFont(QFont("Courier"))
        if placeholder:
            widget.setPlaceholderText(placeholder)
        if line_wrap_column is not None:
            widget.setLineWrapMode(QTextEdit.LineWrapMode.FixedColumnWidth)
            widget.setLineWrapColumnOrWidth(line_wrap_column)
        if word_wrap_mode is not None:
            widget.setWordWrapMode(word_wrap_mode)
        if width is not None:
            widget.setFixedWidth(width)
        if height is not None:
            widget.setFixedHeight(height)
        self.add_label(label, row, col)
        self.form.addWidget(widget, row, col + 1)
        return widget

    def add_checkbox(self, row: int, label: str, col: int, *, checked: bool = False) -> QCheckBox:
        widget = QCheckBox()
        widget.setChecked(checked)
        self.add_label(label, row, col)
        self.form.addWidget(widget, row, col + 1)
        return widget

    def save_form(self):
        self.report.name = self.name.text()
        self.report.rate = self.rate.text()
        self.report.desig = self.desig.text()
        self.report.ssn = self.ssn.text()
        group_text = self.group.currentText()
        self.report.group = None if group_text == "" else SummaryGroup(group_text)
        self.report.uic = self.uic.text()
        self.report.station = self.station.text()
        self.report.promotion_status = (
            None if self.promotion_status.currentText() == "" else PromotionStatus(self.promotion_status.currentText())
        )
        self.report.date_reported = self.date_reported.date().toPython()  # ty: ignore[invalid-assignment]
        self.report.periodic = self.periodic.isChecked()
        self.report.det_indiv = self.det_indiv.isChecked()
        self.report.special = self.special.isChecked()
        self.report.period_start = self.period_start.date().toPython()  # ty: ignore[invalid-assignment]
        self.report.period_end = self.period_end.date().toPython()  # ty: ignore[invalid-assignment]
        self.report.not_observed = self.not_observed.isChecked()
        self.report.regular = self.regular.isChecked()
        self.report.concurrent = self.concurrent.isChecked()
        self.report.physical_readiness = self.physical_readiness.text()
        if self.billet_subcategory.currentText() == "":
            self.report.billet_subcategory = None
        else:
            self.report.billet_subcategory = BilletSubcategory(self.billet_subcategory.currentText())
        self.report.senior_name = self.senior_name.text()
        self.report.senior_grade = self.senior_grade.text()
        self.report.senior_desig = self.senior_desig.text()
        self.report.senior_title = self.senior_title.text()
        self.report.senior_uic = self.senior_uic.text()
        self.report.senior_ssn = self.senior_ssn.text()
        self.report.duties_abbreviation = self.duties_abbreviation.text()
        self.report.duties_description = self.duties_description.toPlainText().strip()
        self.report.job = self.job.toPlainText()
        self.report.date_counseled = self.date_counseled.date().toPython()  # ty: ignore[invalid-assignment]
        self.report.counselor = self.counselor.text()
        self.report.trait1 = self.trait_options[self.trait1.currentText()]
        self.report.trait2 = self.trait_options[self.trait2.currentText()]
        self.report.trait3 = self.trait_options[self.trait3.currentText()]
        self.report.trait4 = self.trait_options[self.trait4.currentText()]
        self.report.trait5 = self.trait_options[self.trait5.currentText()]
        self.report.trait6 = self.trait_options[self.trait6.currentText()]
        self.report.trait7 = self.trait_options[self.trait7.currentText()]
        self.report.career_rec_1 = self.report_type.validate_career_rec(self.career_rec_1.toPlainText())
        self.report.career_rec_2 = self.career_rec_2.toPlainText()
        self.report.comments = self.report_type.validate_comments(self.comments.toPlainText())
        self.report.indiv_promo_rec = self.promotion_recs[self.indiv_promo_rec.currentText()]
        self.report.senior_address = self.senior_address.toPlainText()
