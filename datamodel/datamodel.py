""" Datamodel for SAXS with export functionalities to JSON and XML. """

__all__ = []
__version__ = "0.0.1"
__author__ = "Torsten Giess"

import json
from typing import List
from dataclasses import field

from pydantic.dataclasses import dataclass
from pydantic.json import pydantic_encoder
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig


@dataclass
class Value:
    """ Values are the endpoints of the metadata tree. """

    pass


@dataclass
class List_:
    """ Lists contain instances of `Value`. """

    pass


@dataclass
class Group:
    """ Groups contain instances of `Value` and `List_`. """

    pass


class Setup:
    """ Setup contains instrument-related instances of `Group`. """

    pass


@dataclass
class Parameter:
    """ Parameters describe the measurement program through instances of `Value`. """

    pass


@dataclass
class Column:
    """ Columns describe the data columns through instances of `Value`. """

    pass


@dataclass
class Fileinfo:
    """ Root element of SAXS metadata. """

    pass


if __name__ == "__main__":
    pass
