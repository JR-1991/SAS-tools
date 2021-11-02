""" Datamodel for SAXS with export functionalities to JSON and XML. """

__all__ = []
__version__ = "0.0.1"
__author__ = "Torsten Giess"

import json
from typing import List, Union, Optional
from dataclasses import field

from pydantic.dataclasses import dataclass
from pydantic.json import pydantic_encoder
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig


@dataclass
class Value:
    """ Values are the endpoints of the metadata tree. """
    
    key: Optional[str]
    name: Optional[str]
    value: Optional[str]
    stddev: Optional[str]
    unit: Optional[str]
    quantity: Optional[str]
    counts: Optional[str]
    type: Optional[str]
    db: Optional[str]
    link: Optional[str]
    list__: Optional[str]
    meaning: Optional[str]
    index: Optional[int]
    positionindex: Optional[int]
    waxsindex: Optional[int]
    X: Optional[int]
    Y: Optional[int]
    tol: Optional[Union[int, float]]
    min_: Optional[Union[int, float]]
    max_: Optional[Union[int, float]]


@dataclass
class List_:
    """ Lists contain instances of `Value`. """
    
    key: str
    value: List[Value]


@dataclass
class Group:
    """ Groups contain instances of `Value` and `List_`. """
    
    isdevice: bool
    category: str
    sub: str = ""
    key: str
    id_: str
    list_: List[List_]
    value: List[Value]


@dataclass
class Setup:
    """ Setup contains instrument-related instances of `Group`. """
    
    key: str
    group: List[Group]


@dataclass
class Parameter:
    """ Parameters describe the measurement program through instances of `Value`. """
    
    key: str
    value: List[Value]


@dataclass
class Column:
    """ Columns describe the data columns through instances of `Value`. """    
    
    key: str
    value: List[Value]


@dataclass
class Fileinfo:
    """ Metadata class for SAXS datamodel. """
    
    version: str
    column: List[Column]
    parameter: List[Parameter]
    setup: List[Setup]


if __name__ == "__main__":
    pass
