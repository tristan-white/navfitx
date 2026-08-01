from pathlib import Path

import pymupdf
import pytest

from navfitx.models import ChiefEval, Eval, Fitrep


def test_blank_fitrep_pdf_creation(tmp_path: Path):
    """
    Test that the PDF creation process completes without errors.
    """
    fitrep = Fitrep()
    fitrep.create_pdf(tmp_path / "fitrep.pdf")


def test_mock_fitrep_pdf_creation(fitrep: Fitrep, tmp_path: Path):
    fitrep.create_pdf(tmp_path / "fitrep.pdf")


def test_blank_eval_pdf_creation(tmp_path: Path):
    """
    Test that the PDF creation process for evals completes without errors.
    """
    eval = Eval()
    pdf_path = tmp_path / "eval.pdf"
    eval.create_pdf(pdf_path)


def test_mock_eval_pdf_creation(eval: Eval, tmp_path: Path):
    pdf_path = tmp_path / "eval.pdf"
    eval.create_pdf(pdf_path)
    # downloads_path = Path.home() / "Downloads" / "eval.pdf"
    # shutil.copy(pdf_path, downloads_path)
    # webbrowser.open(downloads_path.as_uri())


def test_blank_chiefeval_pdf_creation(tmp_path: Path):
    """
    Test that the PDF creation process for chief evals completes without errors.
    """
    chiefeval = ChiefEval()
    chiefeval.create_pdf(tmp_path / "chiefeval.pdf")


def test_mock_chiefeval_pdf_creation(chiefeval: ChiefEval, tmp_path: Path):
    pdf_path = tmp_path / "chiefeval.pdf"
    chiefeval.create_pdf(pdf_path)
    # downloads_path = Path.home() / "Downloads" / "chiefeval.pdf"
    # shutil.copy(pdf_path, Path.home() / "Downloads" / "chiefeval.pdf")
    # webbrowser.open(downloads_path.as_uri())


@pytest.mark.parametrize(
    ("report_cls", "doc_type", "filename"),
    [
        (Fitrep, "FITREP", "fitrep.pdf"),
        (Eval, "EVAL", "eval.pdf"),
        (ChiefEval, "CHIEFEVAL", "chiefeval.pdf"),
    ],
)
def test_pdf_metadata_title(report_cls, doc_type: str, filename: str, tmp_path: Path):
    report = report_cls(name="TEST")
    pdf_path = tmp_path / filename
    report.create_pdf(pdf_path)
    doc = pymupdf.open(str(pdf_path))
    try:
        assert doc.metadata.get("title") == f"{doc_type} for TEST"
    finally:
        doc.close()
