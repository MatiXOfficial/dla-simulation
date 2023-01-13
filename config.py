import json
from enum import Enum


class RefreshType(Enum):
    EVERY_TURN = 'every step'
    EVERY_PARTICLE = 'every particle'
    PERIODICALLY = 'periodically'


class InitType(Enum):
    MIDDLE = "middle"
    BOTTOM = "bottom"
    CIRCLE = "circle"
    EDGES = "edges"


class Config:
    def __init__(self):
        self.refresh = RefreshType.EVERY_PARTICLE
        self.init_type = InitType.BOTTOM
        self.canvas_size = 100
        self.image_target_size = 2000
        self.enable_attractors = False
        self.coloring = True
        self.produce_gif = False
        self.gif_frequency = 10
        self.gif_fps = 30

        self.attractors: list[dict[str, str]] = []
        self.reload_attractors()

    def reload_attractors(self):
        if self.enable_attractors:
            with open('attractors_cfg.json') as file:
                self.attractors = json.load(file)['attractors']
        else:
            self.attractors = []
