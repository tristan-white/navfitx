from datetime import date

import pytest

from navfitx.models import (
    BilletSubcategory,
    Eval,
    Fitrep,
    PhysicalReadiness,
    PromotionStatus,
    SummaryGroup,
)


@pytest.fixture()
def fitrep():
    return Fitrep(
        id=1,
        name="JONES, JOHN P",
        rate="LTJG",
        desig="1840",
        ssn="000-00-0000",
        group=SummaryGroup.ACT,
        uic="12345",
        station="NAVPERSCOM",
        promotion_status=PromotionStatus.REGULAR,
        date_reported=date(2022, 9, 22),
        period_start=date(2024, 5, 27),
        period_end=date(2025, 2, 28),
        not_observed=False,
        regular=True,
        physical_readiness=PhysicalReadiness.PASS,
        billet_subcategory=BilletSubcategory.NA,
        senior_name="HOPPER, G",
        senior_grade="CAPT",
        senior_desig="1840",
        senior_title="CO",
        senior_uic="12345",
        senior_ssn="000-00-0000",
        job="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus id mattis elit. Aliquam et sem bibendum, laoreet risus eget, malesuada nisl. Praesent gravida leo cursus velit mattis eleifend. Sed interdum lacinia efficitur. Sed elementum gravida at.",
        duties_abbreviation="EXAMPLE",
        duties_description="Responsible for the overall command and operation of the ship.",
        date_counseled=date(2024, 8, 14),
        counselor="NIMITZ, C",
        career_rec_1="Lorem ipsum egestas",
        career_rec_2="Lorem ipsum egestas",
        pro_expertise=3,
        cmd_climate=3,
        bearing_and_character=3,
        teamwork=3,
        accomp_and_initiative=3,
        leadership=3,
        tactical_performance=3,
        comments="Lorem ipsum dolor sit amet, consectetur adipiscing elit. In rhoncus enim quis magna vestibulum sagittis. Aenean ut pretium libero. Quisque maximus risus vitae ligula mollis viverra. Nullam auctor justo diam, eu porta tellus egestas sit amet. Vivamus et elit non mi imperdiet sodales nec id tellus. Cras sodales scelerisque massa, vel pulvinar erat. Donec molestie augue diam, sed consequat sem vulputate vel. Mauris luctus mi eu tellus tempus, non scelerisque libero imperdiet. Integer facilisis velit ac ligula scelerisque, eu dignissim magna cursus. Vivamus nec libero eget urna congue egestas et id est. Nunc tincidunt lorem erat, ut aliquam magna vulputate eu.  Sed dapibus, augue eget blandit accumsan, velit diam consequat enim, eget rhoncus lorem erat in neque. Nam lobortis volutpat congue. Morbi urna nisl, tincidunt non metus sed, ornare bibendum lectus. Etiam consequat malesuada ligula, eu luctus felis ullamcorper a. Praesent massa massa, cursus non mauris in, finibus porta metus. Integer gravida et risus ac scelerisque. Mauris ut tellus efficitur nunc gravida pharetra. Phasellus vitae nisi vitae tellus mollis consequat tincidunt semper risus. Vivamus nec nulla vitae nunc tristique ornare.  Nulla facilisi. Phasellus nisl sem, imperdiet eget hendrerit elementum, semper quis justo. Mauris at purus hendrerit, molestie orci ut, maximus est. Praesent congue tincidunt sapien, vitae egestas neque auctor sed. Curabitur feugiat orci lorem, a fringilla leo fringilla malesuada. Praesent mattis ornare magna, id consectetur massa. Etiam consectetur lorem eu pellentesque sollicitudin. Proin dapibus leo eu justo.",
        indiv_promo_rec=3,
        senior_address="123 Main St, Anytown, USA",
    )


@pytest.fixture()
def eval():
    return Eval(
        name="John Doe",
        rate="E-2",
        desig="USN",
        ssn="123-45-6789",
        uic="12345",
        station="NAVSTA Norfolk",
        promotion_status=PromotionStatus.REGULAR,
        date_reported=None,
        period_start=None,
        period_end=None,
        not_observed=False,
        physical_readiness=PhysicalReadiness.PASS,
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
