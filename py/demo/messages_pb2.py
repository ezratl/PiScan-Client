# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messages.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import request_pb2 as request__pb2
import context_pb2 as context__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='messages.proto',
  package='piscan_pb',
  syntax='proto3',
  serialized_pb=_b('\n\x0emessages.proto\x12\tpiscan_pb\x1a\rrequest.proto\x1a\rcontext.proto\"\xa5\x02\n\x0e\x43lientToServer\x12,\n\x04type\x18\x01 \x01(\x0e\x32\x1e.piscan_pb.ClientToServer.Type\x12\x31\n\x0egeneralRequest\x18\x02 \x01(\x0b\x32\x19.piscan_pb.GeneralRequest\x12\x38\n\x10scanStateRequest\x18\x03 \x01(\x0b\x32\x1e.piscan_pb.ScannerStateRequest\x12-\n\x0c\x64\x65modRequest\x18\x04 \x01(\x0b\x32\x17.piscan_pb.DemodRequest\"I\n\x04Type\x12\x13\n\x0fGENERAL_REQUEST\x10\x00\x12\x19\n\x15SCANNER_STATE_REQUEST\x10\x01\x12\x11\n\rDEMOD_REQUEST\x10\x02\"\x98\x02\n\x0eServerToClient\x12,\n\x04type\x18\x01 \x01(\x0e\x32\x1e.piscan_pb.ServerToClient.Type\x12\x31\n\x0escannerContext\x18\x02 \x01(\x0b\x32\x19.piscan_pb.ScannerContext\x12-\n\x0c\x64\x65modContext\x18\x03 \x01(\x0b\x32\x17.piscan_pb.DemodContext\x12\x31\n\x0egeneralMessage\x18\x04 \x01(\x0b\x32\x19.piscan_pb.GeneralMessage\"C\n\x04Type\x12\x13\n\x0fSCANNER_CONTEXT\x10\x00\x12\x11\n\rDEMOD_CONTEXT\x10\x01\x12\x13\n\x0fGENERAL_MESSAGE\x10\x02\x62\x06proto3')
  ,
  dependencies=[request__pb2.DESCRIPTOR,context__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_CLIENTTOSERVER_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='piscan_pb.ClientToServer.Type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='GENERAL_REQUEST', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SCANNER_STATE_REQUEST', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEMOD_REQUEST', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=280,
  serialized_end=353,
)
_sym_db.RegisterEnumDescriptor(_CLIENTTOSERVER_TYPE)

_SERVERTOCLIENT_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='piscan_pb.ServerToClient.Type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SCANNER_CONTEXT', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEMOD_CONTEXT', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GENERAL_MESSAGE', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=569,
  serialized_end=636,
)
_sym_db.RegisterEnumDescriptor(_SERVERTOCLIENT_TYPE)


_CLIENTTOSERVER = _descriptor.Descriptor(
  name='ClientToServer',
  full_name='piscan_pb.ClientToServer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='piscan_pb.ClientToServer.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='generalRequest', full_name='piscan_pb.ClientToServer.generalRequest', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='scanStateRequest', full_name='piscan_pb.ClientToServer.scanStateRequest', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='demodRequest', full_name='piscan_pb.ClientToServer.demodRequest', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CLIENTTOSERVER_TYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=60,
  serialized_end=353,
)


_SERVERTOCLIENT = _descriptor.Descriptor(
  name='ServerToClient',
  full_name='piscan_pb.ServerToClient',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='piscan_pb.ServerToClient.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='scannerContext', full_name='piscan_pb.ServerToClient.scannerContext', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='demodContext', full_name='piscan_pb.ServerToClient.demodContext', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='generalMessage', full_name='piscan_pb.ServerToClient.generalMessage', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SERVERTOCLIENT_TYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=356,
  serialized_end=636,
)

_CLIENTTOSERVER.fields_by_name['type'].enum_type = _CLIENTTOSERVER_TYPE
_CLIENTTOSERVER.fields_by_name['generalRequest'].message_type = request__pb2._GENERALREQUEST
_CLIENTTOSERVER.fields_by_name['scanStateRequest'].message_type = request__pb2._SCANNERSTATEREQUEST
_CLIENTTOSERVER.fields_by_name['demodRequest'].message_type = request__pb2._DEMODREQUEST
_CLIENTTOSERVER_TYPE.containing_type = _CLIENTTOSERVER
_SERVERTOCLIENT.fields_by_name['type'].enum_type = _SERVERTOCLIENT_TYPE
_SERVERTOCLIENT.fields_by_name['scannerContext'].message_type = context__pb2._SCANNERCONTEXT
_SERVERTOCLIENT.fields_by_name['demodContext'].message_type = context__pb2._DEMODCONTEXT
_SERVERTOCLIENT.fields_by_name['generalMessage'].message_type = context__pb2._GENERALMESSAGE
_SERVERTOCLIENT_TYPE.containing_type = _SERVERTOCLIENT
DESCRIPTOR.message_types_by_name['ClientToServer'] = _CLIENTTOSERVER
DESCRIPTOR.message_types_by_name['ServerToClient'] = _SERVERTOCLIENT

ClientToServer = _reflection.GeneratedProtocolMessageType('ClientToServer', (_message.Message,), dict(
  DESCRIPTOR = _CLIENTTOSERVER,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:piscan_pb.ClientToServer)
  ))
_sym_db.RegisterMessage(ClientToServer)

ServerToClient = _reflection.GeneratedProtocolMessageType('ServerToClient', (_message.Message,), dict(
  DESCRIPTOR = _SERVERTOCLIENT,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:piscan_pb.ServerToClient)
  ))
_sym_db.RegisterMessage(ServerToClient)


# @@protoc_insertion_point(module_scope)
