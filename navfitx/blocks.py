import datetime
import textwrap
from dataclasses import dataclass, field

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from navfitx.constants import MARGIN_BOTTOM, MARGIN_SIDE, MARGIN_TOP



@dataclass
class Block():
    """
    A block
    """

    nums: tuple[int]
    label: str
    x: float = 0
    y: float = 0


class Name():
    """
    Enter the member's last name, first name, middle initial, and suffix (if any)
    separated by spaces. Place a comma after the last name. Omit spaces and punctuation within a
    name (e.g., Denney, John A; STJohn, Melvin J II; Walters, J Arthur; Obrien, Mary S; Martin,
    Paul T JR; SmithJones, Ann.). The full middle name is acceptable but not required. NMN may
    be used if member does not have a middle name.
    """

    nums: tuple[int] = 1
    label: str = "Name"

    name: str = ""


class GradeRate():
    """
    The grade or rate the Service member is actually wearing on the ending
    date of the report.

    Enlisted: Use standard rate abbreviations (e.g., SA, ADAN, CS2, BM1, LNC, EMCS,
    PSCM, etc.).

    Officers: Use standard grade abbreviations (e.g., CAPT, CDR, LCDR, LT, LTJG, ENS,
    CWO5, CWO4, CWO3, CWO2, WO1 etc.).
    """

    nums: tuple[int] = 2
    label: str = "Rank/Rate"
    grade_or_rate: str = ""

    def __post_init__(self):
        self.x = LETTER[0] / 2
        self.y = Name().y


class DesigSelf():
    """
    Officer designator or enlisted warfare qualification designation

    Enlisted: Up to two enlisted warfare/qualification designators. If two designators are
    entered, separate with a slash. Do not leave spaces (e.g., AW, AW/PJ, SS/DV etc.) (if none,
    leave blank).

    Officers: Enter the four-digit officer designator as of the ending date of report. Do not use an
    alpha character for a numerical character.
    """

    nums: tuple[int] = 3
    label: str = "Design"

    desig: str = ""

    def __post_init__(self):
        grade_rate = GradeRate()
        self.x = grade_rate.x + inch * (65 / 72)
        self.y = grade_rate.y


class SSN():
    """
    Service member's full SSN with hyphens after the third and fifth digits.
    It should be used for all reports that are mailed (e.g., 000-00-0000).
    """

    nums: tuple[int] = 4
    label: str = "SSN"

    ssn: str = ""

    def __post_init__(self):
        desig_self = DesigSelf()
        self.x = desig_self.x + inch * (1 + 3 / 9)
        self.y = desig_self.y


class Group():
    """
    This field is used for summary group comparison. For enlisted, group all
    ACT and Training and Administration of Reserves (TAR) together and group inactive duty
    (INACT) and annual training (AT)/active duty for operational support (ADOS) separately. For
    officers, do not mix summary groups. Place an X in only one box to indicate the member’s
    status as follows:

    ACT – All active duty (ACDU) Navy who compete together for the same active-duty
    promotion quotas.

    TAR – All Navy Reserve personnel designated TAR who compete for TAR promotion
    quotas.

    INACT – All Navy reservists on INACT duty (drill status) who compete for INACT
    promotion quotas (refer to chapter 9).

    AT/ADOS – All Navy Reservists on temporary ACDU but still compete for INACT
    promotion quotas. Includes all annual training (AT), active duty for training (ADT), active
    duty for ADOS, 1-year recall (OYR), canvasser recruiter (CANREC), mobilization, recall,
    etc. (refer to chapter 10).
    """

    nums: tuple[int] = 5
    label: str = "Duty/Competitive Status"

    group: str = ""

    def __post_init__(self):
        self.x = MARGIN_SIDE
        self.y = LETTER[1] - MARGIN_TOP - inch * (2 / 9)


class UIC():
    """
    the UIC of the Service member's ship or station. Normally a UIC is a
    breakout for enlisted personnel; however, if reporting seniors have more than one UIC with
    enlisted personnel attached, but desires to group all enlisted personnel together, they may do so.
    If using UIC as a summary group comparison, block 6 should match the primary UIC of the
    reporting senior in block 26. For activities which no UIC is assigned, enter five zeros. The first
    four characters of a UIC must be numbers.

    Reserve activity (NRA) UIC. Use training unit identification code (TRUIC) if member is in-
    assignment processing (IAP) (refer to chapter 9).
    """

    nums: tuple[int] = 6
    label: str = "Unit ID Code (UIC)"

    uic: str = ""

    def __post_init__(self):
        group = Group()
        self.x = MARGIN_SIDE + 152
        self.y = group.y


class ShipStation():
    """
    Abbreviated name of the activity to which the member is assigned, for the duty reported on. Do not spell
    out letters and numbers (e.g., use A instead of ALFA, 1 instead of ONE etc.).
    """

    nums: tuple[int] = 7
    label: str = "Ship/Station"

    station: str = ""

    def __post_init__(self):
        uic = UIC()
        self.x = 235  # TODO: make this relative?
        self.y = uic.y


class PromotionStatus():
    """
    member's promotion status on the ending date of the report period
    """

    nums: tuple[int] = 8
    label: str = "Promotion Status"

    status: str = ""

    def __post_init__(self):
        ship_station = ShipStation()
        self.x = 428  # TODO: make this relative?
        self.y = ship_station.y


class DateReported():
    nums: tuple[int] = 9
    label: str = "Date Reported"

    date: datetime.date | None = None



