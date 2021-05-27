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


class DS_Input():
    import pandas as pd
    def __init__(self, country: str = '',
                 title: str = '',
                 unique_key: str = '',
                 data: pd.DataFrame = None):
        self.__country = country
        self.__title = title
        self.__unique_key = unique_key
        if data is not None:
            self.__data = data.sort_values('date')

    def set_country(self, country: str) -> None:
        self.__country = country

    def set_title(self, title: str) -> None:
        self.__title = title

    def set_unique_key(self, unique_key: str) -> None:
        self.__unique_key = unique_key

    def set_data(self, data: pd.DataFrame) -> None:
        self.__data = data.sort_values('date')

    def get_country(self) -> str:
        return self.__country

    def get_title(self) -> str:
        return self.__title

    def get_unique_key(self) -> str:
        return self.__unique_key

    def get_data(self) -> pd.DataFrame:
        return self.__data

    def get_columns(self) -> list:
        return [c for c in self.__data]

    def copy(self):
        '''
        provides a deep copy of the object
        :return: a deep copy of the object
        '''
        return DS_Input(country=self.get_country(),
                        title=self.get_title(),
                        unique_key=self.get_unique_key(),
                        data=self.get_data())
