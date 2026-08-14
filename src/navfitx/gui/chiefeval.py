from typing import Callable

from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLayout, QMainWindow

from navfitx.models import ChiefEval

from .report import BaseReportForm


class ChiefEvalForm(BaseReportForm[ChiefEval]):
    window_title = "Chief Evaluation"
    pdf_default_name = "chiefeval.pdf"

    def __init__(
        self,
        main: QMainWindow,
        on_accept: Callable[[ChiefEval], None],
        on_reject: Callable[[], None],
        report: ChiefEval,
    ):
        super().__init__(main=main, on_accept=on_accept, on_reject=on_reject, report=report)

        self.det_rs = QCheckBox("Detachment of Reporting Senior")
        self.det_rs.setChecked(self.report.det_rs)
        occasion_layout = self.occasion_box.layout()
        assert isinstance(occasion_layout, QHBoxLayout)
        occasion_layout.insertWidget(2, self.det_rs)

        type_layout = self.type_box.layout()
        assert isinstance(type_layout, QLayout)
        self.ops_cdr = QCheckBox("OpsCdr")
        self.ops_cdr.setChecked(self.report.ops_cdr)
        type_layout.addWidget(self.ops_cdr)

        self.add_label("Technical Mastery", 16, 0)
        self.add_label("Institutional Expertise", 16, 2)
        self.add_label("Professionalism", 17, 0)
        self.add_label("Integrity", 17, 2)
        self.add_label("Accountability", 18, 0)
        self.add_label("Leadership", 18, 2)
        self.add_label("Teamwork", 19, 0)

    def save_form(self) -> None:
        super().save_form()
        self.report.det_rs = self.det_rs.isChecked()
        self.report.ops_cdr = self.ops_cdr.isChecked()
