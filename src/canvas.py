from curses import window
import tkinter as tk
from turtle import title
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from collections import deque
from numpy import diff

# This is the maximum length of the simulation
HISTORY_LEN = 100000

class App(tk.Frame):
    def __init__(self, main, x_size, y_size, world, master=None, **kwargs):

        # Initialize the superclass
        tk.Frame.__init__(self, master, **kwargs)

        # Track the statistics of the simulation
        self.stats: dict[str, list[int]] = {
            'fishTotal': [],
            'fishNew': [],
            'fishDied': [],
            'sharkTotal': [],
            'sharkNew': [],
            'sharkDied': [],
        }

        # Variables for the animation
        self.running = False
        self.animation = None
        self.xdata = None
        self.iteration = 0

        # Save the game, so we can tick it
        self.main = main

        # Save the root window
        self.master = master

        # Create the window for the world
        self.window = tk.Toplevel(master)
        self.window.resizable(False, False)
        self.window.title("Planetensimulation")

        # Create the upper Frame for the world inside the window
        self.window_world = tk.Canvas(self.window, width=x_size*10+15, height=y_size*10+15)
        # Create the lower Frame for the controls inside the window
        self.window_ctrl = tk.Frame(self.window)

        # Set the grid, so we can align stuff properly
        self.window_world.grid()
        self.window_ctrl.grid()

        # Create a rectangle for each cell in the world
        self.frames: list[list[object]] = \
            [[self.window_world.create_rectangle(x*10+10, y*10+10, x*10+20, y*10+20) for y in range(y_size)] for x in range(x_size)]

        # Color the cells
        for x in range(x_size):
            for y in range(y_size):
                color = world[x][y].color
                self.window_world.itemconfigure(self.frames[x][y], fill=color)

        # Iterations label
        lbl = tk.Label(self.window_ctrl, text="Iterations")
        lbl.grid(column=0, row=0)

        # Iterations entry field
        self.points_ent = tk.Entry(self.window_ctrl, width=5)
        self.points_ent.insert(0, '5000')
        self.points_ent.grid(column=1, row=0)

        # Interval label
        lbl = tk.Label(self.window_ctrl, text="update interval (ms)")
        lbl.grid(column=2, row=0)

        # Interval entry field
        self.interval = tk.Entry(self.window_ctrl, width=5)
        self.interval.insert(0, '100')
        self.interval.grid(column=3, row=0)

        # Start button
        self.btn = tk.Button(self.window_ctrl, text='Start', command=self.on_click)
        self.btn.grid(column=4, row=0)

        # Tick button
        self.tick_btn = tk.Button(self.window_ctrl, text='Tick', command=self.on_click_tick)
        self.tick_btn.grid(column=5, row=0)

        # Prepare the plot for the statistics
        self.fig = plt.Figure()
        self.ax1 = self.fig.add_subplot(111)
        self.line1, = self.ax1.plot([], [], lw=2)
        self.line2, = self.ax1.plot([], [], lw=2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    # Continue the simulation for one tick after the tick button is clicked
    def on_click_tick(self):
        self.start(tick=True)

    # Tick the simulation and store the statistics
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

    # Starts, pauses and un-pauses the simulation
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

    # Method for calculating the derivatives of the fish and shark amount
    def show_diff(self):
        # Calculate the derivatives
        dx = 1
        fishTotal = self.stats["fishTotal"]
        fishDiff = diff(fishTotal)/dx
        sharkTotal = self.stats["sharkTotal"]
        sharkDiff = diff(sharkTotal)/dx

        # Create a new window for the derivatives plot
        window_diff = tk.Toplevel(self.master)
        window_diff.resizable(False, False)
        window_diff.title("Änderungsrate")

        # Plot the derivatives inside the new window
        self.fig_diff = plt.Figure()
        self.ax_diff = self.fig_diff.add_subplot(111)
        self.line_diff_fish, = self.ax_diff.plot(fishDiff, lw=2)
        self.line_diff_shark, = self.ax_diff.plot(sharkDiff, lw=2)
        self.ax_diff.grid()
        self.canvas_diff = FigureCanvasTkAgg(self.fig_diff, master=window_diff)
        self.canvas_diff.draw()
        self.canvas_diff.get_tk_widget().pack()

    # Method for starting the animation
    def start(self, tick=False):
        # If the tick button has been clicked, then we need to tick the simulation only once
        # Else we need to tick the simulation for the given amount of iterations
        if not tick:
            self.points = int(self.points_ent.get())
        else:
           self.points = 0

        # Only initialize the arrays for the plot if it is not already initialized
        if self.xdata is None:
            self.xdata = deque([], maxlen=HISTORY_LEN)
            self.ydata = deque([], maxlen=HISTORY_LEN)
            self.y2data = deque([], maxlen=HISTORY_LEN)

        # Create the animation. This is the main loop of the program
        self.animation = animation.FuncAnimation(
            self.fig,
            self.update_graph,
            frames=self.points + 1,
            interval=self.interval.get(),
            repeat=False)
        self.running = True
        self.btn.config(text='Pause')
        self.animation._start()

    # Method for updating the color of one cell
    def update_animal(self, x, y, color):
        self.window_world.itemconfigure(self.frames[x][y], fill=color)

    # Method for updating the plot
    def update_graph(self, i):
        # This is needed, so that the tick button doesn't tick twice
        if (self.animation is None):
            return

        # Update the plot with the new statistics
        self.xdata.append(self.iteration)
        self.iteration += 1
        self.tick()
        self.ydata = self.stats["fishTotal"]
        self.y2data = self.stats["sharkTotal"]
        self.line1.set_data(self.xdata, self.ydata)
        self.line2.set_data(self.xdata, self.y2data)
        self.ax1.set_ylim(0, max(self.ydata))
        self.ax1.set_xlim(0, max([*self.xdata, 10]))

        # If the given amount of iterations has been reached, then stop the animation
        if i >= self.points - 1:
            self.btn.config(text='Start')
            self.running = False
            self.animation = None
        return self.line1,

