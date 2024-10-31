from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RequestHeader(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class RegisterRequest(_message.Message):
    __slots__ = ("header", "first_connect")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FIRST_CONNECT_FIELD_NUMBER: _ClassVar[int]
    header: RequestHeader
    first_connect: bool
    def __init__(self, header: _Optional[_Union[RequestHeader, _Mapping]] = ..., first_connect: bool = ...) -> None: ...

class RegisterReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Model(_message.Message):
    __slots__ = ("client_health", "opponent_health", "winner", "playing")
    CLIENT_HEALTH_FIELD_NUMBER: _ClassVar[int]
    OPPONENT_HEALTH_FIELD_NUMBER: _ClassVar[int]
    WINNER_FIELD_NUMBER: _ClassVar[int]
    PLAYING_FIELD_NUMBER: _ClassVar[int]
    client_health: int
    opponent_health: int
    winner: bool
    playing: bool
    def __init__(self, client_health: _Optional[int] = ..., opponent_health: _Optional[int] = ..., winner: bool = ..., playing: bool = ...) -> None: ...

class GetModelRequest(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: RequestHeader
    def __init__(self, header: _Optional[_Union[RequestHeader, _Mapping]] = ...) -> None: ...

class GetModelReply(_message.Message):
    __slots__ = ("model",)
    MODEL_FIELD_NUMBER: _ClassVar[int]
    model: Model
    def __init__(self, model: _Optional[_Union[Model, _Mapping]] = ...) -> None: ...

class Move(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CommandRequest(_message.Message):
    __slots__ = ("header", "move")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MOVE_FIELD_NUMBER: _ClassVar[int]
    header: RequestHeader
    move: Move
    def __init__(self, header: _Optional[_Union[RequestHeader, _Mapping]] = ..., move: _Optional[_Union[Move, _Mapping]] = ...) -> None: ...

class CommandReply(_message.Message):
    __slots__ = ("diff",)
    DIFF_FIELD_NUMBER: _ClassVar[int]
    diff: Model
    def __init__(self, diff: _Optional[_Union[Model, _Mapping]] = ...) -> None: ...

class WaitRequest(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: RequestHeader
    def __init__(self, header: _Optional[_Union[RequestHeader, _Mapping]] = ...) -> None: ...

class WaitReply(_message.Message):
    __slots__ = ("diff",)
    DIFF_FIELD_NUMBER: _ClassVar[int]
    diff: Model
    def __init__(self, diff: _Optional[_Union[Model, _Mapping]] = ...) -> None: ...
