import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
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

        self.fishDiff = []
        self.sharkDiff = []

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
        self.ax = self.fig.add_subplot(211)
        self.ax_diff = self.fig.add_subplot(212)

        self.line1, = self.ax.plot([], [], 'g', lw=2)
        self.line1.set_label('Fish')
        self.line2, = self.ax.plot([], [], 'r', lw=2)
        self.line2.set_label('Sharks')
        self.ax.legend(loc="upper left")

        self.line1_diff, = self.ax_diff.plot([], [], 'g', lw=2)
        self.line1_diff.set_label('Fish Diff')
        self.line2_diff, = self.ax_diff.plot([], [], 'r', lw=2)
        self.line2_diff.set_label('Sharks Diff')
        self.ax_diff.legend(loc="upper left")

        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(self.canvas, master)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

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
        else:
            self.animation.event_source.start()
            self.btn.config(text='Pause')
        self.running = not self.running

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
        self.ax.set_ylim(0, max(self.ydata))
        self.ax.set_xlim(0, max([*self.xdata, 10]))


        self.fishDiff.append(self.stats["fishNew"][-1] - self.stats["fishDied"][-1])
        self.sharkDiff.append(self.stats["sharkNew"][-1] - self.stats["sharkDied"][-1])

        self.line1_diff.set_data(self.xdata, self.fishDiff)
        self.line2_diff.set_data(self.xdata, self.sharkDiff)
        self.ax_diff.set_ylim(min([*self.fishDiff, *self.sharkDiff, 1]), max([*self.fishDiff, *self.sharkDiff, 1]))
        self.ax_diff.set_xlim(0, max([*self.xdata, 10]))

        # If the given amount of iterations has been reached, then stop the animation
        if i >= self.points - 1:
            self.btn.config(text='Start')
            self.running = False
            self.animation = None
        # return self.line1,

