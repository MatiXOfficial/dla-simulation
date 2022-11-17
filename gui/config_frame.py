from tkinter import ttk
from typing import TYPE_CHECKING

from .utils import show_askyesno

if TYPE_CHECKING:
    from .main_window import MainWindow


class ConfigFrame:
    def __init__(self, main_window: 'MainWindow', parent: ttk.Frame):
        self.main_window = main_window
        self.simulation_timer = main_window.simulation_timer

        frame = ttk.Frame(parent, relief='groove', borderwidth=3)

        self.settings_frame = ttk.Frame(frame)
        self.settings_row = 0

        # Refresh
        self._add_settings_row('Refresh:')

        # Init mode
        self._add_settings_row('Init mode:')

        # Canvas size
        self._add_settings_row('Canvas size:')

        # Image size
        self._add_settings_row('Image size:')

        self.settings_frame.pack(side='top', expand=False)

        # Reset button
        button_reset = ttk.Button(frame, text='Reset', command=self._button_reset_command)
        button_reset.pack(side='bottom')

        frame.pack(side='bottom', expand=True, fill='both')

    def refresh(self):
        pass

    def _add_settings_row(self, label_text: str, option: ttk.Frame = None):
        label = ttk.Label(self.settings_frame, text=label_text)
        label.grid(row=self.settings_row, column=0, sticky='w', pady=2)
        self.settings_row += 1

    def _button_reset_command(self):
        was_running = self.simulation_timer.is_running()
        self.simulation_timer.stop_timer()
        if show_askyesno('Reset', 'Are you sure want to abandon the current simulation and reset the settings?'):
            self.simulation_timer.kill()
            self.main_window.reinit()
        else:
            if was_running:
                self.simulation_timer.start_timer()
