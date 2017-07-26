"""Constants used for pygaze and the experiment."""

import os.path
import tools as va

# device constants
DIR = os.path.dirname(__file__)
DATADIR = os.path.join(DIR, 'data')
LOGFILE = os.path.join(DATADIR)

DISPTYPE = 'psychopy'
DISPSIZE = (1280, 720)
SCREENSIZE = (60.7, 35)
SCREENDIST = 70
FULLSCREEN = True
BGC = (0, 0, 0)
FGC = (255, 255, 255)
TEXTSIZE = 24

TRACKERTYPE = 'eyelink'
EYELINKCALBEEP = False
DUMMYMODE = True

# Experiment constants
NTRIALS = 100
SET_SIZES = [2, 3, 4, 6, 8]
BAR_FEATURES = ['ori', 'colors']
BAR_ORI = [0, 30, 60, 90, 120, 150]
BAR_HUE = [0, 60, 120, 180, 240, 300]
BAR_RHOS = [va.angle_to_px(5.0), va.angle_to_px(9.0), va.angle_to_px(13.0)]
BAR_PHIS = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
PAUSES = [300, 1000, 300, 500]
SQUAREHEIGHT = va.angle_to_px(2)
SQUAREWIDTH = va.angle_to_px(0.1)
