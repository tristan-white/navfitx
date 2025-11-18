from PySide6.QtGui import QValidator
from PySide6.QtWidgets import QComboBox, QDateEdit, QDialog, QFormLayout, QLineEdit, QTextEdit, QWidget

from navfitx.models import PromotionStatus


class NameValidator(QValidator):
    def __init__(self, parent=None):
        super().__init__(parent)

    def validate(self, input_str: str, pos: int):
        for char in input_str:
            if char != char.upper():
                return QValidator.State.Invalid, input_str, pos
        return QValidator.State.Acceptable, input_str, pos

    def fixup(self, input_str: str) -> str:
        return input_str.upper()


class FitrepDialog(QDialog):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setWindowTitle("FITREP Data Entry")

        self.name = QLineEdit()
        self.name.setValidator(NameValidator())

        self.rank = QLineEdit()

        self.desig = QLineEdit()

        self.ssn = QLineEdit()

        self.group = QComboBox()
        self.group.addItems(["ACT", "TAR", "INACT", "AT/ADSW/265"])

        self.uic = QLineEdit()

        self.station = QLineEdit()

        self.promotion_status = QComboBox()
        self.promotion_status.addItems([member.value for member in PromotionStatus])

        self.date_reported = QDateEdit()

        self.comments = QTextEdit()
        self.comments.setLineWrapMode(QTextEdit.LineWrapMode.FixedColumnWidth)
        self.comments.setLineWrapColumnOrWidth(91)

        form_layout = QFormLayout(self)

        form_layout.addRow("Name", self.name)
        form_layout.addRow("Rate", QLineEdit())
        form_layout.addRow("Designator", QLineEdit())
        form_layout.addRow("SSN", QLineEdit())
        form_layout.addRow("Group", QLineEdit())
        form_layout.addRow("UIC", QLineEdit())
        form_layout.addRow("Ship/Station", QLineEdit())
        form_layout.addRow("Promotion Status", QLineEdit())
        form_layout.addRow("Date Reported (mm/dd/yy)", QDateEdit())
        form_layout.addRow("Comments", self.comments)

    def print(self):
        print(type(self.comments))
        print(self.comments.toPlainText())
