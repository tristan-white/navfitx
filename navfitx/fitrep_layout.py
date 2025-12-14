import webbrowser
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import typer
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen.canvas import Canvas
from typing_extensions import Annotated

from navfitx.boxes import Box, Bullets, Checkbox, Multiline, MultilineCentered, String
from navfitx.constants import MARGIN_BOTTOM, MARGIN_LEFT, MARGIN_RIGHT, MARGIN_SIDES, MARGIN_TOP
from navfitx.models import Fitrep, PromotionStatus, SummaryGroup


def make_box_to_right(box: Box, width: float) -> Box:
    """
    Returns a new box of width `width` whose left border overlaps the right border of `box`.

    Args:
        box (Box): The box to the left.
        width (float): The width of the new box.
    """
    return Box(id=box.id + 1, bl=box.br, tr=(box.tr[0] + width, box.tr[1]))


def make_box_below(box: Box, width: float, height: float) -> Box:
    """
    Makes a box with a top border that overlaps with the bottom border of `box`.

    Args:
        box (Box): The box above.
        height (float): The height of the new box.
        width (float): The width of the new box.
    """
    return Box(id=box.id + 1, bl=(box.bl[0], box.bl[1] - height), tr=(box.bl[0] + width, box.br[1]))


def update_name(fitrep: Fitrep, comp: String) -> None:
    comp.text = fitrep.name


def update_rate(fitrep: Fitrep, comp: String) -> None:
    comp.text = fitrep.grade


def update_desig(fitrep: Fitrep, comp: String) -> None:
    comp.text = fitrep.desig


def update_ssn(fitrep: Fitrep, comp: String) -> None:
    comp.text = fitrep.ssn


def update_group_act(fitrep: Fitrep, comp: Checkbox) -> None:
    comp.checked = fitrep.group == SummaryGroup.ACT


def update_group_tar(fitrep: Fitrep, comp: Checkbox) -> None:
    comp.checked = fitrep.group == SummaryGroup.TAR


def update_group_inact(fitrep: Fitrep, comp: Checkbox) -> None:
    comp.checked = fitrep.group == SummaryGroup.INACT


def update_group_at_adsw_265(fitrep: Fitrep, comp: Checkbox) -> None:
    comp.checked = fitrep.group == SummaryGroup.ATADSW


def update_uic(fitrep: Fitrep, comp: String) -> None:
    comp.text = fitrep.uic


def update_station(fitrep: Fitrep, comp: String) -> None:
    comp.text = fitrep.station


def update_promotion_status(fitrep: Fitrep, comp: String) -> None:
    if fitrep.promotion_status:
        comp.text = fitrep.promotion_status.value


def update_date_reported(fitrep: Fitrep, comp: String) -> None:
    if fitrep.date_reported:
        comp.text = fitrep.date_reported.strftime("%y%b%d").upper()


def update_occasion_periodic(fitrep: Fitrep, comp: Checkbox) -> None:
    comp.checked = fitrep.periodic


def update_occasion_detachment_individual(fitrep: Fitrep, comp: Checkbox) -> None:
    comp.checked = fitrep.det_indiv


def update_occasion_detachment_reporting_senior(fitrep: Fitrep, comp: Checkbox) -> None:
    comp.checked = fitrep.det_rs


def update_occasion_special(fitrep: Fitrep, comp: Checkbox) -> None:
    comp.checked = fitrep.special


def update_period_start(fitrep: Fitrep, comp: String) -> None:
    if fitrep.period_start:
        comp.text = fitrep.period_start.strftime("%y%b%d").upper()


def update_period_end(fitrep: Fitrep, comp: String) -> None:
    if fitrep.period_end:
        comp.text = fitrep.period_end.strftime("%y%b%d").upper()


def update_senior_name(fitrep: Fitrep, comp: String) -> None:
    comp.text = fitrep.senior_name


def update_senior_grade(fitrep: Fitrep, comp: String) -> None:
    comp.text = fitrep.senior_grade


def update_senior_desig(fitrep: Fitrep, comp: String) -> None:
    comp.text = fitrep.senior_desig


def update_senior_uic(fitrep: Fitrep, comp: String) -> None:
    comp.text = fitrep.senior_uic


