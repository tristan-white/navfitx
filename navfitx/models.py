import textwrap
from datetime import date
from enum import Enum, StrEnum
from typing import Annotated

from pydantic import StringConstraints, field_validator, model_validator
from sqlmodel import Field, SQLModel

# from sqlmodel import Field as SField
# from sqlmodel import SQLModel


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


class SummaryGroup(StrEnum):
    # BLANK = ""
    ACT = "ACT"
    TAR = "TAR"
    INACT = "INACT"
    ATADSW = "ATADSW"


class PromotionStatus(StrEnum):
    # BLANK = ""
    REGULAR = "REGULAR"
    FROCKED = "FROCKED"
    SELECTED = "SELECTED"
    SPOT = "SPOT"


# class TypeOfReport(Enum):
#     REGULAR = "Regular"
#     CONCURRENT = "Concurrent"
#     OpsCdr = "OpsCdr"


class PhysicalReadiness(StrEnum):
    # BLANK = ""
    PASS = "P"
    BCA_PASS = "B"
    FAIL = "F"
    MED_WAIVED = "M"
    WAIVED = "W"
    NO_PFA = "N"


class BilletSubcategory(StrEnum):
    # BLANK = ""
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
    NOB = 0
    SIGNIFICANT_PROBLEMS = 1
    PROGRESSING = 2
    PROMOTABLE = 3
    MUST_PROMOTE = 4
    EARLY_PROMOTE = 5


