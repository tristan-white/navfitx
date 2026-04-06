"""
Constants used throughout the NAVFITX app.
"""

# Used for drawing PDFs.
# Currently, NAVFITX does not draw PDFs from scratch, but writes data on top of blank PDF templates.
# However, if in the future it needs to create PDFs from scratch, this can be accomplished using
# the reportlab library.
MARGIN_TOP = 22
MARGIN_BOTTOM = 46
MARGIN_RIGHT = 46
MARGIN_LEFT = 17
MARGIN_SIDES = MARGIN_LEFT + MARGIN_RIGHT

SITE_URL = "https://navfitx.com"

BUPERSINST_URL = "https://www.mynavyhr.navy.mil/Portals/55/Reference/Instructions/BUPERS/BUPERSINST%201610.10.pdf?ver=g42WV7fkucvkkZolLrWseA%3d%3d"

# used for platformdirs
APP_NAME = "navfitx"
APP_AUTHOR = "tristan-white"


DUTIES_DESC_SPACE_FOR_ABBREV = 21