def update_senior_ssn(fitrep: Fitrep, comp: String) -> None:
    comp.text = fitrep.senior_ssn


def update_job(fitrep: Fitrep, comp: String) -> None:
    comp.text = fitrep.job


def update_duties_abbreviation(fitrep: Fitrep, comp: String) -> None:
    comp.text = fitrep.duties_abbreviation


def update_duties_description(fitrep: Fitrep, comp: String) -> None:
    comp.text = fitrep.duties_description


def update_date_counseled(fitrep: Fitrep, comp: String) -> None:
    if fitrep.date_counseled:
        comp.text = fitrep.date_counseled.strftime("%y%b%d").upper()
    else:
        comp.text = ""


def update_counselor(fitrep: Fitrep, comp: String) -> None:
    comp.text = fitrep.counselor


def update_pe_0(fitrep: Fitrep, comp: Checkbox) -> None:
    comp.checked = fitrep.pro_expertise == 0


def update_pe_1(fitrep: Fitrep, comp: Checkbox) -> None:
    comp.checked = fitrep.pro_expertise == 1


def update_pe_2(fitrep: Fitrep, comp: Checkbox) -> None:
    comp.checked = fitrep.pro_expertise == 2


def update_pe_3(fitrep: Fitrep, comp: Checkbox) -> None:
    comp.checked = fitrep.pro_expertise == 3


def update_pe_4(fitrep: Fitrep, comp: Checkbox) -> None:
    comp.checked = fitrep.pro_expertise == 4


def update_pe_5(fitrep: Fitrep, comp: Checkbox) -> None:
    comp.checked = fitrep.pro_expertise == 5


# Row 0
box_0 = Box(
    id=0,
    bl=(MARGIN_LEFT, LETTER[1] - MARGIN_TOP - 23),
    tr=(289, LETTER[1] - MARGIN_TOP),
    comps=[
        String(text="1. Name (Last, First MI Suffix)"),
        String(text="", update_fn=update_name, fontname="Courier", y=20, x=6, size=12),
    ],
)

box_1 = make_box_to_right(box_0, 66)
box_1.comps.append(String(text="2. Rank"))
box_1.comps.append(String(text="", update_fn=update_rate, fontname="Courier", y=21, x=6, size=12))

box_2 = make_box_to_right(box_1, 101)
box_2.comps.append(String(text="3. Desig"))
box_2.comps.append(String(text="", update_fn=update_desig, fontname="Courier", y=21, x=6, size=12))

box_3 = make_box_to_right(box_2, LETTER[0] - MARGIN_RIGHT - box_2.br[0])
box_3.comps.append(String(text="4. SSN"))
box_3.comps.append(String(text="", update_fn=update_ssn, fontname="Courier", y=21, x=6, size=12))

# Row 1
box_4 = make_box_below(box_0, 149, box_0.height - 1)
box_4.comps.append(String(text="5.   ACT    TAR      INACT   AT/ADSW/265", size=7, y=8))
box_4.comps.append(Checkbox(y=2, x=-134, update_fn=update_group_act))
box_4.comps.append(Checkbox(y=2, x=-109, update_fn=update_group_tar))
box_4.comps.append(Checkbox(y=2, x=-79, update_fn=update_group_inact))
box_4.comps.append(Checkbox(y=2, x=-46, update_fn=update_group_at_adsw_265))

box_5 = make_box_to_right(box_4, 51)
box_5.comps.append(String(text="6. UIC"))
box_5.comps.append(String(update_fn=update_uic, fontname="Courier", y=21, x=6, size=12))

box_6 = make_box_to_right(box_5, 196)
box_6.comps.append(String(text="7. Ship/Station"))
box_6.comps.append(String(update_fn=update_station, fontname="Courier", y=21, x=6, size=12))

box_7 = make_box_to_right(box_6, 79)
box_7.comps.append(String(text="8. Promotion Status"))
box_7.comps.append(String(update_fn=update_promotion_status, fontname="Courier", y=21, x=6, size=12))

box_8 = make_box_to_right(box_7, LETTER[0] - MARGIN_RIGHT - box_7.br[0])
box_8.comps.append(String(text="9. Date Reported"))
box_8.comps.append(String(update_fn=update_date_reported, fontname="Courier", y=21, x=6, size=12))

