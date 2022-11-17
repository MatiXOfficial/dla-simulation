from tkinter import ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .main_window import MainWindow


class StatisticsFrame:
    def __init__(self, main_window: 'MainWindow', parent: ttk.Frame):
        self.dla_image = main_window.dla_image

        frame = ttk.Frame(parent, relief='groove', borderwidth=3)

        self.size_label = ttk.Label(frame, font=('Arial', 15), text=self._size_label_build_text())
        self.size_label.pack()

        frame.pack(side='top', expand=False, fill='both')

    def refresh(self):
        self.size_label.config(text=self._size_label_build_text())

    def _size_label_build_text(self):
        return f'Image size: {self.dla_image.get_n_grid()} / {self.dla_image.get_target_size()}'
