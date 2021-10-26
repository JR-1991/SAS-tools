from pathlib import Path
import pandas as pd
from lxml import etree
import re

inputFile = Path.cwd() / "Jupyter/datasets/SI06_210623[7].pdh"
xmlFile = Path.cwd() / "Jupyter/datasets/xml-test.xml"

data = pd.read_table(inputFile, delimiter = "   ", usecols=[0,1], names = ["scatteringVector", "countsPerArea"], header=5, skipfooter=496, engine = "python")
scatteringVector = data["scatteringVector"]
countsPerArea = data["countsPerArea"]

anyWhitespace = re.compile("\s*<")

with open(inputFile, "r") as rf:
    with open(xmlFile, "w") as wf:
        for line in rf:
            if not anyWhitespace.match(line) == None:
                wf.write(line)

#xmlTree = etree.parse(xmlFile)

#print((etree.tostring(xmlTree.getroot())).decode("utf-8"))