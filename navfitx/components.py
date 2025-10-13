"""
Components that can be drawn into a Box.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from reportlab.pdfgen.canvas import Canvas

from .fitrep import Box


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

    @abstractmethod
    def draw(self, canvas: Canvas, box: Box) -> None:
        pass


@dataclass
class String(Component):
    """
    A string component.
    """

    text: str = ""
    size: float = 7.9
    leading: float = 7.9

    def draw(self, canvas: Canvas, box: Box):
        """
        Draws a string in the box at the specified coordinates.
        """
        canvas.setFont("Times-Roman", size=self.size, leading=self.leading)
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

    def draw(self, canvas: Canvas, box: Box):
        """
        Draws text in box in the left column of the Performance Traits table.
        """
        t = canvas.beginText(box.tl[0] + self.x, box.tl[1] - self.y)
        t.setFont("Times-Roman", size=self.size, leading=self.leading)
        for line in self.text.splitlines():
            t.textLine(line.strip())
        canvas.drawText(t)


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

    checked: bool = False
    width: float = 14
    height: float = 12

    def draw(self, canvas: Canvas, box: Box):
        canvas.rect(self.x, self.y, self.width, self.height)
        if self.checked:
            canvas.setFont("Times-Roman", 8)
            canvas.drawString(self.x, self.y, "X")


def make_br_checkbox(box: Box) -> Checkbox:
    """
    Creates a Checkbox with coords in the bottom-right corner of the box.
    """
    return Checkbox(x=box.br[0] - 16, y=box.br[1] + 4)


@dataclass
class MultilineCentered(Component):
    """
    A multiline text component, centered horizontally in the box.
    """

    text: str = ""
    size: float = 6.6
    leading: float = 7.7

    def draw(self, canvas: Canvas, box: Box):
        canvas.setFont("Times-Roman", size=self.size)
        line_num = 0
        for line in self.text.splitlines():
            canvas.drawCentredString(x=self.x, y=self.y - line_num * self.leading, text=line.strip())
            line_num += 1
