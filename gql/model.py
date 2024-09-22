from dataclasses import dataclass


@dataclass(kw_only=True)
class CollectTimeline:
    action: int
    subject_name: str
    subject_name_cn: str