# Row 2
box_9 = make_box_below(box_4, 340, box_0.height + 2)
box_9.comps.append(String(text="Occasion for Report", y=9))
box_9.comps.append(Multiline(text="\n10. Periodic", no_strip=True, leading=8, y=14, x=3, size=8))
box_9.comps.append(Checkbox(y=3, x=-285, update_fn=update_occasion_periodic))
box_9.comps.append(Multiline(text="      Detachment\n11. of Individual", no_strip=True, leading=8, y=14, x=79, size=8))
box_9.comps.append(Checkbox(y=3, x=-205, update_fn=update_occasion_detachment_individual))
box_9.comps.append(
    Multiline(text="      Detachment of\n12. Reporting Senior", no_strip=True, leading=8, y=14, x=160, size=8)
)
box_9.comps.append(Checkbox(y=3, x=-110, update_fn=update_occasion_detachment_reporting_senior))
box_9.comps.append(Multiline(text="\n13. Special", no_strip=True, leading=8, y=14, x=270, size=8))
box_9.comps.append(Checkbox(y=3, x=-30, update_fn=update_occasion_special))

box_10 = make_box_to_right(box_9, LETTER[0] - MARGIN_SIDES - box_9.width)
box_10.comps.append(String(text="Period of Report", y=9))
box_10.comps.append(String(text="14. From:"))
# box_10.comps.append(String(text="15. To:"))

# Row 3
box_11 = make_box_below(box_9, 75, box_0.height)
box_11.comps.append(String(text="16. Not Observed"))
box_11.comps.append(Checkbox())

box_12 = make_box_to_right(box_11, box_9.width - box_11.width)
box_12.comps.append(String(text="Type of Report"))

box_13 = make_box_to_right(box_12, 99)
box_13.comps.append(String(text="20. Physical Readiness"))


box_14 = make_box_to_right(box_13, box_10.width - box_13.width)
box_14.comps.append(String(text="21. Billet Subcategory (if any)"))

# Row 4
box_15 = make_box_below(box_11, 151, box_0.height + 1)
box_15.comps.append(String(text="22. Reporting Senior (Last, FI  MI)"))

box_16 = make_box_to_right(box_15, 50)
box_16.comps.append(String(text="23. Grade"))

box_17 = make_box_to_right(box_16, box_16.width + 1)
box_17.comps.append(String(text="24. Desig"))

box_18 = make_box_to_right(box_17, 133)
box_18.comps.append(String(text="25. Title"))

box_19 = make_box_to_right(box_18, box_14.bl[0] - box_18.br[0])
box_19.comps.append(String(text="26. UIC"))

box_20 = make_box_to_right(box_19, LETTER[0] - MARGIN_RIGHT - box_19.br[0])
box_20.comps.append(String(text="27. SSN"))

# Row 5
box_21 = Box(id=21, bl=(MARGIN_LEFT, 601), tr=box_20.br)
box_21.comps.append(String(text="28. Command Employment and Command Achievements", y=9))

# Row 6
box_22 = make_box_below(box_21, box_21.width, 62)
box_22.comps.append(
    String(text="29. Primary/Collateral/Watchstanding duties (Enter primary duty abbreviation in box)", y=9)
)
# self.canvas.rect(box_22.tl[0] + 8, box_22.tl[1] - 23, 115, 12)

# Row 7
box_23 = make_box_below(box_22, 179, 22)
box_23_text = """
For Mid-term Counseling Use. (When completing FITREP,
enter 30 and 31 from counseling worksheet, sign 32.)
"""
box_23.comps.append(Multiline(text=box_23_text, x=3, y=-1, size=7.36))
# box_23.draw_multiline(c, box_23_text, x_off=3, y_off=-1, size=7.36)

box_24 = make_box_to_right(box_23, 79)
box_24.comps.append(String(text="30. Date Counseled", size=7, y=7, x=2))

box_25 = make_box_to_right(box_24, 138)
box_25.comps.append(String(text="31. Counselor", size=7, y=7, x=2))

box_26 = Box(id=26, bl=box_25.br, tr=box_22.br)
box_26.comps.append(String(text="32. Signature of Individual Counseled", size=7, y=7, x=2))

# tiny space
tiny_space = make_box_below(box_23, box_21.width, 2)

