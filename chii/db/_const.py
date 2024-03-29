from typing import NamedTuple, Optional


class Staff(NamedTuple):
    cn: str
    jp: str
    en: str
    rdf: Optional[str] = None

    def str(self) -> str:
        return self.cn or self.jp or self.en or self.rdf or ""


staff_job_real = {
    4001: Staff(cn="原作", jp="", en="creator"),
    4002: Staff(cn="导演", jp="", en="director"),
    4013: Staff(cn="创意总监", jp="", en="creative director"),
    4003: Staff(cn="编剧", jp="", en="writer"),
    4004: Staff(cn="音乐", jp="", en="composer"),
    4005: Staff(cn="执行制片人", jp="製作総指揮", en="executive producer"),
    4006: Staff(cn="共同执行制作", jp="", en="co exec "),
    4007: Staff(cn="制片人/制作人", jp="プロデューサー", en="producer"),
    4008: Staff(cn="监制", jp="", en="supervising producer"),
    4009: Staff(cn="副制作人/制作顾问", jp="", en="consulting producer"),
    4010: Staff(cn="故事", jp="", en="story"),
    4011: Staff(cn="编审", jp="", en="story editor"),
    4012: Staff(cn="剪辑", jp="", en="editor"),
    4014: Staff(cn="摄影", jp="", en="cinematography"),
    4015: Staff(cn="主题歌演出", jp="", en="Theme Song Performance"),
    4016: Staff(cn="主演", jp="", en="Actor"),
    4017: Staff(cn="配角", jp="", en="Supporting Actor"),
    4018: Staff(cn="制作", jp="製作 製作スタジオ", en="Production"),
}

staff_job_music = {
    3001: Staff(cn="艺术家", jp="", en=""),
    3002: Staff(cn="制作人", jp="", en=""),
    3003: Staff(cn="作曲", jp="", en=""),
    3006: Staff(cn="作词", jp="", en="Lyric"),
    3008: Staff(cn="编曲", jp="", en="Arrange"),
    3009: Staff(cn="插图", jp="", en=""),
    3007: Staff(cn="录音", jp="", en=""),
    3004: Staff(cn="厂牌", jp="", en="Label"),
    3005: Staff(cn="原作", jp="", en="Original Creator/Original Work"),
    3010: Staff(cn="脚本", jp="シナリオ", en="Scenario"),
}

staff_job_book = {
    2007: Staff(cn="原作", jp="", en="Original Creator/Original Work"),
    2001: Staff(cn="作者", jp="", en=""),
    2002: Staff(cn="", jp="作画", en=""),
    2003: Staff(cn="插图", jp="イラスト", en=""),
    2004: Staff(cn="", jp="出版社", en=""),
    2005: Staff(cn="连载杂志", jp="掲載誌", en=""),
    2006: Staff(cn="译者", jp="", en=""),
    2008: Staff(cn="客串", jp="ゲスト", en="guest"),
    2009: Staff(cn="人物原案", jp="キャラクター原案", en="Original Character Design"),
}

