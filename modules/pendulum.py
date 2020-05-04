import numpy as np
from scipy.integrate import odeint
import warnings

# Some params
g = 9.81  # gravity acceleration


class Pendulum:
    """Class for pendulum instance with calculations of it's dynamic"""
    def __init__(self, parameters, th1_0, th2_0, time_grid, **kwargs):

        # lengths, masses and initial angles
        self.l1, self.l2, self.m1, self.m2 = parameters
        self.th1_0, self.th2_0 = th1_0, th2_0

        # how long and how precise will simulation be
        self.time_grid = time_grid

        # initial velocities
        if "d_th1_0" in kwargs:
            self.d_th1_0 = kwargs['d_th1_0']
        else:
            self.d_th1_0 = 0

        if "d_th2_0" in kwargs:
            self.d_th2_0 = kwargs['d_th2_0']
        else:
            self.d_th2_0 = 0

    def perform_calculations(self):

        # Initial conditions:
        y0 = np.array([self.th1_0, self.d_th1_0, self.th2_0, self.d_th2_0])

        # Do the numerical integration of the equations of motion
        y = np.array(odeint(Pendulum.deriv, y0, self.time_grid, args=(self.l1, self.l2, self.m1, self.m2)))

        # Unpack th1 and th2 as a function of time
        th1, th2 = y[:, 0], y[:, 2]

        # Convert to Cartesian coordinates of the two bob positions.
        self.x1 = self.l1 * np.sin(th1)
        self.y1 = -self.l1 * np.cos(th1)
        self.x2 = self.x1 + self.l2 * np.sin(th2)
        self.y2 = self.y1 - self.l2 * np.cos(th2)

        # we want to save final state of the system
        return y[-1, :]

    @staticmethod
    def deriv(y, t, l1, l2, m1, m2):
        """Return the first derivatives of y = th1, d_th1, th2, d_th2."""
        th1, d_th1, th2, d_th2 = y

        c, s = np.cos(th1 - th2), np.sin(th1 - th2)

        dd_th1 = (m2 * g * np.sin(th2) * c - m2 * s * (l1 * d_th1 ** 2 * c + l2 * d_th2 ** 2) -
                  (m1 + m2) * g * np.sin(th1)) / l1 / (m1 + m2 * s ** 2)
        dd_th2 = ((m1 + m2) * (l1 * d_th1 ** 2 * s - g * np.sin(th2) + g * np.sin(th1) * c) +
                  m2 * l2 * d_th2 ** 2 * s * c) / l2 / (m1 + m2 * s ** 2)

        return d_th1, dd_th1, d_th2, dd_th2
