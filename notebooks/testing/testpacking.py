import re
from pathlib import Path
from typing import List
from libcombine import CombineArchive, OmexDescription, KnownFormats, VCard


CWD = Path.cwd()
TESTFILE = Path(CWD / "./notebooks/datasets/processed/test_experiment.animl")
TESTARCHIVE = Path(CWD / "./notebooks/testing/OMEX/test_experiment.omex")
TESTDIR = Path(CWD / "./notebooks/datasets/raw")
TESTDIR2 = Path(CWD / "./notebooks/datasets/processed")
IS_SUFFIX = re.compile("(\.*[\w\d]+)+", re.IGNORECASE)


class OMEXWriter():

    def __init__(self):
        self.omex = CombineArchive()
        if KnownFormats.lookupFormat("animl") == "":
            KnownFormats.addKnownFormat("animl", "http://purl.org/NET/mediatypes/application/x.animl")
        if KnownFormats.lookupFormat("pdh") == "":
            KnownFormats.addKnownFormat("pdh", "http://purl.org/NET/mediatypes/application/x.pdh")
        if KnownFormats.lookupFormat("plt") == "":
            KnownFormats.addKnownFormat("plt", "http://purl.org/NET/mediatypes/application/x.plt")
    
    def add_AnIML(self, path_to_dir, *authors_vcards) -> None:
        given_path = Path(path_to_dir)
        if given_path.is_file():
            given_name = str(given_path.name)
        else:
            contents=list(given_path.glob("**/*.animl"))
            if len(contents) == 1:
                given_path = str(contents[0])
                given_name = str(contents[0].name)                
            else:
                raise IndexError(f"One .animl file expected, got {len(contents)}.")
        path_in_omex = f"./{given_name}"

        self.omex.addFile(str(given_path),
            path_in_omex,
            KnownFormats.lookupFormat("animl"),
            True
        )
        description = OmexDescription()
        description.setAbout(path_in_omex)
        description.setDescription("An AnIML test experiment file")
        description.setCreated(OmexDescription.getCurrentDateAndTime())
        for vcard in authors_vcards:
            description.addCreator(vcard)
        self.omex.addMetadata(path_in_omex, description)

    def add_data(self, path_to_dir, file_suffixes: List[str], *authors_vcards) -> None:
        given_path = Path(path_to_dir)
        files_to_add=[]
        for suffix in file_suffixes:
            if IS_SUFFIX.match(suffix):
                contents=list(given_path.glob(f"**/*{suffix}"))
                files_to_add.extend(contents)
                for file in files_to_add:
                    path_in_omex = f"./data/{file.name}"
                    self.omex.addFile(str(file),
                        path_in_omex,
                        KnownFormats.lookupFormat(suffix),
                        False
                    )
                    description = OmexDescription()
                    description.setAbout(path_in_omex)
                    description.setDescription("Additional data referenced in the AnIML file")
                    description.setCreated(OmexDescription.getCurrentDateAndTime())
                    for vcard in authors_vcards:
                        description.addCreator(vcard)
                    self.omex.addMetadata(path_in_omex, description)
            else:
                raise ValueError(f"\"{suffix}\" is not a valid file suffix.")

    def create_omex(self, path_to_dir):
        self.omex.writeToFile(str(path_to_dir))


def _VCard_wrapper(family_name: str, given_name: str, email: str = None, organization: str = None) -> VCard():    
    vcard = VCard()
    vcard.setFamilyName(family_name)
    vcard.setGivenName(given_name)
    if email is not None:
        vcard.setEmail(email)
    if organization is not None:
        vcard.setOrganization(organization)
    return vcard


if __name__ == "__main__":
    writer = OMEXWriter()

    giess = _VCard_wrapper(
        family_name="Giess",
        given_name="Torsten",
        email="torsten.giess@ibtb.uni-stuttgart.de",
        organization="SFB 1333"
    )
    itzigehl = _VCard_wrapper(
        family_name="Itzigehl",
        given_name="Selina"
    )

    writer.add_AnIML(str(TESTFILE), giess, itzigehl)
    writer.add_data(str(TESTDIR), ["pdh"], itzigehl)
    writer.add_data(str(TESTDIR2), ["png", "tsv"], giess, itzigehl)

    writer.create_omex(str(TESTARCHIVE))
