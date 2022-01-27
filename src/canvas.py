import tkinter

from tkinter import *
from tkinter import ttk
from animals.animal import Animal


class Canvas(tkinter.Tk):

    def __init__(self, world: list[list[Animal]], x_size: int, y_size: int):

        super().__init__()

        self.mainframe = ttk.Frame(self, padding="1 1 1 1")
        self.mainframe.grid(column=0, row=0)

        self.resizable(FALSE, FALSE)
        self.title("Planetensimulation")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.frames: list[list[tkinter.Canvas|None]] = [[self.create_canvas(x, y) for y in range(y_size)] for x in
                                                          range(x_size)]

        for x in range(x_size):
            for y in range(y_size):
                color = 'blue' if world[x][y] is None else world[x][y].color()
                self.frames[x][y].configure(background=color)

    def create_canvas(self, x, y):
        canvas = tkinter.Canvas(self.mainframe, width=10, height=10)
        canvas.grid(column=x, row=y)
        return canvas

    def update_animal(self, x, y, color):
        self.frames[x][y].configure(background=color)

    def start_loop(self, report):
        self.after(0, report.update())
        self.mainloop()
