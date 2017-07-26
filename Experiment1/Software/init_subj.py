"""@author: Martijn Schut."""

import time
from psychopy import gui
from psychopy import core


class InitSubject:
    """Initalizes a dialog box and stores the info in a dict."""

    def __init__(self):
        """Öpen dialogbox, use .expInfo dict to retrieve info."""
        print ("\twaiting for subject info...")

        self.expInfo = {
            'Participant': '001',
            'Gender': ['Male', 'Female'],
            'Age': 50,
            'Researcher': 'EO',
            'Group': ['PT', 'HC'],
            'date': time.strftime("%d/%m/%Y")
        }

        dlg = gui.DlgFromDict(
            self.expInfo,
            title='Visual Working Memory',
            order=['Participant', 'Gender', 'Age', 'Group', 'Researcher'],
            fixed=['date']
        )

        if dlg.OK:
            pass
        else:
            core.quit()


if __name__ == "__main__":
    isub = InitSubject()
