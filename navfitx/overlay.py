import importlib.resources as resources
import pathlib
import webbrowser
from datetime import date
from pathlib import Path

import pymupdf
import typer
from pymupdf import Point
from typing_extensions import Annotated

from .models import BilletSubcategory, Fitrep, OccasionForReport, PhysicalReadiness, PromotionStatus, SummaryGroup


def get_manual_path() -> pathlib.Path:
    """
    Return a pathlib.Path to the bundled PDF.
    The file is extracted to a temporary location if the package is zipped.
    """
    with resources.path("navfitx.data", "blank_fitrep.pdf") as pdf_path:
        return pdf_path


def format_date(dt: date) -> str:
    """Formats a date object into the Fitrep date format (YYMMMDD)."""
    return dt.strftime("%y%b%d").upper()


def get_group_point(fitrep: Fitrep) -> Point:
    if fitrep.group == SummaryGroup.ACT:
        return Point(33, 64)
    if fitrep.group == SummaryGroup.TAR:
        return Point(63, 64)
    if fitrep.group == SummaryGroup.INACT:
        return Point(92, 64)
    if fitrep.group == SummaryGroup.AT_ADOS:
        return Point(120, 64)


def get_occasion_points(fitrep: Fitrep) -> set[Point]:
    ret = set()
    if OccasionForReport.PERIODIC in fitrep.occasion_for_report:
        ret.add(Point(76, 88))
    if OccasionForReport.INDIVIDUAL_DETACH in fitrep.occasion_for_report:
        ret.add(Point(157, 88))
    if OccasionForReport.SENIOR_DETACH in fitrep.occasion_for_report:
        ret.add(Point(251, 88))
    if OccasionForReport.SPECIAL in fitrep.occasion_for_report:
        ret.add(Point(329, 88))
    return ret


def get_perfomance_points(fitrep: Fitrep) -> set[Point]:
    ret = set()
    if fitrep.pro_expertise == 0:
        ret.add(Point(76, 403))
    if fitrep.pro_expertise == 1:
        ret.add(Point(205, 403))
    if fitrep.pro_expertise == 2:
        ret.add(Point(241, 403))
    if fitrep.pro_expertise == 3:
        ret.add(Point(377, 403))
    if fitrep.pro_expertise == 4:
        ret.add(Point(414, 403))
    if fitrep.pro_expertise == 5:
        ret.add(Point(551, 403))
    if fitrep.cmd_climate == 0:
        ret.add(Point(76, 486))
    if fitrep.cmd_climate == 1:
        ret.add(Point(205, 486))
    if fitrep.cmd_climate == 2:
        ret.add(Point(241, 486))
    if fitrep.cmd_climate == 3:
        ret.add(Point(377, 486))
    if fitrep.cmd_climate == 4:
        ret.add(Point(414, 486))
    if fitrep.cmd_climate == 5:
        ret.add(Point(551, 486))
    if fitrep.bearing_and_character == 0:
        ret.add(Point(76, 571))
    if fitrep.bearing_and_character == 1:
        ret.add(Point(205, 571))
    if fitrep.bearing_and_character == 2:
        ret.add(Point(241, 571))
    if fitrep.bearing_and_character == 3:
        ret.add(Point(377, 571))
    if fitrep.bearing_and_character == 4:
        ret.add(Point(414, 571))
    if fitrep.bearing_and_character == 5:
        ret.add(Point(551, 571))
    return ret


def get_perf_points_back(fitrep: Fitrep) -> set[Point]:
    ret = set()
    if fitrep.leadership == 0:
        ret.add(Point(76, 186))
    if fitrep.leadership == 1:
        ret.add(Point(205, 186))
    if fitrep.leadership == 2:
        ret.add(Point(241, 186))
    if fitrep.leadership == 3:
        ret.add(Point(377, 186))
    if fitrep.leadership == 4:
        ret.add(Point(414, 186))
    if fitrep.leadership == 5:
        ret.add(Point(551, 186))
    if fitrep.tactical_performance == 0:
        ret.add(Point(76, 281))
    if fitrep.tactical_performance == 1:
        ret.add(Point(205, 281))
    if fitrep.tactical_performance == 2:
        ret.add(Point(241, 281))
    if fitrep.tactical_performance == 3:
        ret.add(Point(377, 281))
    if fitrep.tactical_performance == 4:
        ret.add(Point(414, 281))
    if fitrep.tactical_performance == 5:
        ret.add(Point(551, 281))
    return ret


