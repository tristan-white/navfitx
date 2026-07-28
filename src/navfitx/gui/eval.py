import json
from typing import Callable

from pydantic import ValidationError
from PySide6.QtCore import Slot
from PySide6.QtGui import QFont, QTextOption
from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QTextEdit,
)

from navfitx.models import Eval, RetentionRecommendation

from .report import BaseReportForm


class EvalForm(BaseReportForm[Eval]):
    retention_recs = {
        "": None,
        "Recommended": RetentionRecommendation.RECOMMENDED.value,
        "Not Recommended": RetentionRecommendation.NOT_RECOMMENDED.value,
    }

    def build_fields(self):
        super().build_fields()
        # TODO: move field definitions from __init__ to here

    def __init__(
        self,
        main: QMainWindow,
        on_accept: Callable[[Eval], None],
        on_reject: Callable[[], None],
        report: Eval,
    ):
        super().__init__(main=main, on_accept=on_accept, on_reject=on_reject, report=report)

        self.prom_frock = QCheckBox("Promotion/Frocking")
        self.prom_frock.setChecked(self.report.prom_frock)
        hboxlayout = self.occasion_box.layout()
        assert isinstance(hboxlayout, QHBoxLayout)
        hboxlayout.insertWidget(2, self.prom_frock)

        self.add_label("Professional Knowledge", 16, 0)
        self.add_label("Quality of Work", 16, 2)
        self.add_label("Command or Organizational Climate", 17, 0)
        self.add_label("Military Bearing/Character", 17, 2)
        self.add_label("Personal Job Accomplishment/Initiative", 18, 0)
        self.add_label("Teamwork", 18, 2)
        self.add_label("Leadership", 19, 0)

        self.achievements = QTextEdit(tabChangesFocus=True, lineWrapMode=QTextEdit.LineWrapMode.FixedColumnWidth)
        self.achievements.setFont(QFont("Courier"))
        self.achievements.setPlaceholderText("Maximum of 2 lines. Excess lines will be trimmed.")
        self.achievements.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.achievements.setLineWrapColumnOrWidth(91)
        self.achievements.setText(self.report.achievements)
        line_height = self.achievements.fontMetrics().lineSpacing()
        self.achievements.setFixedHeight(int(line_height * 3))
        self.achievements.setFixedWidth(900)
        self.achievements_label = QLabel(
            f"Qualifications/Achievements\n"
            f"(Line Count: {len(self.report_type.wrap_text(self.achievements.toPlainText(), 91).split(chr(10)))}/2)"
        )
        self.achievements.textChanged.connect(
            lambda: self.achievements_label.setText(
                f"Qualifications/Achievements\n"
                f"(Line Count: {len(self.report_type.wrap_text(self.achievements.toPlainText(), 91).split(chr(10)))}/2)"
            )
        )
        self.form.addWidget(self.achievements_label, 23, 0)
        self.form.addWidget(self.achievements, 23, 1, 1, 3)

        # Move shared senior address widgets down one row for Eval to place retain between
        # Promotion Recommendation and Reporting Senior Address.
        senior_address_label_item = self.form.itemAtPosition(25, 0)
        senior_address_label = None
        if senior_address_label_item is not None:
            senior_address_label = senior_address_label_item.widget()
        if senior_address_label is not None:
            self.form.addWidget(senior_address_label, 26, 0)
        self.form.addWidget(self.senior_address, 26, 1, 1, 3)

        self.retain = self.add_value_combo(
            row=25,
            col=0,
            label="Retention Reccomended?",
            values=self.retention_recs,
            value=self.report.retain,
        )
        retain_label_item = self.form.itemAtPosition(25, 0)
        if retain_label_item is not None:
            retain_label = retain_label_item.widget()
            if isinstance(retain_label, QLabel):
                retain_label.setToolTip("Select Recommended or Not Recommended")

        # self.setWindowTitle("EVAL Data Entry")

    # @staticmethod
    # def get_idx_for_enum(member: Enum | None) -> int:
    #     """
    #     Return 1-based index of the enum member within its enum class, or 0 if None/not found.

    #     Useful for setting QComboBox current index based on enum member.
    #     """
    #     if member is None:
    #         return 0
    #     return list(type(member).__members__).index(member.name) + 1

    # @Slot()
    # def validate_special(self, check_state: Qt.CheckState):
    #     if check_state == Qt.CheckState.Checked:
    #         self.det_indiv.setChecked(False)
    #         self.prom_frock.setChecked(False)
    #         self.periodic.setChecked(False)

    # @Slot()
    # def validate_career_rec1(self):
    #     text = self.career_rec_1.document().toPlainText()
    #     # width is 13 because that's what navfit98 allows on one line
    #     wrapped = textwrap.wrap(text, width=13)
    #     if len(text) > 20:
    #         QMessageBox.information(
    #             self,
    #             "Career Reccomendation Validation",
    #             "Maximum of 20 characters allowed (including whitespace)",
    #             QMessageBox.StandardButton.Ok,
    #         )
    #         self.career_rec_1.setText(text[:20])
    #     if len(wrapped) > 2:
    #         QMessageBox.information(
    #             self,
    #             "Career Reccomendation Validation",
    #             "Carreer Reccomenation may not exceed two lines.",
    #             QMessageBox.StandardButton.Ok,
    #         )
    #         allowed_text = "\n".join(wrapped[:2])
    #         self.career_rec_1.setText(allowed_text)

    def print(self):
        self.save_form()

        try:
            Eval.model_validate(self.report)
            # validation_failed = False
            # err_msgs = ""
        except ValidationError as err:
            # validation_failed = True
            errors = json.loads(err.json())
            err_msgs = ""
            for error in errors:
                python_field_name = error["loc"][0]
                err_msgs += f"{Eval.model_fields[python_field_name].title}: {error['msg']}\n"

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

    @Slot()
    def submit(self):
        self.save_form()
        self.on_accept(self.report)

    def save_form(self):
        """
        Create a Eval class from the data input in the GUI Form.
        """
        super().save_form()

        # Save the data unique to Eval form defined in its init method
        self.report.prom_frock = self.prom_frock.isChecked()
        self.report.achievements = self.report_type.validate_achievements(self.achievements.toPlainText())
        self.report.retain = self.retain.currentData()
