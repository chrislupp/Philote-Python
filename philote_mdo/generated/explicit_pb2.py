# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: explicit.proto
"""Generated protocol buffer code."""
from . import options_pb2 as options__pb2
from . import metadata_pb2 as metadata__pb2
from . import array_pb2 as array__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0e\x65xplicit.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a\x0b\x61rray.proto\x1a\x0emetadata.proto\x1a\roptions.proto2\x8d\x02\n\x11\x45xplicitComponent\x12\x36\n\x10SetStreamOptions\x12\x08.Options\x1a\x16.google.protobuf.Empty\"\x00\x12\x36\n\x05Setup\x12\x16.google.protobuf.Empty\x1a\x11.VariableMetaData\"\x00\x30\x01\x12>\n\rSetupPartials\x12\x16.google.protobuf.Empty\x1a\x11.PartialsMetaData\"\x00\x30\x01\x12\x1f\n\x07\x43ompute\x12\x06.Array\x1a\x06.Array\"\x00(\x01\x30\x01\x12\'\n\x0f\x43omputePartials\x12\x06.Array\x1a\x06.Array\"\x00(\x01\x30\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'explicit_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _EXPLICITCOMPONENT._serialized_start = 92
    _EXPLICITCOMPONENT._serialized_end = 361
# @@protoc_insertion_point(module_scope)