# Row 8
box_27 = make_box_below(tiny_space, box_21.width, 23)
box_27_text = """
PERFORMANCE TRAITS: 1.0 - Below standards/not progressing or UNSAT in any one standard; 2.0 - Does not yet meet all 3.0 standards; 3.0 - Meets all 3.0
standards; 4.0 - Exceeds most 3.0 standards; 5.0 - Meets overall criteria and most of the specific standards for 5.0. Standards are not all inclusive.
"""
box_27.comps.append(Multiline(text=box_27_text, x=2, y=2, size=8.15))
# box_27.draw_multiline(c, box_27_text, x_off=2, y_off=2, size=8.15)

# Row 9
box_28 = make_box_below(box_27, 73, 24)

box_29 = make_box_to_right(box_28, 129)
box_29_text = """\n1.0*\nBelow Standards\n"""
box_29.comps.append(MultilineCentered(text=box_29_text, x=152, y=490))
# box_29.draw_centered_multiline(c, box_29_text, x=152, y=490)

box_30 = make_box_to_right(box_29, 36)
box_30_text = """
2.0
Pro-
gressing 
"""
box_30.comps.append(MultilineCentered(text=box_30_text, x=box_30.bl[0] + box_30.width / 2, y=493))
# box_30.draw_centered_multiline(c, box_30_text, x=box_30.bl[0] + box_30.width / 2, y=493)

box_31 = make_box_to_right(box_30, 137)
box_31_text = """
3.0
Meets Standards
"""
box_31.comps.append(MultilineCentered(text=box_31_text, x=box_31.bl[0] + box_31.width / 2, y=490))
# box_31.draw_centered_multiline(c, box_31_text, x=box_31.bl[0] + box_31.width / 2, y=490)

box_32 = make_box_to_right(box_31, 36)
box_32_text = """
4.0
Above
Standards
"""
box_32.comps.append(MultilineCentered(text=box_32_text, x=box_32.bl[0] + box_32.width / 2, y=493))
# box_32.draw_centered_multiline(c, box_32_text, x=box_32.bl[0] + box_32.width / 2, y=493)

box_33 = Box(id=33, bl=box_32.br, tr=box_27.br)
box_33_text = """
5.0
Greatly Exceeds Standards
"""
box_33.comps.append(MultilineCentered(text=box_33_text, x=box_33.bl[0] + box_33.width / 2, y=490))

# row 10
box_34 = make_box_below(box_28, box_28.width, 85)
box_34_txt = "33.\nPROFESSIONAL\nEXPERTISE:\nProfessional knowledge\nproficiency, and\nqualifications"
box_34.comps.append(Multiline(text=box_34_txt))
box_34.comps.append(Checkbox(update_fn=update_pe_0))

box_35 = make_box_below(box_29, box_29.width, box_34.height)
box_35_text = """-Lacks basic professional knowledge to
perform effectively
-Cannot apply basic skills
-Fails to develop professionally or
achieve timely qualifications
"""
box_35.comps.append(Bullets(text=box_35_text))
box_35.comps.append(Checkbox(update_fn=update_pe_1))

box_36 = make_box_below(box_30, box_30.width, box_34.height)
box_36_text = "-\n\n-\n\n-"
box_36.comps.append(Multiline(text=box_36_text))
box_36.comps.append(Checkbox(update_fn=update_pe_2))

box_37 = make_box_below(box_31, box_31.width, box_34.height)
box_37_text = """- Has thorough professional knowledge
- Competently performs both routine and
new tasks
- Steadily improves skills, achieves timely
qualifications
"""
box_37.comps.append(Bullets(text=box_37_text))
box_37.comps.append(Checkbox(update_fn=update_pe_3))

box_38 = make_box_below(box_32, box_32.width, box_34.height)
box_38.comps.append(Multiline(text=box_36_text))
box_38.comps.append(Checkbox(update_fn=update_pe_4))

box_39 = make_box_below(box_33, box_33.width, box_34.height)
box_39_text = """- Recognized expert, sought after to solve
difficult problems
- Exceptionally skilled, develops and
executes innovative ideas
- Achieves early/highly advanced
qualifications
"""
box_39.comps.append(Bullets(text=box_39_text))
box_39.comps.append(Checkbox(update_fn=update_pe_5))

