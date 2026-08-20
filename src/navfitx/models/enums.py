from enum import Enum, StrEnum


class DutyStatus(StrEnum):
    # BLANK = ""
    ACT = "ACT"
    TAR = "TAR"
    INACT = "INACT"
    ATADSW = "ATADSW"


class PromotionStatus(StrEnum):
    # BLANK = ""
    REGULAR = "REGULAR"
    FROCKED = "FROCKED"
    SELECTED = "SELECTED"
    SPOT = "SPOT"


# class PhysicalReadiness(StrEnum):
#     # BLANK = ""
#     PASS = "P"
#     BCA_PASS = "B"
#     FAIL = "F"
#     MED_WAIVED = "M"
#     WAIVED = "W"
#     NO_PFA = "N"


class BilletSubcategory(StrEnum):
    # BLANK = ""
    NA = "NA"
    BASIC = "BASIC"
    APPROVED = "APPROVED"
    INDIV_AUGMENT = "INDIV AUG"
    CO_AFLOAT = "CO AFLOAT"
    CO_ASHORE = "CO ASHORE"
    OIC = "OIC"
    SEA_COMP = "SEA COMP"
    CRF = "CRF"
    CANVASSER = "CANVASSER"
    RESIDENT = "RESIDENT"
    INTERN = "INTERN"
    INSTRUCTOR = "INSTRUCTOR"
    STUDENT = "STUDENT"
    RESAC1 = "RESAC1"
    RESAC6 = "RESAC6"
    SCREENED = "SCREENED"
    SPECIAL01 = "SPECIAL01"
    SPECIAL02 = "SPECIAL02"
    SPECIAL03 = "SPECIAL03"
    SPECIAL04 = "SPECIAL04"
    SPECIAL05 = "SPECIAL05"
    SPECIAL06 = "SPECIAL06"
    SPECIAL07 = "SPECIAL07"
    SPECIAL08 = "SPECIAL08"
    SPECIAL09 = "SPECIAL09"
    SPECIAL10 = "SPECIAL10"
    SPECIAL11 = "SPECIAL11"
    SPECIAL12 = "SPECIAL12"
    SPECIAL13 = "SPECIAL13"
    SPECIAL14 = "SPECIAL14"
    SPECIAL15 = "SPECIAL15"
    SPECIAL16 = "SPECIAL16"
    SPECIAL17 = "SPECIAL17"
    SPECIAL18 = "SPECIAL18"
    SPECIAL19 = "SPECIAL19"
    SPECIAL20 = "SPECIAL20"


class PromotionRecommendation(Enum):
    NOB = 0
    SIGNIFICANT_PROBLEMS = 1
    PROGRESSING = 2
    PROMOTABLE = 3
    MUST_PROMOTE = 4
    EARLY_PROMOTE = 5


class RetentionRecommendation(Enum):
    NOT_RECOMMENDED = 0
    RECOMMENDED = 1