def create_fitrep_pdf(fitrep: Fitrep, path: Path) -> Path:
    """Fills out a Fitrep PDF form with the provided Fitrep data."""
    # doc = pymupdf.open("/home/tristan/Downloads/fitrep_files/navfit98_pdfs/blank_fitrep.pdf")
    blank_fitrep = get_manual_path()
    print(blank_fitrep)
    doc = pymupdf.open(str(blank_fitrep))
    front = doc[0]
    back = doc[1]
    front.insert_text(Point(22, 43), fitrep.name, fontsize=12, fontname="Cour")
    back.insert_text(Point(22, 43), fitrep.name, fontsize=12, fontname="Cour")
    front.insert_text(Point(292, 43), fitrep.rate, fontsize=12, fontname="Cour")
    back.insert_text(Point(292, 43), fitrep.rate, fontsize=12, fontname="Cour")
    front.insert_text(Point(360, 43), fitrep.desig, fontsize=12, fontname="Cour")
    back.insert_text(Point(360, 43), fitrep.desig, fontsize=12, fontname="Cour")
    front.insert_text(Point(460, 43), fitrep.ssn, fontsize=12, fontname="Cour")
    back.insert_text(Point(460, 43), fitrep.ssn, fontsize=12, fontname="Cour")
    group_point = get_group_point(fitrep)
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

    front.insert_text(Point(361, 115), fitrep.physical_readiness.value, fontsize=12, fontname="Cour")
    front.insert_text(Point(460, 115), fitrep.billet_subcategory, fontsize=12, fontname="Cour")

    front.insert_text(Point(22, 140), fitrep.senior_name, fontsize=12, fontname="Cour")
    front.insert_text(Point(172, 140), fitrep.senior_grade, fontsize=12, fontname="Cour")
    front.insert_text(Point(222, 140), fitrep.senior_desig, fontsize=12, fontname="Cour")

    for point in get_perfomance_points(fitrep):
        front.insert_text(point, "X", fontsize=12, fontname="Cour")

    front.insert_text(Point(273, 140), fitrep.senior_title, fontsize=12, fontname="Cour")
    front.insert_text(Point(405, 140), fitrep.senior_uic, fontsize=12, fontname="Cour")
    front.insert_text(Point(461, 140), fitrep.senior_ssn, fontsize=12, fontname="Cour")
    front.insert_text(Point(24, 164), fitrep.job, fontsize=10, fontname="Cour")
    front.insert_text(Point(28, 212), fitrep.duties_abbreviation, fontsize=12, fontname="Cour")
    front.insert_text(Point(146, 212), fitrep.duties_description, fontsize=10, fontname="Cour")

    counsel_date_str = format_date(fitrep.date_counseled)
    front.insert_text(Point(200, 272), counsel_date_str, fontsize=12, fontname="Cour")

    output = Path("output.pdf")
    doc.save(str(output))
    doc.close()
    return output


app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command()
def overlay(
    output: Annotated[Path, typer.Option(help="Path to the output file", dir_okay=False, writable=True)],
):
    fitrep = Fitrep(
        name="LAST, FIRST MI",
        rate="LTJG",
        desig="1840",
        ssn="123-45-6789",
        uic="12345",
        station="MYSHIP",
        group=SummaryGroup.AT_ADOS,
        promotion_status=PromotionStatus.REGULAR,
        date_reported=date(2024, 6, 1),
        occasion_for_report={
            OccasionForReport.PERIODIC,
            OccasionForReport.INDIVIDUAL_DETACH,
            OccasionForReport.SPECIAL,
            OccasionForReport.SENIOR_DETACH,
        },
        period_start=date(2023, 12, 1),
        period_end=date(2024, 5, 31),
        not_observed=True,
        physical_readiness=PhysicalReadiness.PASS,
        billet_subcategory=BilletSubcategory.NA,
        senior_name="SENIOR, FIRST MI",
        senior_grade="CDR",
        senior_desig="1840",
        senior_title="CO",
        senior_uic="54321",
        senior_ssn="987-65-4321",
        job="blah blah blah",
        duties_abbreviation="DIVO",
        duties_description="Responsible for leading the division in all aspects.",
        date_counseled=date(2024, 5, 15),
        counselor="LAST, FIRST MI",
        pro_expertise=3,
        bearing_and_character=4,
        cmd_climate=4,
        teamwork=5,
        accomp_and_initiative=4,
        leadership=5,
        tactical_performance=3,
    )
    output = create_fitrep_pdf(fitrep, output)
    webbrowser.open(str(output))
