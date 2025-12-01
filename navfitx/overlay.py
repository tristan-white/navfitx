import textwrap
import webbrowser
from datetime import date
from pathlib import Path

import pymupdf
import typer
from pymupdf import Point
from typing_extensions import Annotated

from navfitx.utils import get_blank_report_path

from .models import (
    BilletSubcategory,
    Fitrep,
    OccasionForReport,
    PhysicalReadiness,
    PromotionRecommendation,
    PromotionStatus,
    SummaryGroup,
    TypeOfReport,
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
    if fitrep.group == SummaryGroup.AT_ADOS:
        return Point(120, 64)


def get_occasion_points(fitrep: Fitrep) -> set[Point]:
    ret: set[Point] = set()
    if OccasionForReport.PERIODIC == fitrep.occasion_for_report:
        ret.add(Point(76, 88))
    if OccasionForReport.INDIVIDUAL_DETACH == fitrep.occasion_for_report:
        ret.add(Point(157, 88))
    if OccasionForReport.SENIOR_DETACH == fitrep.occasion_for_report:
        ret.add(Point(251, 88))
    if OccasionForReport.SPECIAL == fitrep.occasion_for_report:
        ret.add(Point(329, 88))
    return ret


# def get_type_of_report_point(fitrep: Fitrep) -> Point:
#     if TypeOfReport.REGULAR == fitrep.type_of_report:
#         return Point(76, 130)


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
    match fitrep.leadership:
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
        case PromotionRecommendation.NOB:
            return Point(101, 606)
        case PromotionRecommendation.SIGNIFICANT_PROBLEMS:
            return Point(151, 606)
        case PromotionRecommendation.PROGRESSING:
            return Point(202, 606)
        case PromotionRecommendation.PROMOTABLE:
            return Point(253, 606)
        case PromotionRecommendation.MUST_PROMOTE:
            return Point(304, 606)
        case PromotionRecommendation.EARLY_PROMOTE:
            return Point(355, 606)
        case _:
            raise Exception()


def create_eval_pdf():
    """Fills out an Eval PDF with the provided Eval data."""
    pass
    # blank_eval = get_blank_report_path("eval")
    # doc = pymupdf.open(str(blank_eval))
    # front = doc[0]
    # back = doc[1]


def create_fitrep_pdf(fitrep: Fitrep, path: Path) -> None:
    """Fills out a FITREP PDF report with the provided FITREP data."""
    blank_fitrep = get_blank_report_path("fitrep")
    doc = pymupdf.open(str(blank_fitrep))
    front = doc[0]
    back = doc[1]
    front.insert_text(Point(22, 43), fitrep.name, fontsize=12, fontname="Cour")
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

    front.insert_text(Point(24, 164), fitrep.job, fontsize=10, fontname="Cour", lineheight=1.0)
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
        fitrep.comments,
        fontsize=9.2,
        fontname="Cour",
    )

    back.insert_text(Point(388, 586), fitrep.senior_address, fontsize=9, fontname="Cour", lineheight=1.1)
    back.insert_text(Point(105, 694), fitrep.member_trait_avg(), fontsize=12, fontname="Cour")
    back.insert_text(Point(240, 694), fitrep.summary_group_avg(), fontsize=12, fontname="Cour")
    back.insert_text(Point(370, 300), fitrep.career_rec_1, fontsize=10, fontname="Cour")
    back.insert_text(Point(467, 300), fitrep.career_rec_2, fontsize=10, fontname="Cour")

    doc.save(str(path))
    doc.close()


app = typer.Typer(no_args_is_help=True, add_completion=False)


