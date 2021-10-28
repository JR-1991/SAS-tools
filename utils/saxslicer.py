import re
from pathlib import Path
import pandas as pd
from lxml import etree


class SAXSlicer:
    """Separate data block and XML metadata footer of a .pdh SAXS output file."""

    def __init__(self, input_file: str = None):
        if input_file is None: input_file = "notebooks/datasets/SI06_210623[7].pdh"
        self.input_file = input_file

    def _line_is_xml(self, line_in_file):
        """Match n whitespaces, followed by an XML opening tag `<`."""
        any_whitespace = re.compile("\s*<").match(line_in_file)
        return any_whitespace
    
    
    def extract_data(self) -> pd.DataFrame:
        """Extract data block as `pandas.DataFrame`."""
        dataframe = pd.read_table(self.input_file, 
                                  delimiter = "   ", 
                                  usecols=[0,1], 
                                  names = ["scattering_vector", "counts_per_area"], 
                                  header=5, 
                                  skipfooter=496, 
                                  engine = "python"
                                 )
        return dataframe

    def extract_metadata(self, directory_for_XML_file: str = None) -> etree.ElementTree:
        """Extract XML metadata footer as `etree.ElementTree` and save to file."""
        if directory_for_XML_file is None: directory_for_XML_file = "notebooks/datasets/xml-test.xml"
        if not Path(directory_for_XML_file).is_file():
            with open(self.input_file, "r") as rf:
                with open(directory_for_XML_file, "w") as wf:
                    for line in rf:
                        if self._line_is_xml(line) is not None:
                            wf.write(line)
        XML_tree = etree.parse(directory_for_XML_file)
        return XML_tree