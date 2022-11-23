import tkinter as tk

from config import Config
from .information_frame import InformationFrame
from .simulation_frame import SimulationFrame
from .simulation_handler import SimulationHandler


class MainWindow:
    def __init__(self, config: Config):
        self.config = config

        self.simulation_handler = SimulationHandler(self)

        self.root = tk.Tk()
        self.root.title('DLA Simulation')
        self.root.protocol('WM_DELETE_WINDOW', exit)

        self.refresh_complex = True

        self.simulation_frame = SimulationFrame(self)
        self.information_frame = InformationFrame(self)

        self.root.update()

        self.start_loop()

    def reinit(self):
        self.simulation_handler.reinit()
        self.refresh()

    def start_loop(self):
        self.root.mainloop()

    def refresh(self, refresh_complex=None):
        if refresh_complex is None:
            refresh_complex = self.refresh_complex
        self.simulation_frame.refresh(refresh_complex)
        self.information_frame.refresh()