staff_job_game = {
    1001: Staff(cn="开发", jp="開発元", en="developer"),
    1002: Staff(cn="发行", jp="発売元", en="publisher"),
    1003: Staff(cn="遊戲設計師", jp="ゲームクリエイター", en="game designer"),
    1015: Staff(cn="原作", jp="", en=""),
    1016: Staff(cn="导演", jp="監督 演出 シリーズ監督", en="Director/Direction"),
    1032: Staff(cn="制作人", jp="プロデューサー", en="Producer"),
    1028: Staff(cn="企画", jp="", en=""),
    1026: Staff(cn="监修", jp="監修", en=""),
    1004: Staff(cn="剧本", jp="腳本", en=""),
    1027: Staff(cn="系列构成", jp="シリーズ構成", en=""),
    1031: Staff(cn="作画监督", jp="作画監督", en=""),
    1013: Staff(cn="原画", jp="", en=""),
    1008: Staff(
        cn="人物设定", jp="キャラ設定 キャラクターデザイン", en="Character Design"
    ),
    1029: Staff(cn="机械设定", jp="メカニック設定", en="Mechanical Design"),
    1005: Staff(cn="美工", jp="美術", en=""),
    1023: Staff(cn="CG监修", jp="CG監修", en=""),
    1024: Staff(cn="SD原画", jp="", en=""),
    1025: Staff(cn="背景", jp="", en=""),
    1030: Staff(cn="音响监督", jp="", en="Sound Director"),
    1006: Staff(cn="音乐", jp="音楽", en=""),
    1021: Staff(cn="程序", jp="プログラム", en="Program"),
    1014: Staff(
        cn="动画制作",
        jp="アニメーション制作 アニメ制作 アニメーション",
        en="Animation Work",
    ),
    1017: Staff(cn="动画监督", jp="アニメーション監督", en=""),
    1020: Staff(cn="动画剧本", jp="アニメーション脚本", en=""),
    1018: Staff(cn="制作总指挥", jp="", en=""),
    1019: Staff(cn="QC", jp="", en="QC"),
    1007: Staff(cn="关卡设计", jp="", en=""),
    1009: Staff(cn="主题歌作曲", jp="", en="Theme Song Composition"),
    1010: Staff(cn="主题歌作词", jp="", en="Theme Song Lyrics"),
    1011: Staff(cn="主题歌演出", jp="", en="Theme Song Performance"),
    1012: Staff(cn="插入歌演出", jp="", en="Inserted Song Performance"),
    1022: Staff(cn="协力", jp="協力", en=""),
}

