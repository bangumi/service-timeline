from typing import TypedDict


class CollectTimeline(TypedDict):
    id: int
    action: int
    user_id: int
    subject_id: list[int]
    created_at: int
