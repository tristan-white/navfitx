import textwrap
from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, StringConstraints, field_validator, model_validator
from pymupdf import Point
from sqlmodel import Field

from navfitx.utils import wrap_duty_desc

from .enums import DutyStatus, PromotionRecommendation, RetentionRecommendation
from .models import Report


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

    trait1: int | None = Field(None, title="Professional Knowledge", ge=0, le=5)
    trait2: int | None = Field(None, title="Quality of Work", ge=0, le=5)
    trait3: int | None = Field(None, title="Command or Organizational Climate", ge=0, le=5)
    trait7: int | None = Field(None, title="Military Bearing/Character", ge=0, le=5)
    trait5: int | None = Field(None, title="Personal Job Accomplishment/Initiative", ge=0, le=5)
    trait4: int | None = Field(None, title="Teamwork", ge=0, le=5)
    trait6: int | None = Field(None, title="Leadership", ge=0, le=5)

    # 182 char constraint from NAVFIT98 user manual
    # TODO: confirm NAVFIT98 actually only allows 182 chars
    achievements: Annotated[str, StringConstraints(min_length=1, max_length=182)] = Field(
        title="Qualifications/Achievements", default=""
    )
    retain: int | None = Field(None)

    @field_validator("achievements")
    @classmethod
    def validate_achievements(cls, achievements: str) -> str:
        wrapped = cls.wrap_text(achievements, 91)
        if len(wrapped.split("\n")) > 2:
            lines = wrapped.split("\n")
            achievements = "\n".join(lines[:2])
        return achievements

    @model_validator(mode="after")
    def validate_occasion_for_report(self):
        if not (self.periodic or self.det_indiv or self.special or self.prom_frock):
            raise ValueError("Occasion for Report must be marked.")
        return self

    def get_group_point(self) -> Point | None:
        if self.group == DutyStatus.ACT:
            return Point(33, 64)
        if self.group == DutyStatus.TAR:
            return Point(63, 64)
        if self.group == DutyStatus.INACT:
            return Point(92, 64)
        if self.group == DutyStatus.ATADSW:
            return Point(120, 64)
        return None

    def _insert_occasion_for_report_fields(self, front) -> None:
        if self.periodic:
            front.insert_text(Point(76, 88), "X", fontsize=12, fontname="Cour")
        if self.det_indiv:
            front.insert_text(Point(157, 88), "X", fontsize=12, fontname="Cour")
        if self.prom_frock:
            front.insert_text(Point(251, 88), "X", fontsize=12, fontname="Cour")
        if self.special:
            front.insert_text(Point(329, 88), "X", fontsize=12, fontname="Cour")

    def _insert_type_of_report_fields(self, front) -> None:
        if self.regular:
            front.insert_text(Point(156, 112), "X", fontsize=12, fontname="Cour")
        if self.concurrent:
            front.insert_text(Point(250, 112), "X", fontsize=12, fontname="Cour")

    def _insert_duties_classification_fields(self, front) -> None:
        front.insert_text(Point(28, 212), self.duties_abbreviation, fontsize=12, fontname="Cour")
        duties_desc = wrap_duty_desc(self.duties_description)
        front.insert_text(Point(24, 212), duties_desc, fontsize=10, fontname="Cour", lineheight=1.0)

    def create_pdf(self, path: Path) -> None:
        doc, front, back = self._open_report_pdf("eval")
        self._insert_common_report_fields(front, back)

        match self.trait1:
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
        match self.trait2:
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
        match self.trait3:
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
        match self.trait4:
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
        match self.trait5:
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

        match self.trait6:
            case 0:
                back.insert_text(Point(76, 124), "X", fontsize=12, fontname="Cour")
            case 1:
                back.insert_text(Point(205, 124), "X", fontsize=12, fontname="Cour")
            case 2:
                back.insert_text(Point(241, 124), "X", fontsize=12, fontname="Cour")
            case 3:
                back.insert_text(Point(377, 124), "X", fontsize=12, fontname="Cour")
            case 4:
                back.insert_text(Point(414, 124), "X", fontsize=12, fontname="Cour")
            case 5:
                back.insert_text(Point(551, 124), "X", fontsize=12, fontname="Cour")
        match self.trait7:
            case 0:
                back.insert_text(Point(76, 246), "X", fontsize=12, fontname="Cour")
            case 1:
                back.insert_text(Point(205, 246), "X", fontsize=12, fontname="Cour")
            case 2:
                back.insert_text(Point(241, 246), "X", fontsize=12, fontname="Cour")
            case 3:
                back.insert_text(Point(377, 246), "X", fontsize=12, fontname="Cour")
            case 4:
                back.insert_text(Point(414, 246), "X", fontsize=12, fontname="Cour")
            case 5:
                back.insert_text(Point(551, 246), "X", fontsize=12, fontname="Cour")

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

        match self.retain:
            case RetentionRecommendation.RECOMMENDED.value:
                back.insert_text(Point(540, 583), "X", fontsize=12, fontname="Cour")
            case RetentionRecommendation.NOT_RECOMMENDED.value:
                back.insert_text(Point(460, 583), "X", fontsize=12, fontname="Cour")

        back.insert_text(Point(47, 304), self.member_trait_avg(), fontsize=12, fontname="Cour")
        # back.insert_text(Point(240, 694), self.summary_group_avg(), fontsize=12, fontname="Cour")
        back.insert_text(Point(121, 292), textwrap.fill(self.career_rec_1, 13), fontsize=10, fontname="Cour")
        back.insert_text(Point(227, 292), textwrap.fill(self.career_rec_2, 13), fontsize=10, fontname="Cour")
        back.insert_text(
            Point(34, 338), self.wrap_text(self.comments, 92), fontsize=9.2, fontname="Cour", lineheight=1.11
        )
        back.insert_text(Point(389, 609), self.senior_address, fontsize=9, fontname="Cour", lineheight=1.0)
        doc.save(str(path))
        doc.close()


class ChiefEvalTrait(BaseModel):
    """
    Chief Evaluation trait model.

    Attributes:
        order (int): The order of the trait as it appears on the form, starting from 1.
        name: (str): The name of the trait, all lowercase.
        grade_descriptions (dict[int, str]): A dictionary mapping trait scores (0-5) to their corresponding descriptions.
    """

    order: int
    name: str
    grade_descriptions: dict[int, str]
