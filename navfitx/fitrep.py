from dataclasses import dataclass

from constants import MARGIN_BOTTOM, MARGIN_LEFT, MARGIN_RIGHT, MARGIN_SIDES, MARGIN_TOP
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen.canvas import Canvas


@dataclass
class Box:
    """A box on the fitrep form."""

    bl: tuple[float, float]
    tr: tuple[float, float]
    br: tuple[float, float] = (0.0, 0.0)
    tl: tuple[float, float] = (0.0, 0.0)
    width: float = 0
    height: float = 0

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
box_29 = make_box_to_right(box_28, 130)
box_30 = make_box_to_right(box_29, 36)
box_31 = make_box_to_right(box_30, 138)
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


def draw_b23_text(c: Canvas):
    text = """
    For Mid-term Counseling Use. (When completing FITREP,
    enter 30 and 31 from counseling worksheet, sign 32.)
    """
    t = c.beginText(box_23.tl[0] + 3, box_23.tl[1] + 1)
    c.setFont("Times-Roman", size=7.36, leading=8)
    for line in text.splitlines():
        t.textLine(line.strip())
    c.drawText(t)


def draw_b27_text(c: Canvas):
    text = """
    PERFORMANCE TRAITS: 1.0 - Below standards/not progressing or UNSAT in any one standard; 2.0 - Does not yet meet all 3.0 standards; 3.0 - Meets all 3.0
    standards; 4.0 - Exceeds most 3.0 standards; 5.0 - Meets overall criteria and most of the specific standards for 5.0. Standards are not all inclusive.
    """
    t = c.beginText(box_27.tl[0] + 2, box_27.tl[1] - 2)
    t.setFont("Times-Roman", size=8.15, leading=8)
    for line in text.splitlines():
        t.textLine(line.strip())
    c.drawText(t)


class Layout:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.canvas.setLineWidth(0.6)

    def draw_label_standard(self, box: Box, text: str, x_off: float = 3, y_off: float = 10.5, size: float = 7.9):
        self.canvas.setFont("Times-Roman", size)
        self.canvas.drawString(box.tl[0] + x_off, box.tl[1] - y_off, text, wordSpace=0.6)

    def draw_checkbox_br(self, box: Box):
        self.canvas.rect(box.br[0] - 16, box.br[1] + 4, 14, 12)

    # def draw_pt_row_header(self, box: Box, blk_num: int, text: str):
    #     header, desc = text.split(":")
    #     string = f"{blk_num}.\n"

    def draw_left_col_pt(self, box: Box, txt: str):
        """
        Draws text in box in the left column of the Performance Traits table.
        """
        t = c.beginText(box.tl[0] + 2, box.tl[1] - 9)
        t.setFont("Times-Roman", size=6.5, leading=7.9)
        for line in txt.splitlines():
            t.textLine(line.strip())
        c.drawText(t)

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

        # use the instance method to draw labels
        self.draw_label_standard(box_0, "1. Name (Last, First MI Suffix)")
        self.draw_label_standard(box_1, "2. Rank")
        self.draw_label_standard(box_2, "3. Desig")
        self.draw_label_standard(box_3, "4. SSN")
        self.draw_label_standard(box_4, "5.")
        self.draw_label_standard(box_5, "6. UIC")
        self.draw_label_standard(box_6, "7. Ship/Station")
        self.draw_label_standard(box_7, "8. Promotion Status")
        self.draw_label_standard(box_8, "9. Date Reported")

        self.draw_label_standard(box_9, "Occasion for Report", y_off=9)

        self.draw_label_standard(box_10, "Period of Report", y_off=9)

        self.draw_label_standard(box_11, "16. Not Observed")
        self.draw_checkbox_br(box_11)

        self.draw_label_standard(box_12, "Type of Report")
        self.draw_label_standard(box_13, "20. Physical Readiness")
        self.draw_label_standard(box_14, "21. Billet Subcategory (if any)")
        self.draw_label_standard(box_15, "22. Reporting Senior (Last, FI  MI)")
        self.draw_label_standard(box_16, "23. Grade")
        self.draw_label_standard(box_17, "24. Desig")
        self.draw_label_standard(box_18, "25. Title")
        self.draw_label_standard(box_19, "26. UIC")
        self.draw_label_standard(box_20, "27. SSN")
        self.draw_label_standard(box_21, "28. Command Employment and Command Achievements", y_off=9)

        self.draw_label_standard(
            box_22, "29. Primary/Collateral/Watchstanding duties (Enter primary duty abbreviation in box)", y_off=9
        )
        self.canvas.rect(box_22.tl[0] + 8, box_22.tl[1] - 23, 115, 12)

        self.draw_label_standard(box_24, "30. Date Counseled", size=7, y_off=7, x_off=2)
        self.draw_label_standard(box_25, "31. Counselor", size=7, y_off=7, x_off=2)
        self.draw_label_standard(box_26, "32. Signature of Individual Counseled", size=7, y_off=7, x_off=2)

        box_34_txt = "33.\nPROFESSIONAL\nEXPERTISE:\nProfessional knowledge\nproficiency, and\nqualifications"
        self.draw_left_col_pt(box_34, box_34_txt)

        box_40_txt = "34.\nCOMMAND OR\nORGANIZATIONAL\nCLIMATE:\n\nContributions to growth\nand development,\nhuman worth,\ncommunity"
        self.draw_left_col_pt(box_40, box_40_txt)

        box_46_txt = "35.\nMILITARY BEARING/\nCHARACTER:\nAppearance, conduct,\nphysical fitness,\nadherance to Navy Core\nValues"
        self.draw_left_col_pt(box_46, box_46_txt)

        box_52_txt = "36.\nTEAMWORK:\nContributions toward\nteam building and\nteam results"
        self.draw_left_col_pt(box_52, box_52_txt)

        box_58_txt = "37.\nMISSION\nACCOMPLISHMENT\nAND INITIATIVE:\nTaking initiative,\nplanning/prioritizing,\nachieving mission\n"
        self.draw_left_col_pt(box_58, box_58_txt)

        draw_b23_text(c)
        draw_b27_text(c)

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
            self.draw_checkbox_br(box)


if __name__ == "__main__":
    c = Canvas("layout.pdf", pagesize=LETTER)
    layout = Layout(canvas=c)
    layout.draw()
    layout.canvas.showPage()
    layout.canvas.save()
