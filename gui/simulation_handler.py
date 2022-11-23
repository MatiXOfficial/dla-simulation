import time
from multiprocessing import Queue, Event
from queue import Empty
from threading import Thread
from typing import TYPE_CHECKING

import numpy as np

from dla_scheduler import DLAScheduler

if TYPE_CHECKING:
    from gui import MainWindow


class SimulationHandler:
    def __init__(self, main_window: 'MainWindow'):
        self.main_window = main_window
        self.config = main_window.config

        self.image = np.zeros((self.config.canvas_size, self.config.canvas_size))
        self.grid_len = 0

        self.queue = Queue()
        self.running_event = Event()
        self.dla_scheduler = DLAScheduler(self.config, self.queue, self.running_event)
        self.dla_scheduler.start()

        # Keep updating the image on a separate thread
        self.update_thread = Thread(target=self._update_image, daemon=True).start()

    def reinit(self):
        self.dla_scheduler.kill()

        self.image = np.zeros((self.config.canvas_size, self.config.canvas_size))
        self.grid_len = 0

        self.queue = Queue()
        self.running_event = Event()
        self.dla_scheduler = DLAScheduler(self.config, self.queue, self.running_event)

        self.dla_scheduler.start()

    def start(self):
        self.running_event.set()

    def stop(self):
        self.running_event.clear()

    def next_turn(self):
        if self.queue.empty():  # Trigger the simulation only if the queue is empty
            self.running_event.set()
            self.running_event.clear()

    def _add_particle(self, x, y):
        self.image[x][y] = 1
        self.grid_len += 1

    def _update_image(self):
        while True:
            if self.grid_len < self.config.image_target_size:
                try:
                    self._add_particle(*self.queue.get(timeout=1))
                except Empty:
                    pass
                self.main_window.refresh()
            else:
                time.sleep(1)

    def _empty_queue(self):
        while not self.queue.empty():
            self.queue.get()
