from collections.abc import Callable
from dataclasses import dataclass, field

from constants import MARGIN_BOTTOM, MARGIN_LEFT, MARGIN_RIGHT, MARGIN_SIDES, MARGIN_TOP
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen.canvas import Canvas

from .components import Component


@dataclass
class Box:
    """
    A visual box on an evaluation PDF.

    Attributes:
        bl (tuple[float, float]): The bottom-left corner of the box (x, y).
        tr (tuple[float, float]): The top-right corner of the box (x
        br (tuple[float, float]): The bottom-right corner of the box (x, y).
        tl (tuple[float, float]): The top-left corner of the box (x,
        width (float): The width of the box.
        height (float): The height of the box.
        components (list[Component]): A list of components to draw inside the box.
    """

    bl: tuple[float, float]
    tr: tuple[float, float]
    br: tuple[float, float] = (0.0, 0.0)
    tl: tuple[float, float] = (0.0, 0.0)
    width: float = 0
    height: float = 0
    components: list[Component] = field(default_factory=list)
    draw_fn: Callable[[Canvas, "Box"], None] | None = None

    def __post_init__(self):
        self.width = self.tr[0] - self.bl[0]
        self.height = self.tr[1] - self.bl[1]
        self.br = (self.tr[0], self.bl[1])
        self.tl = (self.bl[0], self.tr[1])

    def draw_left_border(self, canvas: Canvas):
        canvas.line(self.bl[0], self.bl[1], self.tl[0], self.tl[1])

    def draw_top_border(self, canvas: Canvas):
        canvas.line(self.bl[0], self.tl[1], self.tr[0], self.tr[1])

    def draw_right_border(self, canvas: Canvas):
        canvas.line(self.tr[0], self.tr[1], self.br[0], self.br[1])

    def draw_bottom_border(self, canvas: Canvas):
        canvas.line(self.bl[0], self.bl[1], self.br[0], self.br[1])

    def draw_debug(self, canvas: Canvas, string: str):
        canvas.drawString(self.bl[0] + 2, self.bl[1] + 2, string)

    def draw_label_standard(self, canvas: Canvas, text: str, x_off: float = 3, y_off: float = 10.5, size: float = 7.9):
        canvas.setFont("Times-Roman", size)
        canvas.drawString(self.tl[0] + x_off, self.tl[1] - y_off, text, wordSpace=0.6)

    def draw_centered_multiline(self, canvas: Canvas, txt: str, x: float, y: float, size=6.6, leading=7.7):
        canvas.setFont("Times-Roman", size=size)
        line_num = 0
        for line in txt.splitlines():
            canvas.drawCentredString(x=x, y=y - line_num * leading, text=line.strip())
            line_num += 1

    def draw_multiline(self, canvas: Canvas, txt: str, x_off: float = 2, y_off: float = 9, size=6.5, leading=7.9):
        """
        Draws text in box in the left column of the Performance Traits table.
        """
        t = canvas.beginText(self.tl[0] + x_off, self.tl[1] - y_off)
        t.setFont("Times-Roman", size=size, leading=leading)
        for line in txt.splitlines():
            t.textLine(line.strip())
        canvas.drawText(t)

    def draw_bullets(
        self, canvas: Canvas, txt: str, x_off: float = 2, y_off: float = 9, size: float = 6.5, leading: float = 7.9
    ):
        t = c.beginText(self.tl[0] + x_off, self.tl[1] - y_off)
        t.setFont("Times-Roman", size=size, leading=leading)
        for line in txt.splitlines():
            line = line.strip()
            if line:
                if line[0] != "-":
                    line = "  " + line
                t.textLine(line)
            else:
                t.textLine("")
        c.drawText(t)

    def draw_checkbox_br(self, canvas: Canvas):
        canvas.rect(self.br[0] - 16, self.br[1] + 4, 14, 12)

    def draw(self, canvas: Canvas):
        self.draw_left_border(canvas)
        self.draw_right_border(canvas)
        self.draw_top_border(canvas)
        self.draw_bottom_border(canvas)
        for comp in self.components:
            comp.draw(canvas, self)


