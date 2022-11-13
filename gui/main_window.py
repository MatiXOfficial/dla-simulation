import tkinter as tk

from dla_image import DLAImage
from gui.simulation_frame import SimulationFrame
from gui.utils import SimulationTimer


class MainWindow:
    def __init__(self, dla_image: DLAImage):
        self.dla_image = dla_image

        self.refresh_complex = True

        self.root = None

        self.simulation_timer = None

        self.simulation_frame = None

        self.init()

    def init(self):
        self.dla_image.init()

        self.root = tk.Tk()
        self.root.title('DLA Simulation')
        self.root.protocol('WM_DELETE_WINDOW', exit)

        self.simulation_timer = SimulationTimer(self._next_turn_update)
        self.simulation_timer.start()

        self.simulation_frame = SimulationFrame(self)

        self.root.update()

        self.start_loop()

    def reinit(self):
        self.root.quit()
        self.root.destroy()
        self.init()

    def start_loop(self):
        self.root.mainloop()

    def refresh(self):
        self.simulation_frame.refresh()

    def _next_turn_update(self):
        self.dla_image.simulation_step()
        self.simulation_frame.next_turn_update(self.refresh_complex)
