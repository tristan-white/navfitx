import textwrap
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

eighth = inch / 8
ninth = inch / 9

MARGIN_SIDE = inch * 4 / 9


class RowHeights(Enum):
    HEIGHT_ROW_1: float = inch * 1 / 3
    """For blocks 1-4"""

    HEIGHT_ROW_2: float = HEIGHT_ROW_1
    """For blocks 5-9"""

    HEIGHT_ROW_3: float = HEIGHT_ROW_1
    """For blocks 10-15"""

    HEIGHT_ROW_4: float = HEIGHT_ROW_1
    """For blocks 22-27"""

    HEIGHT_ROW_5: float = HEIGHT_ROW_1
    """For block 28"""

    HEIGHT_ROW_6: float = HEIGHT_ROW_1
    """For block 29"""

    HEIGHT_ROW_7: float = HEIGHT_ROW_1
    """For block 30-32"""

    HEIGHT_ROW_8: float = HEIGHT_ROW_1
    """For the text that explains Performance Traits."""

    HEIGHT_ROW_9: float = HEIGHT_ROW_1
    """For the heading row of the Performance Traits table."""

    HEIGHT_ROW_10: float = 84
    """For block 33"""


@dataclass
class Block(ABC):
    name: str

    @abstractmethod
    def validate(self):
        pass


@dataclass
class Row(ABC):
    x: float
    y_bl: float
    y_tl: float
    width: float

    def height(self) -> float:
        return self.y_tl - self.y_bl

    @abstractmethod
    def draw_labels(self):
        pass


class Block1(Block):
    data: str

    def validate(self):
        pass


class Block29(Block):
    """
    Contains primary, collateral, and watchstanding duties.

    Attributes:
        duty (str):
            An abbreviation of 14 or fewer characters and spaces for the most
            significant primary duty for the period reported on.
        job_statement (str):
            Brief statement about the scope of primary duty responsibilities. Include such
            items as technical or professional duties, personnel supervised, and budget administered. Job-
            scope statements are optional for operational billets
    """

    duty: str = ""

    name: str = "Primary/Collateral/Watchstanding Duties/PFA"


class Block40(Block):
    """
    Contains one or two career recommendations.

    The second recommendation is not required. Each entry may have a
    maximum of 20 characters and spaces. If necessary, use two lines
    for the entry. Do not leave blank. If no recommendation is appropriate, enter “NA” or “NONE”
    in the first block.

    Attributes:
        rec1 (str): The first career recommendation.
        rec2 (str): The second career recommendation.
    """

    rec1: str
    rec2: str

    def validate(self):
        pass


class Block41(Block):
    """
    Contains the reporting senior's comments on the performance of the individual.

    No more than 18 lines, with max of 91 characters per line. Words are not allowed
    to be split between lines.

    Attributes:
        comments (str): The reporting senior's comments.
    """

    comments: str = ""

    name: str = "COMMENTS ON PERFORMANCE"

    def validate(self):
        lines = textwrap.wrap(self.comments, width=91)
        if len(lines) > 18:
            raise ValueError("Block 41 comments cannot exceed 18 lines of 91 characters each.")


def draw_blk_label(c: canvas.Canvas, x: float, y: float, label: str):
    """
    Draws the first block of the form, which contains the name, rank, and date.

    Args:
        c (canvas.Canvas): The canvas to draw on.
        x (float): The x-coordinate of the bottom-left corner of the block.
        y (float): The y-coordinate of the bottom-left corner of the block.
    """
    c.setFontSize(8)
    c.drawString(x + 4, y + ninth * 2, label)


def draw_blk_vertical_line(c: canvas.Canvas, blk_bl_x: float, blk_bl_y: float, height: float):
    """
    Draws a vertical line in a block.
    """
    c.line(blk_bl_x, blk_bl_y, blk_bl_x, blk_bl_y + height)


