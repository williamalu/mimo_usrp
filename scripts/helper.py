#!/usr/bin/env python


""" File that holds helper functions. """


import numpy as np


def wrap_radian(radian):
    """ Wraps an angle measurement in radians to be from -pi to pi. """

    while (radian > np.pi):
        radian -= 2 * np.pi

    while (radian < -np.pi):
        radian += 2 * np.pi

    return radian


if __name__ == "__main__":

    radian = 3 * np.pi
    print wrap_radian(radian)

    radian = -10 * np.pi
    print wrap_radian(radian)
