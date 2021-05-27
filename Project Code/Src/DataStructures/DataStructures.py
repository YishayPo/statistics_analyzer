##################################################################################
#                           Network workshop project                             #
#                                                                                #
# Authors: Nechama Weinberg, Yishay Polatov                                      #
#                                                                                #
# Description:                                                                   #
#                                                                                #
# Creation Date: 10/01/2020                                                      #
#                                                                                #
##################################################################################

from Src.FilesManipulation.DS_Input import DS_Input
from Src.SharedFolderManagement.SharedFolderManagement import *


class DS:
    root_folder = ''
    shared_folder_manager = SharedFolderManagement()
    countries_list = []
    country_files = {}
    ds_inputs = {}

    @staticmethod
    def get_ds_input(country: str, file: str) -> DS_Input:
        ds_input_key = country + file
        if ds_input_key in DS.ds_inputs.keys():
            return DS.ds_inputs[ds_input_key]
        else:
            return None
