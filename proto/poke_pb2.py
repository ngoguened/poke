# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: poke.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'poke.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\npoke.proto\" \n\rRequestHeader\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"H\n\x0fRegisterRequest\x12\x1e\n\x06header\x18\x01 \x01(\x0b\x32\x0e.RequestHeader\x12\x15\n\rfirst_connect\x18\x02 \x01(\x08\"\x0f\n\rRegisterReply\"h\n\x05Model\x12\x15\n\rclient_health\x18\x01 \x01(\x05\x12\x17\n\x0fopponent_health\x18\x02 \x01(\x05\x12\x13\n\x06winner\x18\x03 \x01(\x08H\x00\x88\x01\x01\x12\x0f\n\x07playing\x18\x04 \x01(\x08\x42\t\n\x07_winner\"1\n\x0fGetModelRequest\x12\x1e\n\x06header\x18\x01 \x01(\x0b\x32\x0e.RequestHeader\"&\n\rGetModelReply\x12\x15\n\x05model\x18\x01 \x01(\x0b\x32\x06.Model\"\x06\n\x04Move\"R\n\x0e\x43ommandRequest\x12\x1e\n\x06header\x18\x01 \x01(\x0b\x32\x0e.RequestHeader\x12\x15\n\x04move\x18\x02 \x01(\x0b\x32\x05.MoveH\x00\x42\t\n\x07\x63ommand\"$\n\x0c\x43ommandReply\x12\x14\n\x04\x64iff\x18\x01 \x01(\x0b\x32\x06.Model\"-\n\x0bWaitRequest\x12\x1e\n\x06header\x18\x01 \x01(\x0b\x32\x0e.RequestHeader\"!\n\tWaitReply\x12\x14\n\x04\x64iff\x18\x01 \x01(\x0b\x32\x06.Model2\xb7\x01\n\x04Poke\x12.\n\x08Register\x12\x10.RegisterRequest\x1a\x0e.RegisterReply\"\x00\x12.\n\x08GetModel\x12\x10.GetModelRequest\x1a\x0e.GetModelReply\"\x00\x12+\n\x07\x43ommand\x12\x0f.CommandRequest\x1a\r.CommandReply\"\x00\x12\"\n\x04Wait\x12\x0c.WaitRequest\x1a\n.WaitReply\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'poke_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_REQUESTHEADER']._serialized_start=14
  _globals['_REQUESTHEADER']._serialized_end=46
  _globals['_REGISTERREQUEST']._serialized_start=48
  _globals['_REGISTERREQUEST']._serialized_end=120
  _globals['_REGISTERREPLY']._serialized_start=122
  _globals['_REGISTERREPLY']._serialized_end=137
  _globals['_MODEL']._serialized_start=139
  _globals['_MODEL']._serialized_end=243
  _globals['_GETMODELREQUEST']._serialized_start=245
  _globals['_GETMODELREQUEST']._serialized_end=294
  _globals['_GETMODELREPLY']._serialized_start=296
  _globals['_GETMODELREPLY']._serialized_end=334
  _globals['_MOVE']._serialized_start=336
  _globals['_MOVE']._serialized_end=342
  _globals['_COMMANDREQUEST']._serialized_start=344
  _globals['_COMMANDREQUEST']._serialized_end=426
  _globals['_COMMANDREPLY']._serialized_start=428
  _globals['_COMMANDREPLY']._serialized_end=464
  _globals['_WAITREQUEST']._serialized_start=466
  _globals['_WAITREQUEST']._serialized_end=511
  _globals['_WAITREPLY']._serialized_start=513
  _globals['_WAITREPLY']._serialized_end=546
  _globals['_POKE']._serialized_start=549
  _globals['_POKE']._serialized_end=732
# @@protoc_insertion_point(module_scope)