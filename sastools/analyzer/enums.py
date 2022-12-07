"""Enums used throughout the SAS-tools library"""

from enum import Enum, auto


class SAXSStandards(Enum):
    """Different standards used for calibration SAXS data"""

    CHOLESTERYL_PALMITATE = auto()
    SILVER_BEHENATE = auto()
