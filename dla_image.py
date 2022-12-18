import math
import random

import numpy as np
from matplotlib import pyplot as plt

from config import Config, InitType


def length(p1, p2):
    vec = (abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))
    return math.sqrt(vec[0] * vec[0] + vec[1] * vec[1])


class Attractor:
    def __init__(self, pos, force, negative=False):
        self.pos = pos
        self.negative = negative
        self.force = force

    def distance_function(self, pos1, pos2) -> float:
        pass

    def check(self, pos):
        distance = self.distance_function(self.pos, pos)
        if distance <= 1.:
            return False
        return True

    def get_probability(self, pos):
        distance = self.distance_function(self.pos, pos)
        weight = []
        for move in DLAImage.possible_moves:
            current_pos = pos + move
            current_distance = self.distance_function(self.pos, current_pos)
            default_probability = 1. / len(DLAImage.possible_moves)

            if current_distance <= 1.0:
                weight.append((current_distance - distance) * (
                        1. / (abs(current_distance) + 0.001)) * 100.0 + default_probability)
                continue

            if self.negative == False:
                weight.append(
                    max(distance - current_distance, 0.) * (1. / current_distance) * self.force + default_probability)
            else:
                weight.append(
                    max(current_distance - distance, 0.) * (1. / current_distance) * self.force + default_probability)

        weight = np.array(weight)
        min = np.min(weight)
        weight += abs(min)
        sum = np.sum(weight)
        # if sum != 0:
        weight /= sum
        # else:
        #     weight+=default_probability

        return weight


class SphereAttractor(Attractor):
    def __init__(self, pos, radius, force, negative=False):
        super().__init__(pos, force, negative)
        self.radius = radius

    def distance_function(self, pos1, pos2) -> float:
        return length(pos1, pos2) - self.radius


class RectangleAttractor(Attractor):
    def __init__(self, pos, a, b, force, negative=False):
        super().__init__(pos, force, negative)
        self.a = a
        self.b = b

    def distance_function(self, pos1, pos2) -> float:
        p = (pos2[0] - pos1[0], pos2[1] - pos1[1])
        d = (abs(p[0]) - self.a, abs(p[1]) - self.b)
        l = length((0., 0.), (max(d[0], 0.0), max(d[1], 0.0))) + min(max(d[0], 0.0), max(d[1], 0.0))
        return l


class AttractorField:

    def __init__(self):
        self.attractorList = []

    def add_attractor(self, attractor):
        self.attractorList.append(attractor)

    def get_weights(self, pos):
        if len(self.attractorList) == 0:
            return [1. / len(DLAImage.possible_moves)] * len(DLAImage.possible_moves)
        weights = np.zeros(len(DLAImage.possible_moves))

        for attractor in self.attractorList:
            weights += attractor.get_probability(pos)
        weights /= len(self.attractorList)

        return list(weights)

    def check(self, pos):
        for attractor in self.attractorList:
            if attractor.check(pos) == False:
                return False
        return True

    def build_from_config(self, config: Config):
        for att_cfg in config.attractors:
            position = att_cfg['position']
            position[0] *= config.canvas_size
            position[1] *= config.canvas_size

            negative = att_cfg['negative'] if 'negative' in att_cfg else True
            if negative in ['false', 'False', 'FALSE']:
                negative = False

            force = att_cfg['force']

            if att_cfg['type'] == 'sphere':
                radius = att_cfg['radius']
                self.add_attractor(SphereAttractor(position, radius, force, negative))
            elif att_cfg['type'] == 'rectangle':
                a = att_cfg['a']
                b = att_cfg['b']
                self.add_attractor(RectangleAttractor(position, a, b, force, negative))
            else:
                raise ValueError(f"{att_cfg['type']} is not a valid attractor type")


class DLAImage:
    possible_moves = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    PERIOD = 10

    def __init__(self, config: Config):
        self.config = config

        self.grid = set()
        self.initialize_grid()

        self.grid_len = len(self.grid)
        self.attractorField = AttractorField()
        self.attractorField.build_from_config(self.config)

        self.particles = np.array([self._random_position()])

    def initialize_grid(self):
        if self.config.init_type == InitType.MIDDLE:
            self.grid.add((self.config.canvas_size // 2, self.config.canvas_size // 2))
        elif self.config.init_type == InitType.BOTTOM:
            for i in range(0, self.config.canvas_size):
                self.grid.add((0, i))
        elif self.config.init_type == InitType.CIRCLE:
            self._init_circle()
        else:
            raise ValueError(f'Wrong init type: {self.config.init_type}')

    def simulate_step(self):
        growth = []
        for i, particle in enumerate(self.particles):
            move = self._random_move(particle)

            new_position = particle + move
            # print(new_position)

            if tuple(new_position) in self.grid:
                self.grid.add(tuple(particle))
                growth.append(tuple(particle))
                self.particles[i] = self._random_position()
                self.grid_len += 1
                continue

            if self._is_valid_pos(new_position):
                self.particles[i] = new_position
            # if self.attractorField.check(new_position)==False:
            #     self.particles[i] = self._random_position()

        return growth

    def simulate_until_growth(self):
        while True:
            if growth := self.simulate_step():
                return growth

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

    def _init_circle(self):
        n = self.config.canvas_size * 4
        r = self.config.canvas_size // 3

        mult = 2 * np.pi / n
        points = np.array([(np.cos(mult * i) * r, np.sin(mult * i) * r) for i in range(n + 1)])  # generate the circle
        points += self.config.canvas_size // 2  # move the circle to the middle of the canvas
        points = np.round(points).astype(int)

        for point in points:
            self.grid.add((point[0], point[1]))

    def _random_position(self):
        while True:
            pos = np.random.randint(low=0, high=self.config.canvas_size, size=2)
            pos = (pos[0], pos[1])
            if pos not in self.grid and self.attractorField.check(pos):
                return pos

    def _random_move(self, pos):
        w = self.attractorField.get_weights(pos)
        return random.choices(DLAImage.possible_moves, weights=w)[0]

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

    image.simulate()

    print(len(image.grid))
    print(image.generate_image())

    image.print()
