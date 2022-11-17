from tkinter import ttk
from typing import TYPE_CHECKING

from .config_frame import ConfigFrame
from .statistics_frame import StatisticsFrame

if TYPE_CHECKING:
    from .main_window import MainWindow


class InformationFrame:
    def __init__(self, main_window: 'MainWindow'):
        frame = ttk.Frame(main_window.root, relief='groove', borderwidth=3)

        self.statistics_frame = StatisticsFrame(main_window)
        self.config_frame = ConfigFrame(main_window, frame)

        frame.pack(side='left', expand=True, fill='both')

    def refresh(self):
        self.statistics_frame.refresh()
        self.config_frame.refresh()