def make_box_to_right(box: Box, width: float) -> Box:
    """
    Returns a new box of width `width` whose left border overlaps the right border of `box`.

    Args:
        box (Box): The box to the left.
        width (float): The width of the new box.
    """
    return Box(bl=box.br, tr=(box.tr[0] + width, box.tr[1]))


def make_box_below(box: Box, width: float, height: float) -> Box:
    """
    Returns a new box of width `width` and height `height` whose top border overlaps the bottom border of `box`.

    Args:
        box (Box): The box above.
        height (float): The height of the new box.
        width (float): The width of the new box.
    """
    return Box(bl=(box.bl[0], box.bl[1] - height), tr=(box.bl[0] + width, box.br[1]))


# Row 0
box_0 = Box(
    bl=(MARGIN_LEFT, LETTER[1] - MARGIN_TOP - 24),
    tr=(289, LETTER[1] - MARGIN_TOP),
)
box_1 = make_box_to_right(box_0, 66)
box_2 = make_box_to_right(box_1, 101)
box_3 = make_box_to_right(box_2, LETTER[0] - MARGIN_RIGHT - box_2.br[0])

# Row 1
box_4 = make_box_below(box_0, 149, box_0.height)
box_5 = make_box_to_right(box_4, 51)
box_6 = make_box_to_right(box_5, 196)
box_7 = make_box_to_right(box_6, 79)
box_8 = make_box_to_right(box_7, LETTER[0] - MARGIN_RIGHT - box_7.br[0])

# Row 2
box_9 = make_box_below(box_4, 340, box_0.height)
box_10 = make_box_to_right(box_9, LETTER[0] - MARGIN_SIDES - box_9.width)

# Row 3
box_11 = make_box_below(box_9, 75, box_0.height)
box_12 = make_box_to_right(box_11, box_9.width - box_11.width)
box_13 = make_box_to_right(box_12, 99)
box_14 = make_box_to_right(box_13, box_10.width - box_13.width)

# Row 4
box_15 = make_box_below(box_11, 151, box_0.height + 1)
box_16 = make_box_to_right(box_15, 50)
box_17 = make_box_to_right(box_16, box_16.width + 1)
box_18 = make_box_to_right(box_17, 133)
box_19 = make_box_to_right(box_18, box_14.bl[0] - box_18.br[0])
box_20 = make_box_to_right(box_19, LETTER[0] - MARGIN_RIGHT - box_19.br[0])

# Row 5
box_21 = Box(bl=(MARGIN_LEFT, 601), tr=box_20.br)

# Row 6
box_22 = make_box_below(box_21, box_21.width, 62)

# Row 7
box_23 = make_box_below(box_22, 179, 22)
box_24 = make_box_to_right(box_23, 79)
box_25 = make_box_to_right(box_24, 138)
box_26 = Box(bl=box_25.br, tr=box_22.br)

# tiny space
tiny_space = make_box_below(box_23, box_21.width, 2)

# Row 8
box_27 = make_box_below(tiny_space, box_21.width, 23)

# Row 9
box_28 = make_box_below(box_27, 73, 24)
box_29 = make_box_to_right(box_28, 129)
box_30 = make_box_to_right(box_29, 36)
box_31 = make_box_to_right(box_30, 137)
box_32 = make_box_to_right(box_31, 36)
box_33 = Box(bl=box_32.br, tr=box_27.br)

# row 10
box_34 = make_box_below(box_28, box_28.width, 85)
box_35 = make_box_below(box_29, box_29.width, box_34.height)
box_36 = make_box_below(box_30, box_30.width, box_34.height)
box_37 = make_box_below(box_31, box_31.width, box_34.height)
box_38 = make_box_below(box_32, box_32.width, box_34.height)
box_39 = make_box_below(box_33, box_33.width, box_34.height)

# row 11
box_40 = make_box_below(box_34, box_34.width, 83)
box_41 = make_box_below(box_35, box_35.width, box_40.height)
box_42 = make_box_below(box_36, box_36.width, box_40.height)
box_43 = make_box_below(box_37, box_37.width, box_40.height)
box_44 = make_box_below(box_38, box_38.width, box_40.height)
box_45 = make_box_below(box_39, box_39.width, box_40.height)

