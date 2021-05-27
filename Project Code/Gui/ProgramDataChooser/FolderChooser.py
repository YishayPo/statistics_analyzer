##################################################################################
#                           Network workshop project                             #
#                                                                                #
# Authors: Nechama Weinberg, Yishay Polatov                                      #
#                                                                                #
# Description:                                                                   #
#                                                                                #
# Creation Date: 11/25/2020                                                      #
#                                                                                #
##################################################################################
import os
import tkinter as tk
from tkinter import filedialog


class FileChooser_GUI():
    @staticmethod
    def get_path_for_parent_folder() -> str:
        window = tk.Tk()
        path = filedialog.askdirectory(parent=window, initialdir=os.getcwd(),
                                       title='Choose where to store local copy of data and statistics')
        window.destroy()
        return path


if __name__ == '__main__':
    print(FileChooser_GUI.get_path_for_parent_folder())
