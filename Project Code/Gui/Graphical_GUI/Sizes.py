from Gui.Sizes import *

GUI_INTERFACE_SIZES = {
    'x': DISPLAY_SIZES['x'],
    'y': DISPLAY_SIZES['y'],
    'width': DISPLAY_SIZES['width'],
    'height': DISPLAY_SIZES['height'],
}

SYNCHRONIZE_FRAME = {
    'x': 0,
    'y': 0,
    'width': GUI_INTERFACE_SIZES['width'],
    'height': (GUI_INTERFACE_SIZES['height'] / 2) - 5
}

ADD_DATA_FRAME = {
    'x': GUI_INTERFACE_SIZES['x'],
    'y': SYNCHRONIZE_FRAME['y'] + SYNCHRONIZE_FRAME['height'],
    'width': GUI_INTERFACE_SIZES['width'],
    'height': GUI_INTERFACE_SIZES['height'] / 3
}

STATISTICS_PRESENTET_FRAME = {
    'x': GUI_INTERFACE_SIZES['x'],
    'y': SYNCHRONIZE_FRAME['y'] + SYNCHRONIZE_FRAME['height'] + 5,
    'width': GUI_INTERFACE_SIZES['width'],
    'height': GUI_INTERFACE_SIZES['height'] / 2
}