staff_job_anime = {
    1: Staff(cn="原作", jp="", en="Original Creator/Original Work"),
    74: Staff(cn="总导演", jp="総監督", en="Chief Director"),
    2: Staff(
        cn="导演", jp="監督 シリーズ監督", en="Director/Direction", rdf="directedBy"
    ),
    3: Staff(cn="脚本", jp="シナリオ", en="Script/Screenplay"),
    4: Staff(
        cn="分镜", jp="コンテ  ストーリーボード  画コンテ  絵コンテ", en="Storyboard"
    ),
    5: Staff(cn="演出", jp="", en="Episode Director"),
    6: Staff(cn="音乐", jp="楽曲  音楽", en="Music"),
    7: Staff(cn="人物原案", jp="キャラ原案", en="Original Character Design"),
    8: Staff(cn="人物设定", jp="キャラ設定", en="Character Design"),
    9: Staff(cn="分镜构图", jp="レイアウト", en="Layout"),
    10: Staff(
        cn="系列构成",
        jp="シナリオディレクター  構成  シリーズ構成  脚本構成",
        en="Series Composition",
    ),
    72: Staff(cn="副导演", jp="助監督", en="Assistant director"),
    11: Staff(cn="美术监督", jp="アートディレクション 背景監督", en="Art Direction"),
    71: Staff(cn="美术设计", jp="美術設定", en="Art Design"),
    13: Staff(cn="色彩设计", jp="色彩設定", en="Color Design"),
    14: Staff(cn="总作画监督", jp="チーフ作画監督", en="Chief Animation Director"),
    15: Staff(cn="作画监督", jp="作監 アニメーション演出", en="Animation Direction"),
    70: Staff(
        cn="机械作画监督", jp="メカニック作監", en="Mechanical Animation Direction"
    ),
    77: Staff(
        cn="动作作画监督", jp="アクション作画監督", en="Action Animation Direction"
    ),
    16: Staff(cn="机械设定", jp="メカニック設定", en="Mechanical Design"),
    17: Staff(cn="摄影监督", jp="撮影監督", en="Director of Photography"),
    69: Staff(cn="CG 导演", jp="CG 監督", en="CG Director"),
    18: Staff(
        cn="监修", jp="シリーズ監修 スーパーバイザー", en="Supervision/Supervisor"
    ),
    19: Staff(cn="道具设计", jp="プロップデザイン", en="Prop Design"),
    20: Staff(cn="原画", jp="作画 原画", en="Key Animation"),
    21: Staff(cn="第二原画", jp="原画協力", en="2nd Key Animation"),
    22: Staff(cn="动画检查", jp="動画チェック", en="Animation Check"),
    63: Staff(cn="制作", jp="製作 製作スタジオ", en="Production"),
    67: Staff(
        cn="动画制作",
        jp="アニメーション制作 アニメ制作 アニメーション",
        en="Animation Work",
    ),
    73: Staff(cn="OP・ED 分镜", jp="OP・ED 分鏡", en="OP ED"),
    65: Staff(cn="音乐制作", jp="楽曲制作 音楽制作", en="Music Work"),
    23: Staff(cn="助理制片人", jp="協力プロデューサー", en="Assistant Producer"),
    24: Staff(cn="", jp="アソシエイトプロデューサー", en="Associate Producer"),
    25: Staff(cn="背景美术", jp="背景", en="Background Art"),
    26: Staff(cn="色彩指定", jp="", en="Color Setting"),
    27: Staff(cn="数码绘图", jp="", en="Digital Paint"),
    75: Staff(cn="3DCG", jp="", en="3DCG"),
    37: Staff(
        cn="制作管理", jp="制作マネージャー 制作担当 制作班長", en="Production Manager"
    ),
    28: Staff(cn="剪辑", jp="編集", en="Editing"),
    29: Staff(cn="原案", jp="", en="Original Plan"),
    30: Staff(cn="主题歌编曲", jp="", en="Theme Song Arrangement"),
    31: Staff(cn="主题歌作曲", jp="", en="Theme Song Composition"),
    32: Staff(cn="主题歌作词", jp="", en="Theme Song Lyrics"),
    33: Staff(cn="主题歌演出", jp="", en="Theme Song Performance"),
    34: Staff(cn="插入歌演出", jp="", en="Inserted Song Performance"),
    35: Staff(cn="企画", jp="プランニング  企画開発", en="Planning"),
    36: Staff(
        cn="", jp="企画プロデューサー  企画営業プロデューサー", en="Planning Producer"
    ),
    38: Staff(
        cn="宣传", jp="パブリシティ  宣伝  広告宣伝  番組宣伝  製作宣伝", en="Publicity"
    ),
    39: Staff(cn="录音", jp="録音", en="Recording"),
    40: Staff(cn="录音助理", jp="録音アシスタント  録音助手", en="Recording Assistant"),
    41: Staff(cn="系列监督", jp="", en="Series Production Director"),
    42: Staff(cn="製作", jp="", en="Production"),
    43: Staff(cn="设定", jp="設定", en="Setting"),
    44: Staff(cn="音响监督", jp="", en="Sound Director"),
    45: Staff(cn="音响", jp="音響", en="Sound"),
    46: Staff(cn="音效", jp="音響効果", en="Sound Effects"),
    47: Staff(cn="特效", jp="視覚効果", en="Special Effects"),
    48: Staff(cn="配音监督", jp="", en="ADR Director"),
    49: Staff(cn="联合导演", jp="", en="Co-Director"),
    50: Staff(cn="背景设定", jp="基本設定  場面設定  場面設計  設定", en="Setting"),
    51: Staff(cn="补间动画", jp="動画", en="In-Between Animation"),
    52: Staff(cn="执行制片人", jp="製作総指揮", en="Executive Producer"),
    53: Staff(cn="助理制片人", jp="協力プロデューサー", en="Assistant Producer"),
    54: Staff(cn="制片人", jp="プロデュース  プロデューサー", en="Producer"),
    55: Staff(cn="助理录音师", jp="", en="Assistant Engineer"),
    56: Staff(cn="助理制片协调", jp="", en="Assistant Production Coordinat"),
    57: Staff(
        cn="演员监督", jp="キャスティングコーディネーター監督", en="Casting Director"
    ),
    58: Staff(
        cn="总制片",
        jp="チーフプロデューサー  チーフ制作  総合プロデューサー",
        en="Chief Producer",
    ),
    59: Staff(cn="联合制片人", jp="", en="Co-Producer"),
    60: Staff(cn="台词编辑", jp="台詞編集", en="Dialogue Editing"),
    61: Staff(
        cn="后期制片协调", jp="ポストプロダクション協力", en="Post-Production Assistant"
    ),
    62: Staff(
        cn="制作助手", jp="制作アシスタント 制作補佐 製作補", en="Production Assistant"
    ),
    64: Staff(cn="制作协调", jp="制作コーディネーター", en="Production Coordination"),
    76: Staff(cn="制作协力", jp="制作協力 / 作品協力", en="Work Assistance"),
    66: Staff(cn="友情協力", jp="特别鸣谢", en="Special Thanks"),
}
