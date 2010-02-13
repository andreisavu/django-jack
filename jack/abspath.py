
import os

def abspath(*args):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_dir, *args)


