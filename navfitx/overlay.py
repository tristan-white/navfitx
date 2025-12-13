import textwrap
from datetime import date
from pathlib import Path

import pymupdf
from pymupdf import Point

from navfitx.utils import get_blank_report_path

from .models import (
    Fitrep,
    PromotionRecommendation,
    SummaryGroup,
)


def wrap_duty_desc(text: str) -> str:
    """
    The duties description is weird because the user manual says the constraint on this
    box is "up to 334 alhphanumeric characters without spaces".
    In practice, there are 4 lines. The first can have up to 69 characters (not including newline),
    and the next three can have up to 91 charaters (not including newline).
    """
    text = 22 * " " + text
    text = textwrap.fill(text, width=91)
    return text


def format_job(text: str) -> str:
    """Formats the 'Command employment and command achievements' to fit within the constraints of the FITREP form."""
    text = textwrap.fill(text, width=91)
    return text


def format_date(dt: date | None) -> str:
    """Formats a date object into the Fitrep date format (YYMMMDD)."""
    if not dt:
        return ""
    return dt.strftime("%y%b%d").upper()


def get_group_point(fitrep: Fitrep) -> Point | None:
    if fitrep.group == SummaryGroup.ACT:
        return Point(33, 64)
    if fitrep.group == SummaryGroup.TAR:
        return Point(63, 64)
    if fitrep.group == SummaryGroup.INACT:
        return Point(92, 64)
    if fitrep.group == SummaryGroup.ATADSW:
        return Point(120, 64)
    return None


def get_occasion_points(fitrep: Fitrep) -> set[Point]:
    ret: set[Point] = set()
    if fitrep.periodic:
        ret.add(Point(76, 88))
    if fitrep.det_indiv:
        ret.add(Point(157, 88))
    if fitrep.det_rs:
        ret.add(Point(251, 88))
    if fitrep.special:
        ret.add(Point(329, 88))
    return ret


def get_perfomance_points(fitrep: Fitrep) -> set[Point]:
    ret = set()
    match fitrep.pro_expertise:
        case 0:
            ret.add(Point(76, 403))
        case 1:
            ret.add(Point(205, 403))
        case 2:
            ret.add(Point(241, 403))
        case 3:
            ret.add(Point(377, 403))
        case 4:
            ret.add(Point(414, 403))
        case 5:
            ret.add(Point(551, 403))
    match fitrep.cmd_climate:
        case 0:
            ret.add(Point(76, 486))
        case 1:
            ret.add(Point(205, 486))
        case 2:
            ret.add(Point(241, 486))
        case 3:
            ret.add(Point(377, 486))
        case 4:
            ret.add(Point(414, 486))
        case 5:
            ret.add(Point(551, 486))
    match fitrep.bearing_and_character:
        case 0:
            ret.add(Point(76, 571))
        case 1:
            ret.add(Point(205, 571))
        case 2:
            ret.add(Point(241, 571))
        case 3:
            ret.add(Point(377, 571))
        case 4:
            ret.add(Point(414, 571))
        case 5:
            ret.add(Point(551, 571))
    match fitrep.teamwork:
        case 0:
            ret.add(Point(76, 655))
        case 1:
            ret.add(Point(205, 655))
        case 2:
            ret.add(Point(241, 655))
        case 3:
            ret.add(Point(377, 655))
        case 4:
            ret.add(Point(414, 655))
        case 5:
            ret.add(Point(551, 655))
    match fitrep.accomp_and_initiative:
        case 0:
            ret.add(Point(76, 739))
        case 1:
            ret.add(Point(205, 739))
        case 2:
            ret.add(Point(241, 739))
        case 3:
            ret.add(Point(377, 739))
        case 4:
            ret.add(Point(414, 739))
        case 5:
            ret.add(Point(551, 739))
    return ret


def get_perf_points_back(fitrep: Fitrep) -> set[Point]:
    ret = set()
    match fitrep.leadership:
        case 0:
            ret.add(Point(76, 186))
        case 1:
            ret.add(Point(205, 186))
        case 2:
            ret.add(Point(241, 186))
        case 3:
            ret.add(Point(377, 186))
        case 4:
            ret.add(Point(414, 186))
        case 5:
            ret.add(Point(551, 186))

    match fitrep.tactical_performance:
        case 0:
            ret.add(Point(76, 282))
        case 1:
            ret.add(Point(205, 282))
        case 2:
            ret.add(Point(241, 282))
        case 3:
            ret.add(Point(377, 282))
        case 4:
            ret.add(Point(414, 282))
        case 5:
            ret.add(Point(551, 282))
    return ret


def get_promo_rec_point(fitrep: Fitrep) -> Point:
    """Returns a Point where 'X' should be drawn given the fitrep's
    Promotion Reccomendation.
    """
    match fitrep.indiv_promo_rec:
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


def create_eval_pdf():
    """Fills out an Eval PDF with the provided Eval data.

    TODO: Implement this function.
    """
    pass


