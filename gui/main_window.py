import tkinter as tk

from config import Config
from dla_image import DLAImage
from .information_frame import InformationFrame
from .simulation_frame import SimulationFrame
from .utils import SimulationTimer


class MainWindow:
    def __init__(self, dla_image: DLAImage, config: Config):
        self.dla_image = dla_image
        self.dla_image.init()

        self.config = config

        self.root = tk.Tk()
        self.root.title('DLA Simulation')
        self.root.protocol('WM_DELETE_WINDOW', exit)

        self.refresh_complex = True
        self.simulation_timer = SimulationTimer(self.next_turn)
        self.simulation_timer.start()

        self.simulation_frame = SimulationFrame(self)
        self.information_frame = InformationFrame(self)

        self.root.update()

        self.start_loop()

    def reinit(self):
        self.dla_image.init()
        self.simulation_timer = SimulationTimer(self.next_turn)
        self.refresh()

    def start_loop(self):
        self.root.mainloop()

    def refresh(self, refresh_complex=None):
        if refresh_complex is None:
            refresh_complex = self.refresh_complex
        self.simulation_frame.refresh(refresh_complex)
        self.information_frame.refresh()

    def next_turn(self):
        self.dla_image.simulation_step()
        self.refresh()
