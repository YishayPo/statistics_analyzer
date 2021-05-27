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
from Gui.Graphical_GUI.GraphicalInterfaceFrame import *
from Gui.Graphical_GUI.Sizes import *
from tkinter import messagebox


class StatisticsAnalyzer_GUI:
    def __init__(self,
                 window_title: str = 'Statistics Analyzer for COVID-19'):
        self.__root_window = tk.Tk()
        self.__root_window.title(window_title)
        self.__root_window.geometry(newGeometry=f'{MAIN_WINDOW_SIZES["width"]}x{MAIN_WINDOW_SIZES["height"]}')
        self.__root_window.resizable(False, False)
        GuiDS.graphical_gui = GraphicalInterfaceFrame(master=self.__root_window)
        self.__gui_frame = GuiDS.graphical_gui.get_frame()
        self.__gui_frame.place(
            x=GUI_INTERFACE_SIZES['x'],
            y=GUI_INTERFACE_SIZES['y'],
            width=GUI_INTERFACE_SIZES['width'],
            height=GUI_INTERFACE_SIZES['height']
        )

    def run_graphical_interface(self) -> None:
        self.__root_window.mainloop()

    @staticmethod
    def show_message_box(text: str):
        messagebox.showinfo(text)


if __name__ == '__main__':
    gui = StatisticsAnalyzer_GUI()
    gui.run_graphical_interface()
