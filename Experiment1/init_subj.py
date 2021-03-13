"""@author: Martijn Schut."""

import time
import json
import os

from dir_creator import make_dir
import constants

from psychopy import gui
from psychopy import core


class InitSubject:
    """Initalizes a dialog box and stores the info in a dict."""

    def __init__(self):
        """Open dialogbox, use .expInfo dict to retrieve info."""
        print("\twaiting for subject info...")

        self.expInfo = {
            "Participant": "001",
            "Gender": ["M", "F", "NB"],
            "Age": 50,
            "Researcher": "EO",
            "Group": ["PT", "HC"],
            "Overwrite old data": ["No", "Yes"],
            "date": time.strftime("%d/%m/%Y"),
        }

        dlg = gui.DlgFromDict(
            self.expInfo,
            title="Visual Working Memory",
            order=["Participant", "Gender", "Age", "Group", "Researcher"],
            fixed=["date"],
        )

        if dlg.OK:
            file_name = "ppt_data_{}.csv".format(self.expInfo.get("Participant"))
            make_dir(constants.DATADIR)
            file_location = os.path.join(constants.DATADIR, file_name)

            if (
                os.path.isfile(file_location)
                and self.expInfo.get("Overwrite old data") != "Yes"
            ):
                print("deze proefpersoon bestaat al, programma wordt afgesloten")

            with open(file_location, "w") as outfile:
                for key in self.expInfo.keys():
                    outfile.write('{},{}\n'.format(key, self.expInfo.get(key)))
        else:
            core.quit()


if __name__ == "__main__":
    isub = InitSubject()
