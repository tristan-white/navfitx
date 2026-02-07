"""
Utility functions used multiple times throughout the NAVFITX app.
"""

import importlib.resources as resources
import textwrap
from pathlib import Path

from navfitx.constants import DUTIES_DESC_SPACE_FOR_ABBREV


def get_blank_report_path(report: str) -> Path:
    """
    Return a pathlib.Path to the bundled PDF.
    The file is extracted to a temporary location if the package is zipped.

    Args:
        report (str): The type of report for which to retrieve a path.
    """
    options = {"fitrep", "chief", "eval", "summary"}
    assert report in options, f"report must be one of {options}"
    with resources.path("navfitx.data", f"blank_{report}.pdf") as pdf_path:
        return pdf_path


def get_icon_path() -> Path:
    """
    Return a pathlib.Path to the bundled icon.
    The file is extracted to a temporary location if the package is zipped.
    """
    with resources.path("navfitx.data", "navfit98.ico") as icon_path:
        return icon_path


def wrap_duty_desc(text: str) -> str:
    """
    The duties description is weird because the user manual says the constraint on this
    box is "up to 334 alhphanumeric characters without spaces".
    In practice, there are 4 lines. The first can have up to 69 characters (not including newline),
    and the next three can have up to 91 charaters (not including newline).
    """
    text = DUTIES_DESC_SPACE_FOR_ABBREV * " " + text
    text = textwrap.fill(text, width=91)
    return text
