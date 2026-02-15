"""
SQLModels for each type of report.
"""

import textwrap
from abc import abstractmethod
from datetime import date
from enum import Enum, StrEnum
from pathlib import Path
from typing import Annotated

import pymupdf
from pydantic import StringConstraints, field_validator, model_validator
from pymupdf import Point
from sqlmodel import Field, SQLModel

from navfitx.utils import get_blank_report_path, wrap_duty_desc


class N98Report(SQLModel, table=True):
    """
    A SQLModel that mirrors the 'Reports' table in NAVFIT98A Access db files. This is used to convert
    NAVFIT98A Access db files (.accdb) to NAVFITX SQLite db files and vice versa.

    Args:
        report_id (int): Primary key for the report record.
        parent (str): Identifier of a parent report, if applicable.
        report_type (str): Type of report (e.g., 'FitRep').
        full_name (str): Full name of the subject.
        first_name (str): Subject's first name.
        mi (str): Subject's middle initial.
        last_name (str): Subject's last name.
        suffix (str): Name suffix (e.g., 'Jr', 'III').
        rate (str): Rate or paygrade.
        desig (str): Designator code.
        ssn (str): Social Security Number (format: XXX-XX-XXXX).
        active (bool): Active status flag.
        tar (bool): TAR status flag.
        inactive (bool): Inactive status flag.
        atadsw (bool): ATADSW flag.
        uic (str): Unit Identification Code.
        ship_station (str): Ship or station name.
        promotion_status (str): Promotion status string.
        date_reported (date): Date the report was filed.
        periodic (bool): Periodic report flag.
        det_ind (bool): Detachment individual flag.
        frocking (bool): Frocking flag.
        special (bool): Special occasion report flag.
        from_date (date): Start date of reporting period.
        to_date (date): End date of reporting period.
        nob (bool): Not observed by reporting senior flag.
        regular (bool): Regular report flag.
        concurrent (bool): Concurrent report flag.
        ops_cdr (bool): Ops commander report flag.
        physical_readiness (str): Primary physical readiness code.
        physical_readiness2 (str): Secondary physical readiness code.
        physical_readiness_dt (date): Date of physical readiness assessment.
        billet_subcat (str): Billet subcategory code.
        rs_last_name (str): Reporting senior last name.
        rs_fi (str): Reporting senior first initial.
        rs_mi (str): Reporting senior middle initial.
        reporting_senior (str): Reporting senior full name.
        rs_grade (str): Reporting senior grade.
        rs_desig (str): Reporting senior designator.
        rs_title (str): Reporting senior title.
        rs_uic (str): Reporting senior UIC.
        rs_ssn (str): Reporting senior SSN.
        achievements (str): Achievements text field.
        primary_duty (str): Primary duty description.
        duties (str): Duties text field.
        date_counseled (date): Date counseled.
        counselor (str): Counselor full name.
        counselor_ln (str): Counselor last name.
        counselor_fi (str): Counselor first initial.
        counselor_mi (str): Counselor middle initial.
        prof (int): Professional expertise score.
        prof_dn1 (str): Professional detail/notes 1.
        prof_dn2 (str): Professional detail/notes 2.
        prof_dn3 (str): Professional detail/notes 3.
        qual (int): Qualification score.
        qual_dn1 (str): Qualification detail 1.
        qual_dn2 (str): Qualification detail 2.
        qual_dn3 (str): Qualification detail 3.
        eo (int): Equal opportunity score.
        eo_dn1 (str): EO detail 1.
        eo_dn2 (str): EO detail 2.
        eo_dn3 (str): EO detail 3.
        mil (int): Military bearing score.
        mil_dn1 (str): Military detail 1.
        mil_dn2 (str): Military detail 2.
        mil_dn3 (str): Military detail 3.
        pa (int): Personnel awareness score.
        pa_dn1 (str): PA detail 1.
        pa_dn2 (str): PA detail 2.
        pa_dn3 (str): PA detail 3.
        team (int): Teamwork score.
        team_dn1 (str): Team detail 1.
        team_dn2 (str): Team detail 2.
        team_dn3 (str): Team detail 3.
        lead (int): Leadership score.
        lead_dn1 (str): Leadership detail 1.
        lead_dn2 (str): Leadership detail 2.
        lead_dn3 (str): Leadership detail 3.
        mis (int): Mission score.
        mis_dn1 (str): Mission detail 1.
        mis_dn2 (str): Mission detail 2.
        mis_dn3 (str): Mission detail 3.
        tac (int): Tactical performance score.
        tac_dn1 (str): Tactical detail 1.
        tac_dn2 (str): Tactical detail 2.
        tac_dn3 (str): Tactical detail 3.
        recommend_1 (str): First recommendation text.
        recommend_2 (str): Second recommendation text.
        rater (str): Rater name.
        rater_date (date): Rater signature/date.
        comments_pitch (str): Short comments pitch field.
        comments (str): Full comments text.
        qualifications (str): Qualifications text field.
        promotion_recom (int): Promotion recommendation code.
        summary_rank (int): Summary rank numeric field.
        summary_sp (str): Summary SP text.
        summary_prog (str): Summary progression text.
        summary_prom (str): Summary promotion text.
        summary_mp (str): Summary MP text.
        summary_ep (str): Summary EP text.
        retention_yes (bool): Retention yes flag.
        retention_no (bool): Retention no flag.
        rsca (int): RSCA code.
        rs_address (str): Reporting senior address (combined).
        rs_address1 (str): Reporting senior address line 1.
        rs_address2 (str): Reporting senior address line 2.
        rs_city (str): Reporting senior city.
        rs_state (str): Reporting senior state.
        rs_zip_cd (str): Reporting senior ZIP code.
        rs_phone (str): Reporting senior phone number.
        rs_dsn (str): Reporting senior DSN number.
        senior_rater (str): Senior rater name.
        senior_rater_date (date): Senior rater signature/date.
        statement_yes (bool): Statement yes flag.
        statement_no (bool): Statement no flag.
        rs_info (str): Reporting senior additional info.
        rrs_fi (str): RRS first initial.
        rrs_mi (str): RRS middle initial.
        rrs_last_name (str): RRS last name.
        rrs_grade (str): RRS grade.
        rrs_command (str): RRS command.
        rrs_uic (str): RRS UIC.
        user_comments (str): User-provided comments.
        psswrd (str): Password or protection field.
        standards (str): Standards text field.
        is_validated (str): Validation status flag or note.
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


class Report(SQLModel):
    """
    A class that encapsulates the fields common to every type of report (FitRep, Eval, and ChiefEval).
    Each type of report inherits this class and adds any additional fields specific to that report type.

    Note:
        I haven't dug into why, but the @field_validator decorator *must* come before the @classmethod decorator
        on validator methods for them to trigger when calling `Fitrep.model_validate(some_fitrep.model_dump())`.

    Args:
        id (int): Primary key for the report record.
        name (str): Full name of the subject.
        desig (str): Designator code.
        ssn (str): Social Security Number (format: XXX-XX-XXXX).
        group (SummaryGroup): Summary group category.
        uic (str): Unit Identification Code.
        station (str): Ship or station name.
        promotion_status (PromotionStatus): Promotion status category.
        date_reported (date): Date the report was filed.
        periodic (bool): 'Periodic' checkbox.
        det_indiv (bool): 'Detachment of Individual' checkbox.
        special (bool): Special occasion report checkbox.
        period_start (date): Start date of reporting period.
        period_end (date): End date of reporting period.
        not_observed (bool): 'Not Observed' checkbox.
        regular (bool): 'Regular' report checkbox.
        concurrent (bool): 'Concurrent' checkbox.
        billet_subcategory (BilletSubcategory): Billet subcategory code.
        senior_name (str): Reporting senior full name.
        senior_grade (str): Reporting senior grade.
        senior_desig (str): Reporting senior designator code.
        senior_title (str): Reporting senior title.
        senior_uic (str): Reporting senior UIC.
        senior_ssn (str): Reporting senior SSN (format: XXX-XX-XXXX).
        job (str): Job title or description.
        duties_abbreviation (str): Abbreviated duties description.
        duties_description (str): Full duties description text.
        date_counseled (date): Date counseled by reporting senior.
        counselor (str): Counselor full name.
        career_rec_1 (str): First career recommendation text field.
        career_rec_2 (str): Second career recommendation text field.
        comments (str): Comments text field with a minimum length of 1 character and no maximum length constraint. This field is required and cannot be blank. It is used to provide detailed comments about the subject's performance, achievements, or any other relevant information that the reporting senior wishes to include in the report. The comments should be comprehensive and informative, offering insights into the subject's strengths, areas for improvement, and overall contributions during the reporting period. The content of this field can vary widely based on the specific circumstances and performance of the subject being evaluated, but it must always contain meaningful information that adds value to the report and assists in
    """

    doc_type: str
    id: int = Field(primary_key=True, default=None)
    name: Annotated[str, StringConstraints(max_length=27, min_length=1, strip_whitespace=True, to_upper=True)] = Field(
        title="Name", default=""
    )
    rate: str = ""
    desig: Annotated[str, StringConstraints(max_length=12, min_length=1, strip_whitespace=True)] = Field(
        title="Designator", default=""
    )
    ssn: Annotated[str, StringConstraints(strip_whitespace=True, pattern=r"^\d{3}-\d{2}-\d{4}$")] = Field(
        title="SSN", default=""
    )
    group: SummaryGroup | None = Field(title="Group", default=None)
    uic: Annotated[str, StringConstraints(max_length=5, min_length=1, strip_whitespace=True)] = Field(
        title="UIC", default=""
    )
    station: Annotated[str, StringConstraints(min_length=1, max_length=18, strip_whitespace=True)] = Field(
        title="Ship/Station", default=""
    )
    promotion_status: PromotionStatus | None = Field(title="Promotion Status", default=None)
    date_reported: date | None = None
    periodic: bool = False
    det_indiv: bool = False
    special: bool = False
    period_start: date | None = None
    period_end: date | None = None
    not_observed: bool = False
    regular: bool = False
    concurrent: bool = False
    billet_subcategory: BilletSubcategory | None = None
    senior_name: Annotated[str, StringConstraints(min_length=1, max_length=27, strip_whitespace=True)] = ""
    senior_grade: Annotated[str, StringConstraints(min_length=1, max_length=5, strip_whitespace=True)] = ""
    senior_desig: Annotated[str, StringConstraints(min_length=1, max_length=5, strip_whitespace=True)] = ""
    senior_title: Annotated[str, StringConstraints(min_length=1, max_length=14, strip_whitespace=True)] = ""
    senior_uic: Annotated[str, StringConstraints(min_length=1, max_length=5, strip_whitespace=True)] = ""
    senior_ssn: Annotated[str, StringConstraints(strip_whitespace=True, pattern=r"^\d{3}-\d{2}-\d{4}$")] = ""
    job: str = ""
    duties_abbreviation: Annotated[str, StringConstraints(min_length=1, max_length=14)] = ""
    # duties_description: Annotated[str, StringConstraints(min_length=1, max_length=334)] = ""
    duties_description: str = ""
    date_counseled: date | None = None
    counselor: Annotated[str, StringConstraints(min_length=1, max_length=20)] = ""
    career_rec_1: Annotated[str, StringConstraints(min_length=1, max_length=20, strip_whitespace=True)] = ""
    career_rec_2: Annotated[str, StringConstraints(min_length=1, max_length=20, strip_whitespace=True)] = ""
    comments: Annotated[str, StringConstraints(min_length=1)] = ""
    indiv_promo_rec: int | None = Field(None, ge=0, le=5)
    senior_address: Annotated[str, StringConstraints(min_length=1, max_length=40)] = ""

    def format_job(self, text: str) -> str:
        """Formats the 'Command employment and command achievements' to fit within the constraints of the FITREP form."""
        text = textwrap.fill(text, width=91)
        return text

    def format_date(self, dt: date | None) -> str:
        """Formats a date object into the Fitrep date format (YYMMMDD)."""
        if not dt:
            return ""
        return dt.strftime("%y%b%d").upper()

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

    @field_validator("duties_description")
    @classmethod
    def validate_duties_description(cls, duties_description: str) -> str:
        """
        The duties description field technically has a max character limit according to the NAVFIT98v30 User Guide,
        but it is ignored by the NAVFIT98 v33 app, which will allow as much text as can fit into the field. This gets
        weird because of the small box within the block that holds the duties abbreviation. The account for the space
        this block takes, spaces can be prepended to the description text before counting its lines.
        """
        duties_description = wrap_duty_desc(duties_description)
        num_lines = len(duties_description.split("\n"))
        if num_lines > 4:
            raise ValueError(f"Duties description must be 4 lines or less (currently {num_lines} lines).")
        return duties_description

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

    def average_traits(self, traits: list[int | None]) -> str:
        if len(traits) != 7:
            raise ValueError("Traits list must contain exactly 7 trait scores.")
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

    @abstractmethod
    def member_trait_avg(self) -> str:
        pass

    @abstractmethod
    def create_pdf(self, path: Path):
        pass
        # blank_fitrep = get_blank_report_path(f"{self.doc_type}")
        # doc = pymupdf.open(str(blank_fitrep))
        # meta = doc.metadata
        # meta["title"] = f"{self.doc_type.upper()} for {self.name}"
        # doc.set_metadata(meta)
        # front = doc[0]
        # back = doc[1]
        # front.insert_text(Point(22, 43), self.name, fontsize=12, fontname="cour")
        # back.insert_text(Point(22, 43), self.name, fontsize=12, fontname="Cour")
        # front.insert_text(Point(292, 43), self.rate, fontsize=12, fontname="Cour")
        # back.insert_text(Point(292, 43), self.rate, fontsize=12, fontname="Cour")
        # front.insert_text(Point(360, 43), self.desig, fontsize=12, fontname="Cour")
        # back.insert_text(Point(360, 43), self.desig, fontsize=12, fontname="Cour")
        # front.insert_text(Point(460, 43), self.ssn, fontsize=12, fontname="Cour")
        # back.insert_text(Point(460, 43), self.ssn, fontsize=12, fontname="Cour")
        # if group_point := self.get_group_point():
        #     front.insert_text(group_point, "X", fontsize=12, fontname="Cour")
        # front.insert_text(Point(170, 67), self.uic, fontsize=12, fontname="Cour")
        # front.insert_text(Point(223, 67), self.station, fontsize=12, fontname="Cour")
        # front.insert_text(Point(416, 67), self.promotion_status, fontsize=12, fontname="Cour")
        # report_date_str = self.format_date(self.date_reported)
        # front.insert_text(Point(496, 67), report_date_str, fontsize=12, fontname="Cour")

        # if self.periodic:
        #     front.insert_text(Point(76, 88), "X", fontsize=12, fontname="Cour")
        # if self.det_indiv:
        #     front.insert_text(Point(157, 88), "X", fontsize=12, fontname="Cour")
        # # if self.det_rs:
        # #     front.insert_text(Point(251, 88), "X", fontsize=12, fontname="Cour")
        # if self.special:
        #     front.insert_text(Point(329, 88), "X", fontsize=12, fontname="Cour")

        # from_date_str = self.format_date(self.period_start)
        # front.insert_text(Point(395, 92), from_date_str, fontsize=12, fontname="Cour")
        # to_date_str = self.format_date(self.period_end)
        # front.insert_text(Point(494, 92), to_date_str, fontsize=12, fontname="Cour")
        # if self.not_observed:
        #     front.insert_text(Point(77, 112), "X", fontsize=12, fontname="Cour")

        # if self.regular:
        #     front.insert_text(Point(156, 112), "X", fontsize=12, fontname="Cour")
        # if self.concurrent:
        #     front.insert_text(Point(250, 112), "X", fontsize=12, fontname="Cour")
        # if self.ops_cdr:
        #     front.insert_text(Point(329, 112), "X", fontsize=12, fontname="Cour")

        # front.insert_text(Point(361, 115), self.physical_readiness, fontsize=12, fontname="Cour")
        # front.insert_text(Point(460, 115), self.billet_subcategory, fontsize=12, fontname="Cour")

        # front.insert_text(Point(22, 140), self.senior_name, fontsize=12, fontname="Cour")
        # front.insert_text(Point(172, 140), self.senior_grade, fontsize=12, fontname="Cour")
        # front.insert_text(Point(222, 140), self.senior_desig, fontsize=12, fontname="Cour")
        # front.insert_text(Point(273, 140), self.senior_title, fontsize=12, fontname="Cour")
        # front.insert_text(Point(405, 140), self.senior_uic, fontsize=12, fontname="Cour")
        # front.insert_text(Point(461, 140), self.senior_ssn, fontsize=12, fontname="Cour")

        # front.insert_text(Point(24, 164), self.format_job(self.job), fontsize=10, fontname="Cour", lineheight=1.0)
        # front.insert_text(Point(28, 212), self.duties_abbreviation, fontsize=12, fontname="Cour")

        # duties_desc = wrap_duty_desc(self.duties_description)
        # front.insert_text(Point(24, 212), duties_desc, fontsize=10, fontname="Cour", lineheight=1.0)

        # match self.pro_expertise:
        #     case 0:
        #         front.insert_text(Point(76, 403), "X", fontsize=12, fontname="Cour")
        #     case 1:
        #         front.insert_text(Point(205, 403), "X", fontsize=12, fontname="Cour")
        #     case 2:
        #         front.insert_text(Point(241, 403), "X", fontsize=12, fontname="Cour")
        #     case 3:
        #         front.insert_text(Point(377, 403), "X", fontsize=12, fontname="Cour")
        #     case 4:
        #         front.insert_text(Point(414, 403), "X", fontsize=12, fontname="Cour")
        #     case 5:
        #         front.insert_text(Point(551, 403), "X", fontsize=12, fontname="Cour")
        # match self.cmd_climate:
        #     case 0:
        #         front.insert_text(Point(76, 486), "X", fontsize=12, fontname="Cour")
        #     case 1:
        #         front.insert_text(Point(205, 486), "X", fontsize=12, fontname="Cour")
        #     case 2:
        #         front.insert_text(Point(241, 486), "X", fontsize=12, fontname="Cour")
        #     case 3:
        #         front.insert_text(Point(377, 486), "X", fontsize=12, fontname="Cour")
        #     case 4:
        #         front.insert_text(Point(414, 486), "X", fontsize=12, fontname="Cour")
        #     case 5:
        #         front.insert_text(Point(551, 486), "X", fontsize=12, fontname="Cour")
        # match self.bearing_and_character:
        #     case 0:
        #         front.insert_text(Point(76, 571), "X", fontsize=12, fontname="Cour")
        #     case 1:
        #         front.insert_text(Point(205, 571), "X", fontsize=12, fontname="Cour")
        #     case 2:
        #         front.insert_text(Point(241, 571), "X", fontsize=12, fontname="Cour")
        #     case 3:
        #         front.insert_text(Point(377, 571), "X", fontsize=12, fontname="Cour")
        #     case 4:
        #         front.insert_text(Point(414, 571), "X", fontsize=12, fontname="Cour")
        #     case 5:
        #         front.insert_text(Point(551, 571), "X", fontsize=12, fontname="Cour")
        # match self.teamwork:
        #     case 0:
        #         front.insert_text(Point(76, 655), "X", fontsize=12, fontname="Cour")
        #     case 1:
        #         front.insert_text(Point(205, 655), "X", fontsize=12, fontname="Cour")
        #     case 2:
        #         front.insert_text(Point(241, 655), "X", fontsize=12, fontname="Cour")
        #     case 3:
        #         front.insert_text(Point(377, 655), "X", fontsize=12, fontname="Cour")
        #     case 4:
        #         front.insert_text(Point(414, 655), "X", fontsize=12, fontname="Cour")
        #     case 5:
        #         front.insert_text(Point(551, 655), "X", fontsize=12, fontname="Cour")
        # match self.accomp_and_initiative:
        #     case 0:
        #         front.insert_text(Point(76, 739), "X", fontsize=12, fontname="Cour")
        #     case 1:
        #         front.insert_text(Point(205, 739), "X", fontsize=12, fontname="Cour")
        #     case 2:
        #         front.insert_text(Point(241, 739), "X", fontsize=12, fontname="Cour")
        #     case 3:
        #         front.insert_text(Point(377, 739), "X", fontsize=12, fontname="Cour")
        #     case 4:
        #         front.insert_text(Point(414, 739), "X", fontsize=12, fontname="Cour")
        #     case 5:
        #         front.insert_text(Point(551, 739), "X", fontsize=12, fontname="Cour")

        # counsel_date_str = self.format_date(self.date_counseled)
        # front.insert_text(Point(200, 272), counsel_date_str, fontsize=12, fontname="Cour")

        # front.insert_text(Point(279, 272), self.counselor, fontsize=12, fontname="Cour")

        # # for point in self.get_perf_points_back(self):
        # #     back.insert_text(point, "X", fontsize=12, fontname="Cour")

        # match self.leadership:
        #     case 0:
        #         back.insert_text(Point(76, 186), "X", fontsize=12, fontname="Cour")
        #     case 1:
        #         back.insert_text(Point(205, 186), "X", fontsize=12, fontname="Cour")
        #     case 2:
        #         back.insert_text(Point(241, 186), "X", fontsize=12, fontname="Cour")
        #     case 3:
        #         back.insert_text(Point(377, 186), "X", fontsize=12, fontname="Cour")
        #     case 4:
        #         back.insert_text(Point(414, 186), "X", fontsize=12, fontname="Cour")
        #     case 5:
        #         back.insert_text(Point(551, 186), "X", fontsize=12, fontname="Cour")
        # match self.tactical_performance:
        #     case 0:
        #         back.insert_text(Point(76, 282), "X", fontsize=12, fontname="Cour")
        #     case 1:
        #         back.insert_text(Point(205, 282), "X", fontsize=12, fontname="Cour")
        #     case 2:
        #         back.insert_text(Point(241, 282), "X", fontsize=12, fontname="Cour")
        #     case 3:
        #         back.insert_text(Point(377, 282), "X", fontsize=12, fontname="Cour")
        #     case 4:
        #         back.insert_text(Point(414, 282), "X", fontsize=12, fontname="Cour")
        #     case 5:
        #         back.insert_text(Point(551, 282), "X", fontsize=12, fontname="Cour")

        # back.insert_text(
        #     Point(34, 354),
        #     self.wrap_text(self.comments, 92),
        #     fontsize=9.2,
        #     fontname="Cour",
        # )

        # match self.indiv_promo_rec:
        #     case PromotionRecommendation.NOB.value:
        #         # return Point(101, 606)
        #         back.insert_text(Point(101, 606), "X", fontsize=12, fontname="Cour")
        #     case PromotionRecommendation.SIGNIFICANT_PROBLEMS.value:
        #         # return Point(151, 606)
        #         back.insert_text(Point(151, 606), "X", fontsize=12, fontname="Cour")
        #     case PromotionRecommendation.PROGRESSING.value:
        #         # return Point(202, 606)
        #         back.insert_text(Point(202, 606), "X", fontsize=12, fontname="Cour")
        #     case PromotionRecommendation.PROMOTABLE.value:
        #         # return Point(253, 606)
        #         back.insert_text(Point(253, 606), "X", fontsize=12, fontname="Cour")
        #     case PromotionRecommendation.MUST_PROMOTE.value:
        #         # return Point(304, 606)
        #         back.insert_text(Point(304, 606), "X", fontsize=12, fontname="Cour")
        #     case PromotionRecommendation.EARLY_PROMOTE.value:
        #         # return Point(355, 606)
        #         back.insert_text(Point(355, 606), "X", fontsize=12, fontname="Cour")

    def summary_group_avg(self) -> str:
        """
        Get the text representation of the summary group average.

        TODO: Get avg of all fitreps with same summary group field.
        """
        return self.member_trait_avg()

    @staticmethod
    def wrap_text(txt: str, width: int) -> str:
        """
        Formats text so that no lines has more than `width` characters.

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


