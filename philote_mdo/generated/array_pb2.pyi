from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Array(_message.Message):
    __slots__ = ["continuous", "discrete", "end", "name", "start", "subname"]
    CONTINUOUS_FIELD_NUMBER: _ClassVar[int]
    DISCRETE_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    SUBNAME_FIELD_NUMBER: _ClassVar[int]
    continuous: _containers.RepeatedScalarFieldContainer[float]
    discrete: _containers.RepeatedScalarFieldContainer[float]
    end: int
    name: str
    start: int
    subname: str
    def __init__(self, name: _Optional[str] = ..., subname: _Optional[str] = ..., start: _Optional[int] = ..., end: _Optional[int] = ..., continuous: _Optional[_Iterable[float]] = ..., discrete: _Optional[_Iterable[float]] = ...) -> None: ...
