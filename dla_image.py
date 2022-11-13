import random

import numpy as np
from matplotlib import pyplot as plt

class DLAImage:

    def __init__(self, image_size, n_particles, init_method='middle'):
        self.image_size = image_size
        self.n_particles = n_particles
        self.init_method = init_method

        self.grid: set = None
        self.grid_len: int = None
        self.particles: np.ndarray = None

        self.init()

    def init(self):
        self.grid = set()
        self.grid_len = 0
        if self.init_method == 'middle':
            self.initialize_middle()
        else:
            raise ValueError(f'Init method {self.init_method} does not exist')

        self.particles = np.array([self._random_position()])

    def initialize_middle(self):
        self.grid.add((self.image_size // 2, self.image_size // 2))

    def simulation_step(self):
        for i, particle in enumerate(self.particles):
            move = self._random_move()

            new_position = particle + move

            if tuple(new_position) in self.grid:
                self.grid.add(tuple(particle))
                self.particles[i] = self._random_position()
                self.grid_len += 1
                continue

            if self._is_valid_pos(new_position):
                self.particles[i] = new_position

    def simulate(self):
        while self.grid_len < self.n_particles:
            self.simulation_step()

    def generate_image(self):
        image = np.zeros((self.image_size, self.image_size))
        for x, y in self.grid:
            image[x][y] = 2
        for x, y in self.particles:
            image[x][y] = 1
        return image

    def _random_position(self):
        while True:
            pos = np.random.randint(low=0, high=self.image_size, size=2)
            pos = (pos[0], pos[1])
            if pos not in self.grid:
                return pos

    @staticmethod
    def _random_move():
        return random.choice([(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)])

    def _is_valid_pos(self, pos):
        return 0 <= pos[0] < self.image_size and 0 <= pos[1] < self.image_size

    def print(self):
        margin = 0.12
        subplot_fraction = 1 - 2 * margin
        fig = plt.figure(figsize=(3, 3))
        fig.subplots_adjust(margin, margin, 1 - margin, 1 - margin, 0, 0)
        array=np.array(list(self.grid)).astype(np.float32)
        array+=0.5
        marker_size = (subplot_fraction*3 * 72 / self.image_size) ** 2
        plt.scatter(array[:,0],array[:,1],marker="s",s=marker_size)
        array = np.array(list(self.particles)).astype(np.float32)
        array+=0.5
        plt.scatter(array[:, 0], array[:, 1], marker="s", s=marker_size)
        plt.xlim(0, self.image_size)
        plt.ylim(0, self.image_size)
        ax = plt.gca()
        ax.set_aspect('equal')
        ax.set_xticks(np.arange(0, self.image_size, 1))
        ax.set_yticks(np.arange(0, self.image_size, 1))
        plt.grid()
        plt.show()

if __name__ == '__main__':
    image = DLAImage(10, 10)
    image.simulate()
    print(len(image.grid))
    print(image.generate_image())

    image.print()