class Fitrep(SQLModel, table=True):
    """
    Docstring for Fitrep

    Note: I haven't dug into why, but the @field_validator decorator *must* come before the @classmethod decorator
    on validator methods for them to trigger when calling `Fitrep.model_validate(some_fitrep.model_dump())`.

    Args:
        TODO
    """

    id: int = Field(primary_key=True, default=None)
    name: Annotated[str, StringConstraints(max_length=27, min_length=1, strip_whitespace=True, to_upper=True)] = ""
    grade: Annotated[str, StringConstraints(max_length=5, min_length=1, strip_whitespace=True)] = ""
    desig: Annotated[str, StringConstraints(max_length=12, min_length=1, strip_whitespace=True)] = ""
    ssn: Annotated[str, StringConstraints(strip_whitespace=True, pattern=r"^\d{3}-\d{2}-\d{4}$")] = ""
    group: SummaryGroup | None = None
    uic: Annotated[str, StringConstraints(max_length=5, min_length=1, strip_whitespace=True)] = ""
    station: Annotated[str, StringConstraints(min_length=1, max_length=18, strip_whitespace=True)] = ""
    promotion_status: PromotionStatus | None = None
    date_reported: date | None = None
    periodic: bool = False
    det_indiv: bool = False
    det_rs: bool = False
    special: bool = False
    period_start: date | None = None
    period_end: date | None = None
    not_observed: bool = False
    regular: bool = False
    concurrent: bool = False
    ops_cdr: bool = False
    physical_readiness: PhysicalReadiness | None = None
    billet_subcategory: BilletSubcategory | None = None
    senior_name: Annotated[str, StringConstraints(min_length=1, max_length=27, strip_whitespace=True)] = ""
    senior_grade: Annotated[str, StringConstraints(min_length=1, max_length=5, strip_whitespace=True)] = ""
    senior_desig: Annotated[str, StringConstraints(min_length=1, max_length=5, strip_whitespace=True)] = ""
    senior_title: Annotated[str, StringConstraints(min_length=1, max_length=14, strip_whitespace=True)] = ""
    senior_uic: Annotated[str, StringConstraints(min_length=1, max_length=5, strip_whitespace=True)] = ""
    senior_ssn: Annotated[str, StringConstraints(strip_whitespace=True, pattern=r"^\d{3}-\d{2}-\d{4}$")] = ""
    job: str = ""
    duties_abbreviation: Annotated[str, StringConstraints(min_length=1, max_length=14)] = ""
    duties_description: Annotated[str, StringConstraints(min_length=1, max_length=334)] = ""
    date_counseled: date | None = None
    counselor: Annotated[str, StringConstraints(min_length=1, max_length=20)] = ""
    pro_expertise: int | None = Field(None, ge=0, le=5)
    cmd_climate: int | None = Field(None, ge=0, le=5)
    bearing_and_character: int | None = Field(None, ge=0, le=5)
    teamwork: int | None = Field(None, ge=0, le=5)
    accomp_and_initiative: int | None = Field(None, ge=0, le=5)
    leadership: int | None = Field(None, ge=0, le=5)
    tactical_performance: int | None = Field(None, ge=0, le=5)
    career_rec_1: Annotated[str, StringConstraints(min_length=1, max_length=20, strip_whitespace=True)] = ""
    career_rec_2: Annotated[str, StringConstraints(min_length=1, max_length=20, strip_whitespace=True)] = ""
    comments: Annotated[str, StringConstraints(min_length=1)] = ""
    indiv_promo_rec: int | None = Field(None, ge=0, le=5)
    senior_address: Annotated[str, StringConstraints(min_length=1, max_length=40)] = ""

    @field_validator("group")
    @classmethod
    def validate_group(cls, group: SummaryGroup | None) -> SummaryGroup:
        if group is None:
            raise ValueError("Summary Group must be specified.")
        return group

    @field_validator("station")
    @classmethod
    def validate_station(cls, station: str) -> str:
        if len(station.strip()) == 0:
            raise ValueError("Ship/Station cannot be blank.")
        if len(station) > 18:
            raise ValueError("Ship/Station must be 18 characters or less.")
        return station

    @field_validator("promotion_status")
    @classmethod
    def validate_promotion_status(cls, promotion_status: PromotionStatus | None) -> PromotionStatus:
        if promotion_status is None:
            raise ValueError("Promotion Status must be specified.")
        return promotion_status

    @field_validator("billet_subcategory")
    @classmethod
    def validate_billet_subcategory(cls, billet_subcategory: BilletSubcategory | None) -> BilletSubcategory:
        if billet_subcategory is None:
            raise ValueError("Billet Subcategory must be specified.")
        return billet_subcategory

    @field_validator("career_rec_2", "career_rec_1")
    @classmethod
    def validate_career_rec(cls, career_rec: str) -> str:
        if len(career_rec) > 20:
            raise ValueError("Career Recommendation must be 20 characters or less (including whitespace).")

        wrapped = cls.wrap_text(career_rec, 13)
        length = len(wrapped.split())
        if length > 2:
            lines = wrapped.split("\n")
            career_rec = "\n".join(lines[:2])
        return career_rec

    @field_validator("comments")
    @classmethod
    def validate_comments(cls, comments: str) -> str:
        wrapped = cls.wrap_text(comments, 92)
        length = len(wrapped.split())
        if length > 18:
            # raise ValueError(f"Comments must be 18 lines or less (currently {length} lines).")

            # trim comments to 18 lines
            lines = wrapped.split("\n")
            comments = "\n".join(lines[:18])
        return comments

    @model_validator(mode="after")
    def check_dates(self):
        if (
            self.date_reported is None
            or self.period_start is None
            or self.period_end is None
            or self.date_counseled is None
        ):
            raise ValueError("All date fields must be set.")
        if self.date_reported > self.period_start:
            raise ValueError("Report date cannot be after the period of report start date.")
        if self.date_reported > self.period_end:
            raise ValueError("Report date cannot be after the period of report end date.")
        if self.date_counseled < self.date_reported:
            raise ValueError("Counseling date cannot be before the report date.")
        if self.date_counseled < self.period_start:
            raise ValueError("Counseling date cannot be before the period of report start date.")
        if self.period_end < self.period_start:
            raise ValueError("Period of report end date cannot be before the start date.")
        return self

    @model_validator(mode="after")
    def check_type_of_report(self):
        if self.ops_cdr and self.concurrent:
            raise ValueError("OpsCdr and Concurrent cannot both be selected. [Ref: page 45 of NAVFIT98v30 User Guide]")

    @model_validator(mode="after")
    def check_occasion_for_report(self):
        if self.special:
            if self.det_indiv or self.det_rs or self.periodic:
                raise ValueError(
                    "Special Occasion reports cannot also be Detachment Individual, Detachment Reporting Senior, or Periodic reports."
                )

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
        """
        Get the text representation of the summary group average.

        TODO: Get avg of all fitreps with same summary group field.
        """
        return self.member_trait_avg()

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

    @staticmethod
    def wrap_text(txt: str, width: int) -> str:
        """
        Formats text so that no lines has more than 92 characters.

        This is used for inserting newlines into text from long form text blocks to ensure the text
        prints correctly on generated PDFs.

        Note:
            Soley using the wrap or fill function from the textwrap module to format the comments completely
            isn't quite sufficient because it doesn't appropriately handle cases when users want
            to add empty lines to the comments. The textwrap module by default eliminates newlines. This behavior
            can be disabled, but then newlines are counted as characters that count towards the character limit
            for each line. This function handles each situation appropriately.
        """
        parts = txt.split("\n")
        all_lines: list[str] = []
        for part in parts:
            lines = textwrap.wrap(part, width=width)
            if not lines:
                lines = [""]
            all_lines.extend(lines)
        ret = "\n".join(all_lines)
        return ret
