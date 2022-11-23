from tkinter import ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .main_window import MainWindow


class StatisticsFrame:
    def __init__(self, main_window: 'MainWindow', parent: ttk.Frame):
        self.config = main_window.config
        self.simulation_handler = main_window.simulation_handler

        frame = ttk.Frame(parent, relief='groove', borderwidth=3)

        self.size_label = ttk.Label(frame, font=('Arial', 15), text=self._size_label_build_text())
        self.size_label.pack()

        frame.pack(side='top', expand=False, fill='both')

    def refresh(self):
        self.size_label.config(text=self._size_label_build_text())

    def _size_label_build_text(self):
        return f'Image size: {self.simulation_handler.grid_len} / {self.config.image_target_size}'
