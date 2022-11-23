import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

if TYPE_CHECKING:
    from .main_window import MainWindow


class SimulationFrame:
    # EMPTY_COLOR = 'black'
    # GRID_COLOR = 'white'
    # PARTICLE_COLOR = 'gray'

    def __init__(self, main_window: 'MainWindow'):
        self.main_window = main_window
        self.config = main_window.config
        self.simulation_handler = main_window.simulation_handler
        self.root = main_window.root

        frame = ttk.Frame(self.root)

        # map
        self.fig = Figure(figsize=(5, 5))

        self.ax = self.fig.add_subplot()
        self._draw_plot()
        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.draw()

        self.canvas.get_tk_widget().pack(expand=True, fill='both')

        # options frame
        options_frame = ttk.Frame(frame, relief='ridge', borderwidth=2)

        button_start = ttk.Button(options_frame, text='Start', command=self._button_start_command)
        button_start.pack(side='left')

        button_stop = ttk.Button(options_frame, text='Stop', command=self._button_stop_command)
        button_stop.pack(side='left')

        button_next_turn = ttk.Button(options_frame, text='Next turn', command=self._button_next_turn_command)
        button_next_turn.pack(side='left')

        self.button_refresh = tk.Button(options_frame, text='Refresh', command=self._button_refresh_command, bd=1,
                                        relief=tk.GROOVE, width=6, fg='white', bg='#007aff')
        self.button_refresh.pack(side='left')

        options_frame.pack(padx=2, pady=2)

        frame.pack(side='right', expand=True, fill='both')

    def refresh(self, refresh_complex=True):
        if refresh_complex:
            self.ax.clear()
            self._draw_plot()
            self.canvas.draw()

    def _draw_plot(self):
        self.ax.imshow(self.simulation_handler.image, origin='lower')
        self.fig.gca().set_xticks([])
        self.fig.gca().set_yticks([])

    # margin = 0.12
    # subplot_fraction = 1 - 2 * margin
    # self.fig.subplots_adjust(margin, margin, 1 - margin, 1 - margin, 0, 0)
    # array = np.array(list(self.dla_image.grid)).astype(np.float32)
    # array += 0.5
    # marker_size = (subplot_fraction * self.fig.get_size_inches()[0] * 72 / self.dla_image.image_size) ** 2
    # self.ax.scatter(array[:, 0], array[:, 1], marker="s", s=marker_size)
    # array = np.array(list(self.dla_image.particles)).astype(np.float32)
    # array += 0.5
    # self.ax.scatter(array[:, 0], array[:, 1], marker="s", s=marker_size)
    # self.ax.set_xlim(0, self.dla_image.image_size)
    # self.ax.set_ylim(0, self.dla_image.image_size)
    # ax = self.fig.gca()
    # ax.set_aspect('equal')
    # ax.set_xticks(np.arange(0, self.dla_image.image_size, 1))
    # ax.set_yticks(np.arange(0, self.dla_image.image_size, 1))
    # self.ax.grid()

    def _update_plot(self):
        self.im.set_data(self.simulation_handler.image)

    def _button_start_command(self):
        self.simulation_handler.start()

    def _button_stop_command(self):
        self.simulation_handler.stop()

    def _button_next_turn_command(self):
        self.simulation_handler.next_turn()

    def _button_refresh_command(self):
        self.main_window.refresh_complex = not self.main_window.refresh_complex
        if self.main_window.refresh_complex:
            self.main_window.refresh()
        if self.main_window.refresh_complex:
            self.button_refresh.config(bg='#007aff')
        else:
            self.button_refresh.config(bg='#bcbcbc')
