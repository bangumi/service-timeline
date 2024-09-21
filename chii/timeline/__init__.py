from typing import Dict, Optional

from pydantic import BaseModel

from chii.const import CollectionType, IntEnum, SubjectType


class SubjectMemo(BaseModel):
    collect_comment: str
    collect_rate: int
    subject_id: str
    collect_id: int = 0


class SubjectImage(BaseModel):
    subject_id: str
    images: str


class ProgressMemo(BaseModel):
    vols_update: Optional[int] = None
    vols_total: Optional[str] = None

    eps_update: Optional[int] = None
    eps_total: Optional[str] = None

    subject_id: Optional[str] = None
    subject_type_id: Optional[str] = None
    subject_name: Optional[str] = None

    ep_name: Optional[str] = None
    ep_sort: Optional[float] = None
    ep_id: Optional[int] = None


class Image(BaseModel):
    id: Optional[int] = None
    subject_id: Optional[int] = None

    name: Optional[str] = None
    title: Optional[str] = None

    images: str


class TimelineCat(IntEnum):
    Unknown = 0
    Relation = 1  # add friends, join group
    Wiki = 2
    Subject = 3
    Progress = 4
    # Type = 2 时为 [SayEditMemo] 其他类型则是 string
    Say = 5
    Blog = 6
    Index = 7
    Mono = 8
    Doujin = 9


SUBJECT_TYPE_MAP: Dict[int, Dict[int, int]] = {
    SubjectType.book: {
        CollectionType.wish: 1,
        CollectionType.done: 5,
        CollectionType.doing: 9,
        CollectionType.on_hold: 13,
        CollectionType.dropped: 14,
    },
    SubjectType.anime: {
        CollectionType.wish: 2,
        CollectionType.done: 6,
        CollectionType.doing: 10,
        CollectionType.on_hold: 13,
        CollectionType.dropped: 14,
    },
    SubjectType.music: {
        CollectionType.wish: 3,
        CollectionType.done: 7,
        CollectionType.doing: 11,
        CollectionType.on_hold: 13,
        CollectionType.dropped: 14,
    },
    SubjectType.game: {
        CollectionType.wish: 4,
        CollectionType.done: 8,
        CollectionType.doing: 12,
        CollectionType.on_hold: 13,
        CollectionType.dropped: 14,
    },
    SubjectType.real: {
        CollectionType.wish: 2,
        CollectionType.done: 6,
        CollectionType.doing: 10,
        CollectionType.on_hold: 13,
        CollectionType.dropped: 14,
    },
}
