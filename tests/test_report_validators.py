# ty: ignore
import re

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


def test_desig_validation(fitrep: Fitrep):
    # Surprisingly, the NAVFIT98 v30 User guide says speical chars are ok
    # validate min desig length
    fitrep.desig = ""
    with pytest.raises(ValidationError, match="desig"):
        Fitrep.model_validate(fitrep)

    # validate max desig length
    fitrep.desig = "a" * 13
    with pytest.raises(ValidationError, match="desig"):
        Fitrep.model_validate(fitrep)

    fitrep.desig = "a" * 12
    Fitrep.model_validate(fitrep)


def test_ssn_validation(fitrep: Fitrep):
    # ensure SSN matches the regex pattern xxx-xx-xxxx
    assert bool(re.fullmatch(r"\d{3}-\d{2}-\d{4}", fitrep.ssn))

    fitrep.ssn = "123456789"
    with pytest.raises(ValidationError, match="ssn"):
        Fitrep.model_validate(fitrep)

    fitrep.ssn = ""
    with pytest.raises(ValidationError, match="ssn"):
        Fitrep.model_validate(fitrep)


def test_group_validation(fitrep: Fitrep):
    # ensure group is a valid DutyStatus enum value
    fitrep.group = "INVALID_GROUP"
    with pytest.raises(ValidationError, match="group"):
        Fitrep.model_validate(fitrep)

    fitrep.group = None
    with pytest.raises(ValidationError, match="group"):
        Fitrep.model_validate(fitrep)


def test_uic_validation(fitrep: Fitrep):
    # ensure UIC is not empty and has a max length of 5
    fitrep.uic = ""
    with pytest.raises(ValidationError, match="uic"):
        Fitrep.model_validate(fitrep)

    # Too long
    fitrep.uic = "123456"
    with pytest.raises(ValidationError, match="uic"):
        Fitrep.model_validate(fitrep)

    # only alphanumeric characters
    fitrep.uic = "1234!"
    with pytest.raises(ValidationError, match="uic"):
        Fitrep.model_validate(fitrep)


def test_ship_station_validation(fitrep: Fitrep):
    # possible to have non-alphanumeric characters; eg: CG-47 TICONDEROGA
    # ensure station is not empty and has a max length of 18
    fitrep.station = ""
    with pytest.raises(ValidationError, match="station"):
        Fitrep.model_validate(fitrep)

    fitrep.station = "a" * 19
    with pytest.raises(ValidationError, match="station"):
        Fitrep.model_validate(fitrep)

    fitrep.station = "a" * 18
    Fitrep.model_validate(fitrep)


def test_promotion_status_validation(fitrep: Fitrep):
    # ensure promotion_status is a valid PromotionStatus enum value
    fitrep.promotion_status = "INVALID_STATUS"
    with pytest.raises(ValidationError, match="promotion_status"):
        Fitrep.model_validate(fitrep)

    fitrep.promotion_status = None
    with pytest.raises(ValidationError, match="promotion_status"):
        Fitrep.model_validate(fitrep)


def test_date_reported_validation(fitrep: Fitrep):
    fitrep.date_reported = None
    with pytest.raises(ValidationError, match="Report date must be set"):
        Fitrep.model_validate(fitrep)


def test_periodic_validation(fitrep: Fitrep):
    fitrep.periodic = None
    with pytest.raises(ValidationError, match="periodic"):
        Fitrep.model_validate(fitrep)


def test_career_rec_1_validation(fitrep: Fitrep):
    # both career recs should be blank if report is not observed
    fitrep.career_rec_1 = ""
    fitrep.career_rec_2 = ""
    fitrep.not_observed = False
    Fitrep.model_validate(fitrep)

    fitrep.career_rec_1 = "a" * 20
    Fitrep.model_validate(fitrep)

    fitrep.career_rec_1 = "a" * 21
    with pytest.raises(ValidationError, match="career_rec_1"):
        Fitrep.model_validate(fitrep)

    fitrep.not_observed = True
    fitrep.career_rec_1 = "recommendation"
    # mark fitrep traits as NOB, else traits will fail validation
    fitrep.trait1 = 0
    fitrep.trait2 = 0
    fitrep.trait3 = 0
    fitrep.trait4 = 0
    fitrep.trait5 = 0
    fitrep.trait6 = 0
    fitrep.trait7 = 0
    with pytest.raises(ValidationError, match="Career Recommendations should be blank if 'Not Observed' is checked"):
        Fitrep.model_validate(fitrep)

    # TODO: validate the formatted career rec is not more than 2 lines
