import textwrap
from typing import Callable

from PySide6.QtCore import Slot
from PySide6.QtGui import QFont, QTextOption
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDialogButtonBox,
    QGridLayout,
    QLabel,
    QLayout,
    QLineEdit,
    QMessageBox,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from navfitx.models import (
    BilletSubcategory,
    Fitrep,
    OccasionForReport,
    PhysicalReadiness,
    PromotionStatus,
    TypeOfReport,
)

# class NameValidator(QValidator):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#     def validate(self, input_str: str, pos: int):
#         for char in input_str:
#             if char != char.upper():
#                 return QValidator.State.Invalid, input_str, pos
#         return QValidator.State.Acceptable, input_str, pos
#     def fixup(self, input_str: str) -> str:
#         return input_str.upper()


class FitrepForm(QWidget):
    def __init__(self, on_submit: Callable[[Fitrep], None]):
        super().__init__()
        self.on_submit = on_submit
        self.setWindowTitle("FITREP Data Entry")

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        grid_layout = QGridLayout()
        grid_layout.setColumnStretch(0, 0)
        container_widget = QWidget()
        container_widget.setLayout(grid_layout)

        # form_layout = QFormLayout(form_widget)
        grid_layout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)

        self.name = QLineEdit()
        self.name.editingFinished.connect(self.validate_name)
        self.name.setMaximumWidth(200)
        grid_layout.addWidget(QLabel("Name"), 0, 0)
        grid_layout.addWidget(self.name, 0, 1)

        self.rank = QLineEdit()
        self.rank.editingFinished.connect(self.validate_grade)
        # form_layout.addRow("Rate", self.rank)
        grid_layout.addWidget(QLabel("Rank"), 0, 2)
        grid_layout.addWidget(self.rank, 0, 3)

        self.desig = QLineEdit()
        # form_layout.addRow("Designator", self.desig)
        grid_layout.addWidget(QLabel("Designator"), 1, 0)
        grid_layout.addWidget(self.desig, 1, 1)

        self.ssn = QLineEdit()
        self.ssn.setToolTip("Format: XXX-XX-XXXX")
        self.ssn.editingFinished.connect(self.validate_ssn)
        # form_layout.addRow("SSN", self.ssn)
        grid_layout.addWidget(QLabel("SSN"), 1, 2)
        grid_layout.addWidget(self.ssn, 1, 3)

        self.group = QComboBox()
        self.group.addItems(["ACT", "TAR", "INACT", "AT/ADSW/265"])
        # form_layout.addRow("Group", self.group)
        grid_layout.addWidget(QLabel("Group"), 2, 0)
        grid_layout.addWidget(self.group, 2, 1)

        self.uic = QLineEdit()
        self.uic.editingFinished.connect(self.validate_uic)
        # form_layout.addRow("UIC", self.uic)
        grid_layout.addWidget(QLabel("UIC"), 2, 2)
        grid_layout.addWidget(self.uic, 2, 3)

        self.station = QLineEdit()
        self.station.editingFinished.connect(self.validate_ship_station)
        # form_layout.addRow("Ship/Station", self.station)
        grid_layout.addWidget(QLabel("Ship/Station"), 3, 0)
        grid_layout.addWidget(self.station, 3, 1)

        self.promotion_status = QComboBox()
        self.promotion_status.addItems([member.value for member in PromotionStatus])
        # form_layout.addRow("Promotion Status", self.promotion_status)
        grid_layout.addWidget(QLabel("Promotion Status"), 3, 2)
        grid_layout.addWidget(self.promotion_status, 3, 3)

        self.date_reported = QDateEdit()
        # form_layout.addRow("Date Reported", self.date_reported)
        # self.date_reported.setCalendarPopup(True)
        grid_layout.addWidget(QLabel("Date Reported"), 4, 0)
        grid_layout.addWidget(self.date_reported, 4, 1)

        self.occasion_for_report = QComboBox()
        self.occasion_for_report.addItems([member.name for member in OccasionForReport])
        # form_layout.addRow("Occasion for Report", self.occasion_for_report)
        grid_layout.addWidget(QLabel("Occasion for Report"), 4, 2)
        grid_layout.addWidget(self.occasion_for_report, 4, 3)

        self.period_start = QDateEdit()
        # form_layout.addRow("Period Start", self.period_start)
        grid_layout.addWidget(QLabel("Period Start"), 5, 0)
        grid_layout.addWidget(self.period_start, 5, 1)

        self.period_end = QDateEdit()
        # form_layout.addRow("Period End", self.period_end)
        grid_layout.addWidget(QLabel("Period End"), 5, 2)
        grid_layout.addWidget(self.period_end, 5, 3)

        self.not_observed = QCheckBox()
        # form_layout.addRow("Not Observed Report", self.not_observed)
        grid_layout.addWidget(QLabel("Not Observed Report"), 6, 0)
        grid_layout.addWidget(self.not_observed, 6, 1)

        self.type_of_report = QComboBox()
        self.type_of_report.addItems([member.name for member in TypeOfReport])
        self.type_of_report.currentIndexChanged.connect(self.validate_type_of_report)
        # form_layout.addRow("Type of Report", self.type_of_report)
        grid_layout.addWidget(QLabel("Type of Report"), 6, 2)
        grid_layout.addWidget(self.type_of_report, 6, 3)

        self.physical_readiness = QComboBox()
        self.physical_readiness.addItems("")
        self.physical_readiness.addItems([member.value for member in PhysicalReadiness])
        # form_layout.addRow("Physical Readiness", self.physical_readiness)
        grid_layout.addWidget(QLabel("Physical Readiness"), 7, 0)
        grid_layout.addWidget(self.physical_readiness, 7, 1)

        self.billet_subcategory = QComboBox()
        self.billet_subcategory.addItems([member.value for member in BilletSubcategory])
        # form_layout.addRow("Billet Subcategory", self.billet_subcategory)
        grid_layout.addWidget(QLabel("Billet Subcategory"), 7, 2)
        grid_layout.addWidget(self.billet_subcategory, 7, 3)

        self.senior_name = QLineEdit()
        # form_layout.addRow("Reporting Senior Name", self.senior_name)
        grid_layout.addWidget(QLabel("Reporting Senior Name"), 8, 0)
        grid_layout.addWidget(self.senior_name, 8, 1)

        self.senior_grade = QLineEdit()
        # form_layout.addRow("Reporting Senior Grade", self.senior_grade)
        grid_layout.addWidget(QLabel("Reporting Senior Grade"), 8, 2)
        grid_layout.addWidget(self.senior_grade, 8, 3)

        self.senior_desig = QLineEdit()
        # form_layout.addRow("Reporting Senior Designator", self.senior_desig)
        grid_layout.addWidget(QLabel("Reporting Senior Designator"), 9, 0)
        grid_layout.addWidget(self.senior_desig, 9, 1)

        self.senior_title = QLineEdit()
        # form_layout.addRow("Reporting Senior Title", self.senior_title)
        grid_layout.addWidget(QLabel("Reporting Senior Title"), 9, 2)
        grid_layout.addWidget(self.senior_title, 9, 3)

        self.senior_uic = QLineEdit()
        # form_layout.addRow("Reporting Senior UIC", self.senior_uic)
        grid_layout.addWidget(QLabel("Reporting Senior UIC"), 10, 0)
        grid_layout.addWidget(self.senior_uic, 10, 1)

        self.senior_ssn = QLineEdit()
        # form_layout.addRow("Reporting Senior SSN", self.senior_ssn)
        grid_layout.addWidget(QLabel("Reporting Senior SSN"), 10, 2)
        grid_layout.addWidget(self.senior_ssn, 10, 3)

        self.duties_abbreviation = QLineEdit()
        self.duties_abbreviation.editingFinished.connect(self.validate_duties_abbreviation)
        # form_layout.addRow("Primary Duty Abbreviation", self.duties_abbreviation)
        grid_layout.addWidget(QLabel("Primary Duty Abbreviation"), 11, 0)
        grid_layout.addWidget(self.duties_abbreviation, 11, 1)

        self.duties_description = QLineEdit()
        # form_layout.addRow("Primary/Collateral/Watchstanding Duties", self.duties_description)
        grid_layout.addWidget(QLabel("Primary/Collateral/Watchstanding Duties"), 11, 2)
        grid_layout.addWidget(self.duties_description, 11, 3)

        self.date_counseled = QDateEdit()
        # form_layout.addRow("Date Counseled", self.date_counseled)
        grid_layout.addWidget(QLabel("Date Counseled"), 12, 0)
        grid_layout.addWidget(self.date_counseled, 12, 1)

        self.counselor = QLineEdit()
        # form_layout.addRow("Counselor", self.counselor)
        grid_layout.addWidget(QLabel("Counselor"), 12, 2)
        grid_layout.addWidget(self.counselor, 12, 3)

        # h = self.counselor.sizeHint().height()
        # w = self.counselor.sizeHint().width()

        # grid_layout.addItem(QSpacerItem(0, h), 13, 0)

        self.job = QTextEdit()
        # self.comments.setLineWrapMode(QTextEdit.LineWrapMode.FixedColumnWidth)
        # self.comments.setLineWrapColumnOrWidth(10)
        # form_layout.addRow("Command Employment and\nCommand Achievements", self.job)
        grid_layout.addWidget(QLabel("Command Employment and\nCommand Achievements"), 14, 0)
        grid_layout.addWidget(self.job, 14, 1, 1, 3)

        performance_trait_options = [
            "",
            "Not Observed",
            "1 - Below Standards",
            "2 - Progressing",
            "3 - Meets Standards",
            "4 - Above Standards",
            "5 - Greatly Exceeds Standards",
        ]

        self.pro_expertise = QComboBox()
        self.pro_expertise.addItems(performance_trait_options)
        # form_layout.addRow("Professional Expertise", self.pro_expertise)
        grid_layout.addWidget(QLabel("Professional Expertise"), 15, 0)
        grid_layout.addWidget(self.pro_expertise, 15, 1)

        self.cmd_climate = QComboBox()
        self.cmd_climate.addItems(performance_trait_options)
        # form_layout.addRow("Command or Organizational Climate", self.cmd_climate)
        grid_layout.addWidget(QLabel("Command or Organizational Climate"), 15, 2)
        grid_layout.addWidget(self.cmd_climate, 15, 3)

        self.bearing_and_character = QComboBox()
        self.bearing_and_character.addItems(performance_trait_options)
        # form_layout.addRow("Military Bearing/Character", self.bearing_and_character)
        grid_layout.addWidget(QLabel("Military Bearing/Character"), 16, 0)
        grid_layout.addWidget(self.bearing_and_character, 16, 1)

        self.teamwork = QComboBox()
        self.teamwork.addItems(performance_trait_options)
        # form_layout.addRow("Teamwork", self.teamwork)
        grid_layout.addWidget(QLabel("Teamwork"), 16, 2)
        grid_layout.addWidget(self.teamwork, 16, 3)

        self.accomp_and_initiative = QComboBox()
        self.accomp_and_initiative.addItems(performance_trait_options)
        # form_layout.addRow("Mission Accomplishment and Initiative", self.accomp_and_initiative)
        grid_layout.addWidget(QLabel("Mission Accomplishment and Initiative"), 17, 0)
        grid_layout.addWidget(self.accomp_and_initiative, 17, 1)

        self.leadership = QComboBox()
        self.leadership.addItems(performance_trait_options)
        # form_layout.addRow("Leadership", self.leadership)
        grid_layout.addWidget(QLabel("Leadership"), 17, 2)
        grid_layout.addWidget(self.leadership, 17, 3)

        self.tactical_performance = QComboBox()
        self.tactical_performance.addItems(performance_trait_options)
        # form_layout.addRow("Tactical Performance", self.tactical_performance)
        grid_layout.addWidget(QLabel("Tactical Performance"), 18, 0)
        grid_layout.addWidget(self.tactical_performance, 18, 1)

        self.career_rec_1 = QTextEdit(tabChangesFocus=True)
        self.career_rec_1.setLineWrapMode(QTextEdit.LineWrapMode.FixedColumnWidth)
        self.career_rec_1.setLineWrapColumnOrWidth(13)
        self.career_rec_1.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.career_rec_1.setFont(QFont("Courier"))
        line_spacing = self.career_rec_1.fontMetrics().lineSpacing()
        # capHeight = self.career_rec_1.fontMetrics().capHeight()
        # height = self.career_rec_1.height()
        self.career_rec_1.setFixedHeight(line_spacing * 2)
        self.career_rec_1.setFixedWidth(900)
        self.career_rec_1.textChanged.connect(self.validate_career_rec1)
        # form_layout.addRow("Career Recommendation 1", self.career_rec_1)
        grid_layout.addWidget(QLabel("Career Recommendation 1"), 19, 0)
        grid_layout.addWidget(self.career_rec_1, 19, 1, 1, 3)

        self.career_rec_2 = QTextEdit()
        self.career_rec_2.setLineWrapMode(QTextEdit.LineWrapMode.FixedColumnWidth)
        self.career_rec_2.setLineWrapColumnOrWidth(13)
        self.career_rec_2.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.career_rec_2.setFont(QFont("Courier"))
        line_height = self.career_rec_2.fontMetrics().lineSpacing()
        self.career_rec_2.setFixedHeight(line_height * 2)
        self.career_rec_2.setFixedWidth(900)
        # form_layout.addRow("Career Recommendation 2", self.career_rec_2)
        grid_layout.addWidget(QLabel("Career Recommendation 2"), 20, 0)
        grid_layout.addWidget(self.career_rec_2, 20, 1, 1, 3)

        self.comments = QTextEdit()
        self.comments.setLineWrapMode(QTextEdit.LineWrapMode.FixedColumnWidth)
        self.comments.setLineWrapColumnOrWidth(91)
        self.comments.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.comments.setFont(QFont("Courier"))
        line_height = self.comments.fontMetrics().lineSpacing()
        self.comments.setFixedHeight(line_height * 18)
        self.comments.setFixedWidth(900)
        # form_layout.addRow("Comments", self.comments)
        grid_layout.addWidget(QLabel("Comments"), 21, 0)
        grid_layout.addWidget(self.comments, 21, 1, 1, 3)

        self.indiv_promo_rec = QComboBox()
        choices = ["", "NOB", "Significant Problems", "Progressing", "Promotable", "Must Promote", "Early Promote"]
        self.leadership.addItems(choices)
        # form_layout.addRow("Promotion Reccomendation", self.indiv_promo_rec)
        grid_layout.addWidget(QLabel("Promotion Reccomendation"), 22, 0)
        grid_layout.addWidget(self.indiv_promo_rec, 22, 1)

        self.senior_address = QTextEdit()
        self.senior_address.setLineWrapMode(QTextEdit.LineWrapMode.FixedColumnWidth)
        self.senior_address.setLineWrapColumnOrWidth(27)
        self.senior_address.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.senior_address.setFont(QFont("Courier"))
        line_height = self.name.fontMetrics().lineSpacing()
        self.senior_address.setFixedHeight(line_height * 5)
        self.senior_address.setFixedWidth(500)
        # form_layout.addRow("Reporting Senior Address", self.senior_address)
        grid_layout.addWidget(QLabel("Reporting Senior Address"), 23, 0)
        grid_layout.addWidget(self.senior_address, 23, 1, 1, 3)

        # layout = QVBoxLayout()

        # grid_layout.addItem(QSpacerItem(0, 0))
        # grid_layout.setRowStretch(15, 1)

        # ---- buttons ----
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        ok_btn = button_box.button(QDialogButtonBox.StandardButton.Ok)
        ok_btn.setText("Submit")
        button_box.accepted.connect(self.submit)
        button_box.rejected.connect(lambda: print("rejected"))

        # scroll_area.setWidget(form_widget)
        scroll_area.setWidget(container_widget)

        # Set the layout for the secondary window
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        main_layout.addWidget(button_box)

        # Set the layout for the secondary window
        self.setLayout(main_layout)

    def submit(self):
        fitrep = self.create_fitrep()
        self.on_submit(fitrep)

    @Slot()
    def validate_career_rec1(self):
        text = self.career_rec_1.document().toPlainText()
        wrapped = textwrap.wrap(text, width=13)
        msg = (
            "In order to mimic the exact constraints of NAVFIT98, the following constraints\n"
            "apply to the the career reccomendation blocks:\n"
            "- Maximum of 20 characters, including spaces, but not including newlines.\n"
            "- No more than 13 characters on a line."
        )
        if len(wrapped) > 2 or len(text) > 20:
            QMessageBox.information(
                self,
                "Career Reccomendation Validation",
                msg,
                QMessageBox.StandardButton.Ok,
            )
            self.career_rec_1.setText(text[:20])

    @Slot()
    def validate_type_of_report(self):
        # text = self.type_of_report.currentText()
        pass

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

    def create_fitrep(self) -> Fitrep:
        """
        Create a Fitrep class from the data input in the GUI Form.
        """
        return Fitrep(
            name=self.name.text(),
            rate=self.rank.text(),
            desig=self.desig.text(),
            ssn=self.ssn.text(),
            # group=self.group.currentText(),
            uic=self.uic.text(),
            station=self.station.text(),
            promotion_status=self.promotion_status.currentText(),
            date_reported=self.date_reported.date().toPython(),
            # occasion_for_report=self.occasion_for_report.currentText(),
            period_start=self.period_start.date().toPython(),
            period_end=self.period_end.date().toPython(),
            not_observed=self.not_observed.isChecked(),
            # type_of_report=self.type_of_report.currentText(),
            physical_readiness=self.physical_readiness.currentText(),
            billet_subcategory=self.billet_subcategory.currentText(),
            senior_name=self.senior_name.text(),
            senior_grade=self.senior_grade.text(),
            senior_desig=self.senior_desig.text(),
            senior_title=self.senior_title.text(),
            senior_uic=self.senior_uic.text(),
            senior_ssn=self.senior_ssn.text(),
            duties_abbreviation=self.duties_abbreviation.text(),
            duties_description=self.duties_description.text(),
            date_counseled=self.date_counseled.date().toPython(),
            counselor=self.counselor.text(),
            # pro_expertise=self.pro_expertise,
            # cmd_climate=self.cmd_climate,
            # bearing_and_character=self.bearing_and_character,
            # teamwork=self.teamwork,
            # accomp_and_initiative=self.accomp_and_initiative,
            # leadership=self.leadership,
            # tactical_performance=self.tactical_performance,
            career_rec_1=self.career_rec_1.toPlainText(),
            career_rec_2=self.career_rec_2.toPlainText(),
            comments=self.comments.toPlainText(),
            # indiv_promo_rec=self.indiv_promo_rec,
            senior_address=self.senior_address.toPlainText(),
        )
