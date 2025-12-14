import textwrap
from enum import Enum
from pathlib import Path
from typing import Callable

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
    QMessageBox,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from navfitx.models import (
    BilletSubcategory,
    Fitrep,
    PhysicalReadiness,
    PromotionRecommendation,
    PromotionStatus,
    SummaryGroup,
)
from navfitx.overlay import create_fitrep_pdf


class NoScrollComboBox(QComboBox):
    def wheelEvent(self, event):
        event.ignore()


# promotion_recs is moved into FitrepForm as a class attribute (see below)


class FitrepForm(QWidget):
    # Performance trait mapping used by multiple combo boxes. Kept as a class
    # attribute so instances can reference it as `self.perf_traits`.
    perf_traits = {
        "": None,
        "Not Observed": 0,
        "1 - Below Standards": 1,
        "2 - Progressing": 2,
        "3 - Meets Standards": 3,
        "4 - Above Standards": 4,
        "5 - Greatly Exceeds Standards": 5,
    }
    # Promotion recommendation mapping used by the promotion combo in the form.
    promotion_recs = {
        "": None,
        "NOB": PromotionRecommendation.NOB.value,
        "Significant Problems": PromotionRecommendation.SIGNIFICANT_PROBLEMS.value,
        "Progressing": PromotionRecommendation.PROGRESSING.value,
        "Promotable": PromotionRecommendation.PROMOTABLE.value,
        "Must Promote": PromotionRecommendation.MUST_PROMOTE.value,
        "Early Promote": PromotionRecommendation.EARLY_PROMOTE.value,
    }

    def __init__(self, on_accept: Callable[[Fitrep], None], on_reject: Callable[[], None], fitrep: Fitrep | None):
        super().__init__()
        self.fitrep = fitrep or Fitrep()
        self.on_accept = on_accept
        self.on_reject = on_reject

        self.setWindowTitle("FITREP Data Entry")

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        grid_layout = QGridLayout()
        grid_layout.setColumnStretch(0, 0)
        container_widget = QWidget()
        container_widget.setLayout(grid_layout)

        grid_layout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)

        self.name = QLineEdit()
        self.name.setText(self.fitrep.name)
        self.name.setPlaceholderText("LAST, FIRST MI Suffix")
        self.name.editingFinished.connect(self.validate_name)
        grid_layout.addWidget(QLabel("1. Name"), 0, 0)
        grid_layout.addWidget(self.name, 0, 1)

        self.grade = QLineEdit()
        self.grade.setText(self.fitrep.grade)
        self.grade.editingFinished.connect(self.validate_grade)
        grid_layout.addWidget(QLabel("2. Rank"), 0, 2)
        grid_layout.addWidget(self.grade, 0, 3)

        self.desig = QLineEdit()
        self.desig.setText(self.fitrep.desig)
        grid_layout.addWidget(QLabel("3. Designator"), 1, 0)
        grid_layout.addWidget(self.desig, 1, 1)

        self.ssn = QLineEdit()
        self.ssn.setText(self.fitrep.ssn)
        self.ssn.setPlaceholderText("XXX-XX-XXXX")
        self.ssn.editingFinished.connect(self.validate_ssn)
        grid_layout.addWidget(QLabel("4. SSN"), 1, 2)
        grid_layout.addWidget(self.ssn, 1, 3)

        self.group = NoScrollComboBox()
        # AT/ADSW/265 does not match the ATADSW option in BUPERS, the NAVFIT98 user guide, nor
        # the NAVFIT98 .accdb database, but it is what is shown on paper reports themselves,
        # so it's used here to look the same as the form.
        self.group.addItem("")
        self.group.addItems([member.value for member in SummaryGroup])
        grid_layout.addWidget(QLabel("5. Group"), 2, 0)
        grid_layout.addWidget(self.group, 2, 1)

        self.uic = QLineEdit()
        self.uic.setText(self.fitrep.uic)
        self.uic.editingFinished.connect(self.validate_uic)
        grid_layout.addWidget(QLabel("6. UIC"), 2, 2)
        grid_layout.addWidget(self.uic, 2, 3)

        self.station = QLineEdit()
        self.station.setText(self.fitrep.station)
        self.station.editingFinished.connect(self.validate_ship_station)
        grid_layout.addWidget(QLabel("7. Ship/Station"), 3, 0)
        grid_layout.addWidget(self.station, 3, 1)

        self.promotion_status = QComboBox(currentText=self.fitrep.promotion_status)
        self.promotion_status.addItem("")
        self.promotion_status.addItems([member.value for member in PromotionStatus])
        self.promotion_status.setCurrentIndex(self.get_idx_for_enum(self.fitrep.promotion_status))
        grid_layout.addWidget(QLabel("8. Promotion Status"), 3, 2)
        grid_layout.addWidget(self.promotion_status, 3, 3)

        # Move Date Reported so it appears before Type of Report in the grid
        self.date_reported = QDateEdit(calendarPopup=True, displayFormat="dd MMMM yyyy")  # type: ignore[call-overload]
        if self.fitrep.date_reported is not None:
            y = self.fitrep.date_reported.year
            m = self.fitrep.date_reported.month
            d = self.fitrep.date_reported.day
            self.date_reported.setDate(QDate(y, m, d))
        grid_layout.addWidget(QLabel("9. Date Reported"), 4, 0)
        grid_layout.addWidget(self.date_reported, 4, 1)

        group_box = QGroupBox("Occasion for Report")
        self.periodic = QCheckBox("10. Periodic")
        self.periodic.setChecked(self.fitrep.periodic)
        self.periodic.checkStateChanged.connect(self.validate_occasion)
        self.det_indiv = QCheckBox("11. Detachment of Individual")
        self.det_indiv.setChecked(self.fitrep.det_indiv)
        self.det_indiv.checkStateChanged.connect(self.validate_occasion)
        self.det_rs = QCheckBox("12. Detachment of Reporting Senior")
        self.det_rs.setChecked(self.fitrep.det_rs)
        self.det_rs.checkStateChanged.connect(self.validate_occasion)
        self.special = QCheckBox("13. Special")
        self.special.setChecked(self.fitrep.special)
        self.special.checkStateChanged.connect(self.validate_special)
        vbox = QHBoxLayout()
        vbox.addWidget(self.periodic)
        vbox.addWidget(self.det_indiv)
        vbox.addWidget(self.det_rs)
        vbox.addWidget(self.special)
        group_box.setLayout(vbox)
        grid_layout.addWidget(group_box, 4, 2, 1, 2)

        self.period_start = QDateEdit(calendarPopup=True, displayFormat="dd MMMM yyyy")  # type: ignore[call-overload]
        if self.fitrep.period_start:
            y = self.fitrep.period_start.year
            m = self.fitrep.period_start.month
            d = self.fitrep.period_start.day
            self.period_start.setDate(QDate(y, m, d))
        grid_layout.addWidget(QLabel("14. Period Start"), 6, 0)
        grid_layout.addWidget(self.period_start, 6, 1)

        self.period_end = QDateEdit(calendarPopup=True, displayFormat="dd MMMM yyyy")  # type: ignore[call-overload]
        if self.fitrep.period_end:
            y = self.fitrep.period_end.year
            m = self.fitrep.period_end.month
            d = self.fitrep.period_end.day
            self.period_end.setDate(QDate(y, m, d))
        grid_layout.addWidget(QLabel("15. Period End"), 6, 2)
        grid_layout.addWidget(self.period_end, 6, 3)

        self.not_observed = QCheckBox()
        self.not_observed.setChecked(self.fitrep.not_observed)
        grid_layout.addWidget(QLabel("16. Not Observed Report"), 7, 0)
        grid_layout.addWidget(self.not_observed, 7, 1)

        group_box = QGroupBox("Type of Report")
        self.regular = QCheckBox("17. Regular")
        self.regular.setChecked(self.fitrep.regular)
        self.concurrent = QCheckBox("18. Concurrent")
        self.concurrent.setChecked(self.fitrep.concurrent)
        self.concurrent.checkStateChanged.connect(self.validate_concurrent)
        self.ops_cdr = QCheckBox("19. OpsCdr")
        self.ops_cdr.setChecked(self.fitrep.ops_cdr)
        self.ops_cdr.checkStateChanged.connect(self.validate_ops_cdr)
        hbox = QHBoxLayout()
        hbox.addWidget(self.regular)
        hbox.addWidget(self.concurrent)
        hbox.addWidget(self.ops_cdr)
        group_box.setLayout(hbox)
        grid_layout.addWidget(group_box, 7, 2, 1, 2)

        self.physical_readiness = QComboBox()
        self.physical_readiness.addItem("")
        self.physical_readiness.addItems([member.value for member in PhysicalReadiness])
        self.physical_readiness.setCurrentIndex(self.get_idx_for_enum(self.fitrep.physical_readiness))
        grid_layout.addWidget(QLabel("20. Physical Readiness"), 8, 0)
        grid_layout.addWidget(self.physical_readiness, 8, 1)

        self.billet_subcategory = QComboBox()
        self.billet_subcategory.addItem("")
        self.billet_subcategory.addItems([member.value for member in BilletSubcategory])
        self.billet_subcategory.setCurrentIndex(self.get_idx_for_enum(self.fitrep.billet_subcategory))
        grid_layout.addWidget(QLabel("21. Billet Subcategory"), 8, 2)
        grid_layout.addWidget(self.billet_subcategory, 8, 3)

        self.senior_name = QLineEdit()
        self.senior_name.setText(self.fitrep.senior_name)
        self.senior_name.setPlaceholderText("LAST, FI MI")
        grid_layout.addWidget(QLabel("22. Reporting Senior Name"), 9, 0)
        grid_layout.addWidget(self.senior_name, 9, 1)

        self.senior_grade = QLineEdit()
        self.senior_grade.setText(self.fitrep.senior_grade)
        grid_layout.addWidget(QLabel("23. Reporting Senior Grade"), 9, 2)
        grid_layout.addWidget(self.senior_grade, 9, 3)

        self.senior_desig = QLineEdit()
        self.senior_desig.setText(self.fitrep.senior_desig)
        grid_layout.addWidget(QLabel("24. Reporting Senior Designator"), 10, 0)
        grid_layout.addWidget(self.senior_desig, 10, 1)

        self.senior_title = QLineEdit()
        self.senior_title.setText(self.fitrep.senior_title)
        grid_layout.addWidget(QLabel("25. Reporting Senior Title"), 10, 2)
        grid_layout.addWidget(self.senior_title, 10, 3)

        self.senior_uic = QLineEdit()
        self.senior_uic.setText(self.fitrep.senior_uic)
        grid_layout.addWidget(QLabel("26. Reporting Senior UIC"), 11, 0)
        grid_layout.addWidget(self.senior_uic, 11, 1)

        self.senior_ssn = QLineEdit()
        self.senior_ssn.setText(self.fitrep.senior_ssn)
        self.senior_ssn.setPlaceholderText("XXX-XX-XXXX")
        grid_layout.addWidget(QLabel("27. Reporting Senior SSN"), 11, 2)
        grid_layout.addWidget(self.senior_ssn, 11, 3)

        self.job = QTextEdit()
        self.job.setText(self.fitrep.job)
        grid_layout.addWidget(QLabel("28. Command Employment and\nCommand Achievements"), 12, 0)
        grid_layout.addWidget(self.job, 12, 1, 1, 3)

        self.duties_abbreviation = QLineEdit()
        self.duties_abbreviation.setPlaceholderText("(14 characters max)")
        self.duties_abbreviation.setMaxLength(14)
        self.duties_abbreviation.setText(self.fitrep.duties_abbreviation)
        # self.duties_abbreviation.editingFinished.connect(self.validate_duties_abbreviation)
        grid_layout.addWidget(QLabel("Primary Duty Abbreviation"), 13, 0)
        grid_layout.addWidget(self.duties_abbreviation, 13, 1)

        self.duties_description = QLineEdit()
        self.duties_description.setText(self.fitrep.duties_description)
        grid_layout.addWidget(QLabel("Primary/Collateral/Watchstanding Duties"), 13, 2)
        grid_layout.addWidget(self.duties_description, 13, 3)

        self.date_counseled = QDateEdit(calendarPopup=True, displayFormat="dd MMMM yyyy")  # type: ignore[call-overload]
        if self.fitrep.date_counseled:
            y = self.fitrep.date_counseled.year
            m = self.fitrep.date_counseled.month
            d = self.fitrep.date_counseled.day
            self.date_counseled.setDate(QDate(y, m, d))
        grid_layout.addWidget(QLabel("Date Counseled"), 14, 0)
        grid_layout.addWidget(self.date_counseled, 14, 1)

        self.counselor = QLineEdit()
        self.counselor.setText(self.fitrep.counselor)
        grid_layout.addWidget(QLabel("Counselor"), 14, 2)
        grid_layout.addWidget(self.counselor, 14, 3)

        # h = self.counselor.sizeHint().height()
        # w = self.counselor.sizeHint().width()
        # grid_layout.addItem(QSpacerItem(0, h), 13, 0)

        self.pro_expertise = QComboBox()
        self.pro_expertise.addItems([p for p in self.perf_traits.keys()])
        if self.fitrep.pro_expertise is not None:
            self.pro_expertise.setCurrentIndex(self.fitrep.pro_expertise + 1)
        grid_layout.addWidget(QLabel("Professional Expertise"), 16, 0)
        grid_layout.addWidget(self.pro_expertise, 16, 1)

        self.cmd_climate = QComboBox()
        self.cmd_climate.addItems([p for p in self.perf_traits.keys()])
        if self.fitrep.cmd_climate is not None:
            self.cmd_climate.setCurrentIndex(self.fitrep.cmd_climate + 1)
        grid_layout.addWidget(QLabel("Command or Organizational Climate"), 16, 2)
        grid_layout.addWidget(self.cmd_climate, 16, 3)

        self.bearing_and_character = QComboBox()
        self.bearing_and_character.addItems([p for p in self.perf_traits.keys()])
        if self.fitrep.bearing_and_character is not None:
            self.bearing_and_character.setCurrentIndex(self.fitrep.bearing_and_character + 1)
        grid_layout.addWidget(QLabel("Military Bearing/Character"), 17, 0)
        grid_layout.addWidget(self.bearing_and_character, 17, 1)

        self.teamwork = QComboBox()
        self.teamwork.addItems([p for p in self.perf_traits.keys()])
        if self.fitrep.teamwork is not None:
            self.teamwork.setCurrentIndex(self.fitrep.teamwork + 1)
        grid_layout.addWidget(QLabel("Teamwork"), 17, 2)
        grid_layout.addWidget(self.teamwork, 17, 3)

        self.accomp_and_initiative = QComboBox()
        self.accomp_and_initiative.addItems([p for p in self.perf_traits.keys()])
        if self.fitrep.accomp_and_initiative is not None:
            self.accomp_and_initiative.setCurrentIndex(self.fitrep.accomp_and_initiative + 1)
        grid_layout.addWidget(QLabel("Mission Accomplishment and Initiative"), 18, 0)
        grid_layout.addWidget(self.accomp_and_initiative, 18, 1)

        self.leadership = QComboBox()
        self.leadership.addItems([p for p in self.perf_traits.keys()])
        if self.fitrep.leadership is not None:
            self.leadership.setCurrentIndex(self.fitrep.leadership + 1)
        grid_layout.addWidget(QLabel("Leadership"), 18, 2)
        grid_layout.addWidget(self.leadership, 18, 3)

        self.tactical_performance = QComboBox()
        self.tactical_performance.addItems([p for p in self.perf_traits.keys()])
        if self.fitrep.tactical_performance is not None:
            self.tactical_performance.setCurrentIndex(self.fitrep.tactical_performance + 1)
        grid_layout.addWidget(QLabel("Tactical Performance"), 19, 0)
        grid_layout.addWidget(self.tactical_performance, 19, 1)

        self.career_rec_1 = QTextEdit(tabChangesFocus=True, lineWrapMode=QTextEdit.LineWrapMode.FixedColumnWidth)
        self.career_rec_1.setToolTip("Maximum of 20 characters and two lines.")
        self.career_rec_1.setWordWrapMode(QTextOption.WrapMode.WrapAnywhere)
        self.career_rec_1.setText(self.fitrep.career_rec_1)
        self.career_rec_1.setLineWrapColumnOrWidth(13)
        self.career_rec_1.setFont(QFont("Courier"))
        line_spacing = self.career_rec_1.fontMetrics().lineSpacing()
        self.career_rec_1.setFixedHeight(line_spacing * 2)
        # self.career_rec_1.setFixedWidth(900)
        self.career_rec_1.textChanged.connect(self.validate_career_rec1)
        grid_layout.addWidget(QLabel("Career Recommendation 1"), 20, 0)
        grid_layout.addWidget(self.career_rec_1, 20, 1)

        self.career_rec_2 = QTextEdit(tabChangesFocus=True, lineWrapMode=QTextEdit.LineWrapMode.FixedColumnWidth)
        self.career_rec_2.setToolTip("Maximum of 20 characters and two lines.")
        self.career_rec_2.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.career_rec_2.setText(self.fitrep.career_rec_2)
        self.career_rec_2.setLineWrapColumnOrWidth(13)
        self.career_rec_2.setFont(QFont("Courier"))
        line_height = self.career_rec_2.fontMetrics().lineSpacing()
        self.career_rec_2.setFixedHeight(line_height * 2)
        # self.career_rec_2.setFixedWidth(900)
        grid_layout.addWidget(QLabel("Career Recommendation 2"), 20, 2)
        grid_layout.addWidget(self.career_rec_2, 20, 3)

        self.comments = QTextEdit(tabChangesFocus=True, lineWrapMode=QTextEdit.LineWrapMode.FixedColumnWidth)
        self.comments.setText(self.fitrep.comments)
        self.comments.setPlaceholderText("Maximum of 18 lines. Excess lines will be trimmed.")
        self.comments.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.comments.setLineWrapColumnOrWidth(92)
        self.comments.setFont(QFont("Courier"))
        line_height = self.comments.fontMetrics().lineSpacing()
        self.comments.setFixedHeight(line_height * 18)
        self.comments.setFixedWidth(900)
        # self.comments.textChanged.connect(self.validate_comments)

        self.comments_label = QLabel(
            f"Comments\n\nLine Count: ({len(Fitrep.wrap_text(self.comments.toPlainText(), 92).split('\n'))}/18)"
        )
        # num_lines = len(Fitrep.format_comments(self.comments.toPlainText()).split())
        self.comments.textChanged.connect(
            lambda: self.comments_label.setText(
                f"Comments\n\nLine Count: ({len(Fitrep.wrap_text(self.comments.toPlainText(), 92).split('\n'))}/18)"
            )
        )

        grid_layout.addWidget(self.comments_label, 22, 0)
        grid_layout.addWidget(self.comments, 22, 1, 1, 3)

        self.indiv_promo_rec = QComboBox()
        self.indiv_promo_rec.addItems([k for k in self.promotion_recs.keys()])
        if self.fitrep.indiv_promo_rec is not None:
            self.indiv_promo_rec.setCurrentIndex(self.fitrep.indiv_promo_rec + 1)
        grid_layout.addWidget(QLabel("Promotion Reccomendation"), 23, 0)
        grid_layout.addWidget(self.indiv_promo_rec, 23, 1)

        self.senior_address = QTextEdit()
        self.senior_address.setText(self.fitrep.senior_address)
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

        # scroll_area.setWidget(form_widget)
        scroll_area.setWidget(container_widget)

        # Set the layout for the secondary window
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        main_layout.addWidget(button_box)

        # Set the layout for the secondary window
        self.setLayout(main_layout)

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

    def print(self):
        self.save_form()
        filename, selected_filter = QFileDialog.getSaveFileName(self, "Export FITREP PDF", "fitrep.pdf")
        if filename:
            create_fitrep_pdf(self.fitrep, Path(filename))

    def submit(self):
        self.save_form()
        self.on_accept(self.fitrep)

    def save_form(self):
        """
        Create a Fitrep class from the data input in the GUI Form.
        """
        self.fitrep.name = self.name.text()
        self.fitrep.grade = self.grade.text()
        self.fitrep.desig = self.desig.text()
        self.fitrep.ssn = self.ssn.text()
        group_text = self.group.currentText()
        self.fitrep.group = None if group_text == "" else SummaryGroup(group_text)
        self.fitrep.uic = self.uic.text()
        self.fitrep.station = self.station.text()
        self.fitrep.promotion_status = (
            None if self.promotion_status.currentText() == "" else PromotionStatus(self.promotion_status.currentText())
        )
        self.fitrep.date_reported = self.date_reported.date().toPython()
        self.fitrep.periodic = self.periodic.isChecked()
        self.fitrep.det_indiv = self.det_indiv.isChecked()
        self.fitrep.det_rs = self.det_rs.isChecked()
        self.fitrep.special = self.special.isChecked()
        self.fitrep.period_start = self.period_start.date().toPython()
        self.fitrep.period_end = self.period_end.date().toPython()
        self.fitrep.not_observed = self.not_observed.isChecked()
        self.fitrep.regular = self.regular.isChecked()
        self.fitrep.concurrent = self.concurrent.isChecked()
        self.fitrep.ops_cdr = self.ops_cdr.isChecked()

        if self.physical_readiness.currentText() == "":
            self.fitrep.physical_readiness = None
        else:
            self.fitrep.physical_readiness = PhysicalReadiness(self.physical_readiness.currentText())

        if self.billet_subcategory.currentText() == "":
            self.fitrep.billet_subcategory = None
        else:
            self.fitrep.billet_subcategory = BilletSubcategory(self.billet_subcategory.currentText())

        self.fitrep.senior_name = self.senior_name.text()
        self.fitrep.senior_grade = self.senior_grade.text()
        self.fitrep.senior_desig = self.senior_desig.text()
        self.fitrep.senior_title = self.senior_title.text()
        self.fitrep.senior_uic = self.senior_uic.text()
        self.fitrep.senior_ssn = self.senior_ssn.text()
        self.fitrep.duties_abbreviation = self.duties_abbreviation.text()
        self.fitrep.duties_description = self.duties_description.text()
        self.fitrep.job = self.job.toPlainText()
        self.fitrep.date_counseled = self.date_counseled.date().toPython()
        self.fitrep.counselor = self.counselor.text()
        self.fitrep.pro_expertise = self.perf_traits[self.pro_expertise.currentText()]
        self.fitrep.cmd_climate = self.perf_traits[self.cmd_climate.currentText()]
        self.fitrep.bearing_and_character = self.perf_traits[self.bearing_and_character.currentText()]
        self.fitrep.teamwork = self.perf_traits[self.teamwork.currentText()]
        self.fitrep.accomp_and_initiative = self.perf_traits[self.accomp_and_initiative.currentText()]
        self.fitrep.leadership = self.perf_traits[self.leadership.currentText()]
        self.fitrep.tactical_performance = self.perf_traits[self.tactical_performance.currentText()]
        self.fitrep.career_rec_1 = Fitrep.validate_career_rec(self.career_rec_1.toPlainText())
        self.fitrep.career_rec_2 = self.career_rec_2.toPlainText()
        self.fitrep.comments = Fitrep.validate_comments(self.comments.toPlainText())
        self.fitrep.indiv_promo_rec = self.promotion_recs[self.indiv_promo_rec.currentText()]
        self.fitrep.senior_address = self.senior_address.toPlainText()

        # try:
        #     Fitrep.model_validate(self.fitrep.model_dump())
        # except ValidationError as err:
        #     print(err.json())
