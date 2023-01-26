# Import required libraries
from scipy.stats import kendalltau
import csv
import math
from operator import itemgetter
import networkx as nx
import sys
import numpy as np
import pandas as pd
np.set_printoptions(threshold=sys.maxsize)


def K_t(data_f, sheet, cols):
    df_2016 = pd.read_excel(data_f, sheet_name=sheet, usecols=cols[0])
    df_2018 = pd.read_excel(data_f, sheet_name=sheet, usecols=cols[1])
    df_2020 = pd.read_excel(data_f, sheet_name=sheet, usecols=cols[2])
    df_2022 = pd.read_excel(data_f, sheet_name=sheet, usecols=cols[3])

    my_dict = {}
    for item in df_2016.iloc[:, 0]:
        if item not in my_dict:
            my_dict[item] = 0
    for item in df_2018.iloc[:, 0]:
        if item not in my_dict:
            my_dict[item] = 0
    for item in df_2020.iloc[:, 0]:
        if item not in my_dict:
            my_dict[item] = 0
    for item in df_2022.iloc[:, 0]:
        if item not in my_dict:
            my_dict[item] = 0

    array_2016 = my_dict.copy()
    array_2018 = my_dict.copy()
    array_2020 = my_dict.copy()
    array_2022 = my_dict.copy()
    i = 1
    for item in df_2016.iloc[:, 0]:
        array_2016[item] = i
        i += 1

    i = 1
    for item in df_2018.iloc[:, 0]:
        array_2018[item] = i
        i += 1

    i = 1
    for item in df_2020.iloc[:, 0]:
        array_2020[item] = i
        i += 1

    i = 1
    for item in df_2022.iloc[:, 0]:
        array_2022[item] = i
        i += 1

    rank_2016 = list(array_2016.values())
    rank_2018 = list(array_2018.values())
    rank_2020 = list(array_2020.values())
    rank_2022 = list(array_2022.values())

    # Calculating Kendall Rank correlation
    print(sheet, " ", cols[0])
    corr, _ = kendalltau(rank_2016, rank_2018)
    print('2016-2018: %.4f' % corr)
    corr2, _ = kendalltau(rank_2018, rank_2020)
    print('2018-2020: %.4f' % corr2)
    corr3, _ = kendalltau(rank_2020, rank_2022)
    print('2020-2022: %.4f' % corr3)


if __name__ == '__main__':
    file = '../tmp-2.xlsx'
    sheet_list = ["India", "US", "UK", "other", "student", "prof"]
    cols_in = ["A", "B", "C", "D"]
    cols_out = ["G", "H", "I", "J"]
    cols_edge = ["M", "N", "O", "P"]

    sheet_list2 = ["16_20", "21_30", "31_up"]
    cols_in2 = ["A", "B", "C"]
    cols_out2 = ["G", "H", "I"]
    cols_edge2 = ["M", "N", "O"]

    for sheet in sheet_list:
        K_t(file, sheet, cols_in)
        K_t(file, sheet, cols_out)
        K_t(file, sheet, cols_edge)