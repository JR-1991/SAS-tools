"""Prototype feature that packs files into an OMEX archive."""

__all__ = ["OMEXWriter", "OMEXvCard"]


from dataclasses import dataclass
from pathlib import Path
import re
from typing import List, Optional

from libcombine import CombineArchive, OmexDescription, KnownFormats, VCard

from modules.loggerfromjson import logger_from_json


IS_SUFFIX = re.compile("(\.*[\w\d]+)+", re.IGNORECASE)


print(f"Initializing logger for '{__name__}'.")
logger = logger_from_json(Path(__file__).parents[2] / "logs/")
logger.name = __name__


class OMEXWriter:
    """Writer for adding AnIML and other files to a Combine archive."""

    def __init__(self):
        logger.debug(
            f"Constructor called, '{self.__repr__()}'@{hex(id(self))} initialised."
        )
        self.omex = CombineArchive()
        if KnownFormats.lookupFormat("animl") == "":
            KnownFormats.addKnownFormat(
                "animl", "http://purl.org/NET/mediatypes/application/x.animl"
            )
            logger.info("Format 'animl' unknown, generic format URI added.")
        if KnownFormats.lookupFormat("pdh") == "":
            KnownFormats.addKnownFormat(
                "pdh", "http://purl.org/NET/mediatypes/application/x.pdh"
            )
            logger.info("Format 'pdh' unknown, generic format URI added.")
        if KnownFormats.lookupFormat("plt") == "":
            KnownFormats.addKnownFormat(
                "plt", "http://purl.org/NET/mediatypes/application/x.plt"
            )
            logger.info("Format 'plt' unknown, generic format URI added.")

    def __del__(self):
        logger.debug(
            f"Destructor called, '{self.__repr__()}'@{hex(id(self))} deleted."
        )

    def __del__(self):
        return "OMEXWriter"

    def add_AnIML(self, path_to_dir, *authors_vcards) -> None:
        """Add a single AnIML document to the archive object."""
        given_path = Path(path_to_dir)
        if given_path.is_file():
            given_name = str(given_path.name)
        else:
            contents = list(given_path.glob("**/*.animl"))
            if len(contents) == 1:
                given_path = str(contents[0])
                given_name = str(contents[0].name)
            else:
                raise IndexError(
                    f"One .animl file expected, got {len(contents)}."
                )

        path_in_omex = f"./{given_name}"

        self.omex.addFile(
            str(given_path),
            path_in_omex,
            KnownFormats.lookupFormat("animl"),
            True,
        )
        description = OmexDescription()
        description.setAbout(path_in_omex)
        description.setDescription("An AnIML test experiment file")
        description.setCreated(OmexDescription.getCurrentDateAndTime())
        for vcard in authors_vcards:
            description.addCreator(vcard)
        self.omex.addMetadata(path_in_omex, description)
        logger.debug("AnIML document added to 'CombineArchive' object.")

    def add_data(
        self, path_to_dir, file_suffixes: List[str], *authors_vcards
    ) -> None:
        """Add desired additional documents to the archive object."""
        given_path = Path(path_to_dir)
        files_to_add = []
        for suffix in file_suffixes:
            try:
                if IS_SUFFIX.match(suffix):
                    contents = list(given_path.glob(f"**/*{suffix}"))
                    files_to_add.extend(contents)
                    logger.debug(
                        f"Additional data will be added:\n{files_to_add}."
                    )
                    for file in files_to_add:
                        path_in_omex = f"./data/{file.name}"
                        self.omex.addFile(
                            str(file),
                            path_in_omex,
                            KnownFormats.lookupFormat(suffix),
                            False,
                        )
                        description = OmexDescription()
                        description.setAbout(path_in_omex)
                        description.setDescription(
                            "Additional data referenced in the AnIML file"
                        )
                        description.setCreated(
                            OmexDescription.getCurrentDateAndTime()
                        )
                        for vcard in authors_vcards:
                            description.addCreator(vcard)
                        self.omex.addMetadata(path_in_omex, description)
            except ValueError as e:
                logger.exception(f'"{suffix}" is not a valid file suffix.')
            files_to_add.clear()
            logger.debug("Additional data added to 'CombineArchive' object.")

    def create_omex(self, path_to_dir):
        """Create combine archive from the archive object."""
        self.omex.writeToFile(path_to_dir)
        logger.debug(f"Combine archive created at '{path_to_dir}'.")


@dataclass
class OMEXvCard:
    """Dataclass for author vCards required for Combine archives."""

    family_name: str
    given_name: str
    email: Optional[str] = None
    organization: Optional[str] = None

    def __post_init__(self):
        logger.debug(
            f"Constructor called, '{self.__repr__()}'@{hex(id(self))} initialised."
        )
        self.vcard = VCard()

    def __del__(self):
        logger.debug(
            f"Destructor called, '{self.__repr__()}'@{hex(id(self))} deleted."
        )

    def __repr__(self):
        return "OMEXvCard"

    def set_family_name(self, family_name: str) -> None:
        self.family_name = family_name

    def set_given_name(self, given_name: str) -> None:
        self.given_name = given_name

    def set_email(self, email: str) -> None:
        self.email = email

    def del_email(self) -> None:
        self.email = None

    def set_organization(self, organization: str) -> None:
        self.organization = organization

    def del_organization(self) -> None:
        self.organization = None

    def get_vcard(self):
        self.vcard.setFamilyName(self.family_name)
        self.vcard.setGivenName(self.given_name)
        if self.email:
            self.vcard.setEmail(self.email)
        if self.organization:
            self.vcard.setOrganization(self.organization)
        return self.vcard
