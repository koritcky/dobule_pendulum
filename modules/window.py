from tkinter import *
import numpy as np

from modules.gif_player import Animation
from modules.pendulum import Pendulum
from modules.frames import Frames


class Slider(Scale):
    """Same Scale object, but with more compact initialization"""

    def __init__(self, window, label, row, column, from_=0.5, to=3, init_val=1., resolution=0.01, **kwargs):
        super().__init__(window,
                         orient=HORIZONTAL,
                         label=label,
                         length=170,
                         from_=from_,
                         to=to,
                         resolution=resolution,
                         **kwargs)
        self.set(init_val)
        self.grid(row=row, column=column)


# Set up a geometry of the window
def main():
    width = 1000
    height = 800

    geometry = str(width) + 'x' + str(height)

    # Create the window
    window = Tk()
    window.title('Double Pendulum Simulation')
    window.geometry(geometry)  # Width x Height

    # Sliders fo initial variables: lengths, masses, thetas
    slider_l1 = Slider(window, label="First rope length", init_val=1, row=0, column=0)
    slider_l2 = Slider(window, label="Second rope length", init_val=1, row=1, column=0)
    slider_m1 = Slider(window, label="First ball mass", init_val=1, row=2, column=0)
    slider_m2 = Slider(window, label="Second ball mass", init_val=1, row=3, column=0)
    slider_th1 = Slider(window, label="First deflection angle", row=4, column=0, init_val=3 * np.pi / 7, from_=-np.pi, to=np.pi)
    slider_th2 = Slider(window, label="Second deflection angle", row=5, column=0, init_val=3 * np.pi / 4, from_=-np.pi, to=np.pi)

    init_var_sliders = [slider_l1, slider_l2, slider_m1, slider_m2, slider_th1, slider_th2]

    # Slider for additional variables (see the lables)
    slider_npendulums = Slider(window, label='Number of pendulums', init_val=10, from_=1, to=50, row=0, column=1, resolution=1)
    slider_epsilon = Slider(window, label='Delta thetas', init_val=0.005, from_=0.001, to=0.01, row=1, column=1, resolution=0.001)
    slider_time = Slider(window, label='Simulation time (s)', init_val=5, from_=1, to=50, row=2, column=1, resolution=1)
    slider_fps = Slider(window, label='Frames per second', init_val=30, from_=5, to=100, row=3, column=1, resolution=1)

    def simulation():
        # Get values from initial variables sliders
        variables = np.array([float(s.get()) for s in init_var_sliders])

        # Get values from additional variables sliders
        n_pendulums = int(slider_npendulums.get())
        eps = float(slider_epsilon.get())
        sim_time = int(slider_time.get())
        fps = int(slider_fps.get())

        # Create time grid for solving differential equations
        time_grid = np.arange(0, sim_time, 1 / fps)

        # Create a list of pendulums with th2_0 changed by epsilon
        eps_vec = np.array([0, 0, 0, 0, 0, eps])  # we want to change only  th2_0
        pendulums = np.array([Pendulum(variables + i * eps_vec, time_grid=time_grid) for i in range(n_pendulums)])

        # Create number of shots for these pendulums
        gif = Frames(pendulums)
        gif.create_frames()

        # Play animation of this frames
        anim = Animation(window, fps)
        anim.grid(row=0, column=3, rowspan=7)

    # Compilation start button
    Button(window, text='Compile', command=simulation).grid(row=6,
                                                            column=0,
                                                            sticky=W,
                                                            pady=4)
    window.mainloop()
