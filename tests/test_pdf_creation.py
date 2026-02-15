from pathlib import Path

import pytest

from navfitx.models import Eval, Fitrep

fitrep = Fitrep(
    name="John Doe",
    grade="O-3",
    desig="USN",
    ssn="123-45-6789",
    uic="12345",
    station="NAVSTA Norfolk",
    promotion_status="Promotable",
    date_reported=None,
    period_start=None,
    period_end=None,
    not_observed=False,
    physical_readiness="P2",
    billet_subcategory="Subcategory A",
    senior_name="Jane Smith",
    senior_grade="O-4",
    senior_desig="USN",
    senior_title="Senior Officer",
    senior_uic="54321",
    senior_ssn="987-65-4321",
    job="Commanding Officer of a destroyer.",
    duties_abbreviation="CO Duties",
    duties_description="Responsible for the overall command and operation of the ship.",
)

eval = Eval(
    name="John Doe",
    grade="O-3",
    desig="USN",
    ssn="123-45-6789",
    uic="12345",
    station="NAVSTA Norfolk",
    promotion_status="Promotable",
    date_reported=None,
    period_start=None,
    period_end=None,
    not_observed=False,
    physical_readiness="P2",
    billet_subcategory="Subcategory A",
    senior_name="Jane Smith",
    senior_grade="O-4",
    senior_desig="USN",
    senior_title="Senior Officer",
    senior_uic="54321",
    senior_ssn="987-65-4321",
    job="Commanding Officer of a destroyer.",
    duties_abbreviation="CO Duties",
    duties_description="Responsible for the overall command and operation of the ship.",
)


def test_fitrep_pdf_creation(tmp_path: Path):
    """
    Test that the PDF creation process completes without errors.
    """
    try:
        # TODO: Ensure mock FITREP a valid FITREP
        fitrep.create_pdf(tmp_path / "fitrep.pdf")
    except Exception as e:
        pytest.fail(f"PDF creation failed with error: {e}")


def test_eval_pdf_creation(tmp_path: Path):
    """
    Test that the PDF creation process for evals completes without errors.
    """
    try:
        # TODO: Ensure mock EVAL a valid EVAL
        eval.create_pdf(tmp_path / "eval.pdf")
    except Exception as e:
        pytest.fail(f"PDF creation failed with error: {e}")
