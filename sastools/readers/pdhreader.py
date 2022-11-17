"""Module for reading PDH files and separating data and metadata."""


import os
from pathlib import Path
import re
import tempfile
from typing import List, Optional, Union

import pandas as pd
from lxml import etree


class PDHReader:
    """Separate data block and XML metadata footer of PDH files."""

    def __init__(
        self, path_to_directory: Optional[Union[str, bytes, os.PathLike]]
    ):
        path = list(Path(path_to_directory).glob("*.pdh"))
        self.input_files = {file.stem: file for file in path if file.is_file()}

    def __repr__(self):
        return "PDHReader"

    def _line_is_xml(self, line_in_file):
        """Match n whitespaces, followed by an XML opening tag `<`."""
        any_whitespace = re.compile("\s*<").match(line_in_file)
        return any_whitespace

    def available_files(self) -> List[str]:
        return {count: value for count, value in enumerate(self.input_files)}

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
        return dataframe

    def extract_metadata(self, filestem: str) -> etree.ElementTree:
        """Extract XML metadata footer as `etree.ElementTree`."""
        with tempfile.NamedTemporaryFile(mode="r+") as tmp:
            with self.input_files[filestem].open("r") as f:
                for line in f:
                    if self._line_is_xml(line) is not None:
                        tmp.write(line)
            tmp.seek(0)
            XML_tree = etree.parse(tmp)
        return XML_tree


def main():
    test = PDHReader(
        (
            Path.cwd()
            / "notebooks/datasets/raw/OTAB_measurement_data/OTAB_000wtp_T025/"
        )
    )
    print(test.available_files())


if __name__ == "__main__":
    main()
