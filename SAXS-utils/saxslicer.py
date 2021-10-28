import re
import pandas as pd
from lxml import etree

class SAXSlicer:
    """Separate data block and XML metadata footer of a .pdh SAXS output file."""
    
    def __init__(self, inputFile: str = None):
        if inputFile is None: inputFile = "Jupyter/datasets/SI06_210623[7].pdh"
        self.inputFile = inputFile

    def _line_is_xml(self, lineInFile):
        """Match n whitespaces, followed by an XML opening tag `<`."""
        anyWhitespace = re.compile("\s*<").match(lineInFile)
        return anyWhitespace
    
    def extract_data(self) -> pd.DataFrame:
        """Extract data block as `pandas.DataFrame`."""
        dataFrame = pd.read_table(self.inputFile, delimiter = "   ", usecols=[0,1], names = ["scatteringVector", "countsPerArea"], header=5, skipfooter=496, engine = "python")
        return dataFrame

    def extract_metadata(self, directoryForXMLFile: str = None) -> etree.ElementTree:
        """Extract XML metadata footer as `etree.ElementTree` and save to file."""
        if directoryForXMLFile is None: directoryForXMLFile = "Jupyter/datasets/xml-test.xml"
        with open(self.inputFile, "r") as rf:
            with open(directoryForXMLFile, "w") as wf:
                for line in rf:
                    if self._line_is_xml(line) is not None:
                        wf.write(line)
        XMLTree = etree.parse(directoryForXMLFile)
        return XMLTree