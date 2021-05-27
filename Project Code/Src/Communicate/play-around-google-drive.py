import datetime

from Src.Communicate.Communicate import *


def test1():
    print('starting upload')
    folder = Communicate.create_folder(Communicate(), '189ExmXs6CH9u1fgVf-Lrq8osHO94cnvz',
                                       datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S"))
    Communicate.upload_item(Communicate(), folder['id'])


def test2():
    # ROOT_DIR = os.path.abspath(os.pardir)
    # print(ROOT_DIR)
    d1 = datetime.date.now().strftime("%d/%m/%Y")
    d2 = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    listFolders = Communicate.list_folders_and_files(Communicate(), '189ExmXs6CH9u1fgVf-Lrq8osHO94cnvz')
    # Communicate.upload_item(Communicate(), '189ExmXs6CH9u1fgVf-Lrq8osHO94cnvz')
    folder = Communicate.create_folder(Communicate(), '189ExmXs6CH9u1fgVf-Lrq8osHO94cnvz', d2)
    print('folder id is:', folder['id'])
    file = Communicate.create_file(Communicate(), folder['id'], 'text/csv', d1 + '.csv',
                                   'hello, world, I, am, first, file!')
    file = Communicate.create_file(Communicate(), folder['id'], 'text/txt', d1 + '.txt', 'hello world I am first file!')
    print('file id is: ', file['id'])
    Communicate.retrieve_created_datetime(Communicate(), file)
    # Communicate.delete_file(Communicate(), file)
    # Communicate.delete_folder(Communicate(), folder)


def test3():
    # Communicate.list_folders_and_files_in_drive_folder(Communicate(), '189ExmXs6CH9u1fgVf-Lrq8osHO94cnvz')
    folder = Communicate.create_folder(Communicate(), parent_folder_id='1I8weqrFj2PAqwaZ_s5PQOb6l7jWVqskQ',
                                       folder_name='StatisticsIsrael-11-18-2020')

    excelfile1 = Communicate.upload_excel(Communicate(), 'IsraelCases',
                                          "C:\local_SA_GoogleDriveData\StatisticsIsrael\IsraelCases.xlsx", folder['id'])
    excelfile2 = Communicate.upload_excel(Communicate(), 'IsraelDeaths',
                                          "C:\local_SA_GoogleDriveData\StatisticsIsrael\IsraelDeaths.xlsx",
                                          folder['id'])
    # excelfile3 = Communicate.upload_excel(Communicate(), 'IsraelReports', "C:\local_SA_GoogleDriveData\StatisticsIsrael\IsraelReports.xlsx", folder['id'])
    # excelfile4 = Communicate.upload_excel(Communicate(), 'IsraelCities', "C:\local_SA_GoogleDriveData\StatisticsIsrael\IsraelCities.xlsx", folder['id'])
    #
    Communicate.download_excel(Communicate(), excelfile1['id'], 'IsraelCases', 'Cases',
                               'C:\local_SA_GoogleDriveData\DOWNLOADED')
    Communicate.download_excel(Communicate(), excelfile1['id'], 'IsraelDeaths', 'Deaths',
                               'C:\local_SA_GoogleDriveData\DOWNLOADED')


# Communicate.download_excel(Communicate(), excelfile1['id'], 'IsraelReports', 'Reports', 'C:\local_SA_GoogleDriveData\DOWNLOADED')
# Communicate.download_excel(Communicate(), excelfile1['id'], 'IsraelCities', 'Cities', 'C:\local_SA_GoogleDriveData\DOWNLOADED')

# Communicate.downloadFolder(Communicate(), '189ExmXs6CH9u1fgVf-Lrq8osHO94cnvz', "C:\local_SA_GoogleDriveData")
# Communicate.downloadFile(Communicate(), excelfile['id'], 'isrealstat', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

def test4():
    # Communicate.list_folders_and_files_in_drive_folder(Communicate(), '13cpeqI6mWm24elK3UCdfJhoRsKCOVxZv')
    item_id = Communicate.get_folder_id_by_name(Communicate(), 'StatisticsAnalyzerSharedFolder')
    print(item_id)
    Communicate.download_folder(Communicate(), item_id, 'C:\local_SA_GoogleDriveData')


def test5():
    folder = Communicate.create_folder(Communicate(), parent_folder_id='1I8weqrFj2PAqwaZ_s5PQOb6l7jWVqskQ',
                                       folder_name='TestPull1')
    Communicate.upload_excel(Communicate(), 'IsraelCases',
                             "C:\Git projects\SA_Files\Israel\Deaths.xlsx", folder['id'])
    # Communicate.list_folders_in_drive_folder(Communicate(), '1I8weqrFj2PAqwaZ_s5PQOb6l7jWVqskQ')
    # print('list files inside folder')
    # Communicate.list_files_in_drive_folder(Communicate(), '1tYRKAPS9HTSDMbpwIppigut-r-iWvC21')


def test6():
    list_folders = Communicate.list_folders_in_drive_folder(Communicate(), '1I8weqrFj2PAqwaZ_s5PQOb6l7jWVqskQ')
    for folder in list_folders:
        cur_folder = Communicate.get_folder_id_by_name(Communicate(), folder['name'])
        Communicate.delete_folder(Communicate(), cur_folder)


def test7():
    Communicate.upload_excel(Communicate(), local_source_path="C:\\Git projects\\SA_FilesTest\\Greece")
    # Communicate.upload_folder(Communicate(), local_source_path="C:\\Git projects\\SA_Files\\Israel")
    # Communicate.upload_folder(Communicate(), local_source_path="C:\\Git projects\\SA_Files\\USA")


if __name__ == '__main__':
    # test3()
    test5()
    # test6()
    # test1()
    # test2()
