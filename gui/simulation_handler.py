import shutil
import time
from multiprocessing import Queue, Event
from pathlib import Path
from queue import Empty
from threading import Thread
from typing import TYPE_CHECKING

import numpy as np
from matplotlib.figure import Figure

from config import RefreshType
from dla_scheduler import DLAScheduler

if TYPE_CHECKING:
    from gui import MainWindow


class FieldType:
    EMPTY = 0
    ATTACHED = 2
    PARTICLE = 1


class SimulationHandler:
    PERIOD = 10
    COLOR_MULT = 2
    TMP_GIF_DIR = './tmp_gif'
    GIF_SAVE_DIR = './gifs'
    GIF_DPI = 150

    def __init__(self, main_window: 'MainWindow'):
        self.main_window = main_window
        self.config = main_window.config

        self.image = np.full(shape=(self.config.canvas_size, self.config.canvas_size), fill_value=FieldType.EMPTY)
        self.grid_len = 0
        self.particles = []

        self.queue = Queue()
        self.running_event = Event()
        self.dla_scheduler = DLAScheduler(self.config, self.queue, self.running_event)
        self.dla_scheduler.start()
        self.simulation_initialized = False

        if self.config.coloring:
            self.current_color = self.config.image_target_size * self.COLOR_MULT

        if self.config.produce_gif:
            try:
                Path(self.TMP_GIF_DIR).mkdir(exist_ok=False)
            except FileExistsError:
                shutil.rmtree(self.TMP_GIF_DIR)
                Path(self.TMP_GIF_DIR).mkdir(exist_ok=False)

            Path(self.GIF_SAVE_DIR).mkdir(exist_ok=True)

        # Keep updating the image on a separate thread
        self.update_thread = Thread(target=self._update_image, daemon=True).start()

    def reinit(self):
        self.dla_scheduler.kill()

        self.image = np.full(shape=(self.config.canvas_size, self.config.canvas_size), fill_value=FieldType.EMPTY)
        self.grid_len = 0
        self.particles = []

        self.queue = Queue()
        self.running_event = Event()
        self.dla_scheduler = DLAScheduler(self.config, self.queue, self.running_event)
        self.simulation_initialized = False

        if self.config.coloring:
            self.current_color = self.config.image_target_size * self.COLOR_MULT

        if self.config.produce_gif:
            try:
                Path(self.TMP_GIF_DIR).mkdir(exist_ok=False)
            except FileExistsError:
                shutil.rmtree(self.TMP_GIF_DIR)
                Path(self.TMP_GIF_DIR).mkdir(exist_ok=False)

            Path(self.GIF_SAVE_DIR).mkdir(exist_ok=True)

        self.dla_scheduler.start()

    def start(self):
        self.running_event.set()

    def stop(self):
        self.running_event.clear()

    def next_turn(self):
        # Trigger the simulation only if the queue is empty and simulation is stopped
        if self.queue.empty() and not self.running_event.is_set():
            self.running_event.set()
            self.running_event.clear()
        self.main_window.refresh()

    def _attach_particle(self, x, y, freeze_color=False):
        if not self.config.coloring:
            self.image[x][y] = FieldType.ATTACHED
        else:
            self.image[x][y] = self.current_color
            if not freeze_color:
                self.current_color += 1
        self.grid_len += 1
        if self.config.produce_gif and not freeze_color:
            if self.grid_len % self.config.gif_frequency == 0:
                self._save_gif_image()

    def _reset_moving_particles(self, particles):
        for x, y in self.particles:
            if self.image[x][y] != FieldType.ATTACHED:
                self.image[x][y] = FieldType.EMPTY
        self.particles = particles
        if self.config.refresh == RefreshType.EVERY_TURN:
            for x, y in self.particles:
                self.image[x][y] = FieldType.PARTICLE

    def _handle_init_particles(self):
        particles = self.queue.get()
        for particle in particles:
            self._attach_particle(*particle, freeze_color=True)
        if self.config.coloring:
            self.current_color += self.grid_len

    def _handle_particles(self):
        try:
            particle = self.queue.get(timeout=1)
            # attach only if simulation is initialized
            if self.simulation_initialized:
                if type(particle) == tuple:  # particle attached to the grid
                    self._attach_particle(*particle)
                else:  # new positions of not-attached particles
                    self._reset_moving_particles(particle)
        except Empty:
            pass

    def _update_image(self):
        start = time.time()
        while True:
            if not self.simulation_initialized:  # Init particles
                self._handle_init_particles()
                self.main_window.refresh()
                self.simulation_initialized = True
            else:
                if self.grid_len < self.config.image_target_size:
                    self._handle_particles()
                    if not self.running_event.is_set():
                        self.main_window.refresh(refresh_complex=False)
                    elif self.config.refresh == RefreshType.PERIODICALLY and time.time() < start + \
                            SimulationHandler.PERIOD:
                        self.main_window.refresh(refresh_complex=False)
                    else:
                        self.main_window.refresh()
                        start = time.time()
                else:
                    time.sleep(1)

    def _empty_queue(self):
        while not self.queue.empty():
            self.queue.get()

    def _save_gif_image(self):
        fig = Figure(figsize=(5, 5))
        ax = fig.add_subplot()

        ax.imshow(self.image, origin='lower')
        fig.gca().set_xticks([])
        fig.gca().set_yticks([])

        fig.tight_layout()
        fig.savefig(f'{self.TMP_GIF_DIR}/{self.grid_len}.jpeg', dpi=self.GIF_DPI)