# row 12
box_46 = make_box_below(box_40, box_40.width, 84)
box_47 = make_box_below(box_41, box_41.width, box_46.height)
box_48 = make_box_below(box_42, box_42.width, box_46.height)
box_49 = make_box_below(box_43, box_43.width, box_46.height)
box_50 = make_box_below(box_44, box_44.width, box_46.height)
box_51 = make_box_below(box_45, box_45.width, box_46.height)

# row 13
box_52 = make_box_below(box_46, box_46.width, 84)
box_53 = make_box_below(box_47, box_47.width, box_52.height)
box_54 = make_box_below(box_48, box_48.width, box_52.height)
box_55 = make_box_below(box_49, box_49.width, box_52.height)
box_56 = make_box_below(box_50, box_50.width, box_52.height)
box_57 = make_box_below(box_51, box_51.width, box_52.height)

# row 14
box_58 = Box(bl=(MARGIN_LEFT, MARGIN_BOTTOM), tr=box_52.br)
box_59 = make_box_below(box_53, box_53.width, box_58.height)
box_60 = make_box_below(box_54, box_54.width, box_58.height)
box_61 = make_box_below(box_55, box_55.width, box_58.height)
box_62 = make_box_below(box_56, box_56.width, box_58.height)
box_63 = make_box_below(box_57, box_57.width, box_58.height)

# class Layout():
#     """A collection of all the boxes on the fitrep form."""

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


