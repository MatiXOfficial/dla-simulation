import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from .utils import show_askyesno

if TYPE_CHECKING:
    from .main_window import MainWindow


class ConfigFrame:
    def __init__(self, main_window: 'MainWindow', parent: ttk.Frame):
        self.main_window = main_window
        self.config = main_window.config
        self.simulation_timer = main_window.simulation_timer

        frame = ttk.Frame(parent, relief='groove', borderwidth=3)

        ##### settings frame #####
        self.settings_frame = ttk.Frame(frame)
        self.settings_row = 0

        # Refresh
        self._add_settings_row('Refresh:')

        # Init mode
        self._add_settings_row('Init mode:')

        # Canvas size
        self.canvas_var = tk.IntVar(value=self.config.canvas_size)
        canvas_spinbox = ttk.Spinbox(self.settings_frame, from_=0, to=999999999, textvariable=self.canvas_var, width=5,
                                     increment=1)
        self._add_settings_row('Canvas size:', canvas_spinbox)

        # Image size
        self.image_size_var = tk.IntVar(value=self.config.image_target_size)
        image_size_spinbox = ttk.Spinbox(self.settings_frame, from_=0, to=999999999, textvariable=self.image_size_var,
                                         width=5, increment=1)
        self._add_settings_row('Image target size:', image_size_spinbox)

        self.settings_frame.pack(side='top')

        ##### control frame #####
        control_frame = ttk.Frame(frame, relief='ridge', borderwidth=2)

        # Reset button
        button_reset = ttk.Button(control_frame, text='Reset settings', command=self._button_reset_command)
        button_reset.pack(side='left', padx=2, pady=2)

        # Reinit button
        button_reinit = ttk.Button(control_frame, text='Reinit simulation', command=self._button_reinit_command)
        button_reinit.pack(side='left', padx=2, pady=2)

        control_frame.pack(side='bottom', padx=2, pady=2)

        frame.pack(side='bottom', expand=True, fill='both')

    def refresh(self):
        pass

    def _add_settings_row(self, label_text: str, option: ttk.Entry = None):
        label = ttk.Label(self.settings_frame, text=label_text)

        label.grid(row=self.settings_row, column=0, sticky='w', padx=10, pady=2)
        if option is not None:
            option.grid(row=self.settings_row, column=1)

        self.settings_row += 1

    def _button_reinit_command(self):
        was_running = self.simulation_timer.is_running()
        self.simulation_timer.stop_timer()
        if show_askyesno('Reset', 'Are you sure want to abandon the current simulation?'):
            self._config_update()
            self.main_window.reinit()
        else:
            if was_running:
                self.simulation_timer.start_timer()

    def _button_reset_command(self):
        self._config_reset()

    def _config_reset(self):
        self.canvas_var.set(self.config.canvas_size)
        self.image_size_var.set(self.config.image_target_size)

    def _config_update(self):
        self.config.canvas_size = self.canvas_var.get()
        self.config.image_target_size = self.image_size_var.get()
