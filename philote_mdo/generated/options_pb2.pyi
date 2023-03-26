from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Options(_message.Message):
    __slots__ = ["num_double", "num_int"]
    NUM_DOUBLE_FIELD_NUMBER: _ClassVar[int]
    NUM_INT_FIELD_NUMBER: _ClassVar[int]
    num_double: int
    num_int: int
    def __init__(self, num_double: _Optional[int] = ..., num_int: _Optional[int] = ...) -> None: ...
