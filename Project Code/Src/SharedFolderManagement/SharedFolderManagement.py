import os
import pathlib
import shutil
from datetime import datetime
from os.path import isfile, join

from path import Path

from Src.FilesManipulation.CompareExcelFiles import *
from Src.Sync.Semaphore import *
from Gui.StatisticsAnalyzer_gui import *


class SharedFolderManagement():

    def __init__(self):
        self.__drive_root_folder_id = '1I8weqrFj2PAqwaZ_s5PQOb6l7jWVqskQ'

    # ------------------------------------------------------------------------------
    # Clone - download google drive shared folder to local folder
    # ------------------------------------------------------------------------------
    def clone(self, destination_folder: str):
        try:
            if not os.path.exists(destination_folder):
                msg = "Going to create local shared folder: %s" % (destination_folder)
                pathlib.Path(destination_folder).mkdir(parents=True, exist_ok=True)
            msg = "Going to download google drive shared folder..."
            sac.Communicate.download_drive_folder(self=sac.Communicate(),
                                                  drive_folder_id=self.__drive_root_folder_id,
                                                  destination_folder=destination_folder)
            msg = "Done download google drive shared folder to local folder: %s ..." % (destination_folder)
        except Exception as e:
            raise RuntimeError(e)

    # ------------------------------------------------------------------------------
    # Pull - update local folder to same as in google drive shared folder
    # ------------------------------------------------------------------------------
    def pull(self, destination_folder: str):
        try:
            list_folders = sac.Communicate.list_folders_in_drive_folder(
                self=sac.Communicate(), parent_id=self.__drive_root_folder_id)
            for folder in list_folders:
                current_folder = os.path.join(destination_folder, folder['name'])
                msg = "Current folder in loop: %s" % (folder['name'])
                if os.path.exists(current_folder):
                    msg = "Folder: %s exists in local: " % (folder['name'])
                    list_files = sac.Communicate.list_files_in_drive_folder(
                        self=sac.Communicate(), parent_id=folder['id'])
                    for file in list_files:
                        current_file = os.path.join(current_folder, file['name'] + '.xlsx')
                        msg = "Current file in loop: %s, local file path: %s" % (file['name'], current_file)
                        if os.path.exists(current_file):
                            msg = "File exists in local! going to check modified time and date"
                            drive_file_modified_datetime = sac.Communicate.retrieve_modified_datetime(item=file)
                            local_file_creation_datetime = time.ctime(os.path.getctime(os.path.join(current_file)))
                            local_file_creation_datetime = datetime.datetime.strptime(local_file_creation_datetime,
                                                                             "%a %b %d %H:%M:%S %Y")
                            msg = "drive modified time: %s" % (drive_file_modified_datetime)
                            msg = "local creation time: %s" % (local_file_creation_datetime)

                            if drive_file_modified_datetime > local_file_creation_datetime:
                                msg = "File %s in drive is modified." \
                                      " Need to update local folder." \
                                      " Going to download file from drive ..." % (current_file)
                                sac.Communicate.download_excel(
                                    self=sac.Communicate(),
                                    spreadsheet_id=file['id'],
                                    output_file_name=file['name'],
                                    sheet_name=file['name'],
                                    output_save_path=current_folder)
                        else:
                            msg = "file %s not exist. Going to download.." % (file['name'])
                            sac.Communicate.download_excel(
                                self=sac.Communicate(),
                                spreadsheet_id=file['id'],
                                output_file_name=file['name'],
                                sheet_name=file['name'],
                                output_save_path=current_folder)

                else:
                    msg = "Folder %s not exist in local. Going to to download.." % (folder['name'])
                    sac.Communicate.download_drive_folder(
                        self=sac.Communicate(),
                        drive_folder_id=folder['id'],
                        destination_folder=os.path.join(destination_folder, folder['name']))
        except Exception as e:
            raise RuntimeError(e)

    # ------------------------------------------------------------------------------
    # Merge - merge changes from local folder to files in google drive shared folder
    # ------------------------------------------------------------------------------
    def merge(self, local_temp_folder: str, local_user_folder: str):
        try:
            list_folders = Path(local_user_folder).dirs()
            for folder in list_folders:
                current_user_folder = folder
                current_user_folder_name = current_user_folder.split(sep=os.path.sep)[-1]
                msg = "Current local user folder in loop: %s" % (current_user_folder)
                if os.path.exists(os.path.join(local_temp_folder, current_user_folder.split(sep=os.path.sep)[
                    -1])):  # if folder exists in both locals
                    current_temp_folder = os.path.join(local_temp_folder,
                                                       current_user_folder.split(sep=os.path.sep)[-1])
                    msg = "Folder: %s exists in GoogleDrive (local temp folder): " % (current_temp_folder)
                    list_files = [f for f in os.listdir(folder) if isfile(join(folder, f))]
                    for file in list_files:
                        current_user_file = os.path.join(current_user_folder, file)
                        msg = "Current local user file in loop: %s" % (file)
                        if os.path.exists(os.path.join(current_temp_folder, file)):
                            current_temp_file = os.path.join(current_temp_folder, file)
                            msg = "File exists in GoogleDrive (temp local)! going to check if modified"
                            compare_excel_files(current_user_file, current_temp_file)
                            file_name = current_user_file.split(sep=os.path.sep)[-1][:-5]
                            file_id = sac.Communicate.get_file_id_by_name(self=sac.Communicate(),
                                                                          file_name=file_name,
                                                                          root_folder_name=current_user_folder_name)
                            drive_folder_id = sac.Communicate.get_folder_id_by_name(self=sac.Communicate(),
                                                                                    folder_name=current_user_folder_name)
                            sac.Communicate.delete_item(self=sac.Communicate(), item_id=file_id)
                            sac.Communicate.upload_excel(self=sac.Communicate(),
                                                         file_name=file_name,
                                                         local_source_path=current_user_file,
                                                         drive_folder_id=drive_folder_id)

                        else:
                            drive_folder_id = sac.Communicate.get_folder_id_by_name(self=sac.Communicate(),
                                                                                    folder_name=current_user_folder_name)
                            solve_contradict(filename=current_user_file)
                            sac.Communicate.upload_excel(self=sac.Communicate(),
                                                         file_name=current_user_file.split(sep=os.path.sep)[-1][:-5],
                                                         local_source_path=current_user_file,
                                                         drive_folder_id=drive_folder_id)
                else:
                    msg = "Folder %s not exist in GoogleDrive. Going to upload folder.." % (folder)
                    sac.Communicate.upload_folder(self=sac.Communicate(), local_source_path=folder)
        except Exception as e:
            raise RuntimeError(e)

    # ------------------------------------------------------------------------------
    # Push - push the changes in local folder to google drive shared folder
    # ------------------------------------------------------------------------------
    def push(self, local_user_folder: str, destination_local_temp_folder="C:\\StatisticsAnalyzerSharedFolder\\Temp"):
        semaphore = Semaphore()
        try:
            if semaphore.lock():
                msg = "Going to clone temp local shared folder: %s" % (destination_local_temp_folder)
                if not os.path.exists(destination_local_temp_folder):
                    msg = "Going to create local shared folder: %s" % (destination_local_temp_folder)
                    pathlib.Path(destination_local_temp_folder).mkdir(parents=True, exist_ok=True)
                else:
                    msg = "Local shared folder: %s exists. Deleting folder content.." % (destination_local_temp_folder)
                    if not destination_local_temp_folder:  # folder is not empty
                        shutil.rmtree(destination_local_temp_folder)
                self.clone(destination_folder=destination_local_temp_folder)
                self.merge(local_temp_folder=destination_local_temp_folder, local_user_folder=local_user_folder)
            else:
                msg = "Google drive is not available... "
                StatisticsAnalyzer_GUI.show_message_box(msg)
        except Exception as e:
            raise RuntimeError(e)
        finally:
            semaphore.unlock()
            if os.path.exists("C:\\StatisticsAnalyzerSharedFolder"):
                shutil.rmtree("C:\\StatisticsAnalyzerSharedFolder")


if __name__ == '__main__':
    sfm1 = SharedFolderManagement()
    # sfm1.clone("C:\\Git projects\\SA_Files")
    # to test: upload manual a file to DG
    sac.Communicate.upload_excel(self=sac.Communicate(), file_name='Reports',
                                 local_source_path="C:\\Git projects\\SA_Files\\Israel\\Reports.xlsx",
                                 drive_folder_id=sac.Communicate.get_folder_id_by_name(self=sac.Communicate(),
                                                                                       folder_name="Vienna"))
    sfm1.pull("C:\\Git projects\\SA_Files")
    # to test: manual add folder\file to local cloned drive
    sfm1.push("C:\\Git projects\\SA_Files")
