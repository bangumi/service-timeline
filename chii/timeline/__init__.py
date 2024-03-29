from typing import Any, Dict, Optional

from pydantic import BaseModel

from chii.compat import phpseralize
from chii.db.const import IntEnum
from chii.db.tables import ChiiTimeline
from chii.subject import SubjectType


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


class Timeline(BaseModel):
    type: int
    cat: int
    id: int
    memo: Any


SUBJECT_TYPE_MAP: Dict[int, Dict[int, int]] = {
    SubjectType.book: {1: 1, 2: 5, 3: 9, 4: 13, 5: 14},
    SubjectType.anime: {1: 2, 2: 6, 3: 10, 4: 13, 5: 14},
    SubjectType.music: {1: 3, 2: 7, 3: 11, 4: 13, 5: 14},
    SubjectType.game: {1: 4, 2: 8, 3: 12, 4: 13, 5: 14},
    SubjectType.real: {1: 2, 2: 6, 3: 10, 4: 13, 5: 14},
}


def parseMemo(cat: int, type: int, batch: bool, memo: str):
    if cat == TimelineCat.Relation and type in [2, 3, 4]:
        return phpseralize.loads(memo)

    if cat == TimelineCat.Say:
        if type == 2:
            return phpseralize.loads(memo)
        return phpseralize.loads(memo)
    return None


def parseTimeLine(tl: ChiiTimeline) -> Timeline:
    memo = parseMemo(tl.cat, tl.type, bool(tl.batch), tl.memo)

    if not memo:
        raise ValueError(
            f"unexpected timeline<id=${tl.id}> cat ${tl.cat} type ${tl.type} ${tl.memo}"
        )

    if tl.cat == TimelineCat.Relation and type in [2, 3, 4]:
        return Timeline(id=tl.id, cat=tl.cat, type=tl.type, memo=memo)

    raise ValueError("unknown timeline")
