from datetime import date
from enum import Enum, StrEnum, auto

# from pydantic import BaseModel, Field
from sqlmodel import Field, SQLModel


class SummaryGroup(Enum):
    ACT = auto()
    TAR = auto()
    INACT = auto()
    AT_ADOS = auto()


class PromotionStatus(StrEnum):
    REGULAR = "REGULAR"
    FROCKED = "FROCKED"
    SELECTED = "SELECTED"
    SPOT = "SPOT"


class OccasionForReport(Enum):
    PERIODIC = auto()
    INDIVIDUAL_DETACH = auto()
    SENIOR_DETACH = auto()
    SPECIAL = auto()


class TypeOfReport(Enum):
    REGULAR = auto()
    CONCURRENT = auto()
    OpsCdr = auto()


class PhysicalReadiness(StrEnum):
    PASS = "P"
    BCA_PASS = "B"
    FAIL = "F"
    MED_WAIVED = "M"
    WAIVED = "W"
    NO_PFA = "N"


class BilletSubcategory(StrEnum):
    NA = "NA"
    BASIC = "BASIC"
    APPROVED = "APPROVED"
    INDIV_AUGMENT = "INDIV AUG"
    CO_AFLOAT = "CO AFLOAT"
    CO_ASHORE = "CO ASHORE"
    OIC = "OIC"
    SEA_COMP = "SEA COMP"
    CRF = "CRF"
    CANVASSER = "CANVASSER"
    RESIDENT = "RESIDENT"
    INTERN = "INTERN"
    INSTRUCTOR = "INSTRUCTOR"
    STUDENT = "STUDENT"
    RESAC1 = "RESAC1"
    RESAC6 = "RESAC6"
    SCREENED = "SCREENED"
    SPECIAL01 = "SPECIAL01"
    SPECIAL02 = "SPECIAL02"
    SPECIAL03 = "SPECIAL03"
    SPECIAL04 = "SPECIAL04"
    SPECIAL05 = "SPECIAL05"
    SPECIAL06 = "SPECIAL06"
    SPECIAL07 = "SPECIAL07"
    SPECIAL08 = "SPECIAL08"
    SPECIAL09 = "SPECIAL09"
    SPECIAL10 = "SPECIAL10"
    SPECIAL11 = "SPECIAL11"
    SPECIAL12 = "SPECIAL12"
    SPECIAL13 = "SPECIAL13"
    SPECIAL14 = "SPECIAL14"
    SPECIAL15 = "SPECIAL15"
    SPECIAL16 = "SPECIAL16"
    SPECIAL17 = "SPECIAL17"
    SPECIAL18 = "SPECIAL18"
    SPECIAL19 = "SPECIAL19"
    SPECIAL20 = "SPECIAL20"


class PerformanceTrait(Enum):
    NOB = 0
    BELOW_STANDARDS = 1
    PROGRESSING = 2
    MEETS_STANDARDS = 3
    ABOVE = 4
    GREATLY_EXCEEDS = 5


class PromotionRecommendation(Enum):
    NOB = auto()
    SIGNIFICANT_PROBLEMS = auto()
    PROGRESSING = auto()
    PROMOTABLE = auto()
    MUST_PROMOTE = auto()
    EARLY_PROMOTE = auto()


class Fitrep(SQLModel):
    name: str = ""
    rate: str = ""
    desig: str = ""
    ssn: str = ""
    group: SummaryGroup | None = None
    uic: str = ""
    station: str = ""
    promotion_status: PromotionStatus | None = None
    date_reported: date | None = None
    occasion_for_report: set[OccasionForReport] = Field(default_factory=set)
    period_start: date | None = None
    period_end: date | None = None
    not_observed: bool = False
    type_of_report: set[TypeOfReport] = Field(default_factory=set)
    physical_readiness: PhysicalReadiness | None = None
    billet_subcategory: BilletSubcategory | None = None
    senior_name: str = ""
    senior_grade: str = ""
    senior_desig: str = ""
    senior_title: str = ""
    senior_uic: str = ""
    senior_ssn: str = ""
    job: str = ""
    duties_abbreviation: str = ""
    duties_description: str = ""
    date_counseled: date | None = None
    counselor: str = ""
    pro_expertise: PerformanceTrait | None = None
    cmd_climate: PerformanceTrait | None = None
    bearing_and_character: PerformanceTrait | None = None
    teamwork: PerformanceTrait | None = None
    accomp_and_initiative: PerformanceTrait | None = None
    leadership: PerformanceTrait | None = None
    tactical_performance: PerformanceTrait | None = None
    career_rec_1: str = ""
    career_rec_2: str = ""
    comments: str = ""
    indiv_promo_rec: PromotionRecommendation | None = None
    summary_promo_rec: list[int] = Field(default_factory=list)
    senior_address: str = ""

    def member_trait_avg(self) -> str:
        traits = [
            self.pro_expertise,
            self.cmd_climate,
            self.bearing_and_character,
            self.teamwork,
            self.accomp_and_initiative,
            self.leadership,
            self.tactical_performance,
        ]
        observed = 0
        total = 0
        for trait in traits:
            if trait is not PerformanceTrait.NOB:
                observed += 1
                total += trait.value
        if observed != 0:
            avg = total / observed
            return f"{avg:.2f}"
        return "0.00"