class OccasionForReport():
    """
    Select all applicable options or place an “X” in each block that
    applies. See chapter 3 for reporting occasions.

    Note: More than one occasion may apply, except Special cannot be combined with another
    occasion. Do not submit a Special report if another occasion applies.
    """

    nums: tuple[int] = (10, 11, 12, 13)
    label: str = "Occasion for Report"

    occasion: str = ""


class PeriodOfReport():
    """
    YYMMMDD format

    Regular Reports: The FROM date must be the day following the TO date of the last Regular
    report. It can be earlier than block 9 if en route leave, travel, or temporary duty (TEMDU) is
    included.
    """

    nums: tuple[int] = (14, 15)
    label: str = "Period of Report"

    start: datetime.date | None = None
    end: datetime.date | None = None



class NotObserved():
    nums: tuple[int] = 16
    label: str = "Not Observed Report (NOB)"
    nob: bool = False



class TypeOfReport():
    """
    Select the option or place an “X” in the block that applies. If this is a
    Concurrent/Regular report, place an “X” in blocks 17 and 18.
    """

    nums: tuple[int] = (17, 18, 19)
    label: str = "Type of Report"

    tor: str = ""



class PhysicalReadiness():
    nums: tuple[int] = 20
    label: str = "Physical Readiness"

    pfa_code: str = ""



class BilletSubcategory():
    nums: tuple[int] = 21
    label: str = "Billet Subcategory"

    code: str = ""


class ReportingSeniorName():
    nums: tuple[int] = 22
    label: str = "Reporting Senior Name"

    name: str = ""

class ReportingSeniorGrade():
    nums: tuple[int] = 23
    label: str = "Reporing Senior Grade"

    grade: str = ""



class ReportingSeniorDesig():
    nums: tuple[int] = 24
    label: str = "Reporting Senior Designator"

    desig: str = ""


class ReportingSeniorTitle():
    nums: tuple[int] = 25
    label: str = "Reporting Senior Title"

    title: str = ""


class ReportingSeniorUIC():
    nums: tuple[int] = 26
    label: str = "Reporting Senior UIC"

    uic: str = ""


class ReportingSeniorSSN():
    nums: tuple[int] = 27
    label: str = "Reporting Senior SSN"

    ssn: str = ""


class EmploymentAndAchievements():
    label: str = "Command Employment and Commmand Achievements"

    text: str = ""


class DutiesAndPFA():
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

    label: str = "Primary/Collateral/Watchstanding Duties/PFA"

    duty: str = ""
    text: str = ""


class DateCounseled():
    label: str = "Date Counseled"

    date: datetime.date | None = None


class Counselor(Block):
    label: str = "Counselor"

    name: str = ""


class Signature(Block):
    label: str = "Signature"

    signed: bool = False


class ProfessionalExpertise(Block):
    label: str = "Professional Expertise"

    rating: int | None = None


class CMEO(Block):
    label: str = "Command or Organizational Climate/Equal Opportunity and Accountability"

    rating: int | None = None


class Bearing(Block):
    label: str = "Military Bearing/Character"


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

    label: str = "COMMENTS ON PERFORMANCE"

    def validate(self):
        lines = textwrap.wrap(self.comments, width=91)
        if len(lines) > 18:
            raise ValueError("Block 41 comments cannot exceed 18 lines of 91 characters each.")


@dataclass
class Fitrep:
    c: canvas.Canvas = field(default_factory=lambda: canvas.Canvas("fitrep.pdf", pagesize=LETTER))

    b1: Name = field(default_factory=Name)
    b2: GradeRate = field(default_factory=GradeRate)
    b3: DesigSelf = field(default_factory=DesigSelf)
    b4: SSN = field(default_factory=SSN)
    b5: Group = field(default_factory=Group)
    b6: UIC = field(default_factory=UIC)
    b7: ShipStation = field(default_factory=ShipStation)
    b8: PromotionStatus = field(default_factory=PromotionStatus)
    b9: DateReported = field(default_factory=DateReported)
    b10_to_13: OccasionForReport = field(default_factory=OccasionForReport)
    b14_to_15: PeriodOfReport = field(default_factory=PeriodOfReport)
    b16: NotObserved = field(default_factory=NotObserved)
    b17_to_19: TypeOfReport = field(default_factory=TypeOfReport)
    b20: PhysicalReadiness = field(default_factory=PhysicalReadiness)
    b21: BilletSubcategory = field(default_factory=BilletSubcategory)
    b22: ReportingSeniorName = field(default_factory=ReportingSeniorName)
    b23: ReportingSeniorGrade = field(default_factory=ReportingSeniorGrade)
    b24: ReportingSeniorDesig = field(default_factory=ReportingSeniorDesig)
    b25: ReportingSeniorTitle = field(default_factory=ReportingSeniorTitle)
    b26: ReportingSeniorUIC = field(default_factory=ReportingSeniorUIC)
    b27: ReportingSeniorSSN = field(default_factory=ReportingSeniorSSN)
    b28: EmploymentAndAchievements = field(default_factory=EmploymentAndAchievements)
    b29: DutiesAndPFA = field(default_factory=DutiesAndPFA)
    b30: DateCounseled = field(default_factory=DateCounseled)
    b31: Counselor = field(default_factory=Counselor)
    b32: Signature = field(default_factory=Signature)
    b33: ProfessionalExpertise = field(default_factory=ProfessionalExpertise)
    b34: CMEO = field(default_factory=CMEO)

    def draw_layout(self):
        self.c.rect(MARGIN_SIDE, MARGIN_BOTTOM, LETTER[0] - 2 * MARGIN_SIDE, LETTER[1] - MARGIN_TOP - MARGIN_BOTTOM)


f = Fitrep()
