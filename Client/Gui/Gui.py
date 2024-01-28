import tkinter as Tk
import networking
from threading import Thread


class Gui():
    def __init__(self) -> None:
        self.client = networking.client()
        self.window = Tk.Tk()
        self.window.title("Chatterbots")