"""
SQLModels for each type of report.
"""

import re
import textwrap
from abc import abstractmethod
from datetime import date
from enum import Enum
from pathlib import Path
from typing import Annotated

import pymupdf
import tomlkit
from pydantic import StringConstraints, field_validator, model_validator
from pymupdf import Point
from sqlmodel import Field, SQLModel

from navfitx.utils import get_blank_report_path, wrap_duty_desc

from .enums import BilletSubcategory, DutyStatus, PromotionStatus


class Report(SQLModel):
    """
    A class that encapsulates the fields common to every type of report (FitRep, Eval, and ChiefEval).
    Each type of report inherits this class and adds any additional fields specific to that report type.

    Note:
        I haven't dug into why, but the @field_validator decorator *must* come before the @classmethod decorator
        on validator methods for them to trigger when calling `Fitrep.model_validate(some_fitrep.model_dump())`.
    """

    id: int | None = Field(primary_key=True, default=None)
    doc_type: str
    name: Annotated[str, StringConstraints(max_length=27, min_length=1, strip_whitespace=True, to_upper=True)] = Field(
        title="Name", default=""
    )
    rate: Annotated[str, StringConstraints(min_length=1, max_length=5, to_upper=True, strip_whitespace=True)] = Field(
        title="Rate", default=""
    )
    desig: Annotated[str, StringConstraints(max_length=12, min_length=1, strip_whitespace=True)] = Field(
        title="Designator", default=""
    )
    ssn: str = Field(title="SSN", default="")
    group: DutyStatus | None = Field(title="Group", default=None)
    uic: Annotated[str, StringConstraints(max_length=5, min_length=1, strip_whitespace=True)] = Field(
        title="UIC", default=""
    )
    station: Annotated[str, StringConstraints(min_length=1, max_length=18, strip_whitespace=True)] = Field(
        title="Ship/Station", default=""
    )
    promotion_status: PromotionStatus | None = Field(title="Promotion Status", default=None)
    date_reported: date | None = Field(title="Date Reported", default=None)
    periodic: bool = Field(title="Periodic", default=False)
    det_indiv: bool = Field(title="Detachment of Individual", default=False)
    special: bool = Field(title="Special", default=False)
    period_start: date | None = Field(title="Period of Start", default=None)
    period_end: date | None = Field(title="Period of End", default=None)
    not_observed: bool = Field(title="Not Observed", default=False)
    regular: bool = Field(title="Regular", default=False)
    concurrent: bool = Field(title="Concurrent", default=False)
    physical_readiness: str = Field("", title="Physical Readiness")
    billet_subcategory: BilletSubcategory | None = Field(title="Billet Subcategory", default=None)
    senior_name: Annotated[str, StringConstraints(min_length=1, max_length=27, strip_whitespace=True)] = Field(
        title="Reporting Senior Name", default=""
    )
    senior_grade: Annotated[str, StringConstraints(min_length=1, max_length=5, strip_whitespace=True)] = Field(
        title="Reporting Senior Grade", default=""
    )
    senior_desig: Annotated[str, StringConstraints(min_length=1, max_length=5, strip_whitespace=True)] = Field(
        title="Reporting Senior Designator", default=""
    )
    senior_title: Annotated[
        str, StringConstraints(min_length=1, max_length=14, strip_whitespace=True, to_upper=True)
    ] = Field(title="Reporting Senior Title", default="")
    senior_uic: Annotated[str, StringConstraints(min_length=1, max_length=5, strip_whitespace=True)] = Field(
        title="Reporting Senior UIC", default=""
    )
    senior_ssn: Annotated[str, StringConstraints(strip_whitespace=True)] = Field(
        title="Reporting Senior SSN", default=""
    )
    job: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)] = Field(
        title="Command Employment and Command Achievements", default=""
    )
    duties_abbreviation: Annotated[str, StringConstraints(min_length=1, max_length=14, strip_whitespace=True)] = Field(
        title="Duties Abbreviation", default=""
    )
    duties_description: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)] = Field(
        title="Duties Description", default=""
    )
    date_counseled: date | None = Field(title="Date Counseled", default=None)
    counselor: Annotated[str, StringConstraints(min_length=1, max_length=20, to_upper=True)] = Field(
        title="Counselor", default=""
    )

    # Subclasses overwrite these fields with Field title metadata
    trait1: int | None = Field(None, ge=0, le=5)
    trait2: int | None = Field(None, ge=0, le=5)
    trait3: int | None = Field(None, ge=0, le=5)
    trait4: int | None = Field(None, ge=0, le=5)
    trait5: int | None = Field(None, ge=0, le=5)
    trait6: int | None = Field(None, ge=0, le=5)
    trait7: int | None = Field(None, ge=0, le=5)

    career_rec_1: Annotated[str, StringConstraints(max_length=20, strip_whitespace=True)] = Field(
        title="Career Recommendation 1", default=""
    )
    career_rec_2: Annotated[str, StringConstraints(max_length=20, strip_whitespace=True)] = Field(
        title="Career Recommendation 2", default=""
    )
    comments: Annotated[str, StringConstraints(min_length=1)] = Field(title="Comments", default="")
    indiv_promo_rec: int | None = Field(title="Individual Promotion Recommendation", default=None, ge=0, le=5)
    senior_address: Annotated[str, StringConstraints(min_length=1)] = Field(
        title="Reporting Senior Address", default=""
    )

    @staticmethod
    def format_job(text: str) -> str:
        """Formats the 'Command employment and command achievements' to fit within the constraints of the FITREP form."""
        text = textwrap.fill(text, width=91)
        return text

    @field_validator("uic")
    @classmethod
    def validate_uic(cls, uic: str) -> str:
        # only alphanumeric characters are allowed in UICs
        if not re.match(r"^[A-Za-z0-9]+$", uic):
            raise ValueError("UIC may only contain alphanumeric characters.")
        return uic

    @field_validator("job")
    @classmethod
    def validate_job(cls, job: str) -> str:
        formatted: str = cls.format_job(job)
        # ensure formatted job is no more than 3 lines
        if len(formatted.split("\n")) > 3:
            raise ValueError(
                "Command employment and command achievements too long; limit of 3 lines of 91 characters each."
            )
        return job

    def format_date(self, dt: date | None) -> str:
        """Formats a date object into the report date format (YYMMMDD)."""
        if not dt:
            return ""
        return dt.strftime("%y%b%d").upper()

    @field_validator("group")
    @classmethod
    def validate_group(cls, group: DutyStatus | None) -> DutyStatus:
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

    @field_validator("ssn", "senior_ssn")
    @classmethod
    def validate_ssn(cls, ssn: str) -> str:
        ssn = ssn.strip()
        if not re.match(r"^\d{3}-\d{2}-\d{4}$", ssn):
            raise ValueError("SSN must be in the format XXX-XX-XXXX")
        return ssn

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

    @model_validator(mode="after")
    def validate_career_recs(self):
        if self.career_rec_2 and not self.career_rec_1:
            raise ValueError("Career Recommendation 2 should be blank if Career Recommendation 1 is blank.")
        if self.career_rec_1.upper() == "NA" or self.career_rec_1.upper() == "NONE":
            if self.career_rec_2:
                raise ValueError(
                    "Career Recommendation 2 should be blank if Career Recommendation 1 is 'NA' or 'NONE'."
                )
        if self.not_observed:
            if self.career_rec_1 or self.career_rec_2:
                raise ValueError("Career Recommendations should be blank if 'Not Observed' is checked.")
        return self

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
    def validate_dates(self):
        if self.date_reported is None:
            raise ValueError("Report date must be set.")
        if self.period_start is None:
            raise ValueError("Period of report start date must be set.")
        if self.period_end is None:
            raise ValueError("Period of report end date must be set.")
        if self.date_counseled is None:
            raise ValueError("Counseling date must be set.")

        # check date_reported against other dates
        if self.date_reported <= date(2000, 1, 1):
            # In the PyQt app, date fields must have a default value, so it uses 01 JAN 2000.
            # This ensures that the default value is not used.
            raise ValueError("Report date too far in the past.")
        if self.date_reported > date.today():
            raise ValueError("Report date cannot be in the future.")
        if self.date_reported > self.period_start:
            raise ValueError("Report date cannot be after the period of report start date.")
        if self.date_reported > self.period_end:
            raise ValueError("Report date cannot be after the period of report end date.")
        if self.date_reported > self.date_counseled:
            raise ValueError("Report date cannot be after the counseling date.")

        if self.period_start <= date(2000, 1, 1):
            raise ValueError("Period of report start date too far in the past.")
        if self.period_start > date.today():
            raise ValueError("Period of report start date cannot be in the future.")
        if self.period_start > self.period_end:
            raise ValueError("Period of report start date cannot be after the end date.")
        if self.period_start > self.date_counseled:
            raise ValueError("Period of report start date cannot be after the counseling date.")

        if self.period_end <= date(2000, 1, 1):
            raise ValueError("Period of report end date too far in the past.")
        if self.period_end < self.date_counseled:
            raise ValueError("Period of report end date cannot be before the counseling date.")
        if self.period_end > date.today():
            raise ValueError("Period of report end date cannot be in the future.")

        if self.date_counseled <= date(2000, 1, 1):
            raise ValueError("Counseling date too far in the past.")
        if self.date_counseled > date.today():
            raise ValueError("Counseling date cannot be in the future.")
        return self

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

    def member_trait_avg(self) -> str:
        traits = [
            self.trait1,
            self.trait2,
            self.trait3,
            self.trait4,
            self.trait5,
            self.trait6,
            self.trait7,
        ]
        return self.average_traits(traits)

    def model_dump_toml(self) -> str:
        """
        Dump the model to a canonical report TOML string.
        """
        from navfitx.importer import SUPPORTED_SCHEMA_VERSION

        report_dict = self.model_dump(exclude={"id"})
        report_dict = {k: v for k, v in report_dict.items() if v is not None and v != ""}
        for key, value in report_dict.items():
            if isinstance(value, Enum):
                report_dict[key] = value.value

        document = tomlkit.document()
        document.add("schema_version", SUPPORTED_SCHEMA_VERSION)
        if "doc_type" in report_dict:
            document.add("doc_type", report_dict.pop("doc_type"))
        for key, value in report_dict.items():
            document.add(key, value)
        return tomlkit.dumps(document)

    @abstractmethod
    def get_group_point(self) -> Point | None:
        pass

    @abstractmethod
    def _insert_occasion_for_report_fields(self, front) -> None:
        pass

    @abstractmethod
    def _insert_type_of_report_fields(self, front) -> None:
        pass

    @abstractmethod
    def _insert_duties_classification_fields(self, front) -> None:
        pass

    def _open_report_pdf(self, report_name: str):
        blank_report = get_blank_report_path(report_name)
        doc = pymupdf.open(str(blank_report))
        if isinstance(doc.metadata, dict):
            meta = doc.metadata
            meta["title"] = f"{self.doc_type.upper()} for {self.name}"
            doc.set_metadata(meta)
        return doc, doc[0], doc[1]

    def _insert_common_report_fields(self, front, back) -> None:
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
        front.insert_text(Point(416, 67), str(self.promotion_status), fontsize=12, fontname="Cour")
        report_date_str = self.format_date(self.date_reported)
        front.insert_text(Point(496, 67), report_date_str, fontsize=12, fontname="Cour")

        self._insert_occasion_for_report_fields(front)

        from_date_str = self.format_date(self.period_start)
        front.insert_text(Point(395, 92), from_date_str, fontsize=12, fontname="Cour")
        to_date_str = self.format_date(self.period_end)
        front.insert_text(Point(494, 92), to_date_str, fontsize=12, fontname="Cour")
        if self.not_observed:
            front.insert_text(Point(77, 112), "X", fontsize=12, fontname="Cour")

        self._insert_type_of_report_fields(front)

        front.insert_text(Point(361, 115), str(self.physical_readiness), fontsize=12, fontname="Cour")
        front.insert_text(Point(460, 115), str(self.billet_subcategory), fontsize=12, fontname="Cour")

        front.insert_text(Point(22, 140), self.senior_name, fontsize=12, fontname="Cour")
        front.insert_text(Point(172, 140), self.senior_grade, fontsize=12, fontname="Cour")
        front.insert_text(Point(222, 140), self.senior_desig, fontsize=12, fontname="Cour")
        front.insert_text(Point(273, 140), self.senior_title, fontsize=12, fontname="Cour")
        front.insert_text(Point(405, 140), self.senior_uic, fontsize=12, fontname="Cour")
        front.insert_text(Point(461, 140), self.senior_ssn, fontsize=12, fontname="Cour")

        front.insert_text(Point(19, 164), self.format_job(self.job), fontsize=10, fontname="Cour", lineheight=1.0)
        self._insert_duties_classification_fields(front)

    @abstractmethod
    def create_pdf(self, path: Path):
        pass

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
            Soley relying on the `wrap` or `fill` function from the textwrap module to format the comments
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
