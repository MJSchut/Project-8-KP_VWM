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

    def __init__(self, subject_info=None):
        """Run a bunch of one-shot private functions."""
        if subject_info is None:
            self.subject = 'test'
        self.subject = subject_info.get('Participant', 'error')
        self.__create_screens()
        self.__create_stimuli()
        self.__set_up_input()
        self.__set_up_output()

    def __create_screens(self):
        print("Initializing display")
        self.disp = libscreen.Display()

        print("Initializing screens")
        self.instruction_screen = libscreen.Screen()
        self.instruction_screen.draw_text(
            "INSTRUCTIES\n\n"
            "Je krijgt op ieder scherm een aantal balkjes te zien.\n"
            "Daarna verschijnt er kort een scherm met ruis.\n"
            "Tot slot krijg je nogmaals het scherm met balkjes te zien.\n\n"
            "Na een moment verschijnt er een rood vierkant rond een van de balkjes.\n "
            "Geef met de 'a' en 'l' toets aan of het balkje veranderd is.\n\n"
            "Druk op 'a' als het balkje NIET veranderd is.\n "
            "Druk op 'l' als het balkje wel veranderd is.\n"
            "Je krijgt nu eerst {} oefenrondes met feedback aan het eind van iedere ronde.\n\n\n"
            "-- druk op de spatiebalk om te beginnen --".format(constants.NPRACTICE_TRIALS),
            fontsize=24)

        self.intro_screen = libscreen.Screen()
        self.intro_screen.draw_text(
            "INSTRUCTIES\n\n"
            "Nu volgen de echte trials.\n"
            "Je krijgt {} trials in totaal.\n\n\n"
            "-- Druk op de spatiebalk om verder te gaan --".format(constants.NTRIALS),
            fontsize=24)
        self.experiment_screen = libscreen.Screen()

    def __create_stimuli(self):
        print("Initializing stimuli")
        amt = constants.SET_SIZES[-1]

        for i in range(amt):
            rect = visual.Rect(pygaze.expdisplay,
                               width=constants.SQUAREWIDTH,
                               height=constants.SQUAREHEIGHT,
                               fillColor=None,
                               lineWidth=10,
                               lineColor=[1, 1, 1])
            self.experiment_screen.screen.append(rect)

    def __set_up_input(self):
        self.kb_space = libinput.Keyboard(keylist=['space'], timeout=None)
        self.kb_input = libinput.Keyboard(keylist=['a', 'l'], timeout=None)

    def __set_up_output(self):
        # Fair warning, if you plan to use a LOT of trials. Don't use the python list like
        # I did here. Use a queue or something similar.
        self.output = [["participant, response key, response time, changed stimulus, correct answer, practice trial, "
                        "set_size"]]

    def start_practice(self, override_trials=None):
        self._play_text_screen(self.instruction_screen)
        for x in range(constants.NPRACTICE_TRIALS if override_trials is None else override_trials):
            self._play_trial(x, practice=True)

    def start_experiment(self, override_trials=None):
        """Run the entire experiment."""
        self._play_text_screen(self.intro_screen)
        for x in range(constants.NTRIALS if override_trials is None else override_trials):
            self._play_trial(x)

    def _play_text_screen(self, this_screen):
        self.disp.fill(this_screen)
        self.disp.show()
        self.kb_space.get_key()

    def _play_trial(self, trialcounter, practice=False):
        t1, t2, t3, t4 = constants.PAUSES
        stimulus_container = self.experiment_screen.screen[:]

        # background is first stimulus
        set_size = np.random.choice(constants.SET_SIZES) + 1
        change_trial = True
        if np.random.random_sample() < 0.5:
            change_trial = False
        self.experiment_screen.screen = self.experiment_screen.screen[0:set_size]

        self.responseKey = None
        self.responseTime = None

        self._prep_mask()
        self._scramble_stimuli()

        print("\tStarting trial %s" % trialcounter)
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

        print("\tFinished trial %s" % trialcounter)

        self.experiment_screen.screen = stimulus_container[:]

        trial_correct = (self.responseKey == 'a' and not change_trial) or \
                        (self.responseKey == 'l' and change_trial)

        self.output.append([self.subject,
                           self.responseKey,
                           self.responseTime,
                           trial_correct,
                           change_trial,
                           practice,
                           set_size])

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
        self.disp.fill(self.experiment_screen)
        self.disp.show()
        if duration > 0:
            libtime.pause(duration)

    def _scramble_stimuli(self):
        rhophi = []

        for rect in self.experiment_screen.screen[1:]:
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
        return np.random.choice(self.experiment_screen.screen[1:])

    def __add_selection_rect(self, randomrect):
        selectionRect = visual.Rect(pygaze.expdisplay,
                                    width=constants.SQUAREHEIGHT * 1.3,
                                    height=constants.SQUAREHEIGHT * 1.3,
                                    fillColor=None,
                                    lineWidth=10,
                                    lineColor=[1, -1, -1],
                                    pos=randomrect.pos)

        self.experiment_screen.screen.append(selectionRect)

    def __wait_for_trial_response(self):
        starttime = libtime.get_time()
        k, t = self.kb_input.get_key(flush=True)
        libtime.pause(np.random.uniform(800, 1400))

        self.responseKey = k
        self.responseTime = libtime.get_time() - starttime


if __name__ == "__main__":
    experiment = Experiment()
    experiment.start_experiment(override_trials=5)
