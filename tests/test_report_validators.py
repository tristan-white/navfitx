import pytest
from pydantic import ValidationError

from navfitx.models import (
    Fitrep,
)


def test_valid_fitrep(fitrep):
    # Should not raise any exceptions
    Fitrep.model_validate(fitrep)


def test_create_blank_fitrep():
    """
    Reports should be able to be created without error even if they don't pass validation.
    This allows users to save incomplete reports.
    """
    Fitrep()


def test_name_too_short(fitrep: Fitrep):
    with pytest.raises(ValidationError, match="name"):
        fitrep.name = ""
        Fitrep.model_validate(fitrep)


def test_name_too_long(fitrep: Fitrep):
    with pytest.raises(ValidationError, match="name"):
        fitrep.name = "a" * 28
        Fitrep.model_validate(fitrep)
