from curses import window
import tkinter as tk
from turtle import title
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from collections import deque
from numpy import diff

HISTORY_LEN = 100000

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
        self.xdata = None
        self.iteration = 0

        self.main = main
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.resizable(False, False)
        self.window.title("Planetensimulation")
        self.window_world = tk.Canvas(self.window, width=x_size*10+15, height=y_size*10+15)
        self.window_ctrl = tk.Frame(self.window)

        self.window_world.grid()
        self.window_ctrl.grid()

        self.frames: list[list[object]] = \
            [[self.window_world.create_rectangle(x*10+10, y*10+10, x*10+20, y*10+20) for y in range(y_size)] for x in range(x_size)]

        for x in range(x_size):
            for y in range(y_size):
                color = world[x][y].color
                self.window_world.itemconfigure(self.frames[x][y], fill=color)

        lbl = tk.Label(self.window_ctrl, text="Iterations")
        lbl.grid(column=0, row=0)

        self.points_ent = tk.Entry(self.window_ctrl, width=5)
        self.points_ent.insert(0, '5000')
        self.points_ent.grid(column=1, row=0)

        lbl = tk.Label(self.window_ctrl, text="update interval (ms)")
        lbl.grid(column=2, row=0)

        self.interval = tk.Entry(self.window_ctrl, width=5)
        self.interval.insert(0, '100')
        self.interval.grid(column=3, row=0)

        self.btn = tk.Button(self.window_ctrl, text='Start', command=self.on_click)
        self.btn.grid(column=4, row=0)

        self.tick_btn = tk.Button(self.window_ctrl, text='Tick', command=self.on_click_tick)
        self.tick_btn.grid(column=5, row=0)

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

    def on_click_tick(self):
        self.start(tick=True)

    def tick(self):
        stats = self.main.tick()
        # Append stats to self.stats
        for key, value in stats.items():
            self.stats[key].append(value)

        # If sharksTotal or fishTotal is 0, then the simulation is over
        if self.stats["fishTotal"][-1] == 0 or self.stats["sharkTotal"][-1] == 0:
            print("Simulation is over")
            print("Fish: " + str(self.stats["fishTotal"][-1]))
            print("Sharks: " + str(self.stats["sharkTotal"][-1]))

            self.on_click()

    def on_click(self):
        if self.animation is None:
            return self.start()
        if self.running:
            self.animation.event_source.stop()
            self.btn.config(text='Un-Pause')
            self.show_diff()
        else:
            self.animation.event_source.start()
            self.btn.config(text='Pause')
        self.running = not self.running

    def show_diff(self):
        dx = 1
        fishTotal = self.stats["fishTotal"]
        fishDiff = diff(fishTotal)/dx
        sharkTotal = self.stats["sharkTotal"]
        sharkDiff = diff(sharkTotal)/dx

        self.fig_diff = plt.Figure()
        self.ax_diff = self.fig_diff.add_subplot(111)
        self.line_diff_fish, = self.ax_diff.plot(fishDiff, lw=2)
        self.line_diff_shark, = self.ax_diff.plot(sharkDiff, lw=2)
        self.ax_diff.grid()
        window_diff = tk.Toplevel(self.master)
        window_diff.resizable(False, False)
        window_diff.title("Änderungsrate")
        self.canvas_diff = FigureCanvasTkAgg(self.fig_diff, master=window_diff)
        self.canvas_diff.draw()
        self.canvas_diff.get_tk_widget().pack()

    def start(self, tick=False):
        if not tick:
            self.points = int(self.points_ent.get())
        else:
           self.points = 0

        if self.xdata is None:
            self.xdata = deque([], maxlen=HISTORY_LEN)
            self.ydata = deque([], maxlen=HISTORY_LEN)
            self.y2data = deque([], maxlen=HISTORY_LEN)

        self.animation = animation.FuncAnimation(
            self.fig,
            self.update_graph,
            frames=self.points + 1,
            interval=self.interval.get(),
            repeat=False)
        self.running = True
        self.btn.config(text='Pause')
        self.animation._start()

    def update_animal(self, x, y, color):
        self.window_world.itemconfigure(self.frames[x][y], fill=color)

    def update_graph(self, i):
        if (self.animation is None):
            return
        self.xdata.append(self.iteration)
        self.iteration += 1
        self.tick()
        self.ydata = self.stats["fishTotal"]
        self.y2data = self.stats["sharkTotal"]
        self.line1.set_data(self.xdata, self.ydata)
        self.line2.set_data(self.xdata, self.y2data)
        self.ax1.set_ylim(0, max(self.ydata))
        self.ax1.set_xlim(0, max([*self.xdata, 10]))
        if i >= self.points - 1:
            self.btn.config(text='Start')
            self.running = False
            self.animation = None
        return self.line1,

