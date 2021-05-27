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

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from Src.FilesManipulation.DS_Input import DS_Input


class Graph_GUI:
    def __init__(self, data: DS_Input):
        self.__ds_input = data
        self.__data_df = self.__ds_input.get_data()

    def show_graph(self):
        plt.style.use('seaborn-darkgrid')
        pelette = plt.get_cmap('Set1')
        color_num = 0
        for column in self.__data_df.drop(labels=self.__ds_input.get_unique_key(), axis=1):
            color_num += 1
            plt.plot(self.__data_df[self.__ds_input.get_unique_key()],
                     self.__data_df[column],
                     marker='',
                     color=pelette(color_num),
                     linewidth=2,
                     alpha=0.9,
                     label=column)
        plt.legend(loc=2, ncol=2)

        plt.title(f'{self.__ds_input.get_country()} - {self.__ds_input.get_title()}')
        plt.xlabel(self.__ds_input.get_unique_key())
        plt.ylabel(self.__ds_input.get_title())

        plt.show()


def test1():
    file_name = '../../InputFiles/StatisticsIsrael.xlsx'
    file = ReadInput(file_name=file_name, country='Israel')

    # pprint(file.get_sheets_names())
    file_ds_inputs = file.build_input_ds(sheets=file.get_sheets_names())
    for ds_input in file_ds_inputs:
        print('ds_input\'s country: ', ds_input.get_country())
        print('ds_input\'s title: ', ds_input.get_title())
        print('ds_input\'s unique key: ', ds_input.get_unique_key())
        print(ds_input.get_data())
        graph = Graph_GUI(data=ds_input)
        graph.show_graph()
        # t = threading.Thread(target=graph.show_graph)
        # t.start()


def test2():
    # Make a data frame
    df = pd.DataFrame({'x': range(1, 11), 'y1': np.random.randn(10), 'y2': np.random.randn(10) + range(1, 11),
                       'y3': np.random.randn(10) + range(11, 21), 'y4': np.random.randn(10) + range(6, 16),
                       'y5': np.random.randn(10) + range(4, 14) + (0, 0, 0, 0, 0, 0, 0, -3, -8, -6),
                       'y6': np.random.randn(10) + range(2, 12), 'y7': np.random.randn(10) + range(5, 15),
                       'y8': np.random.randn(10) + range(4, 14), 'y9': np.random.randn(10) + range(4, 14),
                       'y10': np.random.randn(10) + range(2, 12)})

    print(df)
    # style
    plt.style.use('seaborn-darkgrid')

    # create a color palette
    palette = plt.get_cmap('Set1')

    # multiple line plot
    num = 0
    for column in df.drop('x', axis=1):
        num += 1
        plt.plot(df['x'], df[column], marker='', color=palette(num), linewidth=1, alpha=0.9, label=column)

    # Add legend
    plt.legend(loc=2, ncol=2)

    # Add titles
    plt.title("A (bad) Spaghetti plot", loc='left', fontsize=12, fontweight=0, color='orange')
    plt.xlabel("Time")
    plt.ylabel("Score")
    plt.show()


if __name__ == '__main__':
    test1()
