"""Module for reading PDH files and separating data and metadata."""


import os
from pathlib import Path
import re
import tempfile
from typing import List, Optional, Union

import pandas as pd
from lxml import etree

from modules.loggerfromjson import logger_from_json


print(f"Initializing logger for '{__name__}'.")
logger = logger_from_json(Path(__file__).parents[2] / "logs/")
logger.name = __name__


class PDHReader:
    """Separate data block and XML metadata footer of PDH files."""

    def __init__(
        self, path_to_directory: Optional[Union[str, bytes, os.PathLike]]
    ):
        logger.debug(
            f"Constructor called, '{self.__repr__()}'@{hex(id(self))} initialised."
        )
        path = list(Path(path_to_directory).glob("*.pdh"))
        self.input_files = {file.stem: file for file in path if file.is_file()}

    def __del__(self):
        logger.debug(
            f"Destructor called, '{self.__repr__()}'@{hex(id(self))} deleted."
        )

    def __repr__(self):
        return "PDHReader"

    def _line_is_xml(self, line_in_file):
        """Match n whitespaces, followed by an XML opening tag `<`."""
        any_whitespace = re.compile("\s*<").match(line_in_file)
        return any_whitespace

    def available_files(self) -> List[str]:
        return [name for name in self.input_files]

    def extract_data(self, filestem: str) -> pd.DataFrame:
        """Extract data block as `pandas.DataFrame`."""
        dataframe = pd.read_table(
            self.input_files[filestem],
            delimiter="   ",
            usecols=[0, 1],
            names=["scattering_vector", "counts_per_area"],
            header=5,
            skipfooter=496,
            engine="python",
        )
        logger.debug(f"Data extracted from '{filestem}'.")
        return dataframe

    def extract_metadata(self, filestem: str) -> etree.ElementTree:
        """Extract XML metadata footer as `etree.ElementTree`."""
        with tempfile.NamedTemporaryFile(mode="r+") as tmp:
            with self.input_files[filestem].open("r") as f:
                for line in f:
                    if self._line_is_xml(line) is not None:
                        tmp.write(line)
            logger.debug(f"Metadata extracted from '{filestem}'.")
            tmp.seek(0)
            XML_tree = etree.parse(tmp)
            logger.debug("Metadata casted to 'etree.ElementTree'.")
        return XML_tree
