from lxml import etree
from saxslicer import SAXSlicer

def main():
    """Test some stuff."""
    slic = SAXSlicer()
    #data = slic.extract_data()
    #print(data)
    metadata = slic.extract_metadata()
    print((etree.tostring(metadata.getroot())).decode("utf-8"))

if __name__ == "__main__":
    main()
