from datetime import date

import pytest

from navfitx.examples import build_validated_example_fitrep
from navfitx.models import (
    BilletSubcategory,
    ChiefEval,
    DutyStatus,
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


@pytest.fixture()
def validated_chiefeval() -> ChiefEval:
    return ChiefEval(
        name="DOE, JANE A",
        rate="CWTC",
        desig="1110",
        ssn="123-45-6789",
        group=DutyStatus.ACT,
        uic="12345",
        station="NAVPERSCOM",
        promotion_status=PromotionStatus.REGULAR,
        date_reported=date(2024, 5, 15),
        periodic=True,
        det_indiv=False,
        det_rs=False,
        special=False,
        period_start=date(2024, 6, 1),
        period_end=date(2024, 12, 31),
        not_observed=False,
        regular=True,
        concurrent=False,
        ops_cdr=False,
        physical_readiness="P",
        billet_subcategory=BilletSubcategory.BASIC,
        senior_name="SMITH, JOHN Q",
        senior_grade="CAPT",
        senior_desig="1110",
        senior_title="CO",
        senior_uic="12345",
        senior_ssn="987-65-4321",
        job="Leads command-level mission execution and mentoring for chief mess responsibilities.",
        duties_abbreviation="CMC",
        duties_description="Serves as command senior enlisted advisor across mission and readiness functions.",
        date_counseled=date(2024, 7, 1),
        counselor="SMITH, J",
        trait1=3,
        trait2=3,
        trait3=3,
        trait4=3,
        trait5=3,
        trait6=3,
        trait7=3,
        career_rec_1="",
        career_rec_2="",
        comments="Strong chief with sustained impact on readiness and team performance.",
        indiv_promo_rec=3,
        senior_address="123 Fleet St, Norfolk VA",
    )
