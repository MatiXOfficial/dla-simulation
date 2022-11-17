from enum import Enum


class RefreshType(Enum):
    EVERY_PARTICLE = "every particle"
    EVERY_TURN = "every turn"


class InitType(Enum):
    MIDDLE = "middle"


class Config:
    def __init__(self):
        self.refresh = RefreshType.EVERY_TURN
        self.init_type = InitType.MIDDLE
        self.canvas_size = 10
        self.image_target_size = 50
