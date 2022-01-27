import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from animals.animal import Animal
# from animals.fish import Fish
# from animals.shark import Shark
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from collections import deque
import random

HISTORY_LEN = 1200


# https://stackoverflow.com/questions/43477681/how-to-speed-up-tkinter-embedded-matplot-lib-and-python

class App(tk.Frame):
    def __init__(self, main, x_size, y_size, world, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.stats: dict[str, list[int]] = {
            'fishTotal': [],
            'fishNew': [],
            'fishDied': [],
            'sharkTotal': [],
            'sharkNew': [],
            'sharkDied': [],
        }

        self.running = False
        self.animation = None

        self.main = main

        self.window = tk.Toplevel(master)
        self.window_world = tk.Frame(self.window)
        self.window_ctrl = tk.Frame(self.window)
        self.window_world.grid()
        self.window_ctrl.grid()

        self.frames: list[list[tk.Canvas]] = \
            [[self.create_canvas(x, y) for x in range(x_size)] for y in range(y_size)]

        for x in range(y_size):
            for y in range(x_size):
                color = world[x][y].color
                self.frames[x][y].configure(background=color)

        lbl = tk.Label(self.window_ctrl, text="Iterations")
        lbl.grid(column=0, row=0)

        self.points_ent = tk.Entry(self.window_ctrl, width=5)
        self.points_ent.insert(0, '500')
        self.points_ent.grid(column=1, row=0)

        lbl = tk.Label(self.window_ctrl, text="update interval (ms)")
        lbl.grid(column=2, row=0)

        self.interval = tk.Entry(self.window_ctrl, width=5)
        self.interval.insert(0, '500')
        self.interval.grid(column=3, row=0)

        self.btn = tk.Button(self.window_ctrl, text='Start', command=self.on_click)
        self.btn.grid(column=4, row=0)

        self.btn = tk.Button(self.window_ctrl, text='Tick', command=self.tick)
        self.btn.grid(column=5, row=0)

        self.fig = plt.Figure()
        self.ax1 = self.fig.add_subplot(111)
        self.line1, = self.ax1.plot([], [], lw=2)
        self.line2, = self.ax1.plot([], [], lw=2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def create_canvas(self, x, y):
        canvas = tk.Canvas(self.window_world, width=10, height=10)
        canvas.grid(column=x, row=y)
        return canvas

    def tick(self):
        stats = self.main.tick()
        # Append stats to self.stats
        for key, value in stats.items():
            self.stats[key].append(value)

        # If sharksTotal or fishTotal is 0, then the simulation is over
        if self.stats["fishTotal"][-1] == 0 or self.stats["sharkTotal"][-1] == 0:
           self.on_click() 

    def on_click(self):
        if self.animation is None:
            return self.start()
        if self.running:
            self.animation.event_source.stop()
            self.btn.config(text='Un-Pause')
        else:
            self.animation.event_source.start()
            self.btn.config(text='Pause')
        self.running = not self.running

    def start(self):
        self.xdata = deque([], maxlen=HISTORY_LEN)
        self.ydata = deque([], maxlen=HISTORY_LEN)
        self.y2data = deque([], maxlen=HISTORY_LEN)
        self.points = int(self.points_ent.get()) + 1
        self.animation = animation.FuncAnimation(
            self.fig,
            self.update_graph,
            frames=self.points,
            interval=int(self.interval.get()),
            repeat=False)
        self.running = True
        self.btn.config(text='Pause')
        self.animation._start()

    def update_animal(self, x, y, color):
        self.frames[x][y].configure(background=color)

    def update_graph(self, i):
        self.xdata.append(i)
        self.tick()
        self.ydata = self.stats["fishTotal"]
        self.y2data = self.stats["sharkTotal"]
        # self.ydata.append(random.randrange(100))
        self.line1.set_data(self.xdata, self.ydata)
        self.line2.set_data(self.xdata, self.y2data)
        self.ax1.set_ylim(min(self.ydata), max(self.ydata))
        self.ax1.set_xlim(min(self.xdata), max(self.xdata))
        if i >= self.points - 1:
            self.btn.config(text='Start')
            self.running = False
            self.animation = None
        return self.line1,

    def update_stats(self, stats: dict[str, list[int]]):
       pass
