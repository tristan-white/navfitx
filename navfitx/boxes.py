"""
Boxes and components for drawing on a PDF canvas.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable

from reportlab.pdfgen.canvas import Canvas


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

    id: int
    bl: tuple[float, float]
    tr: tuple[float, float]
    br: tuple[float, float] = (0.0, 0.0)
    tl: tuple[float, float] = (0.0, 0.0)
    width: float = 0
    height: float = 0
    comps: list["Component"] = field(default_factory=list)

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

    def draw(self, canvas: Canvas):
        self.draw_left_border(canvas)
        self.draw_right_border(canvas)
        self.draw_top_border(canvas)
        self.draw_bottom_border(canvas)
        for comp in self.comps:
            comp.draw(canvas, self)


@dataclass
class Component(ABC):
    """
    An element that can be drawn into a box.

    Attributes:
        x (float): The x coordinate of the component within its containing box.
        y (float): The y coordinate of the component within its containing box.
    """

    x: float
    y: float
    update_fn: Callable | None = None

    @abstractmethod
    def draw(self, canvas: Canvas, box: Box) -> None:
        pass


@dataclass
class String(Component):
    """
    A string component.
    """

    x: float = 3
    y: float = 10.5
    text: str = ""
    size: float = 7.9
    leading: float = 7.9
    fontname: str = "Times-Roman"

    def draw(self, canvas: Canvas, box: Box):
        """
        Draws a string in the box at the specified coordinates.
        """
        canvas.setFont(self.fontname, self.size, self.leading)
        canvas.drawString(box.tl[0] + self.x, box.tl[1] - self.y, self.text, wordSpace=0.6)


@dataclass
class Multiline(Component):
    """
    A multiline text component.
    """

    x: float = 2
    y: float = 9
    text: str = ""
    size: float = 6.5
    leading: float = 7.9
    no_strip: bool = False

    def draw(self, canvas: Canvas, box: Box):
        """
        Draws text in box in the left column of the Performance Traits table.
        """
        t = canvas.beginText(box.tl[0] + self.x, box.tl[1] - self.y)
        t.setFont("Times-Roman", size=self.size, leading=self.leading)
        for line in self.text.splitlines():
            if self.no_strip:
                t.textLine(line)
            else:
                t.textLine(line.strip())
        canvas.drawText(t)


@dataclass
class MultilineCentered(Component):
    """
    A multiline text component, centered horizontally in the box.
    """

    x: float = 2
    y: float = 9
    text: str = ""
    size: float = 6.6
    leading: float = 7.7

    def draw(self, canvas: Canvas, box: Box):
        canvas.setFont("Times-Roman", size=self.size)
        line_num = 0
        for line in self.text.splitlines():
            canvas.drawCentredString(x=self.x, y=self.y - line_num * self.leading, text=line.strip())
            line_num += 1


@dataclass
class Bullets(Component):
    """
    A bullet list component.

    Similar to `Multiline`, but each line that doesn't start with a bullet is prefixed with spaces to align with the text after the bullet.
    """

    x: float = 2
    y: float = 9
    text: str = ""
    size: float = 6.5
    leading: float = 7.9

    def draw(self, canvas: Canvas, box: Box):
        t = canvas.beginText(box.tl[0] + self.x, box.tl[1] - self.y)
        t.setFont("Times-Roman", size=self.size, leading=self.leading)
        for line in self.text.splitlines():
            line = line.strip()
            if line:
                if line[0] != "-":
                    line = "  " + line
                t.textLine(line)
            else:
                t.textLine("")
        canvas.drawText(t)


@dataclass
class Checkbox(Component):
    """
    A checkbox component.
    """

    x: float = -16
    y: float = 4
    checked: bool = False
    width: float = 14
    height: float = 12

    def draw(self, canvas: Canvas, box: Box):
        # canvas.rect(self.x, self.y, self.width, self.height)
        canvas.rect(box.br[0] + self.x, box.br[1] + self.y, self.width, self.height)
        if self.checked:
            canvas.setFont("Courier", 12)
            canvas.drawCentredString(box.br[0] + self.x + self.width / 2, box.br[1] + self.y + 2, "X")


def make_br_checkbox(box: Box) -> Checkbox:
    """
    Creates a Checkbox with coords in the bottom-right corner of the box.
    """
    return Checkbox(x=box.br[0] - 16, y=box.br[1] + 4)
