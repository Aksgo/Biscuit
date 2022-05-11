import tkinter as tk
from tkinter.constants import *

from .....components import Sidebar
from .....components import EditorsFrame


class ContentPane(tk.PanedWindow):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.base = master.base

        self.config(
            orient=HORIZONTAL, bd=0,
            relief=FLAT, opaqueresize=False)

        self.sidebar = Sidebar(self)
        self.mainpane = EditorsFrame(self)
        
        self.add(self.sidebar)
        self.add(self.mainpane)