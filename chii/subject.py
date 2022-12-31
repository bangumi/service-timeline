import enum


class SubjectType(enum.IntEnum):
    """条目类型
    - `1` 为 书籍
    - `2` 为 动画
    - `3` 为 音乐
    - `4` 为 游戏
    - `6` 为 三次元

    没有 `5`
    """

    book = 1
    anime = 2
    music = 3
    game = 4
    real = 6

    def str(self) -> str:
        if self == self.book:
            return "书籍"
        elif self == self.anime:
            return "动画"
        elif self == self.music:
            return "音乐"
        elif self == self.game:
            return "游戏"
        elif self == self.real:
            return "三次元"
        raise ValueError(f"unexpected SubjectType {self}")
