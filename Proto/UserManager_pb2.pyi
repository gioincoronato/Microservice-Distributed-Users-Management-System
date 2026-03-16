from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AddUserRequest(_message.Message):
    __slots__ = ("email", "name")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    email: str
    name: str
    def __init__(self, email: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("id", "email", "name", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    email: str
    name: str
    created_at: str
    def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ..., name: _Optional[str] = ..., created_at: _Optional[str] = ...) -> None: ...

class GetUserRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteUserRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteAck(_message.Message):
    __slots__ = ("delete_ack",)
    DELETE_ACK_FIELD_NUMBER: _ClassVar[int]
    delete_ack: str
    def __init__(self, delete_ack: _Optional[str] = ...) -> None: ...

class EmptyRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
