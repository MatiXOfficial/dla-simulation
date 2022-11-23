from multiprocessing import Process, Event, Queue

from config import Config
from dla_image import DLAImage


class DLAScheduler(Process):
    def __init__(self, config: Config, queue: Queue, running_event: Event):
        super().__init__(daemon=True)
        self.config = config
        self.running_event = running_event
        self.queue = queue

        self.dla_image = DLAImage(config)

    def run(self) -> None:
        for particle in self.dla_image.grid:  # Send init particles
            self.queue.put(particle)

        while True:
            self.running_event.wait()
            self._handle_turn()

    def _handle_turn(self) -> None:
        growth = self.dla_image.simulate_until_growth()
        for particle in growth:
            self.queue.put(particle)
