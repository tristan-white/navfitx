from dataclasses import dataclass

from constants import MARGIN_SIDE, MARGIN_TOP
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


@dataclass(frozen=True)
class Box:
    """A box on the fitrep form."""

    x: float
    y: float
    width: float
    height: float

    def br(self) -> tuple[float, float]:
        """Return the bottom-right corner of the box."""
        return (self.x + self.width, self.y)

    def tr(self) -> tuple[float, float]:
        """Return the top-right corner of the box."""
        return (self.x + self.width, self.y + self.height)

    def tl(self) -> tuple[float, float]:
        """Return the top-left corner of the box."""
        return (self.x, self.y + self.height)

    def draw(self, c: canvas.Canvas, num: int):
        """Draw the box on the canvas."""
        c.rect(self.x, self.y, self.width, self.height)
        c.drawString(self.x + 2, self.y + 2, str(num))

    def draw_left_border(self, c: canvas.Canvas, n: int):
        c.line(self.x, self.y, self.x, self.y + self.height)
        c.drawString(self.x + 2, self.y + 2, str(n))


# Row 0
box_0 = Box(
    x=MARGIN_SIDE,
    y=LETTER[1] - MARGIN_TOP - inch * 1 / 3,
    width=LETTER[0] - 2 * MARGIN_SIDE,
    height=inch * 1 / 3,
)
box_1 = Box(
    x=LETTER[0] / 2,
    y=box_0.y,
    width=66,
    height=box_0.height,
)
box_2 = Box(
    x=box_1.x + box_1.width,
    y=box_0.y,
    width=97,
    height=box_1.height,
)
box_3 = Box(x=box_2.x + box_2.width, y=box_0.y, width=LETTER[0] - MARGIN_SIDE - box_2.br()[0], height=box_0.height)

# Row 1
box_4 = Box(
    x=MARGIN_SIDE,
    y=box_0.y - (inch / 3),
    width=152,
    height=inch / 3,
)
box_5 = Box(
    x=box_4.br()[0],
    y=box_4.y,
    width=49,
    height=box_4.height,
)
box_6 = Box(
    x=box_5.br()[0],
    y=box_4.y,
    width=194,
    height=box_4.height,
)
box_7 = Box(
    x=box_6.br()[0],
    y=box_4.y,
    width=76,
    height=box_4.height,
)
box_8 = Box(
    x=box_7.br()[0],
    y=box_4.y,
    width=LETTER[0] - MARGIN_SIDE - box_7.br()[0],
    height=box_4.height,
)

# Row 2
box_9 = Box(
    x=MARGIN_SIDE,
    y=box_4.y - (inch / 3),
    width=370 - MARGIN_SIDE - 2,
    height=inch / 3,
)
print(370 - MARGIN_SIDE - 2)
box_10 = Box(
    x=box_9.x + box_9.width,
    y=box_9.y,
    width=LETTER[0] - box_9.br()[0] - MARGIN_SIDE,
    height=box_9.height,
)

# Row 3
box_11 = Box(
    x=MARGIN_SIDE,
    y=box_9.y - box_9.height,
    width=112 - MARGIN_SIDE,
    height=box_9.height,
)
box_12 = Box(
    x=box_11.br()[0],
    y=box_11.y,
    width=box_9.width - box_11.width,
    height=box_11.height,
)
box_13 = Box(
    x=box_10.x,
    y=box_11.y,
    width=box_10.width - box_3.width,
    height=box_9.height,
)
box_14 = Box(
    x=box_13.br()[0],
    y=box_11.y,
    width=box_10.width - box_13.width,
    height=box_11.height,
)

# Row 4
box_15 = Box(
    x=MARGIN_SIDE,
    y=box_11.y - box_11.height,
    width=box_4.width - 1,
    height=box_11.height,
)
box_16 = Box(
    x=box_15.br()[0],
    y=box_15.y,
    width=48,
    height=box_15.height,
)
box_17 = Box(
    x=box_16.br()[0],
    y=box_15.y,
    width=box_16.width + 2,
    height=box_15.height,
)
box_18 = Box(
    x=box_17.br()[0],
    y=box_15.y,
    width=412 - box_17.br()[0],
    height=box_15.height,
)
box_19 = Box(
    x=box_18.br()[0],
    y=box_15.y,
    width=48,
    height=box_15.height,
)
box_20 = Box(
    x=box_19.br()[0],
    y=box_15.y,
    width=LETTER[0] - MARGIN_SIDE - box_19.br()[0],
    height=box_15.height,
)


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
]


if __name__ == "__main__":
    c = canvas.Canvas("layout.pdf", pagesize=LETTER)
    c.setLineWidth(0.5)

    top_left = (MARGIN_SIDE, LETTER[1] - MARGIN_TOP)
    top_right = (LETTER[0] - MARGIN_SIDE, LETTER[1] - MARGIN_TOP)
    # row 0
    c.line(top_left[0], top_left[1], top_right[0], top_right[1])

    # row 1
    row_0_y = box_0.y
    c.line(box_0.x, row_0_y, box_3.br()[0], row_0_y)

    # row 2
    row_1_y = box_4.y
    c.line(box_4.x, row_1_y, box_8.br()[0], row_1_y)

    # row 3
    c.line(box_9.x, box_9.y, box_10.br()[0], box_9.y)

    # row 4
    c.line(box_11.x, box_11.y, box_14.br()[0], box_11.y)

    for i, box in enumerate(boxes):
        box.draw_left_border(c, i)

    c.showPage()
    c.save()
