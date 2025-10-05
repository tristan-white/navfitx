import textwrap
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Block(ABC):
    name: str

    @abstractmethod
    def validate(self):
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
