import random
import time

import numpy as np
from matplotlib import pyplot as plt

from config import Config, InitType


class DLAImage:
    PERIOD = 10
    def __init__(self, config: Config):
        self.config = config

        self.grid: set = None
        self.grid_len: int = None
        self.particles: np.ndarray = None

    def init(self):
        self.grid = set()
        if self.config.init_type == InitType.MIDDLE:
            self.initialize_middle()
        else:
            raise ValueError(f'Wrong init type: {self.config.init_type}')

        self.grid_len = len(self.grid)
        self.particles = np.array([self._random_position()])

    def initialize_middle(self):
        self.grid.add((self.config.canvas_size // 2, self.config.canvas_size // 2))

    def simulate_step(self):
        growth = False
        for i, particle in enumerate(self.particles):
            move = self._random_move()

            new_position = particle + move

            if tuple(new_position) in self.grid:
                self.grid.add(tuple(particle))
                self.particles[i] = self._random_position()
                self.grid_len += 1
                growth = True
                continue

            if self._is_valid_pos(new_position):
                self.particles[i] = new_position

        if self.grid_len >= self.config.image_target_size:
            self.particles = np.array([])
        return growth

    def simulate_until_growth(self):
        while not self.simulate_step():  # break loop when growth
            pass

    def simulate_periodically(self):
        start = time.time()
        while self.grid_len < self.config.image_target_size and time.time() - start < self.PERIOD:
            self.simulate_until_growth()

        if self.grid_len >= self.config.image_target_size:
            self.particles = np.array([])

    def simulate(self):
        while self.grid_len < self.config.image_target_size:
            self.simulate_step()
        self.particles = np.array([])

    def generate_image(self, show_particles=False):
        image = np.zeros((self.config.canvas_size, self.config.canvas_size))
        if show_particles:
            for x, y in self.particles:
                image[x][y] = 2
        for x, y in self.grid:
            image[x][y] = 1
        return image

    def _random_position(self):
        while True:
            pos = np.random.randint(low=0, high=self.config.canvas_size, size=2)
            pos = (pos[0], pos[1])
            if pos not in self.grid:
                return pos

    @staticmethod
    def _random_move():
        return random.choice([(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)])

    def _is_valid_pos(self, pos):
        return 0 <= pos[0] < self.config.canvas_size and 0 <= pos[1] < self.config.canvas_size

    def print(self):
        margin = 0.12
        subplot_fraction = 1 - 2 * margin
        fig = plt.figure(figsize=(3, 3))
        fig.subplots_adjust(margin, margin, 1 - margin, 1 - margin, 0, 0)
        array = np.array(list(self.grid)).astype(np.float32)
        array += 0.5
        marker_size = (subplot_fraction * 3 * 72 / self.config.canvas_size) ** 2
        plt.scatter(array[:, 0], array[:, 1], marker="s", s=marker_size)
        array = np.array(list(self.particles)).astype(np.float32)
        array += 0.5
        plt.scatter(array[:, 0], array[:, 1], marker="s", s=marker_size)
        plt.xlim(0, self.config.canvas_size)
        plt.ylim(0, self.config.canvas_size)
        ax = plt.gca()
        ax.set_aspect('equal')
        ax.set_xticks(np.arange(0, self.config.canvas_size, 1))
        ax.set_yticks(np.arange(0, self.config.canvas_size, 1))
        plt.grid()
        plt.show()

    def get_n_grid(self):
        return self.grid_len

    def get_target_size(self):
        return self.config.image_target_size


if __name__ == '__main__':
    config = Config()
    config.canvas_size = 10
    config.image_target_size = 10

    image = DLAImage(config)
    image.init()

    image.simulate()

    print(len(image.grid))
    print(image.generate_image())

    image.print()