# row 11
box_40 = make_box_below(box_34, box_34.width, 83)
box_40_txt = (
    "34.\nCOMMAND OR\nORGANIZATIONAL\nCLIMATE:\n\nContributions to growth\nand development,\nhuman worth,\ncommunity"
)
box_40.comps.append(Multiline(text=box_40_txt))
box_40.comps.append(Checkbox())

box_41 = make_box_below(box_35, box_35.width, box_40.height)
box_41_text = """- Actions counter to Navy's retention goals

- Uninvolved with mentoring or professional
development of subordinates
- Demonstrates behavior that stifles command
or work center success
- Actions counter to good order and
discipline and negatively affect command/
organizational climate
"""
# box_41.draw_bullets(c, box_41_text)
box_41.comps.append(Bullets(text=box_41_text))
box_41.comps.append(Checkbox())

box_42 = make_box_below(box_36, box_36.width, box_40.height)
box_42_text = "-\n\n-\n\n\n-\n\n\n-"
# box_42.draw_multiline(c, box_42_text)
box_42.comps.append(Multiline(text=box_42_text))
box_42.comps.append(Checkbox())

box_43 = make_box_below(box_37, box_37.width, box_40.height)
box_43_text = """- Positive leadership supports Navy's increased
retention goals. Active in decreasing attrition
- Actions adequately encourage/support
subordinates' personal/professional growth
- Fosters an atmosphere conducive to personal
and team success
- Appreciates contributions of Navy personnel
- Positive influence on command climate
- Actions contribute to good order and discipline
and positively improves command/
organizational climate
"""
# box_43.draw_bullets(c, box_43_text, size=6.3, leading=7.1)
box_43.comps.append(Bullets(text=box_43_text, size=6.3, leading=7.1))
box_43.comps.append(Checkbox())

box_44 = make_box_below(box_38, box_38.width, box_40.height)
# box_44.draw_multiline(c, box_42_text)
box_44.comps.append(Multiline(text=box_42_text))
box_44.comps.append(Checkbox())

box_45 = make_box_below(box_39, box_39.width, box_40.height)
box_45_text = """- Measurably contributes to Navy's increased
retention and reduced attrition objectives
- Proactive leader/exemplary mentor. Involved
in subordinates' personal development leading
to professional growth/sustained commitment
- Initiates support programs for military,
civilian, and families to achieve exceptional
command and organizational climate
"""
# box_45.draw_bullets(c, box_45_text, size=6.3, leading=7.1)
box_45.comps.append(Bullets(text=box_45_text, size=6.3, leading=7.1))
box_45.comps.append(Checkbox())

# row 12
box_46 = make_box_below(box_40, box_40.width, 84)
box_46_txt = (
    "35.\nMILITARY BEARING/\nCHARACTER:\nAppearance, conduct,\nphysical fitness,\nadherance to Navy Core\nValues"
)
# box_46.draw_multiline(c, box_46_txt)
box_46.comps.append(Multiline(text=box_46_txt))
box_46.comps.append(Checkbox())

box_47 = make_box_below(box_41, box_41.width, box_46.height)
box_47_text = """- Consistent unsatisfactory appearance
- Unsatisfactory demeanor, or conduct
- Unable to meet one or more physical
readiness standards
- Fails to live up to one or more Navy
Core Values: HONOR, COURAGE,
COMMITMENT
"""
# box_47.draw_bullets(c, box_47_text, size=6.3, leading=7.1)
box_47.comps.append(Bullets(text=box_47_text, size=6.3, leading=7.1))
box_47.comps.append(Checkbox())

box_48 = make_box_below(box_42, box_42.width, box_46.height)
box_48_text = "-\n-\n-\n\n-"
# box_48.draw_multiline(c, box_48_text)
box_48.comps.append(Multiline(text=box_48_text))
box_48.comps.append(Checkbox())

box_49 = make_box_below(box_43, box_43.width, box_46.height)
box_49_text = """- Excellent personal appearance
- Excellent demeanor or conduct
- Complies with physical readiness
program
- Always lives up to Navy Core Values:
HONOR, COURAGE, COMMITMENT
"""
# box_49.draw_bullets(c, box_49_text, size=6.3, leading=7.1)
box_49.comps.append(Bullets(text=box_49_text, size=6.3, leading=7.1))
box_49.comps.append(Checkbox())


