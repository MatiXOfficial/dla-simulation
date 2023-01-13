import tkinter as tk
from sys import exit
from threading import Thread, Event
from tkinter import messagebox


def show_error(error_message):
    """
    Show a window with an error.
    """
    messagebox.showerror('Error', error_message)
    exit()


def show_message(message):
    """
    Show a window with a message.
    """
    messagebox.showinfo(message=message)


def show_askyesno(title, message):
    """
    Show a window with yes/no quesion.
    """
    return messagebox.askyesno(title, message)


def center_window(root: tk.Tk):
    """
    Place the window near the center of the screen.
    """
    # window_width = root.winfo_reqwidth()
    # window_height = root.winfo_reqheight()
    window_width, window_height = [int(val) for val in root.geometry().split('+')[0].split('x')]

    position_right = int(root.winfo_screenwidth() // 3 - window_width / 2)
    position_down = int(root.winfo_screenheight() // 3 - window_height / 2)

    root.geometry(f'+{position_right}+{position_down}')


class SimulationTimer(Thread):
    def __init__(self, action, timeout=1):
        Thread.__init__(self, daemon=True)
        self.action = action
        self.timeout = timeout

        self.can_run = Event()
        self.stopped = Event()

        self.killed = False

    def run(self):
        self.stop_timer()
        while True:
            self.can_run.wait()
            if self.killed:
                break
            while not self.stopped.wait(self.timeout):
                self.action()

    def start_timer(self):
        self.stopped.clear()
        self.can_run.set()

    def stop_timer(self):
        self.can_run.clear()
        self.stopped.set()

    def is_running(self):
        return self.can_run.is_set()

    def kill(self):
        self.killed = True
        self.can_run.set()
        self.stopped.set()

    def update_timeout(self, timeout):
        self.timeout = timeout

    def trigger_action(self):
        self.action()
