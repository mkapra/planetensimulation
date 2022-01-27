import random
import time
from pprint import pprint
import matplotlib
import matplotlib.animation as anim
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class Report:

    def __init__(self, canvas):
        self.canvas = canvas
        self.stats: dict[str, list[int]] = {
            'FishTotal': [],
            'FishNew': [],
            'FishDied': [],
            'SharkTotal': [],
            'SharkNew': [],
            'SharkDied': [],
        }

    def update_stats(self, stats: dict[str, list[int]]):
        self.stats.get("FishTotal").append(stats.get("Fish")[0])
        self.stats.get("FishNew").append(stats.get("Fish")[1])
        self.stats.get("FishDied").append(stats.get("Fish")[2])
        self.stats.get("SharkTotal").append(stats.get("Shark")[0])
        self.stats.get("SharkNew").append(stats.get("Shark")[1])
        self.stats.get("SharkDied").append(stats.get("Shark")[2])

    def update(self):
        y = []
        fig = plt.figure()
        plt.axis([0, 50, 0, 50])
        ax = fig.add_subplot(1, 1, 1)
        # ax = plt.gca()
        # ax.set_xlim([0, 100])
        # ax.set_ylim([0, 50])
        xmax = 100

        def values():
            # Return new value
            colors = ['red', 'blue', 'green']
            for _x in range(15):
                for _y in range(15):
                    self.canvas.update_animal(_x, _y, colors[random.randint(0, 2)])
            return self.stats.get('FishTotal')

        def update_self(i):
            y = values()
            x = range(len(y))
            ax.clear()
            ax.plot(x, y)

        a = anim.FuncAnimation(fig, update_self, frames=xmax, repeat=False)
        plt.show()





















            # Total
            # plt.figure()
            # plt.grid(True)
            # plt.plot(x, ft, 'g-')
            # plt.plot(x, st, 'r-')
            # plt.plot(x, [sum(x) for x in zip(ft, st)], 'b-')
            # plt.title('Total')
            # plt.ylabel('Number of')
            # plt.xlabel('Time')
            # plt.legend(['FishTotal', 'SharkTotal', 'AnimalTotal'])

            # # New
            # plt.figure()
            # plt.grid(True)
            # plt.plot(x, fn, 'g-')
            # plt.plot(x, sn, 'r-')
            # plt.title('New')
            # plt.ylabel('Number of')
            # plt.xlabel('Time')
            # plt.legend(['FishNew', 'SharkNew'])
            #
            # # Died
            # plt.figure()
            # plt.grid(True)
            # plt.plot(x, fd, 'g-')
            # plt.plot(x, sd, 'r-')
            # plt.title('Died')
            # plt.ylabel('Number of')
            # plt.xlabel('Time')
            # plt.legend(['FishDied', 'SharkDied'])
            #
            # # SharkTotal <-> FishDied
            # plt.figure()
            # plt.grid(True)
            # plt.plot(x, fd, 'g-')
            # plt.plot(x, st, 'r-')
            # plt.title('SharkTotal <-> FishDied')
            # plt.ylabel('Number of')
            # plt.xlabel('Time')
            # plt.legend(['FishDied', 'SharkTotal'])

            # plt.pause(0.01)
            # time.sleep(1)