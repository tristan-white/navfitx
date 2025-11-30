import re
from datetime import date
from enum import Enum, StrEnum, auto

from pydantic import field_validator
from sqlmodel import Field, SQLModel


class Report(SQLModel, table=True):
    """
    A model for the Reports table in NAVFIT98A Access database.

    Args:
        report_id (int): Primary key for Reports database table.
        parent
    """

    report_id: int = Field(primary_key=True)
    parent: str
    report_type: str
    full_name: str
    first_name: str
    mi: str
    last_name: str
    suffix: str
    rate: str
    desig: str
    ssn: str
    active: bool
    tar: bool
    inactive: bool
    atadsw: bool
    uic: str
    ship_station: str
    promotion_status: str
    date_reported: date
    periodic: bool
    det_ind: bool
    frocking: bool
    special: bool
    from_date: date
    to_date: date
    nob: bool
    regular: bool
    concurrent: bool
    ops_cdr: bool
    physical_readiness: str
    physical_readiness2: str
    physical_readiness_dt: date
    billet_subcat: str
    rs_last_name: str
    rs_fi: str
    rs_mi: str
    reporting_senior: str
    rs_grade: str
    rs_desig: str
    rs_title: str
    rs_uic: str
    rs_ssn: str
    achievements: str
    primary_duty: str
    duties: str
    date_counseled: date
    counselor: str
    counselor_ln: str
    counselor_fi: str
    counselor_mi: str
    prof: int
    prof_dn1: str
    prof_dn2: str
    prof_dn3: str
    qual: int
    qual_dn1: str
    qual_dn2: str
    qual_dn3: str
    eo: int
    eo_dn1: str
    eo_dn2: str
    eo_dn3: str
    mil: int
    mil_dn1: str
    mil_dn2: str
    mil_dn3: str
    pa: int
    pa_dn1: str
    pa_dn2: str
    pa_dn3: str
    team: int
    team_dn1: str
    team_dn2: str
    team_dn3: str
    lead: int
    lead_dn1: str
    lead_dn2: str
    lead_dn3: str
    mis: int
    mis_dn1: str
    mis_dn2: str
    mis_dn3: str
    tac: int
    tac_dn1: str
    tac_dn2: str
    tac_dn3: str
    recommend_1: str
    recommend_2: str
    rater: str
    rater_date: date
    comments_pitch: str
    comments: str
    qualifications: str
    promotion_recom: int
    summary_rank: int
    summary_sp: str
    summary_prog: str
    summary_prom: str
    summary_mp: str
    summary_ep: str
    retention_yes: bool
    retention_no: bool
    rsca: int
    rs_address: str
    rs_address1: str
    rs_address2: str
    rs_city: str
    rs_state: str
    rs_zip_cd: str
    rs_phone: str
    rs_dsn: str
    senior_rater: str
    senior_rater_date: date
    statement_yes: bool
    statement_no: bool
    rs_info: str
    rrs_fi: str
    rrs_mi: str
    rrs_last_name: str
    rrs_grade: str
    rrs_command: str
    rrs_uic: str
    user_comments: str
    psswrd: str
    standards: str
    is_validated: str


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


class PromotionRecommendation(Enum):
    NOB = auto()
    SIGNIFICANT_PROBLEMS = auto()
    PROGRESSING = auto()
    PROMOTABLE = auto()
    MUST_PROMOTE = auto()
    EARLY_PROMOTE = auto()


class Fitrep(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = ""
    grade: str = ""
    desig: str = ""
    ssn: str = ""
    group: SummaryGroup | None = None
    uic: str = ""
    station: str = ""
    promotion_status: PromotionStatus | None = None
    date_reported: date | None = None
    occasion_for_report: OccasionForReport | None = None
    period_start: date | None = None
    period_end: date | None = None
    not_observed: bool = False
    type_of_report: int | None = None
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
    pro_expertise: int | None = None
    cmd_climate: int | None = None
    bearing_and_character: int | None = None
    teamwork: int | None = None
    accomp_and_initiative: int | None = None
    leadership: int | None = None
    tactical_performance: int | None = None
    career_rec_1: str = ""
    career_rec_2: str = ""
    comments: str = ""
    indiv_promo_rec: PromotionRecommendation | None = None
    # summary_promo_rec: int = Field(default_factory=list)
    senior_address: str = ""

    @classmethod
    @field_validator("name")
    def validate_name(cls, name: str) -> str:
        if len(name) > 27:
            raise ValueError("Name must be 27 characters or less")
        return name.upper()

    @classmethod
    @field_validator("grade")
    def validate_grade(cls, grade: str) -> str:
        if len(grade) > 5:
            raise ValueError("Rate must be 5 characters or less")
        return grade

    @classmethod
    @field_validator("desig")
    def validate_desig(cls, desig: str) -> str:
        if len(desig) > 12:
            raise ValueError("Designator must be 12 characters or less")
        return desig.upper()

    @classmethod
    @field_validator("ssn")
    def validate_ssn(cls, ssn: str) -> str:
        ssn = ssn.strip()
        ssn_pattern = re.compile(r"^\d{3}-\d{2}-\d{4}$")
        if not ssn_pattern.match(ssn):
            raise ValueError("SSN must be in the format XXX-XX-XXXX")
        return ssn

    @classmethod
    @field_validator("group")
    def validate_group(cls, group: SummaryGroup | None) -> SummaryGroup:
        if group is None:
            raise ValueError("Summary Group must be specified.")
        return group

    @classmethod
    @field_validator("uic")
    def validate_uic(cls, uic: str) -> str:
        if len(uic) > 5:
            raise ValueError("UIC must be 5 characters or less.")
        if not uic.isalnum():
            raise ValueError("UIC must be alphanumeric.")
        return uic.upper()

    @classmethod
    @field_validator("station")
    def validate_station(cls, station: str) -> str:
        if len(station) > 18:
            raise ValueError("Station must be 18 characters or less.")
        return station

    @classmethod
    @field_validator("promotion_status")
    def validate_promotion_status(cls, promotion_status: PromotionStatus | None) -> PromotionStatus:
        if promotion_status is None:
            raise ValueError("Promotion Status must be specified.")
        return promotion_status

    @classmethod
    @field_validator("occasion_for_report")
    def validate_occasion_for_report(cls, occasion_for_report: int | None) -> int:
        if occasion_for_report is None:
            raise ValueError("Occasion for Report must be specified.")
        return occasion_for_report

    @classmethod
    @field_validator("billet_subcategory")
    def validate_billet_subcategory(cls, billet_subcategory: BilletSubcategory | None) -> BilletSubcategory:
        if billet_subcategory is None:
            raise ValueError("Billet Subcategory must be specified.")
        return billet_subcategory

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
            if trait:
                observed += 1
                total += trait
        if observed != 0:
            avg = total / observed
            return f"{avg:.2f}"
        return "0.00"

    def summary_group_avg(self) -> str:
        return "0.00"

    def generate_report(self) -> Report:
        return Report(
            report_type="FitRep",
            full_name=self.name,
            desig=self.desig,
            ssn=self.ssn,
            uic=self.uic,
            ship_station=self.station,
            from_date=self.period_start,
            to_date=self.period_end,
            reporting_senior=self.senior_name,
            rs_grade=self.senior_grade,
            rs_desig=self.senior_desig,
            rs_title=self.senior_title,
            rs_uic=self.senior_uic,
            rs_ssn=self.senior_ssn,
            billet_subcat=self.billet_subcategory,
            date_counseled=self.date_counseled,
            counselor=self.counselor,
        )
