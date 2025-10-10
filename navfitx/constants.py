from enum import Enum

from reportlab.lib.units import inch

MARGIN_SIDE = inch * 4 / 9
MARGIN_TOP = inch / 2
MARGIN_BOTTOM = MARGIN_SIDE


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
