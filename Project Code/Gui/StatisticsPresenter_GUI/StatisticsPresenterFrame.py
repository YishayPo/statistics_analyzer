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
from collections import defaultdict
from tkinter import messagebox

from PIL import Image, ImageTk

from Gui.StatisticsPresenter_GUI.Graph import Graph_GUI
from Gui.StatisticsPresenter_GUI.Sizes import *
from Src.DataStructures.DataStructures import DS


class StatisticsPresenterFrame:
    def __init__(self, master=None):
        self.__statistics_presenter_frame = tk.Frame(master=master, bg='gray')

        self.__add_present_button()
        self.__add_choose_country_label()
        self.__add_choose_country_drop_down_menu()
        self.__add_choose_file_label()
        self.__add_choose_file_drop_down_menu()

    def get_frame(self) -> tk.Frame:
        return self.__statistics_presenter_frame

    def __add_present_button(self):
        image = Image.open("Resources\PresentStatistics.png")
        image = ImageTk.PhotoImage(image)
        self.__present_button = tk.Button(master=self.__statistics_presenter_frame,
                                          image=image,
                                          command=self.__present_statistics)
        self.__present_button.image = image
        self.__present_button.place(
            x=PRESRNT_STATISTICS_BUTTON['x'],
            y=PRESRNT_STATISTICS_BUTTON['y'],
            width=PRESRNT_STATISTICS_BUTTON['width'],
            height=PRESRNT_STATISTICS_BUTTON['height']
        )

    def __add_choose_country_label(self):
        self.__choose_country_label = tk.Label(master=self.__statistics_presenter_frame,
                                               bg='black',
                                               fg='white',
                                               text='Choose what country to show')
        self.__choose_country_label.place(
            x=CHOOSE_COUNTRY_LABEL['x'],
            y=CHOOSE_COUNTRY_LABEL['y'],
            width=CHOOSE_COUNTRY_LABEL['width'],
            height=CHOOSE_COUNTRY_LABEL['height']
        )

    def __add_choose_country_drop_down_menu(self):
        countries_list = DS.countries_list
        if len(countries_list) == 0:
            countries_list.append('No Countries')
        self.__choose_country_var = tk.StringVar(self.__statistics_presenter_frame)
        self.__choose_country_var.set('Choose Country')
        self.__choose_country_menu = tk.OptionMenu(self.__statistics_presenter_frame,
                                                   self.__choose_country_var,
                                                   *countries_list,
                                                   command=lambda c=self.__choose_country_var.get():
                                                   self.__edit_file_drop_down_menu(c))
        self.__choose_country_menu.place(
            x=CHOOSE_COUNTRY_DROP_DOWN_MENU['x'],
            y=CHOOSE_COUNTRY_DROP_DOWN_MENU['y'],
            width=CHOOSE_COUNTRY_DROP_DOWN_MENU['width'],
            height=CHOOSE_COUNTRY_DROP_DOWN_MENU['height']
        )

    def __add_choose_file_label(self):
        self.__choose_file_label = tk.Label(master=self.__statistics_presenter_frame,
                                            bg='black',
                                            fg='white',
                                            text='Choose what file to show')
        self.__choose_file_label.place(
            x=CHOOSE_FILE_LABEL['x'],
            y=CHOOSE_FILE_LABEL['y'],
            width=CHOOSE_FILE_LABEL['width'],
            height=CHOOSE_FILE_LABEL['height']
        )

    def __add_choose_file_drop_down_menu(self):
        file_dict = defaultdict(lambda: ['No country has been chosen'], DS.country_files)
        files_list = file_dict[self.__choose_country_var.get()]
        self.__choose_file_var = tk.StringVar(self.__statistics_presenter_frame)
        self.__choose_file_var.set('Choose File')
        self.__choose_file_menu = tk.OptionMenu(self.__statistics_presenter_frame,
                                                self.__choose_file_var,
                                                *files_list)
        self.__choose_file_menu.place(
            x=CHOOSE_FILE_DROP_DOWN_MENU['x'],
            y=CHOOSE_FILE_DROP_DOWN_MENU['y'],
            width=CHOOSE_FILE_DROP_DOWN_MENU['width'],
            height=CHOOSE_FILE_DROP_DOWN_MENU['height']
        )

    def __edit_file_drop_down_menu(self, country: str):
        # tk._setit(self.__choose_country_menu, country)
        if country != 'No Countries':
            # Reset var and delete all old options
            self.__choose_file_var.set('Choose file')
            self.__choose_file_menu['menu'].delete(0, 'end')

            # Insert list of new options (tk._setit hooks them up to var)
            file_dict = defaultdict(lambda: ['No country has been chosen'], DS.country_files)
            new_files_list = file_dict[country]
            for file in new_files_list:
                self.__choose_file_menu['menu'].add_command(label=file, command=tk._setit(self.__choose_file_var, file))

    def edit_country_drop_down_menu(self):
        self.__choose_country_menu.place_forget()
        countries_list = DS.countries_list
        if len(countries_list) == 0:
            countries_list.append('No Countries')
        self.__choose_country_var = tk.StringVar(self.__statistics_presenter_frame)
        self.__choose_country_var.set('Choose Country')
        self.__choose_country_menu = tk.OptionMenu(self.__statistics_presenter_frame,
                                                   self.__choose_country_var,
                                                   *countries_list,
                                                   command=lambda c=self.__choose_country_var.get():
                                                   self.__edit_file_drop_down_menu(c))
        self.__choose_country_menu.place(
            x=CHOOSE_COUNTRY_DROP_DOWN_MENU['x'],
            y=CHOOSE_COUNTRY_DROP_DOWN_MENU['y'],
            width=CHOOSE_COUNTRY_DROP_DOWN_MENU['width'],
            height=CHOOSE_COUNTRY_DROP_DOWN_MENU['height']
        )

    """
    def edit_country_drop_down_menu(self):
        # Reset var and delete all old options
        self.__choose_country_var.set('Choose Country')
        self.__choose_country_menu['menu'].delete(0, 'end')

        # Insert list of new options (tk._setit hooks them up to var)
        new_countries_list = DS.countries_list
        for c in new_countries_list:
            if c != 'No Countries':
                self.__choose_country_menu['menu'].add_command(label=c, command=tk._setit(self.__choose_country_var, c))
        self.__choose_country_menu.configure(command=lambda c=self.__choose_country_var.get():self.__edit_file_drop_down_menu(c))
    """

    def __present_statistics(self):
        country = self.__choose_country_var.get()
        file = self.__choose_file_var.get()
        ds_input = DS.get_ds_input(country, file)
        if ds_input is not None:
            Graph_GUI(data=ds_input).show_graph()
        else:
            messagebox.showerror('ERROR', 'Can\'t display graph for the given values')


def show_present_statistics_window():
    root_window = tk.Tk()
    root_window.geometry(
        newGeometry=f'{int(STATISTICS_PRESENTET_FRAME["width"])}x{int(STATISTICS_PRESENTET_FRAME["height"])}')
    root_window.resizable(False, False)
    gui = StatisticsPresenterFrame(master=root_window).get_frame()
    gui.place(
        x=STATISTICS_PRESENTET_FRAME['x'],
        y=STATISTICS_PRESENTET_FRAME['y'],
        width=STATISTICS_PRESENTET_FRAME['width'],
        height=STATISTICS_PRESENTET_FRAME['height']
    )

    root_window.mainloop()


if __name__ == '__main__':
    show_present_statistics_window()
