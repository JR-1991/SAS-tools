"""Enums used in the different analyzers."""

from enum import Enum, auto


class SAXSStandards(Enum):
    """Different standards used for calibration of SAXS data"""

    CHOLESTERYL_PALMITATE = auto()
    SILVER_BEHENATE = auto()
