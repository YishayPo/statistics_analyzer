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

import os
from Src.ModulesImports import ModulesImports

modules_required = {"pillow", "Image", "pandas", 'numpy', 'Path', 'uuid', 'matplotlib', 'openpyxl',
                    "PyDrive", "google-auth", "google-api-python-client",
                    "google-api-core", "google-auth", "path",
                    "google-auth-httplib2", "google-auth-oauthlib", "xlrd",
                    "googleapis-common-protos", "oauthlib", "oauth2client", "uritemplate"}


##################################################################################
#                            StatisticsAnalyzer                                  #
#                              Main Function                                     #
##################################################################################

def first_run():
    directory_contents = [f for f in os.listdir(os.getcwd()) if f == 'sa']
    if len(directory_contents) == 0:
        modules_import = ModulesImports(modules_required)
        modules_import.install_list()


def statistics_analyzer():
    first_run()
    # Import Modules - after ModulesImports is run
    from Gui.StatisticsAnalyzer_gui import StatisticsAnalyzer_GUI
    from Src.DataStructures.BuildDS import BuildDs

    BuildDs.build_ds()
    gui = StatisticsAnalyzer_GUI()
    gui.run_graphical_interface()


####################################################
#                      Run                         #
####################################################
if __name__ == '__main__':
    statistics_analyzer()
