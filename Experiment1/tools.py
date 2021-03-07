"""
Created on Wed May 13 09:16:47 2015.

@author: Martijn Schut
"""

import constants
import numpy as np
from math import atan2, degrees


def poltocart(rho, phi):
    """
    Convert polar coordinates to cartesian coordinates.

    Arguments:
    rho -- the distance, or amplitude of the vector.
    phi -- the angle from 0, where east is 0 and north in 90.

    Returns:
    pos -- a tuple which contains an x and a y cartesian coordinate.

    """
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    pos = (x, y)
    return pos


def angle_to_px(angle):
    """Convert visual angle and return pixels, requires constants.py."""
    SCREENSIZE = constants.SCREENSIZE       # Size of screen
    DISPSIZE = constants.DISPSIZE           # Screen resolution
    SCREENDIST = constants.SCREENDIST       # Distance of screen in cm

    h = SCREENSIZE[1]
    d = SCREENDIST
    r = DISPSIZE[1]

    deg_per_px = degrees(atan2(.5*h, d)) / (.5*r)

    size_in_px = angle / deg_per_px
    return size_in_px


def px_to_angle(px):
    """Convert pixels to visual angle, requires constants.py."""
    SCREENSIZE = constants.SCREENSIZE       # Size of screen
    DISPSIZE = constants.DISPSIZE           # Screen resolution
    SCREENDIST = constants.SCREENDIST       # Distance of screen in cm

    h = SCREENSIZE[1]
    d = SCREENDIST
    r = DISPSIZE[1]

    deg_per_px = degrees(atan2(.5*h, d)) / (.5*r)
    size_in_deg = px * deg_per_px

    return size_in_deg
