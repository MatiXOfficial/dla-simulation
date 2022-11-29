import random
import time
import math

import numpy as np
from matplotlib import pyplot as plt

from config import Config, InitType


def length(p1,p2):
    vec=(abs(p1[0]-p2[0]),abs(p1[1]-p2[1]))
    return math.sqrt(vec[0]*vec[0]+vec[1]*vec[1])


class SphereAttractor:
    def __init__(self,pos,radius,force,negative=False):
        self.pos=pos
        self.radius=radius
        self.negative=negative
        self.force=force

    def check(self, pos):
        distance = length(self.pos, pos) - self.radius
        if distance<0.:
            return False
        return True

    def get_probability(self,pos):
        distance=length(self.pos,pos) - self.radius
        weight=[]
        for move in DLAImage.possible_moves:
            current_pos=pos+move
            current_distance=length(self.pos,current_pos) - self.radius
            default_probability = 1. / len(DLAImage.possible_moves)

            if current_distance<=1.0:
                weight.append((current_distance-distance)*(1./(abs(current_distance)+0.001)) * 100.0+default_probability)
                continue

            if self.negative==False:
                weight.append((distance-current_distance)*(1./current_distance) * self.force+default_probability)
            else:
                weight.append((current_distance-distance)*(1./current_distance) * self.force+default_probability)

        weight=np.array(weight)
        min=np.min(weight)
        weight+=abs(min)
        sum=np.sum(weight)
        # if sum != 0:
        weight/=sum
        # else:
        #     weight+=default_probability

        return weight

class AttractorField:

    def __init__(self):
        self.attractorList=[]

    def add_attractor(self, attractor):
        self.attractorList.append(attractor)

    def get_weights(self,pos):
        if len(self.attractorList)==0:
            return [1./len(DLAImage.possible_moves)]*len(DLAImage.possible_moves)
        weights=np.zeros(len(DLAImage.possible_moves))

        for attractor in self.attractorList:
            weights+=attractor.get_probability(pos)
        weights/=len(self.attractorList)

        return list(weights)

    def check(self,pos):
        for attractor in self.attractorList:
            if attractor.check(pos)==False:
                return False
        return True


class DLAImage:
    possible_moves = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    PERIOD = 10

    def __init__(self, config: Config):
        self.config = config

        self.grid = set()
        self.initialize_grid()

        self.grid_len = len(self.grid)
        self.attractorField = AttractorField()
        self.attractorField.add_attractor(SphereAttractor((5, 5), 5, 10, False))
        self.particles = np.array([self._random_position()])

    def initialize_grid(self):
        if self.config.init_type == InitType.MIDDLE:
            self.grid.add((self.config.canvas_size // 2, self.config.canvas_size // 2))
        else:
            raise ValueError(f'Wrong init type: {self.config.init_type}')

    def simulate_step(self):
        growth = []
        for i, particle in enumerate(self.particles):
            move = self._random_move(particle)

            new_position = particle + move

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

    def _random_position(self):
        while True:
            pos = np.random.randint(low=0, high=self.config.canvas_size, size=2)
            pos = (pos[0], pos[1])
            if pos not in self.grid and self.attractorField.check(pos):
                return pos


    def _random_move(self,pos):
        w=self.attractorField.get_weights(pos)
        return random.choices(DLAImage.possible_moves,weights=w)[0]

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
