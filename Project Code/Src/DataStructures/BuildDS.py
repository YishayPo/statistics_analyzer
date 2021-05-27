##################################################################################
#                           Network workshop project                             #
#                                                                                #
# Authors: Nechama Weinberg, Yishay Polatov                                      #
#                                                                                #
# Description:                                                                   #
#                                                                                #
# Creation Date: 11/26/2020                                                      #
#                                                                                #
##################################################################################
from Gui.ProgramDataChooser.FolderChooser import *
from Src.DataStructures.DataStructures import *


class BuildDs:
    @staticmethod
    def build_ds():
        DS.root_folder = BuildDs.get_root_folder_path()
        DS.shared_folder_manager = SharedFolderManagement()
        BuildDs.build_ds_inputs()

    @staticmethod
    def rebuild_ds():
        BuildDs.build_ds_inputs()

    @staticmethod
    def get_root_folder_path() -> str:
        # check if cfg file exists
        cwd = os.getcwd()
        directory_contents = os.listdir(cwd)
        directory_contents = [f for f in directory_contents if f == 'sa']
        if not len(directory_contents) == 0:
            with open('sa', 'r', encoding='utf-8') as f:
                path = f.read()
                if os.path.isdir(path):
                    return path
        # if not get the file path and create cfg file named sa.sa
        path = FileChooser_GUI.get_path_for_parent_folder()
        # time.sleep(5)
        if path == '':
            raise ValueError('You must choose a directory')
        with open('sa', 'w+') as f:
            f.write(path)
            # make the file hidden
        os.system('attrib +h sa')
        os.chdir(cwd)
        return path

    @staticmethod
    def change_root_folder_path() -> str:
        path = FileChooser_GUI.get_path_for_parent_folder()
        if path == '':
            raise ValueError('You must choose a directory')
        with open('sa', 'w+') as f:
            f.write(path)
            DS.root_folder = path
            return path

    @staticmethod
    def build_ds_inputs():
        directory_contents = [d for d in os.listdir(DS.root_folder) if os.path.isdir(DS.root_folder + '\\' + d)]
        DS.countries_list = [d.split(sep='\\')[-1] for d in directory_contents]

        remove_keys = [d for d in DS.country_files if d not in DS.countries_list]
        for d in remove_keys:
            del DS.country_files[d]

        for d in directory_contents:
            DS.country_files[d.split(sep='\\')[-1]] = [f.split(sep='\\')[-1] for f in
                                                       os.listdir(DS.root_folder + '\\' + d) if f.endswith('.xlsx')]
        DS.countries_list = list(set(DS.countries_list))

        for d in DS.country_files.keys():
            for f in DS.country_files[d]:
                ds_input_key = d + f
                excel_file = pd.ExcelFile(DS.root_folder + '\\' + d + '\\' + f)
                sheet = excel_file.sheet_names[0]
                df = pd.read_excel(excel_file, sheet_name=sheet)
                DS.ds_inputs[ds_input_key] = DS_Input(country=d, title=f, unique_key='date', data=df)
