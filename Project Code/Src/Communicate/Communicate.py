from __future__ import print_function

import csv
import io
import os
import pathlib
import pickle
from datetime import datetime, timedelta

import pandas as pd
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class Communicate():
    def __init__(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'
        self.__SCOPES = ['https://www.googleapis.com/auth/drive',
                         'https://www.googleapis.com/auth/drive.readonly'
                         'https://www.googleapis.com/auth/spreadsheets',
                         'https://www.googleapis.com/auth/spreadsheets.readonly',
                         'https://www.googleapis.com/auth/drive.file',
                         'https://www.googleapis.com/auth/drive.appdata']
        self.__SERVICE_ACCOUNT_FILE = os.path.join(os.getcwd(), 'statisticsanalyzer_key.json')
        self.__service = self.service_creation('drive', 'v3')
        self.__sheetsService = self.service_creation('sheets', 'v4')
        self.__drive = self.connect()
        self.__root_folder = '1I8weqrFj2PAqwaZ_s5PQOb6l7jWVqskQ'  # StatisticsAnalyzer Shared Folder in GoogleDrive

    def func(self):
        return

    # ---------------------------------------
    # Connect to google drive
    # ---------------------------------------
    def connect(self) -> GoogleDrive:
        try:
            gauth = GoogleAuth()
            gauth.LocalWebserverAuth()  # client_secrets.json need to be in the same directory as the script
            return GoogleDrive(gauth)
        except Exception as e:
            raise RuntimeError(e)

    # ---------------------------------------
    # Create service
    # ---------------------------------------
    def service_creation(self, service_name: str, version: str):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.__SCOPES)  # credentials.json download from drive API
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return build(service_name, version, credentials=creds)

    # ---------------------------------------
    # Create New Folder
    # ---------------------------------------
    def create_folder(self, parent_folder_id: str, folder_name: str) -> GoogleDrive:
        try:
            folder_metadata = {
                'parents': [{'id': parent_folder_id}],
                'title': folder_name,
                'mimeType': "application/vnd.google-apps.folder"}

            folder = self.__drive.CreateFile(folder_metadata)
            folder.Upload()
            print('Folder created and uploaded! Folder Name: %s, Folder ID: %s' % (folder['title'], folder['id']))
            return folder
        except Exception as e:
            raise RuntimeError(e)

    # ---------------------------------------
    # Create New File
    # ---------------------------------------
    def create_file(self, parent_folder_id: str, file_mimetype: str, file_name: str, file_content: str) -> GoogleDrive:
        try:
            print('Start creating file..')
            file_metadata = {
                'parents': [{'id': parent_folder_id}],
                'title': file_name,
                'mimeType': file_mimetype}
            file = self.__drive.CreateFile(file_metadata)
            file.SetContentString(file_content)
            file.Upload({'convert': True})
            print('File created and uploaded! File Name: %s, File ID: %s' % (file['title'], file['id']))
            return file
        except Exception as e:
            raise RuntimeError(e)

    # ---------------------------------------
    # Upload folder with all files to GoogleDrive
    # ---------------------------------------
    def upload_folder(self, local_source_path: str):
        try:
            folder_name = local_source_path.split(sep=os.path.sep)[-1]
            drive_folders = self.list_folders_in_drive_folder(parent_id=self.__root_folder)

            if folder_name in drive_folders:
                drive_parent_folder_id = self.get_folder_id_by_name(folder_name)
            else:
                folder = self.create_folder(parent_folder_id=self.__root_folder, folder_name=folder_name)
                drive_parent_folder_id = folder['id']

            local_directory_contents = os.listdir(local_source_path)
            for file in local_directory_contents:
                if file.endswith('.xlsx'):
                    file_name = pathlib.Path(file).stem
                    self.upload_excel(file_name=file_name,
                                      local_source_path=os.path.join(local_source_path, file),
                                      drive_folder_id=drive_parent_folder_id)
        except Exception as e:
            raise RuntimeError(e)

    # ---------------------------------------
    # Upload Excel File
    # ---------------------------------------
    def upload_excel(self, file_name, local_source_path, drive_folder_id: str):
        try:
            file_metadata = {'name': file_name,
                             'parents': [drive_folder_id],
                             'mimeType': 'application/vnd.google-apps.spreadsheet'}
            media = MediaFileUpload(local_source_path, mimetype='application/vnd.ms-excel')
            file = self.__service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print('Upload Success!')
            print('File ID:', file.get('id'))
            return file
        except Exception as e:
            raise RuntimeError(e)

    # ---------------------------------------
    # Download Excel File
    # ---------------------------------------
    def download_excel(self, spreadsheet_id, output_file_name: str, sheet_name: str, output_save_path: str):
        try:
            result = self.__sheetsService.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id, range='A1:AA1000').execute()
            if not os.path.exists(output_save_path):
                os.mkdir(output_save_path)
            output_file = os.path.join(output_save_path, f'{output_file_name}.csv')
            with open(output_file, 'w') as f:
                writer = csv.writer(f)
                writer.writerows(result.get('values'))
            f.close()
            read_file = pd.read_csv(output_file)
            read_file.to_excel(os.path.join(output_save_path, f'{output_file_name}.xlsx'),
                               sheet_name=sheet_name, index=None, header=True)
            os.remove(output_file)
            print(f'Successfully downloaded {output_file_name}.xlsx')
        except Exception as e:
            print(e)
            raise RuntimeError(e)

    # -------------------------------------------
    # Get folder id by name
    # ------------------------------------------
    def get_folder_id_by_name(self, folder_name: str):
        try:
            print('Folder name to search: %s' % (folder_name))
            folder_id = 'None'
            resource = self.__service.files()
            result = resource.list(pageSize=30, fields="files(id, name)").execute()
            file_list = result.get('files')
            for file in file_list:
                if file['name'] == folder_name:
                    print('Folder found: Name = %s, Id = %s' % (file['name'], file['id']))
                    folder_id = file['id']
                    return folder_id
            if folder_id != 'None':
                return folder_id
            else:
                print('Folder not found')
                exit(-1)
        except Exception as e:
            raise RuntimeError(e)

    # -------------------------------------------
    # Get file id by name
    # ------------------------------------------
    def get_file_id_by_name(self, file_name: str, root_folder_name: str):
        try:
            print('File name to search: %s\%s' % (root_folder_name, file_name))
            file_id = 'None'
            root_folder_id = self.get_folder_id_by_name(root_folder_name)
            file_list = self.list_files_in_drive_folder(root_folder_id)
            for file in file_list:
                if os.path.splitext(file['name'])[0] == file_name:
                    print('Item found: Name = %s, Id = %s' % (file['name'], file['id']))
                    file_id = file['id']
                    return file_id
            if file_id != 'None':
                return file_id
            else:
                print('Item not found')
                exit(-1)
        except Exception as e:
            raise RuntimeError(e)

    # ---------------------------------------
    # Delete GoogleDrive item
    # ---------------------------------------
    def delete_item(self, item_id: str):
        try:
            print('Going to delete item..')
            self.__service.files().delete(fileId=item_id).execute()
        except Exception as e:
            raise RuntimeError(e)

    # ---------------------------------------
    # List all Folders by parent folder id
    # ---------------------------------------
    def list_folders_in_drive_folder(self, parent_id: str):
        try:
            print('Listing all folders under parent folder: ')
            results = self.__service.files().list(
                q="mimeType='application/vnd.google-apps.folder' and parents in '" + parent_id + "' and trashed = false",
                fields="nextPageToken, files(id, name, modifiedTime, createdTime)", pageSize=30).execute()

            items = results.get('files', [])
            for item in items:
                print('name: {0} id:({1})'.format(item['name'], item['id']))
            print('Done listing!')
            return items
        except Exception as e:
            raise RuntimeError(e)

    # ---------------------------------------
    # List all files by parent folder id
    # ---------------------------------------
    def list_files_in_drive_folder(self, parent_id: str):
        try:
            print('Listing all files under parent folder: ')
            results = self.__service.files().list(
                q="parents in '" + parent_id + "' and trashed = false",
                fields="nextPageToken, files(id, name, modifiedTime, createdTime, mimeType)", pageSize=30).execute()

            items = results.get('files', [])
            for item in items:
                print('name: {0} id:({1})'.format(item['name'], item['id']))
            print('Done listing!')
            return items
        except Exception as e:
            raise RuntimeError(e)

    # ---------------------------------------
    # Download Folder
    # ---------------------------------------
    def download_drive_folder(self, drive_folder_id: str, destination_folder: str):
        results = self.__service.files().list(
            pageSize=30,
            q="parents in '{0}'".format(drive_folder_id),
            fields="files(id, name, mimeType)").execute()

        items = results.get('files', [])

        for item in items:
            itemName = item['name']
            itemId = item['id']
            itemType = item['mimeType']
            if itemType == 'application/vnd.google-apps.folder':
                filePath = destination_folder + '\\' + itemName
            else:
                filePath = destination_folder

            if itemType == 'application/vnd.google-apps.folder':
                print("Stepping into folder: {0}".format(filePath))
                self.download_drive_folder(itemId, filePath)  # Recursive call
            elif itemType.startswith('application/vnd.google-apps.spreadsheet'):
                self.download_excel(itemId, itemName, itemName, filePath)
            elif not itemType.startswith('application/'):
                self.download_file(itemId, filePath)
            else:
                print("Unsupported file: {0}".format(itemName))

    # ---------------------------------------
    # Download File
    # ---------------------------------------
    def download_file(self, fileId, filePath, filedstmimytype=''):
        # Note: The parent folders in filePath must exist
        print("-> Downloading file with id: {0} name: {1}".format(fileId, filePath))
        request = self.__service.files().export(fileId=fileId, mimeType=filedstmimytype)
        fh = io.FileIO(filePath, mode='wb')

        try:
            downloader = MediaIoBaseDownload(fh, request, chunksize=1024 * 1024)

            done = False
            while done is False:
                status, done = downloader.next_chunk(num_retries=2)
                if status:
                    print("Download %d%%." % int(status.progress() * 100))
            print("Download Complete!")
        finally:
            fh.close()

    # ---------------------------------------
    # Retrieve created datetime from folder or file
    # ---------------------------------------
    @staticmethod
    def retrieve_created_datetime(item):
        try:
            if not item:
                return ""
            else:
                item_created_datetime = item['createdTime']
                item_created_datetime = item_created_datetime.replace("Z", "")
                item_created_datetime = item_created_datetime.replace("T", " ")
                item_created_datetime = item_created_datetime[0: item_created_datetime.index(".")]
                item_created_datetime = datetime.strptime(item_created_datetime, "%Y-%m-%d %H:%M:%S")
                item_created_datetime = item_created_datetime + timedelta(hours=2)
                return item_created_datetime
        except Exception as e:
            raise RuntimeError(e)

    # ---------------------------------------
    # Retrieve modified datetime from folder or file
    # ---------------------------------------
    @staticmethod
    def retrieve_modified_datetime(item):
        try:
            if not item:
                return ""
            else:
                item_modified_datetime = item['modifiedTime']
                item_modified_datetime = item_modified_datetime.replace("Z", "")
                item_modified_datetime = item_modified_datetime.replace("T", " ")
                item_modified_datetime = item_modified_datetime[0: item_modified_datetime.index(".")]
                item_modified_datetime = datetime.strptime(item_modified_datetime, "%Y-%m-%d %H:%M:%S")
                item_modified_datetime = item_modified_datetime + timedelta(hours=2)
                return item_modified_datetime
        except Exception as e:
            raise RuntimeError(e)

    # ---------------------------------------
    # Move to trash
    # ---------------------------------------
    def move_to_trash(self, item):
        try:
            item.Trash()
        except Exception as e:
            raise RuntimeError(e)

    # ---------------------------------------
    # Move out of trash
    # ---------------------------------------
    def move_out_of_trash(self, item):
        try:
            item.UnTrash()
        except Exception as e:
            raise RuntimeError(e)
