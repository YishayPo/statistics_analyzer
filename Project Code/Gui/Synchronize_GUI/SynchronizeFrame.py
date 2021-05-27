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
from Gui.GuiDataStructures import *
from Gui.StatisticsPresenter_GUI.StatisticsPresenterFrame import *
from Gui.Synchronize_GUI.Sizes import *
from Src.DataStructures.BuildDS import *


class SynchronizeFrame:
    def __init__(self, master=None):
        self.__synchronize_frame = tk.Frame(master=master, bg='gray')
        self.__add_refresh_button()
        self.__add_clone_button()
        self.__add_push_button()
        self.__add_pull_button()

    def get_frame(self) -> tk.Frame:
        return self.__synchronize_frame

    def __add_clone_button(self):
        image = Image.open("Resources\CloneButton.png")
        image = ImageTk.PhotoImage(image)
        clone_button = tk.Button(master=self.__synchronize_frame,
                                 bg='white',
                                 image=image,
                                 text='Clone',
                                 command=self.__clone)
        clone_button.image = image
        clone_button.place(
            x=CLONE_BUTTON['x'],
            y=CLONE_BUTTON['y'],
            width=CLONE_BUTTON['width'],
            height=CLONE_BUTTON['height']
        )

    def __add_push_button(self):
        image = Image.open("Resources\PushButton.png")
        image = ImageTk.PhotoImage(image)
        push_button = tk.Button(master=self.__synchronize_frame,
                                image=image,
                                bg='white',
                                text='Push',
                                command=self.__push)
        push_button.image = image
        push_button.place(
            x=PUSH_BUTTON['x'],
            y=PUSH_BUTTON['y'],
            width=PUSH_BUTTON['width'],
            height=PUSH_BUTTON['height']
        )

    def __add_pull_button(self):
        image = Image.open("Resources\PullButton.png")
        image = ImageTk.PhotoImage(image)
        pull_button = tk.Button(master=self.__synchronize_frame,
                                bg='white',
                                image=image,
                                text='Pull',
                                command=self.__pull)
        pull_button.image = image
        pull_button.place(
            x=PULL_BUTTON['x'],
            y=PULL_BUTTON['y'],
            width=PULL_BUTTON['width'],
            height=PULL_BUTTON['height']
        )

    def __add_refresh_button(self):
        image = Image.open("Resources\RefreshButton.png")
        image = ImageTk.PhotoImage(image)
        refresh_button = tk.Button(master=self.__synchronize_frame,
                                   bg='white',
                                   image=image,
                                   text='Refresh',
                                   command=self.__refresh)
        refresh_button.image = image
        refresh_button.place(
            x=REFRESH_BUTTON['x'],
            y=REFRESH_BUTTON['y'],
            width=REFRESH_BUTTON['width'],
            height=REFRESH_BUTTON['height']
        )

    def __refresh(self):
        BuildDs.rebuild_ds()
        GuiDS.statistics_presenter_gui.edit_country_drop_down_menu()
        messagebox.showinfo('Refresh Done Successfully', 'Data has been updated')

    def __clone(self):
        DS.shared_folder_manager.clone(destination_folder=DS.root_folder)
        messagebox.showinfo('Data Downloaded Successfully', 'Data has been downloaded and stored in local folder')

    def __push(self):
        DS.shared_folder_manager.push(local_user_folder=DS.root_folder)
        messagebox.showinfo('Data Uploaded Successfully', 'Data has been uploaded and stored in shared folder')

    def __pull(self):
        DS.shared_folder_manager.pull(destination_folder=DS.root_folder)
        messagebox.showinfo('Data Downloaded Successfully', 'Data has been downloaded and stored in local folder')


if __name__ == '__main__':
    root_window = tk.Tk()
    root_window.geometry(newGeometry=f'{int(SYNCHRONIZE_FRAME["width"])}x{int(SYNCHRONIZE_FRAME["height"])}')
    # root_window.resizable(False, False)
    gui = SynchronizeFrame(master=root_window).get_frame()
    gui.place(
        x=SYNCHRONIZE_FRAME['x'],
        y=SYNCHRONIZE_FRAME['y'],
        width=SYNCHRONIZE_FRAME['width'],
        height=SYNCHRONIZE_FRAME['height']
    )

    root_window.mainloop()
