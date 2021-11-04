import os

from pyaniml import AnIMLDocument, Sample, Series, Parameter, ExperimentStep, Device, IndividualValueSet
from datablubb import Value, List_, Group, Setup, Parameter, Column, Fileinfo

if __name__ == "__main__":
    with open("./datamodel/xml-test.xml", "r") as f:
        xml_string = f.read()
        print(xml_string)
        metadata = Fileinfo.fromXMLString(xml_string)