box_50 = make_box_below(box_44, box_44.width, box_46.height)
# box_50.draw_multiline(c, box_48_text)
box_50.comps.append(Multiline(text=box_48_text))
box_50.comps.append(Checkbox())

box_51 = make_box_below(box_45, box_45.width, box_46.height)
box_51_text = """- Exemplary personal appearance
- Exemplary Navy representative
- A leader in physical readiness
- Exemplifies Navy Core Values:
HONOR, COURAGE, COMMITMENT
"""
# box_51.draw_bullets(c, box_51_text, size=6.3, leading=7.1)
box_51.comps.append(Bullets(text=box_51_text, size=6.3, leading=7.1))
box_51.comps.append(Checkbox())

# row 13
box_52 = make_box_below(box_46, box_46.width, 84)
box_52_txt = "36.\nTEAMWORK:\nContributions toward\nteam building and\nteam results"
# box_52.draw_multiline(c, box_52_txt)
box_52.comps.append(Multiline(text=box_52_txt))
box_52.comps.append(Checkbox())

box_53 = make_box_below(box_47, box_47.width, box_52.height)
box_53_text = """- Creates conflict, unwilling to work
with others, puts self above team
- Fails to understand team goals or
teamwork techniques
- Does not take direction well
"""
# box_53.draw_bullets(c, box_53_text, size=6.3, leading=7.0)
box_53.comps.append(Bullets(text=box_53_text, size=6.3, leading=7.0))
box_53.comps.append(Checkbox())

box_54 = make_box_below(box_48, box_48.width, box_52.height)
box_54_text = "-\n\n-\n\n-"
# box_54.draw_multiline(c, box_54_text)
box_54.comps.append(Multiline(text=box_54_text))
box_54.comps.append(Checkbox())

box_55 = make_box_below(box_49, box_49.width, box_52.height)
box_55_text = """- Reinforces others' efforts, meets personal
commitments to team
- Understands team goals, employs good
teamwork techniques
- Accepts and offers team direction
"""
# box_55.draw_bullets(c, box_55_text, size=6.3, leading=7.1)
box_55.comps.append(Bullets(text=box_55_text, size=6.3, leading=7.1))
box_55.comps.append(Checkbox())

box_56 = make_box_below(box_50, box_50.width, box_52.height)
# box_56.draw_multiline(c, box_54_text)
box_56.comps.append(Multiline(text=box_54_text))
box_56.comps.append(Checkbox())

box_57 = make_box_below(box_51, box_51.width, box_52.height)
box_57_text = """- Team builder, inspires cooperation and
progress
- Talented mentor; focuses goals and
techniques for team
- The best at accepting and offering team
direction
"""
# box_57.draw_bullets(c, box_57_text, size=6.3, leading=7.1)
box_57.comps.append(Bullets(text=box_57_text, size=6.3, leading=7.1))
box_57.comps.append(Checkbox())

# row 14
box_58 = Box(id=58, bl=(MARGIN_LEFT, MARGIN_BOTTOM), tr=box_52.br)
box_58_txt = (
    "37.\nMISSION\nACCOMPLISHMENT\nAND INITIATIVE:\nTaking initiative,\nplanning/prioritizing,\nachieving mission\n"
)
# box_58.draw_multiline(c, box_58_txt)
box_58.comps.append(Multiline(text=box_58_txt))
box_58.comps.append(Checkbox())

box_59 = make_box_below(box_53, box_53.width, box_58.height)
box_59_text = """- Lacks initiative
- Unable to plan or prioritize
- Does not maintain readiness
- Fails to get the job done
"""
# box_59.draw_bullets(c, box_59_text, size=6.3, leading=7.1)
box_59.comps.append(Bullets(text=box_59_text, size=6.3, leading=7.1))
box_59.comps.append(Checkbox())

box_60 = make_box_below(box_54, box_54.width, box_58.height)
box_60_text = "-\n\n-\n\n-\n\n-"
# box_60.draw_multiline(c, box_60_text)
box_60.comps.append(Multiline(text=box_60_text))
box_60.comps.append(Checkbox())

