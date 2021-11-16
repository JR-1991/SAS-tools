""" Datamodel for SAXS with export functionalities to JSON and XML. """


__all__ = []
__version__ = "0.1.1"
__author__ = "Torsten Giess"

from typing import List, Union, Optional

# import pandas as pd
from dataclasses import dataclass
from softdata import SchemaBase, attribute, element


@dataclass
class Value(SchemaBase):
    """ Values are the endpoints of the metadata tree. """

    value: object
    # key: Optional[str] = attribute(name="key")
    # name: Optional[str] = attribute(name="name")
    # value_att: Optional[str] = attribute(name="value")
    # stddev: Optional[str] = attribute(name="stddev")
    # unit: Optional[str] = attribute(name="unit")
    # quantity: Optional[str] = attribute(name="quantity")
    # counts: Optional[str] = attribute(name="counts")
    # type_: Optional[str] = attribute(name="type")
    # db: Optional[str] = attribute(name="db")
    # link: Optional[str] = attribute(name="link")
    # list_: Optional[str] = attribute(name="list")
    # meaning: Optional[str] = attribute(name="meaning")
    # index: Optional[int] = attribute(name="index")
    # positionindex: Optional[int] = attribute(name="positionindex")
    # waxsindex: Optional[int] = attribute(name="waxsindex")
    # x: Optional[int] = attribute(name="X")
    # y: Optional[int] = attribute(name="Y")
    # tol: Optional[Union[int, float]] = attribute(name="tol")
    # min_: Optional[Union[int, float]] = attribute(name="min")
    # max_: Optional[Union[int, float]] = attribute(name="max")


@dataclass
class List_(SchemaBase):
    """ Lists contain instances of `Value`. """

    key: str = attribute(name="key")
    islimited: Optional[bool] = attribute(name="islimited")
    value: List[Value] = element(name="value", default=list)


@dataclass
class Group(SchemaBase):
    """ Groups contain instances of `Value` and `List_`. """

    isdevice: bool = attribute(name="isdevice")
    category: str = attribute(name="category")
    sub: str = attribute(name="sub")
    key: str = attribute(name="key")
    id: str = attribute(name="id")
    list_: List[List_] = element(name="list", default=list)
    value: List[Value] = element(name="value", default=list)


@dataclass
class Setup(SchemaBase):
    """ Setup contains instrument-related instances of `Group`. """

    groups: List[Group] = element(name="group", default=list)


@dataclass
class Parameter(SchemaBase):
    """ Parameters describe the measurement program through instances of `Value`. """

    key: str = attribute(name="key")
    type: Optional[str] = attribute(name="type")
    index: Optional[int] = attribute(name="idex")
    value: List[Value] = element(name="value", default=list)


@dataclass
class Column(SchemaBase):
    """ Columns describe the data columns through instances of `Value`. """

    key: str = attribute(name="key")
    value: List[Value] = element(name="value", default=list)


@dataclass
class Fileinfo(SchemaBase):
    """ Metadata class for SAXS datamodel. """

    version: str = attribute(name="version")
    columns: List[Column] = element(name="column", default=list)
    parameters: List[Parameter] = element(name="parameter", default=list)
    setup: Setup = element(name="setup", default=Setup)
