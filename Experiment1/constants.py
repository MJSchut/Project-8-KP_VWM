"""Constants used for pygaze and the experiment."""

import os.path
import tools as va

# device constants
# base directory
DIR = os.path.dirname(__file__)
# where data is stored
DATADIR = os.path.join(DIR, "data")

# which back-end should pygaze use
DISPTYPE = "psychopy"

# the resolution of your screen
DISPSIZE = (1280, 720)

# the size of your screen in centimeters
SCREENSIZE = (60.7, 35)

# the distance of your screen to the eyes of the participant
SCREENDIST = 70

# whether to render the experiment in full-screen (recommended)
FULLSCREEN = True

# color of the background
BGC = (0, 0, 0)

# color of the foreground (mainly text and default stimulus color, RGB values)
FGC = (255, 255, 255)

# font size of the text
TEXTSIZE = 24

# which eyetracker to use (not implemented currently).
TRACKERTYPE = "eyelink"
# whether the eyetracker should make a noise during calibration, only useful when you don't have a screen.
EYELINKCALBEEP = False
# use the mouse as a dummy eyetracker
DUMMYMODE = True

# Experiment constants
# how many practice trials do you want
NPRACTICE_TRIALS = 10
# how many experiment trials
NTRIALS = 100
# how many trials before taking a break
NBREAK_TRIALS = 25
# how many stimuli does the participant need to remember.
# make sure this is a list.
# if you go too high, stimuli may start overlapping
SET_SIZES = [2, 3, 4, 6, 8]

# this is used to set the set sizes in the practice trials
# e.g. the first practice trial uses 2 stimuli, the second 2, the third 4 etc.
# if the length of this list is shorter than the number of practice trials, it'll pick random set sizes after
# exausting this list
PRACTICE_SET_SIZES = [2, 2, 4, 4, 6, 6, 8, 8]

# different orientations of the bars from vertical (0 is vertical, 90 is horizontal).
BAR_ORI = [0, 30, 60, 90, 120, 150]

# distance from the center of the screen that a stimulus can appear at (polar coordinates)
BAR_RHOS = [va.angle_to_px(4.0), va.angle_to_px(7.0), va.angle_to_px(10.0)]

# distance from the vertical meridian (in degrees) that a stimulus can appear at (polar coordinates)
BAR_PHIS = [0, 60, 120, 180, 240, 300]

# pauses after each phase of the experiment. e.g. the first number is the number of milliseconds before the first stimulus
# is shown on the screen
PAUSES = [300, 1000, 300, 500]

# how high should a bar be
SQUAREHEIGHT = va.angle_to_px(2)

# how wide should a bar be
SQUAREWIDTH = va.angle_to_px(0.1)
