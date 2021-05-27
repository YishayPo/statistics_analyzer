from Gui.Graphical_GUI.Sizes import *

CLONE_BUTTON = {
    'x': 0 + 5,
    'y': 0 + 5,
    'width': (SYNCHRONIZE_FRAME['width'] / 2) - 10,
    'height': (SYNCHRONIZE_FRAME['height'] / 2) - 10
}

PULL_BUTTON = {
    'x': 0 + 5,
    'y': CLONE_BUTTON['y'] + CLONE_BUTTON['height'] + 5,
    'width': (SYNCHRONIZE_FRAME['width'] / 2) - 10,
    'height': (SYNCHRONIZE_FRAME['height'] / 2) - 10
}

REFRESH_BUTTON = {
    'x': CLONE_BUTTON['x'] + CLONE_BUTTON['width'] + 10,
    'y': 0 + 5,
    'width': (SYNCHRONIZE_FRAME['width'] / 2) - 10,
    'height': (SYNCHRONIZE_FRAME['height'] / 2) - 10
}

PUSH_BUTTON = {
    'x': CLONE_BUTTON['x'] + CLONE_BUTTON['width'] + 10,
    'y': CLONE_BUTTON['y'] + CLONE_BUTTON['height'] + 5,
    'width': (SYNCHRONIZE_FRAME['width'] / 2) - 10,
    'height': (SYNCHRONIZE_FRAME['height'] / 2) - 10
}
