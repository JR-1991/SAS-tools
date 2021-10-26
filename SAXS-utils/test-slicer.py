from saxslicer import SAXSlicer
from lxml import etree

def main():
    slic = SAXSlicer()
    data = slic.extract_data()
    #metadata = slic.extract_metadata()
    print(data)
    #print((etree.tostring(metadata.getroot())).decode("utf-8"))

if __name__ == "__main__":
    main()