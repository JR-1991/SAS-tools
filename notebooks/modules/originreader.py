"""Reader for Origin TXT output files containing Lorentzian data."""


from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from modules.loggerfromjson import logger_from_json


print(f"Initializing logger for '{__name__}'.")
logger = logger_from_json(Path(__file__).parents[2] / "logs/")
logger.name = __name__


@dataclass
class LorentzianReader:
    """Dataclass for handling Lorentzian data from Origin TXT file."""

    file: str

    def __post_init__(self):
        logger.debug(
            f"Constructor called, '{self.__repr__()}'@{hex(id(self))} initialised."
        )
        file = Path(self.file)
        with file.open("r") as txt:
            self.dataframe = pd.read_table(
                filepath_or_buffer=txt,
                header=0,
                names=[
                    "quantity",
                    "symbol",
                    "value",
                    "stddev",
                    "t-value",
                    "probabililty",
                    "dependency",
                ],
                engine="python",
            )
        logger.debug(f"Data extracted from '{file}'.")
        self.xc_values = self.dataframe.loc[self.dataframe["symbol"] == "xc"]

    def __del__(self):
        logger.debug(
            f"Destructor called, '{self.__repr__()}'@{hex(id(self))} deleted."
        )

    def __repr__(self):
        return "LorentzianReader"

    def get_full_dataframe(self):
        return self.dataframe

    def get_xc_dataframe(self):
        return self.xc_values
