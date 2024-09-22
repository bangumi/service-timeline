from dataclasses import dataclass


@dataclass(kw_only=True)
class CollectTimeline:
    id: int
    action: int
    user_id: int
    subject_id: list[int]
    created_at: int