def format_comments(txt: str) -> str:
    """
    Format the Comments on Performance text so that it conforms to the constraints:
    - Max of 92 chars per line (not including newlines)
    - Max of 18 lines

    Note:
        Soley using the wrap or fill function from the textwrap module to format the comments completely
        isn't quite sufficient because it doesn't handle appropriately handle cases when users want
        to add newlines to the comments. The textwrap module by default eliminates newlines. This can be
        disabled, but then newlines are counted as characters that count towards the character limit for
        each line. This function handles each situation appropriately.
    """
    parts = txt.split("\n")
    all_lines = []
    for part in parts:
        lines = textwrap.wrap(part, 92)
        if not lines:
            lines = [""]
        all_lines.extend(lines)
    return "\n".join(all_lines)


@app.command()
def overlay_fitrep(
    output: Annotated[Path, typer.Option(help="Path to the output file", dir_okay=False, writable=True)],
):
    comments = (
        "*MY #5 OF 19 LTJGs AMONG VERY COMPETITIVE PEERS! EXTREMELY TALENTED LEADER AND DEVELOPER!*\n\n"
        "-MULTIDISCIPLINARY EXPERT. Actively identifies rare, high-demand skills to address key expertise gaps. Utilizes self-taught methods to reverse-engineer computer hardware, overcoming obstacles to critical vulnerability research and exploit development essential to mission success. Developed a solution to a major data analytics problem that had significantly impacted mission operations.\n"
        "-DISTINGUISHED TECHNICAL LEADER. Hand-selected to join a team of senior developers at a partner site; promptly received recognition from partner's Commanding Officer for exceptional contributions, then solicited to apply for an O3 billet despite current grade of O2. Following these successes, chosen by leadership to be a Division Officer to lead Sailors at partner site, enhancing department's capacity to adapt to evolving requirements.\n"
        "-PROACTIVE LEARNER. Dedicated substantial personal time to obtain the industry's leading certificate in offensive security; resulted in qualification of key role within partner organization and increased department's capacity to meet operational requirements.\n\n"
        "PRESS 100 NOW"
    )
    lines = format_comments(comments)
    fitrep = Fitrep(
        name="WHITE, TRISTAN K",
        rate="LTJG",
        desig="1840",
        ssn="123-45-6789",
        uic="46439",
        station="NAVCYBERWARDEVGRU",
        group=SummaryGroup.AT_ADOS,
        promotion_status=PromotionStatus.REGULAR,
        date_reported=date(2022, 9, 9),
        occasion_for_report={
            OccasionForReport.PERIODIC,
            OccasionForReport.INDIVIDUAL_DETACH,
            OccasionForReport.SPECIAL,
            OccasionForReport.SENIOR_DETACH,
        },
        period_start=date(2024, 5, 27),
        period_end=date(2025, 2, 28),
        # not_observed=True,
        physical_readiness=PhysicalReadiness.PASS,
        billet_subcategory=BilletSubcategory.NA,
        type_of_report={TypeOfReport.REGULAR},
        senior_name="LAST, FI MI",
        senior_grade="CAPT",
        senior_desig="1810",
        senior_title="CO",
        senior_uic="46439",
        senior_ssn="123-45-6789",
        job="Conducts information and Cyber Warfare R&D, intelligence, and operations. Develops deep\ntechnial understanding of adversary systems, discovers vulnerabilities, and builds\ncountermeasures using rapid prototyping and acquisition authorities.",
        duties_abbreviation="12345678901234",
        duties_description="Division Officer-3. Led four sailors in daily execution of Naval and Joint missions. Cyberspace Operations (CO) Developer-12. Researches technologies and develops custom cyber tools to support Navy and national level mission priorities. Cyber Operator Trainee-2. PFA: CY2024.",
        date_counseled=date(2024, 5, 15),
        counselor="LAST, FIRST MI",
        pro_expertise=3,
        bearing_and_character=4,
        cmd_climate=4,
        teamwork=5,
        accomp_and_initiative=4,
        leadership=5,
        tactical_performance=3,
        career_rec_1="1234567890123\n1234567",
        career_rec_2="1234567890123\n1234567",
        comments=lines,
        senior_address="12345\n12345\n12345\n12345\n12345",
    )
    create_fitrep_pdf(fitrep, output)
    webbrowser.open(str(output))
