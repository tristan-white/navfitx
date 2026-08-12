import pytest

from navfitx.examples import build_validated_example_fitrep
from navfitx.models import (
    BilletSubcategory,
    ChiefEval,
    Eval,
    Fitrep,
    PromotionStatus,
)


@pytest.fixture()
def fitrep() -> Fitrep:
    return build_validated_example_fitrep()


@pytest.fixture()
def eval():
    """Returns a valid mock Eval"""
    return Eval(
        name="John Doe",
        rate="YN1",
        desig="SW/AW",
        ssn="123-45-6789",
        uic="12345",
        station="NAVSTA Norfolk",
        promotion_status=PromotionStatus.REGULAR,
        date_reported=None,
        period_start=None,
        period_end=None,
        not_observed=False,
        physical_readiness="P",
        billet_subcategory=BilletSubcategory.BASIC,
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


@pytest.fixture()
def chiefeval():
    """Returns a valid mock ChiefEval"""
    return ChiefEval(
        name="John Doe",
        rate="CWTC",
        desig="USN",
        ssn="123-45-6789",
        uic="12345",
        station="NAVSTA Norfolk",
        promotion_status=PromotionStatus.REGULAR,
        date_reported=None,
        period_start=None,
        period_end=None,
        not_observed=False,
        physical_readiness="P",
        billet_subcategory=BilletSubcategory.BASIC,
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
