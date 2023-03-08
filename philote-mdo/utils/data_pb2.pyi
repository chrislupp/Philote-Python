import array_pb2 as _array_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Partials(_message.Message):
    __slots__ = ["data", "f", "x"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    F_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[_array_pb2.DoubleArray]
    f: _containers.RepeatedScalarFieldContainer[str]
    x: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, f: _Optional[_Iterable[str]] = ..., x: _Optional[_Iterable[str]] = ..., data: _Optional[_Iterable[_Union[_array_pb2.DoubleArray, _Mapping]]] = ...) -> None: ...

class VariableMetaData(_message.Message):
    __slots__ = ["id", "input", "name", "units"]
    ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    id: _containers.RepeatedScalarFieldContainer[int]
    input: bool
    name: str
    units: str
    def __init__(self, input: bool = ..., name: _Optional[str] = ..., id: _Optional[_Iterable[int]] = ..., units: _Optional[str] = ...) -> None: ...

class Variables(_message.Message):
    __slots__ = ["continuous", "discrete"]
    class ContinuousEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _array_pb2.DoubleArray
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_array_pb2.DoubleArray, _Mapping]] = ...) -> None: ...
    class DiscreteEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _array_pb2.IntArray
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_array_pb2.IntArray, _Mapping]] = ...) -> None: ...
    CONTINUOUS_FIELD_NUMBER: _ClassVar[int]
    DISCRETE_FIELD_NUMBER: _ClassVar[int]
    continuous: _containers.MessageMap[str, _array_pb2.DoubleArray]
    discrete: _containers.MessageMap[str, _array_pb2.IntArray]
    def __init__(self, continuous: _Optional[_Mapping[str, _array_pb2.DoubleArray]] = ..., discrete: _Optional[_Mapping[str, _array_pb2.IntArray]] = ...) -> None: ...