def draw_layout(c: canvas.Canvas):
    c.setLineWidth(0.5)
    c.setFont("Times-Roman", 12)
    # draw a border around the page
    width = 612
    height = 792
    blk_width = width - 2 * (4 * ninth)
    blk_height = ninth * 3
    c.rect(4 * ninth, inch / 2, blk_width, height - inch)

    # block 1
    c.line(4 * ninth, height - inch / 2 - blk_height, blk_width + 4 * ninth, height - inch / 2 - blk_height)
    draw_blk_label(c, 4 * ninth, height - inch / 2 - blk_height, "1.  Name (Last, First  MI  Suffix)")

    # block 2
    left_edge = width / 2
    draw_blk_vertical_line(c, left_edge, height - inch / 2 - blk_height, blk_height)
    draw_blk_label(c, left_edge, height - inch / 2 - blk_height, "2.  Grade/Rate")

    # block 3
    left_edge = width / 2 + 65 / 72 * inch
    draw_blk_vertical_line(c, left_edge, height - inch / 2 - blk_height, blk_height)
    draw_blk_label(c, left_edge, height - inch / 2 - blk_height, "3.  Desig")

    # block 4
    left_edge = left_edge + inch * (1 + 3 / 9)
    print(left_edge)
    draw_blk_vertical_line(c, left_edge, height - inch / 2 - blk_height, blk_height)
    draw_blk_label(c, left_edge, height - inch / 2 - blk_height, "4.  SSN")

    # block 5
    c.line(4 * ninth, height - inch / 2 - blk_height * 2, blk_width + 4 * ninth, height - inch / 2 - blk_height * 2)
    draw_blk_label(c, 4 * ninth, height - inch / 2 - blk_height * 2, "5.   ACT      TAR     INACT   AT/ADSW/265")

    # block 6
    left_edge = 4 * ninth + 152
    draw_blk_vertical_line(c, left_edge, height - inch / 2 - blk_height * 2, blk_height)
    draw_blk_label(c, left_edge, height - inch / 2 - blk_height * 2, "6.  UIC")

    # block 7
    left_edge = 235
    draw_blk_vertical_line(c, left_edge, height - inch / 2 - blk_height * 2, blk_height)
    draw_blk_label(c, left_edge, height - inch / 2 - blk_height * 2, "7.  Ship/Station")

    # block 8
    left_edge = 428
    draw_blk_vertical_line(c, left_edge, height - inch / 2 - blk_height * 2, blk_height)
    draw_blk_label(c, left_edge, height - inch / 2 - blk_height * 2, "8.  Promotion Status")

    # block 9
    left_edge = 503
    draw_blk_vertical_line(c, left_edge, height - inch / 2 - blk_height * 2, blk_height)
    draw_blk_label(c, left_edge, height - inch / 2 - blk_height * 2, "9.  Date Reported")

    # block 10
    left_edge = 4 * ninth
    draw_blk_label(c, left_edge, height - inch / 2 - blk_height * 3, "Occasion for Report")

    # block 14-15
    left_edge = width / 2 + 65 / 72 * inch - 2
    draw_blk_vertical_line(c, left_edge, height - inch / 2 - blk_height * 3, blk_height)
    draw_blk_label(c, left_edge, height - inch / 2 - blk_height * 3, "Period of Report")

    # block 16
    left_edge = 4 * ninth
    draw_blk_label(c, left_edge, height - inch / 2 - blk_height * 4, "16.")

    # block 17-19
    left_edge = 113
    draw_blk_vertical_line(c, left_edge, height - inch / 2 - blk_height * 4, blk_height)
    draw_blk_label(c, left_edge, height - inch / 2 - blk_height * 4, "Type of Report")

    # block 20
    left_edge = width / 2 + 65 / 72 * inch - 2
    draw_blk_vertical_line(c, left_edge, height - inch / 2 - blk_height * 4, blk_height)
    draw_blk_label(c, left_edge, height - inch / 2 - blk_height * 4, "20.  Physical Readiness")

    # block 21
    left_edge = 468
    draw_blk_vertical_line(c, left_edge, height - inch / 2 - blk_height * 4, blk_height)
    draw_blk_label(c, left_edge, height - inch / 2 - blk_height * 4, "21.  Billet Subcategory (if any)")

    # block 22
    left_edge = 4 * ninth
    draw_blk_label(c, left_edge, height - inch / 2 - blk_height * 5, "22.  Promoting Senior (Last, FI MI)")

    # block 23
    left_edge = 4 * ninth + 152  # same as block 6
    draw_blk_vertical_line(c, left_edge, height - inch / 2 - blk_height * 5, blk_height)
    draw_blk_label(c, left_edge, height - inch / 2 - blk_height * 5, "23.  Grade")

    # block 24
    left_edge = 230
    draw_blk_vertical_line(c, left_edge, height - inch / 2 - blk_height * 5, blk_height)
    draw_blk_label(c, left_edge, height - inch / 2 - blk_height * 5, "24.  Desig")

    # block 25
    left_edge = 280
    draw_blk_vertical_line(c, left_edge, height - inch / 2 - blk_height * 5, blk_height)
    draw_blk_label(c, left_edge, height - inch / 2 - blk_height * 5, "25.  Title")

    # block 26
    left_edge = 413
    draw_blk_vertical_line(c, left_edge, height - inch / 2 - blk_height * 5, blk_height)
    draw_blk_label(c, left_edge, height - inch / 2 - blk_height * 5, "26.  UIC")

    # block 27
    left_edge = 468
    draw_blk_vertical_line(c, left_edge, height - inch / 2 - blk_height * 5, blk_height)
    draw_blk_label(c, left_edge, height - inch / 2 - blk_height * 5, "27.  SSN")

    # block 28
    left_edge = 4 * ninth
    draw_blk_label(c, left_edge, height - inch / 2 - blk_height * 6, "28. Command employment and command achievements.")

    c.line(4 * ninth, height - inch / 2 - blk_height * 7, blk_width + 4 * ninth, height - inch / 2 - blk_height * 7)

    # block 29
    blk_29_bl_y = height - 267
    left_edge = 4 * ninth
    draw_blk_label(
        c,
        left_edge,
        blk_29_bl_y,
        "29. Primary/Collateral/Watchstanding duties. (Enter primary duty abbreviation in box.)",
    )
    # c.rect(left_edge + 4, blk_29_bl_y, 153-37, 10)

    c.line(4 * ninth, height - inch / 2 - blk_height * 9, blk_width + 4 * ninth, height - inch / 2 - blk_height * 9)

    # block 30
    c.line(4 * ninth, height - inch / 2 - blk_height * 3, blk_width + 4 * ninth, height - inch / 2 - blk_height * 3)
    c.line(4 * ninth, height - inch / 2 - blk_height * 4, blk_width + 4 * ninth, height - inch / 2 - blk_height * 4)
    c.line(4 * ninth, height - inch / 2 - blk_height * 5, blk_width + 4 * ninth, height - inch / 2 - blk_height * 5)

    c.drawString(464, height - inch / 2 + 4, "RCS BUPERS 1610-1")
    c.setFontSize(14.5)
    c.drawString(34, height - inch / 2 + 4, "FITNESS REPORT & COUNSELING RECORD     (E7 - O6)")


if __name__ == "__main__":
    c = canvas.Canvas("hello.pdf", pagesize=LETTER)
    draw_layout(c)

    c.showPage()
    c.save()
