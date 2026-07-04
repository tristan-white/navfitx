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

    @Slot()
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

    @Slot()
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
