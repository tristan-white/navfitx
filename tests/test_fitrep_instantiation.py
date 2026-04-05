from datetime import date

from navfitx.models import (
    BilletSubcategory,
    Fitrep,
    PhysicalReadiness,
    PromotionStatus,
    SummaryGroup,
)


def test_fitrep_instantiation():
    """Fully instantiate a Fitrep model with valid values."""
    fitrep = Fitrep(
        id=1,
        name="Jane Doe",
        rate="E-5",
        desig="USN",
        ssn="111-22-3333",
        group=SummaryGroup.ACT,
        uic="12345",
        station="NAVSTA Norfolk",
        promotion_status=PromotionStatus.REGULAR,
        date_reported=date(2024, 1, 1),
        period_start=date(2024, 1, 1),
        period_end=date(2024, 12, 31),
        not_observed=False,
        regular=True,
        concurrent=False,
        billet_subcategory=BilletSubcategory.BASIC,
        senior_name="John Smith",
        senior_grade="O-5",
        senior_desig="USN",
        senior_title="CO",
        senior_uic="54321",
        senior_ssn="999-88-7777",
        job="Test job",
        duties_abbreviation="Lead",
        duties_description="Testing duties description.",
        date_counseled=date(2024, 6, 1),
        counselor="Counselor Name",
        career_rec_1="Career1",
        career_rec_2="Career2",
        comments="No comments.",
        indiv_promo_rec=3,
        senior_address="123 Navy Way",
        det_rs=False,
        ops_cdr=False,
        physical_readiness=PhysicalReadiness.PASS,
        pro_expertise=3,
        cmd_climate=3,
        bearing_and_character=3,
        teamwork=3,
        accomp_and_initiative=3,
        leadership=3,
        tactical_performance=3,
    )

    Fitrep.model_validate(fitrep)

    assert isinstance(fitrep, Fitrep)
    assert fitrep.doc_type == "fitrep"
    assert fitrep.name == "Jane Doe"
