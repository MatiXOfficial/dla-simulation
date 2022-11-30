import time
from multiprocessing import Process, Event, Queue

from config import Config, RefreshType
from dla_image import DLAImage


class DLAScheduler(Process):
    def __init__(self, config: Config, queue: Queue, running_event: Event):
        super().__init__(daemon=True)
        self.config = config
        self.running_event = running_event
        self.queue = queue

        self.dla_image = DLAImage(config)
        if self.config.refresh == RefreshType.EVERY_TURN:
            self._handle_turn = self._handle_turn_move
        else:
            self._handle_turn = self._handle_turn_growth

    def run(self) -> None:
        # Send init particles
        for particle in self.dla_image.grid:
            self.queue.put(particle)
        self.running_event.set()
        time.sleep(0.5)
        self.running_event.clear()

        # Run the simulation
        while True:
            self.running_event.wait()
            self._handle_turn()

    def _handle_turn_growth(self) -> None:
        growth = self.dla_image.simulate_until_growth()
        for particle in growth:
            self.queue.put(particle)

    def _handle_turn_move(self) -> None:
        growth = self.dla_image.simulate_step()
        self.queue.put([(p[0], p[1]) for p in self.dla_image.particles])  # Send travelling particles as a list
        for particle in growth:
            self.queue.put(particle)