class Fitrep(Report, table=True):
    """
    A SQLModel to represent FITREP reports.

    Args:
        rate (str):
            Grade/rate of the sailor.
        det_rs (bool):
            'Detachment Reporting Senior' checkbox. This particular checkbox does not appear in EVALs.
        ops_cdr (bool):
            'Ops Commander' checkbox. This particular checkbox does not appear in EVALs.
        physical_readiness (PhysicalReadiness | None):
            Physical readiness code.
        pro_expertise (int | None):
            Professional expertise score (0-5).
        cmd_climate (int | None):
            Command or Organizational Climate score (0-5).
        bearing_and_character (int | None):
            Military Bearing / Character score (0-5).
        teamwork (int | None):
            Teamwork score (0-5).
        accomp_and_initiative (int | None):
            Mission Accomplishment and Initiative score (0-5).
        leadership (int | None):
            Leadership score (0-5).
        tactical_performance (int | None):
            Tactical Performance score (0-5).

    """

    doc_type: str = Field(default="fitrep", const=True)
    det_rs: bool = False
    ops_cdr: bool = False
    physical_readiness: PhysicalReadiness | None = None
    pro_expertise: int | None = Field(None, ge=0, le=5)
    cmd_climate: int | None = Field(None, ge=0, le=5)
    bearing_and_character: int | None = Field(None, ge=0, le=5)
    teamwork: int | None = Field(None, ge=0, le=5)
    accomp_and_initiative: int | None = Field(None, ge=0, le=5)
    leadership: int | None = Field(None, ge=0, le=5)
    tactical_performance: int | None = Field(None, ge=0, le=5)

    def get_promo_rec_point(self) -> Point:
        """Returns a Point where 'X' should be drawn given the fitrep's
        Promotion Reccomendation.
        """
        match self.indiv_promo_rec:
            case PromotionRecommendation.NOB.value:
                return Point(101, 606)
            case PromotionRecommendation.SIGNIFICANT_PROBLEMS.value:
                return Point(151, 606)
            case PromotionRecommendation.PROGRESSING.value:
                return Point(202, 606)
            case PromotionRecommendation.PROMOTABLE.value:
                return Point(253, 606)
            case PromotionRecommendation.MUST_PROMOTE.value:
                return Point(304, 606)
            case PromotionRecommendation.EARLY_PROMOTE.value:
                return Point(355, 606)
            case _:
                raise ValueError("Fitrep has no Promotion Recommendation set.")

    def get_group_point(self) -> Point | None:
        if self.group == SummaryGroup.ACT:
            return Point(33, 64)
        if self.group == SummaryGroup.TAR:
            return Point(63, 64)
        if self.group == SummaryGroup.INACT:
            return Point(92, 64)
        if self.group == SummaryGroup.ATADSW:
            return Point(120, 64)
        return None

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
        return self.average_traits(traits)

    def create_pdf(self, path: Path) -> None:
        """
        Fills out a FITREP PDF report with the provided FITREP data.
        """
        blank_fitrep = get_blank_report_path("fitrep")
        doc = pymupdf.open(str(blank_fitrep))
        meta = doc.metadata
        meta["title"] = f"{self.doc_type.upper()} for {self.name}"
        doc.set_metadata(meta)
        front = doc[0]
        back = doc[1]
        front.insert_text(Point(22, 43), self.name, fontsize=12, fontname="cour")
        back.insert_text(Point(22, 43), self.name, fontsize=12, fontname="Cour")
        front.insert_text(Point(292, 43), self.rate, fontsize=12, fontname="Cour")
        back.insert_text(Point(292, 43), self.rate, fontsize=12, fontname="Cour")
        front.insert_text(Point(360, 43), self.desig, fontsize=12, fontname="Cour")
        back.insert_text(Point(360, 43), self.desig, fontsize=12, fontname="Cour")
        front.insert_text(Point(460, 43), self.ssn, fontsize=12, fontname="Cour")
        back.insert_text(Point(460, 43), self.ssn, fontsize=12, fontname="Cour")
        if group_point := self.get_group_point():
            front.insert_text(group_point, "X", fontsize=12, fontname="Cour")
        front.insert_text(Point(170, 67), self.uic, fontsize=12, fontname="Cour")
        front.insert_text(Point(223, 67), self.station, fontsize=12, fontname="Cour")
        front.insert_text(Point(416, 67), self.promotion_status, fontsize=12, fontname="Cour")
        report_date_str = self.format_date(self.date_reported)
        front.insert_text(Point(496, 67), report_date_str, fontsize=12, fontname="Cour")

        if self.periodic:
            front.insert_text(Point(76, 88), "X", fontsize=12, fontname="Cour")
        if self.det_indiv:
            front.insert_text(Point(157, 88), "X", fontsize=12, fontname="Cour")
        if self.det_rs:
            front.insert_text(Point(251, 88), "X", fontsize=12, fontname="Cour")
        if self.special:
            front.insert_text(Point(329, 88), "X", fontsize=12, fontname="Cour")

        from_date_str = self.format_date(self.period_start)
        front.insert_text(Point(395, 92), from_date_str, fontsize=12, fontname="Cour")
        to_date_str = self.format_date(self.period_end)
        front.insert_text(Point(494, 92), to_date_str, fontsize=12, fontname="Cour")
        if self.not_observed:
            front.insert_text(Point(77, 112), "X", fontsize=12, fontname="Cour")

        if self.regular:
            front.insert_text(Point(156, 112), "X", fontsize=12, fontname="Cour")
        if self.concurrent:
            front.insert_text(Point(250, 112), "X", fontsize=12, fontname="Cour")
        if self.ops_cdr:
            front.insert_text(Point(329, 112), "X", fontsize=12, fontname="Cour")

        front.insert_text(Point(361, 115), self.physical_readiness, fontsize=12, fontname="Cour")
        front.insert_text(Point(460, 115), self.billet_subcategory, fontsize=12, fontname="Cour")

        front.insert_text(Point(22, 140), self.senior_name, fontsize=12, fontname="Cour")
        front.insert_text(Point(172, 140), self.senior_grade, fontsize=12, fontname="Cour")
        front.insert_text(Point(222, 140), self.senior_desig, fontsize=12, fontname="Cour")
        front.insert_text(Point(273, 140), self.senior_title, fontsize=12, fontname="Cour")
        front.insert_text(Point(405, 140), self.senior_uic, fontsize=12, fontname="Cour")
        front.insert_text(Point(461, 140), self.senior_ssn, fontsize=12, fontname="Cour")

        front.insert_text(Point(24, 164), self.format_job(self.job), fontsize=10, fontname="Cour", lineheight=1.0)
        front.insert_text(Point(28, 212), self.duties_abbreviation, fontsize=12, fontname="Cour")

        duties_desc = wrap_duty_desc(self.duties_description)
        front.insert_text(Point(24, 212), duties_desc, fontsize=10, fontname="Cour", lineheight=1.0)

        match self.pro_expertise:
            case 0:
                front.insert_text(Point(76, 403), "X", fontsize=12, fontname="Cour")
            case 1:
                front.insert_text(Point(205, 403), "X", fontsize=12, fontname="Cour")
            case 2:
                front.insert_text(Point(241, 403), "X", fontsize=12, fontname="Cour")
            case 3:
                front.insert_text(Point(377, 403), "X", fontsize=12, fontname="Cour")
            case 4:
                front.insert_text(Point(414, 403), "X", fontsize=12, fontname="Cour")
            case 5:
                front.insert_text(Point(551, 403), "X", fontsize=12, fontname="Cour")
        match self.cmd_climate:
            case 0:
                front.insert_text(Point(76, 486), "X", fontsize=12, fontname="Cour")
            case 1:
                front.insert_text(Point(205, 486), "X", fontsize=12, fontname="Cour")
            case 2:
                front.insert_text(Point(241, 486), "X", fontsize=12, fontname="Cour")
            case 3:
                front.insert_text(Point(377, 486), "X", fontsize=12, fontname="Cour")
            case 4:
                front.insert_text(Point(414, 486), "X", fontsize=12, fontname="Cour")
            case 5:
                front.insert_text(Point(551, 486), "X", fontsize=12, fontname="Cour")
        match self.bearing_and_character:
            case 0:
                front.insert_text(Point(76, 571), "X", fontsize=12, fontname="Cour")
            case 1:
                front.insert_text(Point(205, 571), "X", fontsize=12, fontname="Cour")
            case 2:
                front.insert_text(Point(241, 571), "X", fontsize=12, fontname="Cour")
            case 3:
                front.insert_text(Point(377, 571), "X", fontsize=12, fontname="Cour")
            case 4:
                front.insert_text(Point(414, 571), "X", fontsize=12, fontname="Cour")
            case 5:
                front.insert_text(Point(551, 571), "X", fontsize=12, fontname="Cour")
        match self.teamwork:
            case 0:
                front.insert_text(Point(76, 655), "X", fontsize=12, fontname="Cour")
            case 1:
                front.insert_text(Point(205, 655), "X", fontsize=12, fontname="Cour")
            case 2:
                front.insert_text(Point(241, 655), "X", fontsize=12, fontname="Cour")
            case 3:
                front.insert_text(Point(377, 655), "X", fontsize=12, fontname="Cour")
            case 4:
                front.insert_text(Point(414, 655), "X", fontsize=12, fontname="Cour")
            case 5:
                front.insert_text(Point(551, 655), "X", fontsize=12, fontname="Cour")
        match self.accomp_and_initiative:
            case 0:
                front.insert_text(Point(76, 739), "X", fontsize=12, fontname="Cour")
            case 1:
                front.insert_text(Point(205, 739), "X", fontsize=12, fontname="Cour")
            case 2:
                front.insert_text(Point(241, 739), "X", fontsize=12, fontname="Cour")
            case 3:
                front.insert_text(Point(377, 739), "X", fontsize=12, fontname="Cour")
            case 4:
                front.insert_text(Point(414, 739), "X", fontsize=12, fontname="Cour")
            case 5:
                front.insert_text(Point(551, 739), "X", fontsize=12, fontname="Cour")

        counsel_date_str = self.format_date(self.date_counseled)
        front.insert_text(Point(200, 272), counsel_date_str, fontsize=12, fontname="Cour")

        front.insert_text(Point(279, 272), self.counselor, fontsize=12, fontname="Cour")

        # for point in self.get_perf_points_back(self):
        #     back.insert_text(point, "X", fontsize=12, fontname="Cour")

        match self.leadership:
            case 0:
                back.insert_text(Point(76, 186), "X", fontsize=12, fontname="Cour")
            case 1:
                back.insert_text(Point(205, 186), "X", fontsize=12, fontname="Cour")
            case 2:
                back.insert_text(Point(241, 186), "X", fontsize=12, fontname="Cour")
            case 3:
                back.insert_text(Point(377, 186), "X", fontsize=12, fontname="Cour")
            case 4:
                back.insert_text(Point(414, 186), "X", fontsize=12, fontname="Cour")
            case 5:
                back.insert_text(Point(551, 186), "X", fontsize=12, fontname="Cour")
        match self.tactical_performance:
            case 0:
                back.insert_text(Point(76, 282), "X", fontsize=12, fontname="Cour")
            case 1:
                back.insert_text(Point(205, 282), "X", fontsize=12, fontname="Cour")
            case 2:
                back.insert_text(Point(241, 282), "X", fontsize=12, fontname="Cour")
            case 3:
                back.insert_text(Point(377, 282), "X", fontsize=12, fontname="Cour")
            case 4:
                back.insert_text(Point(414, 282), "X", fontsize=12, fontname="Cour")
            case 5:
                back.insert_text(Point(551, 282), "X", fontsize=12, fontname="Cour")

        back.insert_text(
            Point(34, 354),
            self.wrap_text(self.comments, 92),
            fontsize=9.2,
            fontname="Cour",
        )

        match self.indiv_promo_rec:
            case PromotionRecommendation.NOB.value:
                # return Point(101, 606)
                back.insert_text(Point(101, 606), "X", fontsize=12, fontname="Cour")
            case PromotionRecommendation.SIGNIFICANT_PROBLEMS.value:
                # return Point(151, 606)
                back.insert_text(Point(151, 606), "X", fontsize=12, fontname="Cour")
            case PromotionRecommendation.PROGRESSING.value:
                # return Point(202, 606)
                back.insert_text(Point(202, 606), "X", fontsize=12, fontname="Cour")
            case PromotionRecommendation.PROMOTABLE.value:
                # return Point(253, 606)
                back.insert_text(Point(253, 606), "X", fontsize=12, fontname="Cour")
            case PromotionRecommendation.MUST_PROMOTE.value:
                # return Point(304, 606)
                back.insert_text(Point(304, 606), "X", fontsize=12, fontname="Cour")
            case PromotionRecommendation.EARLY_PROMOTE.value:
                # return Point(355, 606)
                back.insert_text(Point(355, 606), "X", fontsize=12, fontname="Cour")

        back.insert_text(Point(388, 586), self.senior_address, fontsize=9, fontname="Cour", lineheight=1.1)
        back.insert_text(Point(105, 694), self.member_trait_avg(), fontsize=12, fontname="Cour")
        back.insert_text(Point(240, 694), self.summary_group_avg(), fontsize=12, fontname="Cour")
        back.insert_text(Point(370, 300), textwrap.fill(self.career_rec_1, 13), fontsize=10, fontname="Cour")
        back.insert_text(Point(467, 300), textwrap.fill(self.career_rec_2, 13), fontsize=10, fontname="Cour")

        doc.save(str(path))
        doc.close()


