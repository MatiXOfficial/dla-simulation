from enum import Enum


class RefreshType(Enum):
    ONLY_AT_THE_END = 1
    EVERY_PARTICLE = 2
    EVERY_TURN = 3


class InitType(Enum):
    MIDDLE = 1


class Config:
    def __init__(self):
        self.refresh = RefreshType.EVERY_TURN
        self.init_type = InitType.MIDDLE
        self.canvas_size = 10
        self.image_target_size = 50
