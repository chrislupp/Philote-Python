from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PartialsMetaData(_message.Message):
    __slots__ = ["name", "subname"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SUBNAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    subname: str
    def __init__(self, name: _Optional[str] = ..., subname: _Optional[str] = ...) -> None: ...

class VariableMetaData(_message.Message):
    __slots__ = ["discrete", "input", "name", "shape", "units"]
    DISCRETE_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    discrete: bool
    input: bool
    name: str
    shape: _containers.RepeatedScalarFieldContainer[int]
    units: str
    def __init__(self, input: bool = ..., discrete: bool = ..., name: _Optional[str] = ..., shape: _Optional[_Iterable[int]] = ..., units: _Optional[str] = ...) -> None: ...
