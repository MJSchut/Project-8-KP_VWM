"""File with helper class, run main.py instead."""
import constants
import tools

import pygaze
from pygaze import libscreen
from pygaze import libtime
from pygaze import libinput

from psychopy import visual

import numpy as np


class Experiment:
    """List of functions to smooth out the code in the main.py file."""

    def __init__(self):
        """Run a bunch of one-shot private functions."""
        self.__create_screens()
        self.__create_stimuli()
        self.__set_up_input()

    def __create_screens(self):
        print ("Initializing display")
        self.disp = libscreen.Display()

        print ("Initializing screens")
        self.introscreen = libscreen.Screen()
        self.introscreen.draw_text(
            "Druk op de spatiebalk om verder te gaan.",
            fontsize=24)
        self.experimentscreen = libscreen.Screen()

    def __create_stimuli(self):
        print ("Initializing stimuli")
        amt = constants.SET_SIZES[-1]

        for i in range(amt):
            rect = visual.Rect(pygaze.expdisplay)
            rect.width = constants.SQUAREWIDTH
            rect.height = constants.SQUAREHEIGHT
            self.experimentscreen.screen.append(rect)

    def __set_up_input(self):
        self.kb_space = libinput.Keyboard(keylist=['space'], timeout=None)
        self.kb_input = libinput.Keyboard(keylist=['a', 'l'], timeout=None)

    def start_experiment(self):
        """Run the entire experiment."""
        self._play_intro_screen()
        for x in range(constants.NTRIALS):
            self._play_trial(x)

    def _play_intro_screen(self):
        self.disp.fill(self.introscreen)
        self.disp.show()
        self.kb_space.get_key()

    def _play_trial(self, trialcounter):
        t1, t2, t3, t4 = constants.PAUSES
        stimulusContainer = self.experimentscreen.screen[:]
        # background is first stimulus
        set_size = np.random.choice(constants.SET_SIZES) + 1
        change_trial = True
        if np.random.random_sample() < 0.5:
            change_trial = False
        self.experimentscreen.screen = self.experimentscreen.screen[0:set_size]

        self.responseKey = None
        self.responseTime = None

        self._prep_mask()
        self._scramble_stimuli()

        print ("\tStarting trial %s" % trialcounter)
        self.__show_empty_screen(t1)
        self.__show_experiment_screen(t2)
        self.__show_mask(t3)
        if change_trial:
            rect = self.__change_feature()
        else:
            rect = self._random_rect()
        self.__show_experiment_screen(t4)
        self.__add_selection_rect(rect)
        self.__show_experiment_screen(0)
        self.__wait_for_trial_response()

        print ("\tFinished trial %s" % trialcounter)

        self.experimentscreen.screen = stimulusContainer[:]

    def __show_empty_screen(self, duration):
        self.disp.fill()
        self.disp.show()
        if duration > 0:
            libtime.pause(duration)

    def _prep_mask(self):
        visualNoiseSize = 128
        noiseSize = 2048

        noiseTexture = np.random.rand(visualNoiseSize, visualNoiseSize) * 2 - 1
        self.visualNoise = visual.PatchStim(win=pygaze.expdisplay,
                                            tex=noiseTexture,
                                            size=(noiseSize, noiseSize),
                                            interpolate=False,
                                            mask='gauss')
        self.noisescreen = libscreen.Screen()
        self.noisescreen.screen.append(self.visualNoise)

    def __show_mask(self, duration):
        self.disp.fill(self.noisescreen)
        self.disp.show()
        if duration > 0:
            libtime.pause(duration)

    def __show_experiment_screen(self, duration):
        self.disp.fill(self.experimentscreen)
        self.disp.show()
        if duration > 0:
            libtime.pause(duration)

    def _scramble_stimuli(self):
        rhophi = []

        for rect in self.experimentscreen.screen[1:]:
            while True:
                rho = np.random.choice(constants.BAR_RHOS)
                phi = np.random.choice(constants.BAR_PHIS)
                rhophitrial = (rho, phi)
                for item in rhophi:
                    if item[0] == rhophitrial[0] and item[1] == rhophitrial[1]:
                        break
                else:
                    rhophi.append(rhophitrial)
                    break

            rect.pos = tools.poltocart(rho, phi)
            rect.ori = np.random.choice(constants.BAR_ORI)

    def __change_feature(self):
        randomrect = self._random_rect()
        oori = nori = randomrect.ori
        while oori == nori:
            nori += np.random.choice([-90, 90])
            nori = nori % 180

        randomrect.ori = nori
        return randomrect

    def _random_rect(self):
        return np.random.choice(self.experimentscreen.screen[1:])

    def __add_selection_rect(self, randomrect):
        selectionRect = visual.Rect(pygaze.expdisplay,
                                    width=constants.SQUAREHEIGHT * 1.3,
                                    height=constants.SQUAREHEIGHT * 1.3,
                                    fillColor=None,
                                    lineWidth=10,
                                    lineColor=[1, -1, -1],
                                    pos=randomrect.pos)

        self.experimentscreen.screen.append(selectionRect)

    def __wait_for_trial_response(self):
        starttime = libtime.get_time()
        # k, t = self.kb_input.get_key()
        libtime.pause(np.random.uniform(800, 1400))

        self.responseKey = 'A'
        self.responseTime = libtime.get_time() - starttime
