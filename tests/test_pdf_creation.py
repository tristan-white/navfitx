from pathlib import Path

from navfitx.models import Eval, Fitrep


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
    eval.create_pdf(tmp_path / "eval.pdf")


def test_mock_eval_pdf_creation(eval: Eval, tmp_path: Path):
    eval.create_pdf(tmp_path / "eval.pdf")
