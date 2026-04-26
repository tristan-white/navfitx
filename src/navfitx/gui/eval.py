import json
from typing import Callable

from pydantic import ValidationError
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
)

from navfitx.models import (
    Eval,
)

from .report import BaseReportForm


class EvalForm(BaseReportForm[Eval]):
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

        # self.setWindowTitle("EVAL Data Entry")

    # def validate_report(self):
    #     """Perform validation on all fields in the form."""
    #     # TODO: save form before validating.
    #     try:
    #         Eval.model_validate(self.report.model_dump())
    #     except ValidationError as err:
    #         errors = json.loads(err.json())
    #         # show a list of all validation errors
    #         error_messages = "\n".join([f"{error['loc'][0]}: {error['msg']}" for error in errors])

    #         test = QMessageBox()
    #         test.setWindowModality(Qt.WindowModality.NonModal)
    #         test.information(self, "Validation", error_messages)
    #         # test.show()

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
    # def validate_occasion(self, check_state: Qt.CheckState):
    #     if check_state == Qt.CheckState.Checked:
    #         self.special.setChecked(False)

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

    # @Slot()
    # def validate_ship_station(self):
    #     if len(self.station.text()) > 18:
    #         QMessageBox.information(
    #             self,
    #             "Ship/Station Validation",
    #             "Maximum of 18 characters allowed.",
    #             QMessageBox.StandardButton.Ok,
    #         )
    #         self.station.setText("")

    # @Slot()
    # def validate_name(self):
    #     self.name.setText(self.name.text().upper())

    # @Slot()
    # def validate_grade(self):
    #     if len(self.grade.text()) > 5:
    #         QMessageBox.information(
    #             self, "Grade Validation", "Rank/Grade cannot be more than 5 characters.", QMessageBox.StandardButton.Ok
    #         )
    #         return

    # @Slot()
    # def validate_desig(self):
    #     if len(self.desig.text()) > 5:
    #         QMessageBox.information(
    #             self,
    #             "Designator Validation",
    #             "Designator must be less than 12 characters.",
    #             QMessageBox.StandardButton.Ok,
    #         )

    # @Slot()
    # def validate_ssn(self):
    #     self.ssn.setText(self.ssn.text().strip())
    #     ssn_text = self.ssn.text()
    #     if len(ssn_text) != 11 or ssn_text[3] != "-" or ssn_text[6] != "-":
    #         QMessageBox.information(
    #             self, "SSN Validation", "SSN must be in the format XXX-XX-XXXX.", QMessageBox.StandardButton.Ok
    #         )
    #         return
    #     for i, char in enumerate(ssn_text):
    #         if i in [3, 6]:
    #             continue
    #         if not char.isdigit():
    #             QMessageBox.information(
    #                 self, "SSN Validation", "SSN must be in the format XXX-XX-XXXX.", QMessageBox.StandardButton.Ok
    #             )
    #             return

    # @Slot()
    # def validate_uic(self):
    #     if len(self.uic.text()) > 5:
    #         QMessageBox.information(
    #             self,
    #             "Block 40 Validation",
    #             "Block 40 may only have up to 20 alpha-numeric characters.",
    #             QMessageBox.StandardButton.Ok,
    #         )
    #     for char in self.uic.text():
    #         if not char.isalnum():
    #             QMessageBox.information(
    #                 self,
    #                 "UIC Validation",
    #                 "UIC may only contain alphanumeric characters.",
    #                 QMessageBox.StandardButton.Ok,
    #             )

    # @Slot()
    # def validate_billet_subcategory(self):
    #     if "SPECIAL" in self.billet_subcategory.currentData():
    #         QMessageBox.information(
    #             self,
    #             "Billet Subcategory Validation",
    #             "Note: 'SPECIAL' subcategories are only permitted use with Commander, Navy Personnel Command approval.",
    #             QMessageBox.StandardButton.Ok,
    #         )

    # @Slot()
    # def validate_duties_description(self):
    #     """
    #     This block is funky because of the duteis abbreviation block, which takes up some space on the first line.
    #     I think the best solution that makes for an acceptable UX is to initialize the box with spaces. However,
    #     the user may delete these, in which case they should be added back so the user sees and accurate line
    #     count. This function, therefore, is not used to validate the length, but rather strip the text of
    #     leading/trailing whitespace, then re-add the spaces to the beginning to ensure the line count is accurate.
    #     """
    #     self.duties_description.setText(
    #         f"{' ' * DUTIES_DESC_SPACE_FOR_ABBREV}{self.duties_description.toPlainText().strip()}"
    #     )

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

    def submit(self):
        self.save_form()
        self.on_accept(self.report)

    def save_form(self):
        """
        Create a Eval class from the data input in the GUI Form.
        """
        super().save_form()
        # self.report.prom_frock = self.prom_frock.isChecked()
