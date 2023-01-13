import os
import threading
import tkinter as tk
from datetime import datetime
from tkinter import ttk
from typing import TYPE_CHECKING

import imageio

from config import RefreshType, InitType
from .simulation_handler import SimulationHandler
from .utils import show_message, show_error

if TYPE_CHECKING:
    from .main_window import MainWindow


class ConfigFrame:
    def __init__(self, main_window: 'MainWindow', parent: ttk.Frame):
        self.main_window = main_window
        self.config = main_window.config
        self.simulation_handler = self.main_window.simulation_handler

        frame = ttk.Frame(parent, relief='groove', borderwidth=3)

        ##### settings frame #####
        self.settings_frame = ttk.Frame(frame)
        self.settings_row = 0

        # Refresh
        refresh_frame = ttk.Frame(self.settings_frame)
        self.refresh_var = tk.Variable(value=self.config.refresh.value)
        for refresh_type in RefreshType:
            ttk.Radiobutton(refresh_frame, variable=self.refresh_var, text=str(refresh_type.value),
                            value=refresh_type.value, command=self._update_refresh).pack(anchor='w', side='top')
        self._add_settings_row('Refresh:', refresh_frame)

        # Init mode
        init_mode_frame = ttk.Frame(self.settings_frame)
        self.init_mode_var = tk.StringVar(value=self.config.init_type.value)
        for init_type in InitType:
            ttk.Radiobutton(init_mode_frame, variable=self.init_mode_var, text=str(init_type.value),
                            value=init_type.value).pack(anchor='w', side='top')
        self._add_settings_row('Init mode:', init_mode_frame)

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

        # Enable attractors
        self.enable_attractors_var = tk.BooleanVar(value=self.config.enable_attractors)
        enable_attractors_checkbutton = ttk.Checkbutton(self.settings_frame, variable=self.enable_attractors_var)
        self._add_settings_row('Enable attractors:', enable_attractors_checkbutton)

        self.settings_frame.pack(side='top')

        # Coloring
        self.coloring_var = tk.BooleanVar(value=self.config.coloring)
        coloring_checkbutton = ttk.Checkbutton(self.settings_frame, variable=self.coloring_var)
        self._add_settings_row('Coloring:', coloring_checkbutton)

        self.settings_frame.pack(side='top')

        # Produce GIF
        self.produce_gif_var = tk.BooleanVar(value=self.config.produce_gif)
        produce_gif_checkbutton = ttk.Checkbutton(self.settings_frame, variable=self.produce_gif_var)
        self._add_settings_row('Produce GIF:', produce_gif_checkbutton)

        self.settings_frame.pack(side='top')

        # GIF frequency
        self.gif_frequency_var = tk.IntVar(value=self.config.gif_frequency)
        gif_frequency_spinbox = ttk.Spinbox(self.settings_frame, from_=0, to=999999999,
                                            textvariable=self.gif_frequency_var, width=5, increment=1)
        self._add_settings_row('GIF frequency:', gif_frequency_spinbox)

        # GIF FPS
        self.gif_fps_var = tk.IntVar(value=self.config.gif_fps)
        gif_fps_spinbox = ttk.Spinbox(self.settings_frame, from_=0, to=999999999,
                                            textvariable=self.gif_fps_var, width=5, increment=1)
        self._add_settings_row('GIF FPS:', gif_fps_spinbox)

        ##### control frame #####
        control_frame = ttk.Frame(frame, relief='ridge', borderwidth=2)

        # Reset button
        button_reset = ttk.Button(control_frame, text='Reset settings', command=self._button_reset_command)
        button_reset.pack(side='left', padx=2, pady=2)

        # Init button
        button_reinit = ttk.Button(control_frame, text='Init simulation', command=self._button_reinit_command)
        button_reinit.pack(side='left', padx=2, pady=2)

        # Save GIF button
        button_save_gif = ttk.Button(control_frame, text='Save GIF', command=self._button_save_gif_command)
        button_save_gif.pack(side='left', padx=2, pady=2)

        control_frame.pack(side='bottom', padx=2, pady=2)

        frame.pack(side='bottom', expand=True, fill='both')

    def refresh(self):
        pass

    def _add_settings_row(self, label_text: str, option: ttk.Widget):
        label = ttk.Label(self.settings_frame, text=label_text)

        label.grid(row=self.settings_row, column=0, sticky='w', padx=10, pady=5)
        option.grid(row=self.settings_row, column=1, sticky='w', pady=5)

        self.settings_row += 1

    def _button_reinit_command(self):
        self.simulation_handler.stop()
        self._config_update()
        self.main_window.reinit()

    def _button_reset_command(self):
        self._config_reset()

    def _button_save_gif_command(self):
        t = threading.Thread(target=self._save_gif, daemon=True).start()

    def _config_reset(self):
        self.refresh_var.set(self.config.refresh.value)
        self.init_mode_var.set(self.config.init_type.value)
        self.canvas_var.set(self.config.canvas_size)
        self.image_size_var.set(self.config.image_target_size)
        self.enable_attractors_var.set(self.config.enable_attractors)
        self.coloring_var.set(self.config.coloring)
        self.produce_gif_var.set(self.config.produce_gif)
        self.gif_frequency_var.set(self.config.gif_frequency)
        self.gif_fps_var.set(self.config.gif_fps)

    def _config_update(self):
        self.config.refresh = RefreshType(self.refresh_var.get())
        self.config.init_type = InitType(self.init_mode_var.get())
        self.config.canvas_size = self.canvas_var.get()
        self.config.image_target_size = self.image_size_var.get()
        self.config.enable_attractors = self.enable_attractors_var.get()
        self.config.coloring = self.coloring_var.get()
        self.config.produce_gif = self.produce_gif_var.get()
        self.config.gif_frequency = self.gif_frequency_var.get()
        self.config.gif_fps = self.gif_fps_var.get()

        self.config.reload_attractors()

    def _update_refresh(self):
        self.config.refresh = RefreshType(self.refresh_var.get())

    def _save_gif(self):
        try:
            with imageio.get_writer(f'{SimulationHandler.GIF_SAVE_DIR}/{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.gif',
                                    mode='I', fps=self.config.gif_fps) as writer:
                for image_name in sorted(os.listdir(SimulationHandler.TMP_GIF_DIR), key=lambda x: int(x[:-5])):
                    image = imageio.imread(f'{SimulationHandler.TMP_GIF_DIR}/{image_name}')
                    writer.append_data(image)
            show_message('GIF saved!')
        except:
            show_error('Could not save GIF')
