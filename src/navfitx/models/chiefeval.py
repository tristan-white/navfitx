import textwrap
from pathlib import Path

from pydantic import field_validator, model_validator
from pymupdf import Point
from sqlmodel import Field

from navfitx.utils import wrap_duty_desc

from .enums import DutyStatus, PromotionRecommendation
from .models import Report


class ChiefEval(Report, table=True):
    """
    A SQLModel to represent Chief EVAL reports.
    """

    doc_type: str = "chiefeval"
    rate: str = ""
    det_rs: bool = False
    ops_cdr: bool = False

    trait1: int | None = Field(None, ge=0, le=5, title="Technical Mastery")
    trait2: int | None = Field(None, ge=0, le=5, title="Institutional Expertise")
    trait3: int | None = Field(None, ge=0, le=5, title="Professionalism")
    trait4: int | None = Field(None, ge=0, le=5, title="Integrity")
    trait5: int | None = Field(None, ge=0, le=5, title="Accountability")
    trait6: int | None = Field(None, ge=0, le=5, title="Leadership")
    trait7: int | None = Field(None, ge=0, le=5, title="Teamwork")

    def trait_values(self) -> list[int | None]:
        return [
            self.trait1,
            self.trait2,
            self.trait3,
            self.trait4,
            self.trait5,
            self.trait6,
            self.trait7,
        ]

    @field_validator(
        "trait1",
        "trait2",
        "trait3",
        "trait4",
        "trait5",
        "trait6",
        "trait7",
    )
    @classmethod
    def validate_traits(cls, value: int | None) -> int | None:
        if value is None:
            raise ValueError("Trait value must be set or marked NOB.")
        return value

    @model_validator(mode="after")
    def validate_nob(self):
        if self.not_observed:
            for trait in self.trait_values():
                if trait != 0:
                    raise ValueError("If 'Not Observed' is checked, all traits must be marked as NOB (0).")
        return self

    @model_validator(mode="after")
    def validate_indiv_promo_rec(self):
        observed = 0
        for trait in self.trait_values():
            if trait is not None and trait > 0:
                observed += 1
        if observed <= 3 and self.indiv_promo_rec is not None:
            raise ValueError("Promotion recommendation should not be set if 3 or fewer traits are observed.")
        if observed > 3 and self.indiv_promo_rec is None:
            raise ValueError("Promotion recommendation must be set if more than 3 traits are observed.")
        return self

    @model_validator(mode="after")
    def validate_special(self):
        if self.special and (self.periodic or self.det_indiv or self.det_rs):
            raise ValueError("The occasion for report cannot have 'Special' checked if any other occasion is selected.")
        return self

    @model_validator(mode="after")
    def validate_type_of_report(self):
        if self.ops_cdr and (self.regular or self.concurrent):
            raise ValueError("Report cannot be marked both as 'OpsCdr' and another Type of Report selection")
        if not self.ops_cdr and not self.regular and not self.concurrent:
            raise ValueError("Type of Report must be marked.")
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
            front.insert_text(Point(114, 88), "X", fontsize=12, fontname="Cour")
        if self.det_indiv:
            front.insert_text(Point(190, 88), "X", fontsize=12, fontname="Cour")
        if self.det_rs:
            front.insert_text(Point(280, 88), "X", fontsize=12, fontname="Cour")
        if self.special:
            front.insert_text(Point(338, 88), "X", fontsize=12, fontname="Cour")

    def _insert_type_of_report_fields(self, front) -> None:
        if self.regular:
            front.insert_text(Point(156, 112), "X", fontsize=12, fontname="Cour")
        if self.concurrent:
            front.insert_text(Point(225, 112), "X", fontsize=12, fontname="Cour")
        if self.ops_cdr:
            front.insert_text(Point(293, 112), "X", fontsize=12, fontname="Cour")

    def _insert_duties_classification_fields(self, front) -> None:
        front.insert_text(Point(22, 212), self.duties_abbreviation, fontsize=12, fontname="Cour")
        duties_desc = wrap_duty_desc(self.duties_description)
        front.insert_text(Point(18, 212), duties_desc, fontsize=10, fontname="Cour", lineheight=1.0)

    def create_pdf(self, path: Path) -> None:
        doc, front, back = self._open_report_pdf("chief")
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
        match self.trait7:
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

        back.insert_text(Point(388, 585), self.senior_address, fontsize=9, fontname="Cour", lineheight=1.0)
        back.insert_text(Point(105, 694), self.member_trait_avg(), fontsize=12, fontname="Cour")
        back.insert_text(Point(240, 694), self.summary_group_avg(), fontsize=12, fontname="Cour")
        back.insert_text(Point(370, 300), textwrap.fill(self.career_rec_1, 13), fontsize=10, fontname="Cour")
        back.insert_text(Point(467, 300), textwrap.fill(self.career_rec_2, 13), fontsize=10, fontname="Cour")
        doc.save(str(path))
        doc.close()