class Eval(Report, table=True):
    """
    A SQLModel to represent EVAL reports.

    Args:
        rate (str):
            Rate/rating of the eval subject.
        prof_knowledge (int | None):
            Professional knowledge score (0-5).
    """

    doc_type: str = "eval"
    prom_frock: bool = False
    physical_readiness: PhysicalReadiness | None = None
    prof_knowledge: int | None = Field(None, ge=0, le=5)
    quality_of_work: int | None = Field(None, ge=0, le=5)
    cmd_climate: int | None = Field(None, ge=0, le=5)
    bearing_and_character: int | None = Field(None, ge=0, le=5)
    initiative: int | None = Field(None, ge=0, le=5)
    teamwork: int | None = Field(None, ge=0, le=5)
    leadership: int | None = Field(None, ge=0, le=5)

    # 182 char constraint from NAVFIT98 user manual
    # TODO: confirm NAVFIT98 actually only allows 182 chars
    achievements: Annotated[str, StringConstraints(min_length=1, max_length=182)] = Field("")
    retain: bool | None = Field(None)

    def member_trait_avg(self) -> str:
        traits = [
            self.prof_knowledge,
            self.quality_of_work,
            self.cmd_climate,
            self.bearing_and_character,
            self.initiative,
            self.teamwork,
            self.leadership,
        ]
        return self.average_traits(traits)

    def get_group_point(self) -> Point | None:
        if self.group == SummaryGroup.ACT:
            return Point(33, 64)
        if self.group == SummaryGroup.TAR:
            return Point(63, 64)
        if self.group == SummaryGroup.INACT:
            return Point(92, 64)
        if self.group == SummaryGroup.ATADSW:
            return Point(120, 64)
        return None

    def create_pdf(self, path: Path) -> None:
        blank_fitrep = get_blank_report_path("fitrep")
        doc = pymupdf.open(str(blank_fitrep))
        meta = doc.metadata
        meta["title"] = f"{self.doc_type.upper()} for {self.name}"
        doc.set_metadata(meta)
        front = doc[0]
        back = doc[1]
        front.insert_text(Point(22, 43), self.name, fontsize=12, fontname="cour")
        back.insert_text(Point(22, 43), self.name, fontsize=12, fontname="Cour")
        front.insert_text(Point(292, 43), self.rate, fontsize=12, fontname="Cour")
        back.insert_text(Point(292, 43), self.rate, fontsize=12, fontname="Cour")
        front.insert_text(Point(360, 43), self.desig, fontsize=12, fontname="Cour")
        back.insert_text(Point(360, 43), self.desig, fontsize=12, fontname="Cour")
        front.insert_text(Point(460, 43), self.ssn, fontsize=12, fontname="Cour")
        back.insert_text(Point(460, 43), self.ssn, fontsize=12, fontname="Cour")
        if group_point := self.get_group_point():
            front.insert_text(group_point, "X", fontsize=12, fontname="Cour")
        front.insert_text(Point(170, 67), self.uic, fontsize=12, fontname="Cour")
        front.insert_text(Point(223, 67), self.station, fontsize=12, fontname="Cour")
        front.insert_text(Point(416, 67), self.promotion_status, fontsize=12, fontname="Cour")
        report_date_str = self.format_date(self.date_reported)
        front.insert_text(Point(496, 67), report_date_str, fontsize=12, fontname="Cour")

        if self.periodic:
            front.insert_text(Point(76, 88), "X", fontsize=12, fontname="Cour")
        if self.det_indiv:
            front.insert_text(Point(157, 88), "X", fontsize=12, fontname="Cour")
        if self.prom_frock:
            front.insert_text(Point(251, 88), "X", fontsize=12, fontname="Cour")
        if self.special:
            front.insert_text(Point(329, 88), "X", fontsize=12, fontname="Cour")

        from_date_str = self.format_date(self.period_start)
        front.insert_text(Point(395, 92), from_date_str, fontsize=12, fontname="Cour")
        to_date_str = self.format_date(self.period_end)
        front.insert_text(Point(494, 92), to_date_str, fontsize=12, fontname="Cour")
        if self.not_observed:
            front.insert_text(Point(77, 112), "X", fontsize=12, fontname="Cour")

        if self.regular:
            front.insert_text(Point(156, 112), "X", fontsize=12, fontname="Cour")
        if self.concurrent:
            front.insert_text(Point(250, 112), "X", fontsize=12, fontname="Cour")

        front.insert_text(Point(361, 115), self.physical_readiness, fontsize=12, fontname="Cour")
        front.insert_text(Point(460, 115), self.billet_subcategory, fontsize=12, fontname="Cour")

        front.insert_text(Point(22, 140), self.senior_name, fontsize=12, fontname="Cour")
        front.insert_text(Point(172, 140), self.senior_grade, fontsize=12, fontname="Cour")
        front.insert_text(Point(222, 140), self.senior_desig, fontsize=12, fontname="Cour")
        front.insert_text(Point(273, 140), self.senior_title, fontsize=12, fontname="Cour")
        front.insert_text(Point(405, 140), self.senior_uic, fontsize=12, fontname="Cour")
        front.insert_text(Point(461, 140), self.senior_ssn, fontsize=12, fontname="Cour")

        front.insert_text(Point(24, 164), self.format_job(self.job), fontsize=10, fontname="Cour", lineheight=1.0)
        front.insert_text(Point(28, 212), self.duties_abbreviation, fontsize=12, fontname="Cour")

        duties_desc = wrap_duty_desc(self.duties_description)
        front.insert_text(Point(24, 212), duties_desc, fontsize=10, fontname="Cour", lineheight=1.0)

        match self.prof_knowledge:
            case 0:
                front.insert_text(Point(76, 403), "X", fontsize=12, fontname="Cour")
            case 1:
                front.insert_text(Point(205, 403), "X", fontsize=12, fontname="Cour")
            case 2:
                front.insert_text(Point(241, 403), "X", fontsize=12, fontname="Cour")
            case 3:
                front.insert_text(Point(377, 403), "X", fontsize=12, fontname="Cour")
            case 4:
                front.insert_text(Point(414, 403), "X", fontsize=12, fontname="Cour")
            case 5:
                front.insert_text(Point(551, 403), "X", fontsize=12, fontname="Cour")
        match self.quality_of_work:
            case 0:
                front.insert_text(Point(76, 486), "X", fontsize=12, fontname="Cour")
            case 1:
                front.insert_text(Point(205, 486), "X", fontsize=12, fontname="Cour")
            case 2:
                front.insert_text(Point(241, 486), "X", fontsize=12, fontname="Cour")
            case 3:
                front.insert_text(Point(377, 486), "X", fontsize=12, fontname="Cour")
            case 4:
                front.insert_text(Point(414, 486), "X", fontsize=12, fontname="Cour")
            case 5:
                front.insert_text(Point(551, 486), "X", fontsize=12, fontname="Cour")
        match self.cmd_climate:
            case 0:
                front.insert_text(Point(76, 571), "X", fontsize=12, fontname="Cour")
            case 1:
                front.insert_text(Point(205, 571), "X", fontsize=12, fontname="Cour")
            case 2:
                front.insert_text(Point(241, 571), "X", fontsize=12, fontname="Cour")
            case 3:
                front.insert_text(Point(377, 571), "X", fontsize=12, fontname="Cour")
            case 4:
                front.insert_text(Point(414, 571), "X", fontsize=12, fontname="Cour")
            case 5:
                front.insert_text(Point(551, 571), "X", fontsize=12, fontname="Cour")
        match self.bearing_and_character:
            case 0:
                front.insert_text(Point(76, 655), "X", fontsize=12, fontname="Cour")
            case 1:
                front.insert_text(Point(205, 655), "X", fontsize=12, fontname="Cour")
            case 2:
                front.insert_text(Point(241, 655), "X", fontsize=12, fontname="Cour")
            case 3:
                front.insert_text(Point(377, 655), "X", fontsize=12, fontname="Cour")
            case 4:
                front.insert_text(Point(414, 655), "X", fontsize=12, fontname="Cour")
            case 5:
                front.insert_text(Point(551, 655), "X", fontsize=12, fontname="Cour")
        match self.initiative:
            case 0:
                front.insert_text(Point(76, 739), "X", fontsize=12, fontname="Cour")
            case 1:
                front.insert_text(Point(205, 739), "X", fontsize=12, fontname="Cour")
            case 2:
                front.insert_text(Point(241, 739), "X", fontsize=12, fontname="Cour")
            case 3:
                front.insert_text(Point(377, 739), "X", fontsize=12, fontname="Cour")
            case 4:
                front.insert_text(Point(414, 739), "X", fontsize=12, fontname="Cour")
            case 5:
                front.insert_text(Point(551, 739), "X", fontsize=12, fontname="Cour")

        counsel_date_str = self.format_date(self.date_counseled)
        front.insert_text(Point(200, 272), counsel_date_str, fontsize=12, fontname="Cour")

        front.insert_text(Point(279, 272), self.counselor, fontsize=12, fontname="Cour")

        match self.teamwork:
            case 0:
                back.insert_text(Point(76, 186), "X", fontsize=12, fontname="Cour")
            case 1:
                back.insert_text(Point(205, 186), "X", fontsize=12, fontname="Cour")
            case 2:
                back.insert_text(Point(241, 186), "X", fontsize=12, fontname="Cour")
            case 3:
                back.insert_text(Point(377, 186), "X", fontsize=12, fontname="Cour")
            case 4:
                back.insert_text(Point(414, 186), "X", fontsize=12, fontname="Cour")
            case 5:
                back.insert_text(Point(551, 186), "X", fontsize=12, fontname="Cour")
        match self.leadership:
            case 0:
                back.insert_text(Point(76, 282), "X", fontsize=12, fontname="Cour")
            case 1:
                back.insert_text(Point(205, 282), "X", fontsize=12, fontname="Cour")
            case 2:
                back.insert_text(Point(241, 282), "X", fontsize=12, fontname="Cour")
            case 3:
                back.insert_text(Point(377, 282), "X", fontsize=12, fontname="Cour")
            case 4:
                back.insert_text(Point(414, 282), "X", fontsize=12, fontname="Cour")
            case 5:
                back.insert_text(Point(551, 282), "X", fontsize=12, fontname="Cour")

        back.insert_text(
            Point(34, 354),
            self.wrap_text(self.comments, 92),
            fontsize=9.2,
            fontname="Cour",
        )

        match self.indiv_promo_rec:
            case PromotionRecommendation.NOB.value:
                # return Point(101, 606)
                back.insert_text(Point(101, 606), "X", fontsize=12, fontname="Cour")
            case PromotionRecommendation.SIGNIFICANT_PROBLEMS.value:
                # return Point(151, 606)
                back.insert_text(Point(151, 606), "X", fontsize=12, fontname="Cour")
            case PromotionRecommendation.PROGRESSING.value:
                # return Point(202, 606)
                back.insert_text(Point(202, 606), "X", fontsize=12, fontname="Cour")
            case PromotionRecommendation.PROMOTABLE.value:
                # return Point(253, 606)
                back.insert_text(Point(253, 606), "X", fontsize=12, fontname="Cour")
            case PromotionRecommendation.MUST_PROMOTE.value:
                # return Point(304, 606)
                back.insert_text(Point(304, 606), "X", fontsize=12, fontname="Cour")
            case PromotionRecommendation.EARLY_PROMOTE.value:
                # return Point(355, 606)
                back.insert_text(Point(355, 606), "X", fontsize=12, fontname="Cour")

        back.insert_text(Point(388, 586), self.senior_address, fontsize=9, fontname="Cour", lineheight=1.1)
        back.insert_text(Point(105, 694), self.member_trait_avg(), fontsize=12, fontname="Cour")
        back.insert_text(Point(240, 694), self.summary_group_avg(), fontsize=12, fontname="Cour")
        back.insert_text(Point(370, 300), textwrap.fill(self.career_rec_1, 13), fontsize=10, fontname="Cour")
        back.insert_text(Point(467, 300), textwrap.fill(self.career_rec_2, 13), fontsize=10, fontname="Cour")

        doc.save(str(path))
        doc.close()


class ChiefEval(Report, table=True):
    """
    A SQLModel to represent Chief EVAL reports.
    """

    rate: str = ""
    det_rs: bool = False
    ops_cdr: bool = False
    physical_readiness: str | None = None
    technical_mastery: int | None = Field(None, ge=0, le=5)
    expertise: int | None = Field(None, ge=0, le=5)
    professionalism: int | None = Field(None, ge=0, le=5)
    integrity: int | None = Field(None, ge=0, le=5)
    accountability: int | None = Field(None, ge=0, le=5)
    leadership: int | None = Field(None, ge=0, le=5)
    teamwork: int | None = Field(None, ge=0, le=5)

    def member_trait_avg(self) -> str:
        traits = [
            self.technical_mastery,
            self.expertise,
            self.professionalism,
            self.integrity,
            self.accountability,
            self.leadership,
            self.teamwork,
        ]
        return self.average_traits(traits)
