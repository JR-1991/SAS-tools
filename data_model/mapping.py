import os

from pyaniml import AnIMLDocument, Sample, Series, Parameter, ExperimentStep, Device, IndividualValueSet
from datablubb import Value, List_, Group, Setup, Parameter, Column, Fileinfo

CWD = os.getcwd()

if __name__ == "__main__":
    xml_file = "/datamodel/xml-test.xml"
    path_to_file = "".join(CWD + xml_file)
    with open(path_to_file, "r") as f:
        xml_string = f.read()
        metadata = Fileinfo.fromXMLString(xml_string)