def create_fitrep_pdf(fitrep: Fitrep, path: Path) -> None:
    """Fills out a FITREP PDF report with the provided FITREP data."""
    blank_fitrep = get_blank_report_path("fitrep")
    doc = pymupdf.open(str(blank_fitrep))
    meta = doc.metadata
    meta["title"] = f"FITREP for {fitrep.name}"
    doc.set_metadata(meta)
    front = doc[0]
    back = doc[1]
    front.insert_text(Point(22, 43), fitrep.name, fontsize=12, fontname="cour")
    back.insert_text(Point(22, 43), fitrep.name, fontsize=12, fontname="Cour")
    front.insert_text(Point(292, 43), fitrep.grade, fontsize=12, fontname="Cour")
    back.insert_text(Point(292, 43), fitrep.grade, fontsize=12, fontname="Cour")
    front.insert_text(Point(360, 43), fitrep.desig, fontsize=12, fontname="Cour")
    back.insert_text(Point(360, 43), fitrep.desig, fontsize=12, fontname="Cour")
    front.insert_text(Point(460, 43), fitrep.ssn, fontsize=12, fontname="Cour")
    back.insert_text(Point(460, 43), fitrep.ssn, fontsize=12, fontname="Cour")
    if group_point := get_group_point(fitrep):
        front.insert_text(group_point, "X", fontsize=12, fontname="Cour")
    front.insert_text(Point(170, 67), fitrep.uic, fontsize=12, fontname="Cour")
    front.insert_text(Point(223, 67), fitrep.station, fontsize=12, fontname="Cour")
    front.insert_text(Point(416, 67), fitrep.promotion_status, fontsize=12, fontname="Cour")
    report_date_str = format_date(fitrep.date_reported)
    front.insert_text(Point(496, 67), report_date_str, fontsize=12, fontname="Cour")

    for point in get_occasion_points(fitrep):
        front.insert_text(point, "X", fontsize=12, fontname="Cour")

    from_date_str = format_date(fitrep.period_start)
    front.insert_text(Point(395, 92), from_date_str, fontsize=12, fontname="Cour")
    to_date_str = format_date(fitrep.period_end)
    front.insert_text(Point(494, 92), to_date_str, fontsize=12, fontname="Cour")
    if fitrep.not_observed:
        front.insert_text(Point(77, 112), "X", fontsize=12, fontname="Cour")

    front.insert_text(Point(156, 112), "X", fontsize=12, fontname="Cour")

    front.insert_text(Point(361, 115), fitrep.physical_readiness, fontsize=12, fontname="Cour")
    front.insert_text(Point(460, 115), fitrep.billet_subcategory, fontsize=12, fontname="Cour")

    front.insert_text(Point(22, 140), fitrep.senior_name, fontsize=12, fontname="Cour")
    front.insert_text(Point(172, 140), fitrep.senior_grade, fontsize=12, fontname="Cour")
    front.insert_text(Point(222, 140), fitrep.senior_desig, fontsize=12, fontname="Cour")
    front.insert_text(Point(273, 140), fitrep.senior_title, fontsize=12, fontname="Cour")
    front.insert_text(Point(405, 140), fitrep.senior_uic, fontsize=12, fontname="Cour")
    front.insert_text(Point(461, 140), fitrep.senior_ssn, fontsize=12, fontname="Cour")

    front.insert_text(Point(24, 164), format_job(fitrep.job), fontsize=10, fontname="Cour", lineheight=1.0)
    front.insert_text(Point(28, 212), fitrep.duties_abbreviation, fontsize=12, fontname="Cour")

    duties_desc = wrap_duty_desc(fitrep.duties_description)
    front.insert_text(Point(24, 212), duties_desc, fontsize=10, fontname="Cour", lineheight=1.0)

    for point in get_perfomance_points(fitrep):
        front.insert_text(point, "X", fontsize=12, fontname="Cour")

    counsel_date_str = format_date(fitrep.date_counseled)
    front.insert_text(Point(200, 272), counsel_date_str, fontsize=12, fontname="Cour")

    front.insert_text(Point(279, 272), fitrep.counselor, fontsize=12, fontname="Cour")

    for point in get_perf_points_back(fitrep):
        back.insert_text(point, "X", fontsize=12, fontname="Cour")

    back.insert_text(
        Point(34, 354),
        Fitrep.wrap_text(fitrep.comments, 92),
        fontsize=9.2,
        fontname="Cour",
    )

    if fitrep.indiv_promo_rec is not None:
        back.insert_text(get_promo_rec_point(fitrep), "X", fontsize=12, fontname="Cour")

    back.insert_text(Point(388, 586), fitrep.senior_address, fontsize=9, fontname="Cour", lineheight=1.1)
    back.insert_text(Point(105, 694), fitrep.member_trait_avg(), fontsize=12, fontname="Cour")
    back.insert_text(Point(240, 694), fitrep.summary_group_avg(), fontsize=12, fontname="Cour")
    back.insert_text(Point(370, 300), textwrap.fill(fitrep.career_rec_1, 13), fontsize=10, fontname="Cour")
    back.insert_text(Point(467, 300), textwrap.fill(fitrep.career_rec_2, 13), fontsize=10, fontname="Cour")

    doc.save(str(path))
    doc.close()
