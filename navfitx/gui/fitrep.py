from PySide6.QtCore import Slot
from PySide6.QtGui import QFont, QTextOption
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDialogButtonBox,
    QFormLayout,
    QLayout,
    QLineEdit,
    QMessageBox,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from navfitx.models import BilletSubcategory, OccasionForReport, PhysicalReadiness, PromotionStatus, TypeOfReport

# class NameValidator(QValidator):
#     def __init__(self, parent=None):
#         super().__init__(parent)

#     def validate(self, input_str: str, pos: int):
#         for char in input_str:
#             if char != char.upper():
#                 return QValidator.State.Invalid, input_str, pos
#         return QValidator.State.Acceptable, input_str, pos

#     def fixup(self, input_str: str) -> str:
#         return input_str.upper()C


class FitrepDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FITREP Data Entry")

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        form_widget = QWidget()
        # form_widget.setMaximumWidth(1200)
        form_layout = QFormLayout(form_widget)
        form_layout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)

        self.name = QLineEdit()
        self.name.editingFinished.connect(self.validate_name)
        form_layout.addRow("Name", self.name)

        self.rank = QLineEdit()
        self.rank.editingFinished.connect(self.validate_grade)
        form_layout.addRow("Rate", self.rank)

        self.desig = QLineEdit()
        form_layout.addRow("Designator", self.desig)

        self.ssn = QLineEdit()
        self.ssn.setToolTip("Format: XXX-XX-XXXX")
        self.ssn.editingFinished.connect(self.validate_ssn)
        form_layout.addRow("SSN", self.ssn)

        self.group = QComboBox()
        self.group.addItems(["ACT", "TAR", "INACT", "AT/ADSW/265"])
        form_layout.addRow("Group", self.group)

        self.uic = QLineEdit()
        self.uic.editingFinished.connect(self.validate_uic)
        form_layout.addRow("UIC", self.uic)

        self.station = QLineEdit()
        form_layout.addRow("Ship/Station", self.station)

        self.promotion_status = QComboBox()
        self.promotion_status.addItems([member.value for member in PromotionStatus])
        form_layout.addRow("Promotion Status", self.promotion_status)

        self.date_reported = QDateEdit()
        form_layout.addRow("Date Reported", self.date_reported)
        # self.date_reported.setCalendarPopup(True)

        self.occasion_for_report = QComboBox()
        self.occasion_for_report.addItems([member.name for member in OccasionForReport])
        form_layout.addRow("Occasion for Report", self.occasion_for_report)

        self.period_start = QDateEdit()
        form_layout.addRow("Period Start", self.period_start)

        self.period_end = QDateEdit()
        form_layout.addRow("Period End", self.period_end)

        self.not_observed = QCheckBox()
        form_layout.addRow("Not Observed Report", self.not_observed)

        self.type_of_report = QComboBox()
        self.type_of_report.addItems([member.name for member in TypeOfReport])
        form_layout.addRow("Type of Report", self.type_of_report)

        self.physical_readiness = QComboBox()
        self.physical_readiness.addItems([member.value for member in PhysicalReadiness])
        form_layout.addRow("Physical Readiness", self.physical_readiness)

        self.billet_subcategory = QComboBox()
        self.billet_subcategory.addItems([member.value for member in BilletSubcategory])
        form_layout.addRow("Billet Subcategory", self.billet_subcategory)

        self.senior_name = QLineEdit()
        form_layout.addRow("Reporting Senior Name", self.senior_name)

        self.senior_grade = QLineEdit()
        form_layout.addRow("Reporting Senior Grade", self.senior_grade)

        self.senior_desig = QLineEdit()
        form_layout.addRow("Reporting Senior Designator", self.senior_desig)

        self.senior_title = QLineEdit()
        form_layout.addRow("Reporting Senior Title", self.senior_title)

        self.senior_uic = QLineEdit()
        form_layout.addRow("Reporting Senior UIC", self.senior_uic)

        self.senior_ssn = QLineEdit()
        form_layout.addRow("Reporting Senior SSN", self.senior_ssn)

        self.duties_abbreviation = QLineEdit()
        self.duties_abbreviation.editingFinished.connect(self.validate_duties_abbreviation)
        form_layout.addRow("Primary Duty Abbreviation", self.duties_abbreviation)

        self.duties_description = QLineEdit()
        form_layout.addRow("Primary/Collateral/Watchstanding Duties", self.duties_abbreviation)

        self.date_counseled = QDateEdit()
        form_layout.addRow("Date Counseled", self.date_counseled)

        self.counselor = QLineEdit()
        form_layout.addRow("Counselor", self.counselor)

        self.job = QTextEdit()
        # self.comments.setLineWrapMode(QTextEdit.LineWrapMode.FixedColumnWidth)
        # self.comments.setLineWrapColumnOrWidth(10)
        form_layout.addRow("Command Employment and\nCommand Achievements", self.job)

        performance_trait_options = [
            "Not Observed",
            "1 - Below Standards",
            "2 - Progressing",
            "3 - Meets Standards",
            "4 - Above Standards",
            "5 - Greatly Exceeds Standards",
        ]

        self.pro_expertise = QComboBox()
        self.pro_expertise.addItems(performance_trait_options)
        form_layout.addRow("Professional Expertise", self.pro_expertise)

        self.cmd_climate = QComboBox()
        self.cmd_climate.addItems(performance_trait_options)
        form_layout.addRow("Command or Organizational Climate", self.cmd_climate)

        self.bearing_and_character = QComboBox()
        self.bearing_and_character.addItems(performance_trait_options)
        form_layout.addRow("Military Bearing/Character", self.bearing_and_character)

        self.teamwork = QComboBox()
        self.teamwork.addItems(performance_trait_options)
        form_layout.addRow("Teamwork", self.teamwork)

        self.accomp_and_initiative = QComboBox()
        self.accomp_and_initiative.addItems(performance_trait_options)
        form_layout.addRow("Mission Accomplishment and Initiative", self.accomp_and_initiative)

        self.leadership = QComboBox()
        self.leadership.addItems(performance_trait_options)
        form_layout.addRow("Leadership", self.leadership)

        self.tactical_performance = QComboBox()
        self.tactical_performance.addItems(performance_trait_options)
        form_layout.addRow("Tactical Performance", self.tactical_performance)

        self.career_rec_1 = QLineEdit()
        form_layout.addRow("Career Recommendation 1", self.career_rec_1)

        self.career_rec_2 = QLineEdit()
        form_layout.addRow("Career Recommendation 2", self.career_rec_2)

        self.comments = QTextEdit()
        self.comments.setLineWrapMode(QTextEdit.LineWrapMode.FixedColumnWidth)
        self.comments.setLineWrapColumnOrWidth(91)
        self.comments.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.comments.setFont(QFont("Courier"))
        line_height = self.comments.fontMetrics().lineSpacing()
        self.comments.setFixedHeight(line_height * 18)
        self.comments.setFixedWidth(900)
        form_layout.addRow("Comments", self.comments)

        self.senior_address = QTextEdit()

        # layout = QVBoxLayout()

        # ---- buttons ----
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        # button_box.accepted.connect(self.verify)
        # button_box.rejected.connect(self.reject)
        # layout.setWidget(button_box)

        scroll_area.setWidget(form_widget)

        # Set the layout for the secondary window
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        main_layout.addWidget(button_box)

        # Set the layout for the secondary window
        self.setLayout(main_layout)

    def print(self):
        print(type(self.comments))
        print(self.comments.toPlainText())

    @Slot()
    def validate_name(self):
        if not self.name.text().isupper():
            answer = QMessageBox.information(
                self,
                "Name Validation",
                "Names are required to be uppercase. Convert to uppercase now?",
                QMessageBox.StandardButton.Yes,
                QMessageBox.StandardButton.No,
            )
            if answer == QMessageBox.StandardButton.Yes:
                self.name.setText(self.name.text().upper())

    @Slot()
    def validate_grade(self):
        if len(self.rank.text()) > 5:
            QMessageBox.information(
                self, "Grade Validation", "Rank/Grade cannot be more than 5 characters.", QMessageBox.StandardButton.Ok
            )
            return
        for char in self.rank.text():
            if not char.isalpha():
                QMessageBox.information(
                    self, "Grade Validation", "Rank/Grade may only contain letters.", QMessageBox.StandardButton.Ok
                )
                return

    @Slot()
    def validate_desig(self):
        if len(self.rank.text()) > 5:
            QMessageBox.information(
                self,
                "Designator Validation",
                "Designator must be less than 12 characters.",
                QMessageBox.StandardButton.Ok,
            )

    @Slot()
    def validate_ssn(self):
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
            # QMessageBox.information(self, "UIC Validation", "UIC cannot be longer than 5 characters.", QMessageBox.StandardButton.Ok)
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
    def validate_duties_abbreviation(self):
        text = self.duties_abbreviation.text()
        if text.isalnum() and len(text) <= 14:
            return
        QMessageBox.information(
            self,
            "Duty Abbreviation Validation",
            "The abbreviation for the primary duty in the small box in block 29 may only contain up to 14 alphanumeric characters.",
            QMessageBox.StandardButton.Ok,
        )

    # @Slot()
    # def verify(self):
    #     print(self.comments.toPlainText().encode())
    #     self.accept()

    # answer = QMessageBox.warning(self, "Invalid Input",
    #                              "The form does not contain all the necessary information.\n"
    #                              "Do you want to discard it?",
    #                              QMessageBox.StandardButton.Ok, QMessageBox.No)

    # if answer == QMessageBox.Yes:
    #     self.reject()
