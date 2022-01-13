# Native packages
from dataclasses import dataclass
from pathlib import Path
# Established packages
from lxml import etree, objectify
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.handlers import LxmlEventHandler
# My packages
from datamodel import SchemaBase, element, text, SAXS


# Set constants
CWD = Path.cwd()
TO_OUTPUTS_REL = Path("notebooks/datasets/processed")
TO_OUTPUTS_ABS = CWD / TO_OUTPUTS_REL


# Define classes and functions
def print_xml(element_tree, pretty_print_bool: bool = True):
    print(etree.tostring(element_tree, pretty_print=pretty_print_bool).decode('utf-8'))


# Test the mapping
data_filename = Path("SAXS_results.tsv")
meta_filename = Path("CholPal_metadata.xml")

pdh_metadata = objectify.parse(str(TO_OUTPUTS_REL / meta_filename))
fileinfo = pdh_metadata.getroot()
print([ el.tag for el in fileinfo.column[0].iterchildren() ])
#print(objectify.dump(fileinfo))

# parser = XmlParser(handler=LxmlEventHandler)
# pdh_metadata = parser.parse(pdh_metadata)
#print(pdh_metadata)
