import pytest
from pydantic import ValidationError

from navfitx.models import (
    Eval,
    Fitrep,
)


def test_valid_fitrep(valid_fitrep):
    # Should not raise any exceptions
    Fitrep.model_validate(valid_fitrep)


def test_create_blank_reports():
    """
    Reports should be able to be created without error even if they don't pass validation.
    This allows users to save incomplete reports.
    """
    Fitrep()
    Eval()


def test_validate_name():
    with pytest.raises(ValidationError, match="name"):
        fitrep = Fitrep()
        Fitrep.model_validate(fitrep)
