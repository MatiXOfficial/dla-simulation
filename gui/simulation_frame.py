import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from .utils import show_askyesno

if TYPE_CHECKING:
    from .main_window import MainWindow


class SimulationFrame:
    # EMPTY_COLOR = 'black'
    # GRID_COLOR = 'white'
    # PARTICLE_COLOR = 'gray'

    def __init__(self, main_window: 'MainWindow'):
        self.main_window = main_window
        self.root = main_window.root
        self.simulation_timer = main_window.simulation_timer
        self.dla_image = main_window.dla_image

        frame = ttk.Frame(self.root)

        # map
        self.fig = Figure(figsize=(5, 5))

        self.plot = self.fig.add_subplot(111)
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

        self.var_simulation_speed = tk.IntVar(value=0)
        scale_simulation_speed = ttk.Scale(options_frame, orient='horizontal', from_=-2, to=14,
                                           variable=self.var_simulation_speed, command=self._update_simulation_speed)
        scale_simulation_speed.pack(side='left')

        button_next_turn = ttk.Button(options_frame, text='Next turn', command=self._button_next_turn_command)
        button_next_turn.pack(side='left')

        button_reset = ttk.Button(options_frame, text='Reset', command=self._button_reset_command)
        button_reset.pack(side='left')

        self.button_refresh = tk.Button(options_frame, text='Refresh', command=self._button_refresh_command, bd=1,
                                        relief=tk.GROOVE, width=6, fg='white', bg='#007aff')
        self.button_refresh.pack(side='left')

        options_frame.pack(padx=2, pady=2)

        frame.pack(side='right', expand=True, fill='both')

    def refresh(self, refresh_complex=True):
        if refresh_complex:
            self.plot.clear()
            self._draw_plot()
            self.canvas.draw()

    def _draw_plot(self):
        self.plot.pcolor(self.dla_image.generate_image())
        self.fig.gca().set_aspect('equal')
        self.fig.gca().set_xticks([])
        self.fig.gca().set_yticks([])

        # margin = 0.12
        # subplot_fraction = 1 - 2 * margin
        # self.fig.subplots_adjust(margin, margin, 1 - margin, 1 - margin, 0, 0)
        # array = np.array(list(self.dla_image.grid)).astype(np.float32)
        # array += 0.5
        # marker_size = (subplot_fraction * self.fig.get_size_inches()[0] * 72 / self.dla_image.image_size) ** 2
        # self.plot.scatter(array[:, 0], array[:, 1], marker="s", s=marker_size)
        # array = np.array(list(self.dla_image.particles)).astype(np.float32)
        # array += 0.5
        # self.plot.scatter(array[:, 0], array[:, 1], marker="s", s=marker_size)
        # self.plot.set_xlim(0, self.dla_image.image_size)
        # self.plot.set_ylim(0, self.dla_image.image_size)
        # ax = self.fig.gca()
        # ax.set_aspect('equal')
        # ax.set_xticks(np.arange(0, self.dla_image.image_size, 1))
        # ax.set_yticks(np.arange(0, self.dla_image.image_size, 1))
        # self.plot.grid()

    def _button_start_command(self):
        self.simulation_timer.start_timer()

    def _button_stop_command(self):
        self.simulation_timer.stop_timer()

    def _update_simulation_speed(self, value):
        timeout = 2 ** -self.var_simulation_speed.get()
        self.simulation_timer.update_timeout(timeout)

    def _button_next_turn_command(self):
        self.simulation_timer.trigger_action()

    def _button_reset_command(self):
        was_running = self.simulation_timer.is_running()
        self.simulation_timer.stop_timer()
        if show_askyesno('Reset', 'Are you sure want to abandon the current simulation and reset the settings?'):
            self.simulation_timer.kill()
            self.main_window.reinit()
        else:
            if was_running:
                self.simulation_timer.start_timer()

    def _button_refresh_command(self):
        self.main_window.refresh_complex = not self.main_window.refresh_complex
        if self.main_window.refresh_complex:
            self.main_window.refresh()
        if self.main_window.refresh_complex:
            self.button_refresh.config(bg='#007aff')
        else:
            self.button_refresh.config(bg='#bcbcbc')
