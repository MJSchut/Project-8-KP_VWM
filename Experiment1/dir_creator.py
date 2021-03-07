'''Check if directory exists, if not, create it'''
import os


def make_dir(this_dir):
    # You should change 'test' to your preferred folder.
    folder_to_check = os.path.isdir(this_dir)

    # If folder doesn't exist, then create it.
    if not folder_to_check:
        os.makedirs(this_dir)
        print("created folder : ", this_dir)

    else:
        print(this_dir, "folder already exists.")
