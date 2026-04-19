import pytest
from pydantic import ValidationError

from navfitx.models import (
    Fitrep,
)


def test_valid_fitrep(fitrep):
    # Should not raise any exceptions
    Fitrep.model_validate(fitrep)


def test_create_blank_fitrep(tmp_path):
    """
    Reports should be able to be created without error even if they don't pass validation.
    This allows users to save incomplete reports.
    """
    Fitrep().create_pdf(tmp_path / "blank_report.pdf")


def test_name_validation(fitrep: Fitrep):
    with pytest.raises(ValidationError, match="name"):
        fitrep.name = ""
        Fitrep.model_validate(fitrep)

    with pytest.raises(ValidationError, match="name"):
        fitrep.name = "a" * 28
        Fitrep.model_validate(fitrep)


def test_rate_validation(fitrep: Fitrep):
    # validate min rate length
    with pytest.raises(ValidationError, match="rate"):
        fitrep.rate = ""
        Fitrep.model_validate(fitrep)

    # validate max rate length
    with pytest.raises(ValidationError, match="rate"):
        fitrep.rate = "a" * 6
        Fitrep.model_validate(fitrep)
