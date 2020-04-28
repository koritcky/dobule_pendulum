import imageio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import os
import shutil

from modules.pendulum import Pendulum

r = 0.05  # standard ball radius


class Frames:
    """Create number of shots of pendulums dynamic"""

    def __init__(self, pendulums, subfolder_name):

        # List of pendulums with different initial params
        self.pendulums = pendulums
        self.subfolder_name = subfolder_name
        try:
            os.makedirs('frames/' + subfolder_name)
        except FileExistsError:
            pass

        # Calculate all the dynamics of pendulums
        self.final_state = np.array([pendulum.perform_calculations() for pendulum in pendulums])

        fig = plt.figure(figsize=(8, 6.25), dpi=72)
        self.shot = fig.add_subplot(111)
        self.frames = []

    def create_frames(self, pb, window, name_shift=0):
        """Create shots of pendulums dynamics and save it in dir 'frames' """
        time_grid = self.pendulums[0].time_grid
        for i in range(len(time_grid)):
            frame = self.create_shot(i, self.shot, self.pendulums, name_shift=name_shift)
            self.frames.append(frame)
            print(i + 1, '/', time_grid.size)
            pb['value'] = (i + 1 + name_shift) / (time_grid.size + name_shift) * 100
            window.update_idletasks()

    def create_shot(self, i, shot, pendulums, name_shift):
        # Clear the frame
        plt.cla()

        # Add all pendulums to given shot
        for pendulum in pendulums:
            Frames.add_to_shot(shot, i, pendulum)

        # Centre the image on the fixed anchor point, and ensure the axes are equal
        l1 = pendulums[0].l1
        l2 = pendulums[0].l2
        shot.set_xlim(-l1 - l2 - r, l1 + l2 + r)
        shot.set_ylim(-l1 - l2 - r, l1 + l2 + r)
        shot.set_aspect('equal', adjustable='box')
        plt.axis('off')

        # Save shot to dir
        filename = ('frames/' + self.subfolder_name + '/img{:04d}.png').format(i + name_shift)
        plt.savefig(filename.format(i), dpi=72)

        return imageio.imread(filename)

    @staticmethod
    def add_to_shot(shot, i, pendulum: Pendulum):
        """Add given pendulum to the shot"""

        x1, y1, x2, y2 = pendulum.x1[i], pendulum.y1[i], pendulum.x2[i], pendulum.y2[i]

        # Plot and save an image of the double pendulum configuration for timepoint i.
        # Rods
        shot.plot([0, x1, x2], [0, y1, y2], lw=2, c='k')

        # Circles representing the anchor point of rod 1, and bobs 1 and 2.
        c0 = Circle((0, 0), r / 2, fc='k', zorder=10)
        c1 = Circle((x1, y1), r * pendulum.m1, fc='g', ec='g', zorder=10)
        c2 = Circle((x2, y2), r * pendulum.m2, fc='b', ec='b', zorder=10)
        shot.add_patch(c0)
        shot.add_patch(c1)
        shot.add_patch(c2)