box_61 = make_box_below(box_55, box_55.width, box_58.height)
box_61_text = """- Takes initiative to meet goals
- Plans/prioritizes effectively
- Maintains high state of readiness
- Always gets the job done
"""
# box_61.draw_bullets(c, box_61_text, size=6.3, leading=7.1)
box_61.comps.append(Bullets(text=box_61_text, size=6.3, leading=7.1))
box_61.comps.append(Checkbox())

box_62 = make_box_below(box_56, box_56.width, box_58.height)
# box_62.draw_multiline(c, box_60_text)
box_62.comps.append(Multiline(text=box_60_text))
box_62.comps.append(Checkbox())

box_63 = make_box_below(box_57, box_57.width, box_58.height)
box_63_text = """- Develops innovative ways to accomplish
mission
- Plans/prioritizes with exceptional skill
and foresight
- Maintains superior readiness, even with
limited resources
- Gets jobs done earlier and far better than
expected
"""
# box_63.draw_bullets(c, box_63_text, size=6.3, leading=7.1)
box_63.comps.append(Bullets(text=box_63_text, size=6.3, leading=7.1))
box_63.comps.append(Checkbox())


boxes = [
    box_0,
    box_1,
    box_2,
    box_3,
    box_4,
    box_5,
    box_6,
    box_7,
    box_8,
    box_9,
    box_10,
    box_11,
    box_12,
    box_13,
    box_14,
    box_15,
    box_16,
    box_17,
    box_18,
    box_19,
    box_20,
    box_21,
    box_22,
    box_23,
    box_24,
    box_25,
    box_26,
    box_27,
    box_28,
    box_29,
    box_30,
    box_31,
    box_32,
    box_33,
    box_34,
    box_35,
    box_36,
    box_37,
    box_38,
    box_39,
    box_40,
    box_41,
    box_42,
    box_43,
    box_44,
    box_45,
    box_46,
    box_47,
    box_48,
    box_49,
    box_50,
    box_51,
    box_52,
    box_53,
    box_54,
    box_55,
    box_56,
    box_57,
    box_58,
    box_59,
    box_60,
    box_61,
    box_62,
    box_63,
    tiny_space,
]


@dataclass
class Layout:
    filename: str
    boxes: list[Box]
    report: Fitrep

    def __post_init__(self):
        self.canvas = Canvas(self.filename, pagesize=LETTER)
        self.canvas.setLineWidth(0.6)

    # def __init__(self):
    #     self.canvas = Canvas("layout.pdf", pagesize=LETTER)
    #     self.canvas.setLineWidth(0.6)

    def draw(self):
        for box in boxes:
            for comp in box.comps:
                if comp.update_fn:
                    comp.update_fn(self.report, comp)
            box.draw(self.canvas)

        self.canvas.setFont("Times-Roman", 12)
        self.canvas.drawString(
            MARGIN_LEFT + 12, LETTER[1] - MARGIN_TOP + 5, "FITNESS REPORT & COUNSELING RECORD (W2-O6)"
        )

        self.canvas.setFont("Times-Roman", 8)
        self.canvas.drawString(MARGIN_LEFT + 4, MARGIN_BOTTOM - 10, "NAVPERS 1610/2 (REV 05-2025)")
        self.canvas.drawString(245, MARGIN_BOTTOM - 10, "CUI When Filled In - Previous Editions are Obsolete")


app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command()
def test_make_fitrep(
    output: Annotated[Path, typer.Option(help="Destination for output PDF file.")] = Path("fitrep.pdf").resolve(),
):
    """Test FITREP PDF generation capabiilty."""
    fitrep = Fitrep(
        name="WHITE, TRISTAN K",
        rate="LTJG",
        desig="1840",
        ssn="000-00-0000",
        group=SummaryGroup.ACT,
        uic="12345",
        station="MYSHIP",
        promotion_status=PromotionStatus.REGULAR,
        date_reported=date(2025, 1, 15),
        period_start=date.today(),
        period_end=date.today(),
        not_observed=True,
        pro_expertise=3,
    )

    layout = Layout(output.name, boxes, fitrep)
    layout.draw()
    layout.canvas.showPage()
    layout.canvas.save()
    webbrowser.open(output.as_uri())
