from tkinter import *
from tkinter.ttk import Progressbar
import numpy as np
import shutil
import os

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


def main():
    try:
        shutil.rmtree('frames')
    except FileNotFoundError:
        pass

    generated_sim = {}

    # Set up a geometry of the window
    width = 1000
    height = 800

    geometry = str(width) + 'x' + str(height)

    # Create the window
    window = Tk()
    window.title('Double Pendulum Simulation')
    window.geometry(geometry)  # Width x Height

    # Sliders fo initial params: lengths, masses
    slider_l1 = Slider(window, label="First rope length", init_val=1, row=0, column=0)
    slider_l2 = Slider(window, label="Second rope length", init_val=1, row=1, column=0)
    slider_m1 = Slider(window, label="First ball mass", init_val=1, row=2, column=0)
    slider_m2 = Slider(window, label="Second ball mass", init_val=1, row=3, column=0)

    parameters_sliders = [slider_l1, slider_l2, slider_m1, slider_m2]

    # Sliders for initial thetas
    slider_th1 = Slider(window, label="First deflection angle", row=4, column=0, init_val=3 * np.pi / 7, from_=-np.pi, to=np.pi)
    slider_th2 = Slider(window, label="Second deflection angle", row=5, column=0, init_val=3 * np.pi / 4, from_=-np.pi, to=np.pi)

    # Slider for additional variables (see the lables)
    slider_npendulums = Slider(window, label='Number of pendulums', init_val=10, from_=1, to=50, row=0, column=1,
                               resolution=1)
    slider_epsilon = Slider(window, label='Delta thetas', init_val=0.5, from_=0.1, to=10, row=1, column=1,
                            resolution=0.001)
    slider_time = Slider(window, label='Simulation time (s)', init_val=5, from_=1, to=50, row=2, column=1, resolution=1)
    slider_fps = Slider(window, label='Frames per second', init_val=30, from_=5, to=100, row=3, column=1, resolution=1)

    def simulation():
        # Get values from pendulum parameters
        parameters = np.array([float(s.get()) for s in parameters_sliders])

        # Get values for initial angles
        th1 = slider_th1.get()
        th2 = slider_th2.get()

        # Get values from additional variables sliders
        n_pendulums = int(slider_npendulums.get())
        eps = float(slider_epsilon.get()) * np.pi / 180
        sim_time = int(slider_time.get())
        fps = int(slider_fps.get())

        input_params = str(hash(tuple(parameters) + (th1, th2, n_pendulums, eps, fps)))

        # Create a progress bar
        pb = Progressbar(window, orient=HORIZONTAL, length=100, mode='determinate')
        pb.grid(row=6, column=1)

        if input_params not in generated_sim.keys():
            # Create time grid for solving differential equations
            time_grid = np.arange(0, sim_time, 1 / fps)

            # Create a list of pendulums with th2_0 changed by epsilon
            pendulums = np.array([Pendulum(parameters, th1, th2 + i * eps, time_grid=time_grid) for i in range(n_pendulums)])

            # Create number of shots for these pendulums
            evol = Frames(pendulums, input_params)
            evol.create_frames(pb, window)

            generated_sim[input_params] = (sim_time, evol.final_state)

        else:
            old_sim_time, thetas = generated_sim[input_params]
            if sim_time > old_sim_time:
                # we need to draw only what is absent
                time_grid = np.arange(old_sim_time, sim_time, 1 / fps)
                pendulums = np.array([Pendulum(parameters,
                                               th1_0=thetas[i, 0],
                                               th2_0=thetas[i, 2],
                                               time_grid=time_grid,
                                               d_th1_0=thetas[i, 1],
                                               d_th2_0=thetas[i, 3]
                                               )
                                      for i in range(n_pendulums)])

                # Create number of shots for these pendulums with shift in file names
                evol = Frames(pendulums, input_params)
                evol.create_frames(pb, window, name_shift=old_sim_time * fps)

                generated_sim[input_params] = (sim_time, evol.final_state)

        # We need to define finish slide number in case of user's sim_time choice is less then was before
        anim = Animation(window, fps, input_params, finish=sim_time * fps)
        anim.grid(row=0, column=3, rowspan=7)

    # Compilation start button
    Button(window, text='Compile', command=simulation).grid(row=6,
                                                            column=0,
                                                            sticky=W,
                                                            pady=4)
    window.mainloop()

    # Remove frames folder to save user's space
    shutil.rmtree('frames')
