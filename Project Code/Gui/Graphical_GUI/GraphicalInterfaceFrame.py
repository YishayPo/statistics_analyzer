##################################################################################
#                           Network workshop project                             #
#                                                                                #
# Authors: Nechama Weinberg, Yishay Polatov                                      #
#                                                                                #
# Description:                                                                   #
#                                                                                #
# Creation Date: 11/18/2020                                                      #
#                                                                                #
##################################################################################
import tkinter as tk

from Gui.Graphical_GUI.Sizes import *
from Gui.GuiDataStructures import *
from Gui.StatisticsPresenter_GUI.StatisticsPresenterFrame import StatisticsPresenterFrame
from Gui.Synchronize_GUI.SynchronizeFrame import SynchronizeFrame


class GraphicalInterfaceFrame:
    def __init__(self, master=None, **kw):
        self.__gui_interface = tk.Frame(master=master, **kw)
        self.__add_present_statistics_frame()
        # self.__add_add_data_frame()
        self.__add_synchronize_frame()

    def get_frame(self) -> tk.Frame:
        return self.__gui_interface

    def __add_synchronize_frame(self):
        GuiDS.synchronize_gui = SynchronizeFrame(master=self.__gui_interface)
        self.__synchronize_frame = GuiDS.synchronize_gui.get_frame()
        self.__synchronize_frame.place(
            x=SYNCHRONIZE_FRAME['x'],
            y=SYNCHRONIZE_FRAME['y'],
            width=SYNCHRONIZE_FRAME['width'],
            height=SYNCHRONIZE_FRAME['height']
        )

    def __add_present_statistics_frame(self):
        GuiDS.statistics_presenter_gui = StatisticsPresenterFrame(master=self.__gui_interface)
        self.__statistic_presenter_frame = GuiDS.statistics_presenter_gui.get_frame()
        self.__statistic_presenter_frame.place(
            x=STATISTICS_PRESENTET_FRAME['x'],
            y=STATISTICS_PRESENTET_FRAME['y'],
            width=STATISTICS_PRESENTET_FRAME['width'],
            height=STATISTICS_PRESENTET_FRAME['height']
        )


if __name__ == '__main__':
    root_window = tk.Tk()
    root_window.geometry(newGeometry=f'{GUI_INTERFACE_SIZES["width"]}x{GUI_INTERFACE_SIZES["height"]}')
    root_window.resizable(False, False)
    gui = GraphicalInterfaceFrame(master=root_window).get_frame()
    gui.place(
        x=GUI_INTERFACE_SIZES['x'],
        y=GUI_INTERFACE_SIZES['y'],
        width=GUI_INTERFACE_SIZES['width'],
        height=GUI_INTERFACE_SIZES['height']
    )

    root_window.mainloop()
