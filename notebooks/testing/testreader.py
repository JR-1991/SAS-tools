from pathlib import Path
from lxml import etree


CWD = Path.cwd()


path_to_AnIML_file = Path(CWD / "./notebooks/datasets/processed/test_experiment.animl")

with path_to_AnIML_file.open("rb") as rbf:
    root = etree.fromstring(rbf.read())

cal_q = [ F.text for F in root.iterfind(".//Series[@seriesID='cal_q']/IndividualValueSet/F") ]
cal_i = [ F.text for F in root.iterfind(".//Series[@seriesID='cal_i']/IndividualValueSet/F") ]
sam_q = [ F.text for F in root.iterfind(".//Series[@seriesID='sam_q']/IndividualValueSet/F") ]
sam_i = [ F.text for F in root.iterfind(".//Series[@seriesID='sam_i']/IndividualValueSet/F") ]

print(f"Successfully read from AnIML.")
