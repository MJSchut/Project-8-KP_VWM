"""File with helper class, run main.py instead."""
import constants
import tools

import os

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
        self.subject = (
            "test" if subject_info is None else subject_info.get("Participant", "error")
        )

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
            "Geef met de 'w' en 'n' toets aan of het balkje veranderd is.\n\n"
            "Druk op 'n' als het balkje (N)iet veranderd is.\n "
            "Druk op 'w' als het balkje (W)el veranderd is.\n"
            "Je krijgt nu eerst {} oefenrondes met feedback aan het eind van iedere ronde.\n\n\n"
            "-- druk op de spatiebalk om te beginnen --".format(
                constants.NPRACTICE_TRIALS
            ),
            fontsize=24,
        )

        self.intro_screen = libscreen.Screen()
        self.intro_screen.draw_text(
            "INSTRUCTIES\n\n"
            "Nu volgen de echte trials.\n"
            "Je hoeft nu niet meer na iedere trial op de spatiebalk te drukken\n"
            "Probeer snel en correct te antwoorden, iedere {} trials krijg je de tijd voor een pauze.\n"
            "Je krijgt {} trials in totaal.\n\n\n"
            "-- Druk op de spatiebalk om verder te gaan --".format(
                constants.NBREAK_TRIALS, constants.NTRIALS
            ),
            fontsize=24,
        )

        self.end_screen = libscreen.Screen()
        self.end_screen.draw_text(
            "Dank je wel voor je deelname aan dit experiment.\n"
            "-- Druk op de spatiebalk het programma af te sluiten --".format(
                constants.NTRIALS
            ),
            fontsize=24,
        )

        self.break_screen = libscreen.Screen()

        self.experiment_screen = libscreen.Screen()

    def __create_stimuli(self):
        print("Initializing stimuli")
        amt = constants.SET_SIZES[-1]

        for i in range(amt):
            rect = visual.Rect(
                pygaze.expdisplay,
                width=constants.SQUAREWIDTH,
                height=constants.SQUAREHEIGHT,
                fillColor=None,
                lineWidth=10,
                lineColor=[1, 1, 1],
            )
            self.experiment_screen.screen.append(rect)

    def __set_up_input(self):
        self.kb_space = libinput.Keyboard(keylist=["space", "escape"], timeout=None)
        self.kb_input = libinput.Keyboard(keylist=["w", "n", "p", "escape"], timeout=None)

    def __set_up_output(self):
        # Fair warning, if you plan to use a LOT of trials. Don't use the python list like
        # I did here. Use a queue or something similar.
        self.output = [
            [
                "participant",
                "response key",
                "response time (ms)",
                "changed stimulus",
                "correct answer",
                "practice trial",
                "set_size",
            ]
        ]

    def start_practice(self, override_trials=None):
        self._play_screen_until_spacebar_press(self.instruction_screen)

        # add 1 to set size since the background counts as 1 stimulus
        for x in range(
            constants.NPRACTICE_TRIALS if override_trials is None else override_trials
        ):
            self._play_trial(
                x, [x + 1 for x in constants.PRACTICE_SET_SIZES], practice=True
            )

    def start_experiment(self, override_trials=None):
        """Run the entire experiment."""
        set_size_list = np.repeat(
            constants.SET_SIZES, np.ceil(constants.NTRIALS / len(constants.SET_SIZES))
        )
        np.random.shuffle(set_size_list)

        # add 1 to set size since the background counts as 1 stimulus
        set_size_list = [x + 1 for x in set_size_list]

        self._play_screen_until_spacebar_press(self.intro_screen)
        total_trials = constants.NTRIALS if override_trials is None else override_trials
        trials_completed = 0

        while trials_completed < total_trials:
            succes = self._play_trial(trials_completed, set_size_list)

            if (
                trials_completed > 0
                and trials_completed % constants.NBREAK_TRIALS == 0
                and trials_completed != constants.NTRIALS - 1
            ):
                self._take_a_break(trials_completed)

            elif not succes:
                np.random.shuffle(set_size_list)
                self._take_a_break(trials_completed)

            if succes:
                trials_completed += 1

        self.__serialize_data_to_csv()
        self._play_screen_until_spacebar_press(self.end_screen)

    def _take_a_break(self, trials_done):
        self.__serialize_data_to_csv()

        self.break_screen.clear()
        self.break_screen.draw_text(
            "PAUZE\n\n"
            "Je hebt even de tijd voor een korte pauze.\n"
            "Nog {} trials te gaan.\n\n\n"
            "-- Druk op de spatiebalk om verder te gaan --".format(
                constants.NTRIALS - trials_done
            ),
            fontsize=24,
        )

        self._play_screen_until_spacebar_press(self.break_screen)

    def __serialize_data_to_csv(self):
        file_name = "ppt_{}.csv".format(self.subject)

        with open(os.path.join(constants.DATADIR, file_name), "w") as outfile:
            for row in self.output:
                for item in row:
                    outfile.write("{},".format(item))
                outfile.write("\n")

    def _play_screen_until_spacebar_press(self, this_screen):
        self.disp.fill(this_screen)
        self.disp.show()
        k, _ = self.kb_space.get_key()
        if k == 'escape':
            self.exit_program()

    def _play_trial(self, trialcounter, set_size_list=None, practice=False):
        t1, t2, t3, t4 = constants.PAUSES
        stimulus_container = self.experiment_screen.screen[:]

        set_size = self._determine_set_size(set_size_list, trialcounter)

        change_trial = True
        if np.random.random_sample() < 0.5:
            change_trial = False
        self.experiment_screen.screen = self.experiment_screen.screen[0:set_size]

        self.responseKey = None
        self.responseTime = None

        self._prep_mask()
        self._scramble_stimuli()

        print("\tStarting trial %s" % trialcounter)
        self.__show_empty_screen(t1 + np.random.uniform(0, 1000))
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

        if self.responseKey == 'p':
            self.experiment_screen.screen = stimulus_container[:]
            return False

        print("\tFinished trial %s" % trialcounter)
        trial_correct = (self.responseKey == "n" and not change_trial) or (
            self.responseKey == "w" and change_trial
        )

        if practice:
            self.experiment_screen.draw_rect(
                color=(0,0,0), x=0, y=constants.DISPSIZE[1]/2 - 50, w=constants.DISPSIZE[0], h=150, fill=True
            )
            self.experiment_screen.draw_text(
                "Goed" if trial_correct else "Fout", fontsize=24
            )
            self.experiment_screen.draw_text(
                "\n\nDruk op de spatiebalk om verder te gaan", fontsize=24
            )
            self._play_screen_until_spacebar_press(self.experiment_screen)

        self.experiment_screen.screen = stimulus_container[:]

        self.output.append(
            [
                self.subject,
                self.responseKey,
                np.round(self.responseTime),
                trial_correct,
                change_trial,
                practice,
                set_size - 1,
            ]
        )
        return True

    @staticmethod
    def _determine_set_size(set_size_list, trialcounter):
        # the background counts as one stimulus, so 1 is added
        random_set_size = np.random.choice(constants.SET_SIZES) + 1

        # if no trial list is given, pick a random set size
        if set_size_list is None:
            set_size = random_set_size
        # get a random set size if the set size list is shorter than the current trial index
        elif len(set_size_list) <= trialcounter + 1:
            set_size = random_set_size
        # else pick a set size from the set size list
        else:
            set_size = set_size_list[trialcounter]
        return set_size

    def __show_empty_screen(self, duration):
        self.disp.fill()
        self.disp.show()
        if duration > 0:
            libtime.pause(duration)

    def _prep_mask(self):
        visual_noise_size = 128
        noise_size = 2048

        noise_texture = np.random.rand(visual_noise_size, visual_noise_size) * 2 - 1
        self.visualNoise = visual.PatchStim(
            win=pygaze.expdisplay,
            tex=noise_texture,
            size=(noise_size, noise_size),
            interpolate=False,
            mask="gauss",
        )
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
        selection_rect = visual.Rect(
            pygaze.expdisplay,
            width=constants.SQUAREHEIGHT * 1.3,
            height=constants.SQUAREHEIGHT * 1.3,
            fillColor=None,
            lineWidth=10,
            lineColor=[1, -1, -1],
            pos=randomrect.pos,
        )

        self.experiment_screen.screen.append(selection_rect)

    def __wait_for_trial_response(self):
        starttime = libtime.get_time()
        k, t = self.kb_input.get_key(flush=True)

        self.responseKey = k
        if self.responseKey == 'escape':
            self.exit_program()
        self.responseTime = libtime.get_time() - starttime

    def exit_program(self):
        from psychopy import core
        self.__serialize_data_to_csv()
        core.quit()


if __name__ == "__main__":
    experiment = Experiment()
    experiment.start_experiment(override_trials=10)
