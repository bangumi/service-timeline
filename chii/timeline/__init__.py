from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from chii.compat import phpseralize
from chii.subject import SubjectType
from chii.db.const import IntEnum
from chii.db.tables import ChiiTimeline


class SubjectMemo(BaseModel):
    collect_comment: str
    collect_rate: int
    subject_id: str
    subject_name: str
    subject_name_cn: str
    subject_series: bool = False
    subject_type_id: str


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


subjectTypeMap: Dict[int, List[int]] = {
    SubjectType.book: [0, 1, 5, 9, 13, 14],
    SubjectType.anime: [0, 2, 6, 10, 13, 14],
    SubjectType.music: [0, 3, 7, 11, 13, 14],
    SubjectType.game: [0, 4, 8, 12, 13, 14],
    SubjectType.real: [0, 2, 6, 10, 13, 14],
}


def parseMemo(cat: int, type: int, batch: bool, memo: str):
    if cat == TimelineCat.Relation:
        if type in [2, 3, 4]:
            return phpseralize.loads(memo)

    if cat == TimelineCat.Say:
        if type == 2:
            return phpseralize.loads(memo)
        return phpseralize.loads(memo)


def parseTimeLine(tl: ChiiTimeline) -> Timeline:
    memo = parseMemo(tl.cat, tl.type, bool(tl.batch), tl.memo)

    if not memo:
        raise Exception(
            f"unexpected timeline<id=${tl.id}> cat ${tl.cat} type ${tl.type} ${tl.memo}"
        )

    if tl.cat == TimelineCat.Relation:
        if type in [2, 3, 4]:
            return Timeline(id=tl.id, cat=tl.cat, type=tl.type, memo=memo)

    raise ValueError("unknown timeline")
