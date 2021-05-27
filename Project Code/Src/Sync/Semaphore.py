import datetime
import operator
import time
import uuid

from Src.Communicate import Communicate as sac


class Semaphore():
    def __init__(self):
        self.__semaphore_name = 'Semaphore'
        self.__semaphore_id = '1C-9zI6MbUKGy-NXqDdYsKjhE9HZepV15'
        self.__user_id = str(uuid.uuid4())
        self.__file = 'NULL'
        self.__max_lock_time = 900  # 15 minute in seconds

    def lock(self):
        start_time = datetime.datetime.now()
        self.__file = sac.Communicate.create_file(self=sac.Communicate(),
                                                  parent_folder_id=self.__semaphore_id,
                                                  file_mimetype='text/txt',
                                                  file_name=self.__user_id,
                                                  file_content=self.__user_id)
        while True:
            first_file = self.get_first_created_file_name()
            cur_time = datetime.datetime.now()
            if str(first_file) == str(self.__file['title']):
                return True
            elif (cur_time - start_time).total_seconds() > self.__max_lock_time:
                first_file = self.get_first_created_file_name()
                first_file_id = sac.Communicate.get_file_id_by_name(self=sac.Communicate(), file_name=first_file,
                                                                    root_folder_name=self.__semaphore_name)
                sac.Communicate.delete_item(self=sac.Communicate(), item_id=first_file_id)
                first_file = self.get_first_created_file_name()
                if str(first_file) == str(self.__file['title']):
                    return True
                else:
                    return False
            else:
                time.sleep(10)  # Sleep for 10 seconds

    def unlock(self):
        sac.Communicate.delete_item(self=sac.Communicate(), item_id=self.__file['id'])
        return

    def get_first_created_file_name(self):
        files_data = {}  # {'uuid1': ['created_time'], 'uuid2': ['created_time']}
        files_list = sac.Communicate.list_files_in_drive_folder(self=sac.Communicate(),
                                                                parent_id=self.__semaphore_id)
        if bool(files_list):
            for file in files_list:
                file_datetime = sac.Communicate.retrieve_created_datetime(item=file)
                files_data[file['name']] = file_datetime

            files_data_sorted = dict(sorted(files_data.items(), key=operator.itemgetter(1), reverse=False))
            first_created_file = list(files_data_sorted.keys())[0]
        else:
            first_created_file = 'NULL'
        return first_created_file


if __name__ == '__main__':
    s = Semaphore()
    s.lock()
    s.unlock()