class Layout:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.canvas.setLineWidth(0.6)

    def draw(self):
        # use the instance canvas
        c = self.canvas

        for i, box in enumerate(boxes):
            box.draw_left_border(c)
            box.draw_right_border(c)
            box.draw_top_border(c)
            # box.draw_debug(c, str(i))

        # draw bottom border on box 58-63
        for box in [box_58, box_59, box_60, box_61, box_62, box_63]:
            box.draw_bottom_border(c)

        self.canvas.setFont("Times-Roman", 12)
        self.canvas.drawString(
            MARGIN_LEFT + 12, LETTER[1] - MARGIN_TOP + 5, "FITNESS REPORT & COUNSELING RECORD (W2-O6)"
        )

        self.canvas.setFont("Times-Roman", 8)
        self.canvas.drawString(MARGIN_LEFT + 4, MARGIN_BOTTOM - 10, "NAVPERS 1610/2 (REV 05-2025)")
        self.canvas.drawString(245, MARGIN_BOTTOM - 10, "CUI When Filled In - Previous Editions are Obsolete")

        c = self.canvas
        # use the instance method to draw labels
        box_0.draw_label_standard(c, "1. Name (Last, First MI Suffix)")
        box_1.draw_label_standard(c, "2. Rank")
        box_2.draw_label_standard(c, "3. Desig")
        box_3.draw_label_standard(c, "4. SSN")
        box_4.draw_label_standard(c, "5.")
        box_5.draw_label_standard(c, "6. UIC")
        box_6.draw_label_standard(c, "7. Ship/Station")
        box_7.draw_label_standard(c, "8. Promotion Status")
        box_8.draw_label_standard(c, "9. Date Reported")

        box_9.draw_label_standard(c, "Occasion for Report", y_off=9)

        box_10.draw_label_standard(c, "Period of Report", y_off=9)

        box_11.draw_label_standard(c, "16. Not Observed")
        box_11.draw_checkbox_br(c)

        box_12.draw_label_standard(c, "Type of Report")
        box_13.draw_label_standard(c, "20. Physical Readiness")
        box_14.draw_label_standard(c, "21. Billet Subcategory (if any)")
        box_15.draw_label_standard(c, "22. Reporting Senior (Last, FI  MI)")
        box_16.draw_label_standard(c, "23. Grade")
        box_17.draw_label_standard(c, "24. Desig")
        box_18.draw_label_standard(c, "25. Title")
        box_19.draw_label_standard(c, "26. UIC")
        box_20.draw_label_standard(c, "27. SSN")
        box_21.draw_label_standard(c, "28. Command Employment and Command Achievements", y_off=9)

        box_22.draw_label_standard(
            c, "29. Primary/Collateral/Watchstanding duties (Enter primary duty abbreviation in box)", y_off=9
        )
        self.canvas.rect(box_22.tl[0] + 8, box_22.tl[1] - 23, 115, 12)

        box_24.draw_label_standard(c, "30. Date Counseled", size=7, y_off=7, x_off=2)
        box_25.draw_label_standard(c, "31. Counselor", size=7, y_off=7, x_off=2)
        box_26.draw_label_standard(c, "32. Signature of Individual Counseled", size=7, y_off=7, x_off=2)

        box_40_txt = "34.\nCOMMAND OR\nORGANIZATIONAL\nCLIMATE:\n\nContributions to growth\nand development,\nhuman worth,\ncommunity"
        box_40.draw_multiline(c, box_40_txt)

        box_46_txt = "35.\nMILITARY BEARING/\nCHARACTER:\nAppearance, conduct,\nphysical fitness,\nadherance to Navy Core\nValues"
        box_46.draw_multiline(c, box_46_txt)

        box_52_txt = "36.\nTEAMWORK:\nContributions toward\nteam building and\nteam results"
        box_52.draw_multiline(c, box_52_txt)

        box_58_txt = "37.\nMISSION\nACCOMPLISHMENT\nAND INITIATIVE:\nTaking initiative,\nplanning/prioritizing,\nachieving mission\n"
        box_58.draw_multiline(c, box_58_txt)

        box_23_text = """
        For Mid-term Counseling Use. (When completing FITREP,
        enter 30 and 31 from counseling worksheet, sign 32.)
        """
        box_23.draw_multiline(c, box_23_text, x_off=3, y_off=-1, size=7.36)

        box_27_text = """
        PERFORMANCE TRAITS: 1.0 - Below standards/not progressing or UNSAT in any one standard; 2.0 - Does not yet meet all 3.0 standards; 3.0 - Meets all 3.0
        standards; 4.0 - Exceeds most 3.0 standards; 5.0 - Meets overall criteria and most of the specific standards for 5.0. Standards are not all inclusive.
        """
        box_27.draw_multiline(c, box_27_text, x_off=2, y_off=2, size=8.15)

        box_29_text = """
        1.0*
        Below Standards
        """
        box_29.draw_centered_multiline(c, box_29_text, x=152, y=490)

        box_30_text = """
        2.0
        Pro-
        gressing 
        """
        # box_30.draw_multiline(c, box_30_text)
        box_30.draw_centered_multiline(c, box_30_text, x=box_30.bl[0] + box_30.width / 2, y=493)

        box_31_text = """
        3.0
        Meets Standards
        """
        box_31.draw_centered_multiline(c, box_31_text, x=box_31.bl[0] + box_31.width / 2, y=490)

        box_32_text = """
        4.0
        Above
        Standards
        """
        box_32.draw_centered_multiline(c, box_32_text, x=box_32.bl[0] + box_32.width / 2, y=493)

        box_33_text = """
        5.0
        Greatly Exceeds Standards
        """
        box_33.draw_centered_multiline(c, box_33_text, x=box_33.bl[0] + box_33.width / 2, y=490)

        box_34_txt = "33.\nPROFESSIONAL\nEXPERTISE:\nProfessional knowledge\nproficiency, and\nqualifications"
        box_34.draw_multiline(c, box_34_txt)

        box_35_text = """-Lacks basic professional knowledge to
        perform effectively
        -Cannot apply basic skills
        -Fails to develop professionally or
        achieve timely qualifications
        """
        box_35.draw_bullets(c, box_35_text)

        box_37_text = """- Has thorough professional knowledge
        - Competently performs both routine and
        new tasks
        - Steadily improves skills, achieves timely
        qualifications
        """
        box_37.draw_bullets(c, box_37_text)

        box_36_text = "-\n\n-\n\n-"
        box_36.draw_multiline(c, box_36_text)
        box_38.draw_multiline(c, box_36_text)

        box_39_text = """- Recognized expert, sought after to solve
        difficult problems
        - Exceptionally skilled, develops and
        executes innovative ideas
        - Achieves early/highly advanced
        qualifications
        """
        box_39.draw_bullets(c, box_39_text)

        box_41_text = """- Actions counter to Navy's retention goals

        - Uninvolved with mentoring or professional
        development of subordinates
        - Demonstrates behavior that stifles command
        or work center success
        - Actions counter to good order and
        discipline and negatively affect command/
        organizational climate
        """
        box_41.draw_bullets(c, box_41_text)

        box_42_text = "-\n\n-\n\n\n-\n\n\n-"
        box_42.draw_multiline(c, box_42_text)
        box_44.draw_multiline(c, box_42_text)

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
        box_43.draw_bullets(c, box_43_text, size=6.3, leading=7.1)

        box_45_text = """- Measurably contributes to Navy's increased
        retention and reduced attrition objectives
        - Proactive leader/exemplary mentor. Involved
        in subordinates' personal development leading
        to professional growth/sustained commitment
        - Initiates support programs for military,
        civilian, and families to achieve exceptional
        command and organizational climate
        """
        box_45.draw_bullets(c, box_45_text, size=6.3, leading=7.1)

        box_47_text = """- Consistent unsatisfactory appearance
        - Unsatisfactory demeanor, or conduct
        - Unable to meet one or more physical
        readiness standards
        - Fails to live up to one or more Navy
        Core Values: HONOR, COURAGE,
        COMMITMENT
        """
        box_47.draw_bullets(c, box_47_text, size=6.3, leading=7.1)

        box_48_text = "-\n-\n-\n\n-"
        box_48.draw_multiline(c, box_48_text)
        box_50.draw_multiline(c, box_48_text)

        box_49_text = """- Excellent personal appearance
        - Excellent demeanor or conduct
        - Complies with physical readiness
        program
        - Always lives up to Navy Core Values:
        HONOR, COURAGE, COMMITMENT
        """
        box_49.draw_bullets(c, box_49_text, size=6.3, leading=7.1)

        box_51_text = """- Exemplary personal appearance
        - Exemplary Navy representative
        - A leader in physical readiness
        - Exemplifies Navy Core Values:
        HONOR, COURAGE, COMMITMENT
        """
        box_51.draw_bullets(c, box_51_text, size=6.3, leading=7.1)

        box_53_text = """- Creates conflict, unwilling to work
        with others, puts self above team
        - Fails to understand team goals or
        teamwork techniques
        - Does not take direction well
        """
        box_53.draw_bullets(c, box_53_text, size=6.3, leading=7.0)

        box_54_text = "-\n\n-\n\n-"
        box_54.draw_multiline(c, box_54_text)
        box_56.draw_multiline(c, box_54_text)

        box_55_text = """- Reinforces others' efforts, meets personal
        commitments to team
        - Understands team goals, employs good
        teamwork techniques
        - Accepts and offers team direction
        """
        box_55.draw_bullets(c, box_55_text, size=6.3, leading=7.1)

        box_57_text = """- Team builder, inspires cooperation and
        progress
        - Talented mentor; focuses goals and
        techniques for team
        - The best at accepting and offering team
        direction
        """
        box_57.draw_bullets(c, box_57_text, size=6.3, leading=7.1)

        box_59_text = """- Lacks initiative
        - Unable to plan or prioritize
        - Does not maintain readiness
        - Fails to get the job done
        """
        box_59.draw_bullets(c, box_59_text, size=6.3, leading=7.1)

        box_60_text = "-\n\n-\n\n-\n\n-"
        box_60.draw_multiline(c, box_60_text)
        box_62.draw_multiline(c, box_60_text)

        box_61_text = """- Takes initiative to meet goals
        - Plans/prioritizes effectively
        - Maintains high state of readiness
        - Always gets the job done
        """
        box_61.draw_bullets(c, box_61_text, size=6.3, leading=7.1)

        box_63_text = """- Develops innovative ways to accomplish
        mission
        - Plans/prioritizes with exceptional skill
        and foresight
        - Maintains superior readiness, even with
        limited resources
        - Gets jobs done earlier and far better than
        expected
        """
        box_63.draw_bullets(c, box_63_text, size=6.3, leading=7.1)

        # draw a check box in the bottom right corner of box 34-63
        for box in [
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
        ]:
            box.draw_checkbox_br(c)


if __name__ == "__main__":
    c = Canvas("layout.pdf", pagesize=LETTER)
    layout = Layout(canvas=c)
    layout.draw()
    layout.canvas.showPage()
    layout.canvas.save()
