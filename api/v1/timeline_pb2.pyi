from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Episode(_message.Message):
    __slots__ = ["id", "name", "name_cn", "sort", "type"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_CN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    name_cn: str
    sort: float
    type: int
    def __init__(self, id: _Optional[int] = ..., type: _Optional[int] = ..., name: _Optional[str] = ..., name_cn: _Optional[str] = ..., sort: _Optional[float] = ...) -> None: ...

class EpisodeCollectRequest(_message.Message):
    __slots__ = ["last", "subject", "user_id"]
    LAST_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    last: Episode
    subject: Subject
    user_id: int
    def __init__(self, user_id: _Optional[int] = ..., last: _Optional[_Union[Episode, _Mapping]] = ..., subject: _Optional[_Union[Subject, _Mapping]] = ...) -> None: ...

class EpisodeCollectResponse(_message.Message):
    __slots__ = ["ok"]
    OK_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    def __init__(self, ok: bool = ...) -> None: ...

class HelloRequest(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class HelloResponse(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class Subject(_message.Message):
    __slots__ = ["eps_total", "id", "image", "name", "name_cn", "series", "type", "vols_total"]
    EPS_TOTAL_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    NAME_CN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VOLS_TOTAL_FIELD_NUMBER: _ClassVar[int]
    eps_total: int
    id: int
    image: str
    name: str
    name_cn: str
    series: bool
    type: int
    vols_total: int
    def __init__(self, id: _Optional[int] = ..., type: _Optional[int] = ..., name: _Optional[str] = ..., name_cn: _Optional[str] = ..., image: _Optional[str] = ..., series: bool = ..., vols_total: _Optional[int] = ..., eps_total: _Optional[int] = ...) -> None: ...

class SubjectCollectRequest(_message.Message):
    __slots__ = ["collection", "comment", "rate", "subject", "user_id"]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    RATE_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    collection: int
    comment: str
    rate: int
    subject: Subject
    user_id: int
    def __init__(self, user_id: _Optional[int] = ..., subject: _Optional[_Union[Subject, _Mapping]] = ..., collection: _Optional[int] = ..., comment: _Optional[str] = ..., rate: _Optional[int] = ...) -> None: ...

class SubjectCollectResponse(_message.Message):
    __slots__ = ["ok"]
    OK_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    def __init__(self, ok: bool = ...) -> None: ...

class SubjectProgressRequest(_message.Message):
    __slots__ = ["eps_update", "subject", "user_id", "vols_update"]
    EPS_UPDATE_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    VOLS_UPDATE_FIELD_NUMBER: _ClassVar[int]
    eps_update: int
    subject: Subject
    user_id: int
    vols_update: int
    def __init__(self, user_id: _Optional[int] = ..., subject: _Optional[_Union[Subject, _Mapping]] = ..., eps_update: _Optional[int] = ..., vols_update: _Optional[int] = ...) -> None: ...

class SubjectProgressResponse(_message.Message):
    __slots__ = ["ok"]
    OK_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    def __init__(self, ok: bool = ...) -> None: ...
