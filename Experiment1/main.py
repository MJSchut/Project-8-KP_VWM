"""File to run the experiment with."""

from init_subj import InitSubject
from experiment import Experiment

print ("main.py was started...")
infoSubject = InitSubject()
print ("Subject info entered succesfully!")

print ("Preparing experiment...")
experiment = Experiment(infoSubject.expInfo)
print ("Preparations are complete!")

print ("Starting experiment")
experiment.start_practice(3)
experiment.start_experiment(5)
print ("Experiment is complete")
