from enum import Enum


class RefreshType(Enum):
    EVERY_TURN = 'every step'
    EVERY_PARTICLE = 'every particle'
    PERIODICALLY = 'periodically'


class InitType(Enum):
    MIDDLE = "middle"


class Config:
    def __init__(self):
        self.refresh = RefreshType.EVERY_PARTICLE
        self.init_type = InitType.MIDDLE
        self.canvas_size = 10
        self.image_target_size = 50
