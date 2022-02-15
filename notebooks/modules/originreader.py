"""Reader for Origin TXT output files containing Lorentzian data."""


from dataclasses import dataclass
from pathlib import Path

import pandas as pd

# from modules.loggerfromjson import logger_from_json


# # Set up logging
# logger = logger_from_json(
#     json_cfg_file="./logs/logcfg.json",
#     custom_filename="SAXS-workflow"
# )
# logger.name = __name__


@dataclass
class ReadOriginLorentzian:
    """Dataclass for handling Lorentzian data from Origin TXT file."""

    file: str
    def __post_init__(self):
        # logger.info(
        #     f"Constructor called, {str(ReadOriginLorentzian)} initialised."
        # )
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
                    "dependency"
                ],
                engine="python"
            )
        self.xc_values = self.dataframe.loc[self.dataframe["symbol"] == "xc"]

    # def __del__(self):
    #     logger.info(f"Destructor called, {str(ReadOriginLorentzian)} deleted.")

    def get_full_dataframe(self):
        return self.dataframe

    def get_xc_dataframe(self):
        return self.xc_values
