import tkinter as tk

from PIL import Image, ImageTk

from .editor import BaseEditor


#TODO: zooming in and out
class ImageViewer(BaseEditor):
    def __init__(self, master, path, editable=False, *args, **kwargs) -> None:
        super().__init__(master, path, editable=editable, *args, **kwargs)
        self.exists = True
        self.open_image()

    def open_image(self):
        self.image = Image.open(self.path)
        self.image.thumbnail((700, 700))
        self.tk_image = ImageTk.PhotoImage(self.image)

        self.image_label = tk.Label(self, image=self.tk_image, **self.base.theme.editors)
        self.image_label.pack(fill=tk.BOTH, expand=True)
