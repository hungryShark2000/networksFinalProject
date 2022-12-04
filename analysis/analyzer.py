import csv
from operator import itemgetter
import networkx as nx
import sys
import numpy as np
import pandas as pd

np.set_printoptions(threshold=sys.maxsize)
from collections import Counter

# This part of networkx, for community detection, needs to be imported separately.
from networkx.algorithms import community


def analyze(node_f, edge_f, gephi_name, file_name, result_file):
    with open(node_f, 'r') as node_csv:  # Open the file
        nodeReader = csv.reader(node_csv)  # Read the csv
        # Retrieve the data, will produce list within list, e.g., [['Bash/Shell/PowerShell'], ['C']]
        node_lst = [n for n in nodeReader][1:]

    # Take nodes out of list, e.g., ['Bash/Shell/PowerShell', 'C']
    all_nodes = [n[0] for n in node_lst]

    with open(edge_f, 'r') as edge_csv:  # Open the file
        edgeReader = csv.reader(edge_csv)  # Read the csv
        edges = [tuple(e) for e in edgeReader][1:]  # Retrieve the data

    my_dict = {}
    for item in edges:
        if item[0] not in my_dict:
            my_dict[item[0]] = 1

        if item[1] not in my_dict:
            my_dict[item[1]] = 1

    curr_nodes = list(my_dict)

    G = nx.MultiDiGraph()
    G.add_nodes_from(all_nodes)
    G.add_edges_from(edges)

    # Uncomment this to download for Gephi
    nx.write_gexf(G, gephi_name)

    density_multiDi = nx.density(G)

    reciprocity = nx.reciprocity(G)

    width_dict = Counter(G.edges())
    edge_width = [(value, u, v) for ((u, v), value) in width_dict.items()]
    sorted_edges = sorted(edge_width, reverse=True)

    # need to first convert to DiGraph
    G2 = nx.DiGraph(G)
    density_Di = nx.density(G2)
    eigenvector_centrality_in_degree = nx.eigenvector_centrality(G2, max_iter=1000)
    eigenvector_centrality_out_degree = nx.eigenvector_centrality(G2.reverse(), max_iter=1000)
    eigenvector_centrality_in_sorted = sorted(eigenvector_centrality_in_degree.items(), key=itemgetter(1), reverse=True)
    eigenvector_centrality_out_sorted = sorted(eigenvector_centrality_out_degree.items(), key=itemgetter(1), reverse=True)

    # Uncomment this to download for Gephi
    gephi_name_2 = gephi_name[:-5] + '_Di.gexf'
    nx.write_gexf(G2, gephi_name_2)

    degree_dict_in = dict(G.degree(G.nodes()))
    nx.set_node_attributes(G, degree_dict_in, 'degree_in')
    degree_dict_in_sorted = sorted(degree_dict_in.items(), key=itemgetter(1), reverse=True)

    degree_dict_out = dict(G.out_degree(G.nodes()))
    nx.set_node_attributes(G, degree_dict_out, 'degree_out')
    degree_dict_out_sorted = sorted(degree_dict_out.items(), key=itemgetter(1), reverse=True)

    curr_node_lst = pd.Series(curr_nodes)
    density_lst = pd.Series([density_multiDi])
    reciprocity_lst = pd.Series([reciprocity])
    sorted_edges_lst = pd.Series(sorted_edges)
    density_di_lst = pd.Series([density_Di])
    eigenvector_centrality_in_lst = pd.Series(eigenvector_centrality_in_sorted)
    eigenvector_centrality_out_lst = pd.Series(eigenvector_centrality_out_sorted)
    degree_dict_in_sorted_lst = pd.Series(degree_dict_in_sorted)
    degree_dict_out_sorted_lst = pd.Series(degree_dict_out_sorted)

    df = pd.concat([curr_node_lst, density_lst, reciprocity_lst, sorted_edges_lst, density_di_lst, eigenvector_centrality_in_lst, eigenvector_centrality_out_lst, degree_dict_in_sorted_lst, degree_dict_out_sorted_lst], ignore_index=True, axis=1)
    df.columns = ['curr_nodes', 'density_multiDi', 'reciprocity', 'edge_count', 'density_Di', 'eigenvector_centrality_in', 'eigenvector_centrality_out', 'in_degree', 'out_degree']

    writer = pd.ExcelWriter(result_file, engine='openpyxl', mode='a')
    df.to_excel(writer, sheet_name=file_name, index=False)
    writer.save()


if __name__ == '__main__':
    edge_file_lst_2020 = [
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Country/2020/2020_survey_graph_data_india.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Country/2020/2020_survey_graph_data_uk.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Country/2020/2020_survey_graph_data_us.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Education/2020/2020_survey_graph_data_Bachelor.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Education/2020/2020_survey_graph_data_Graduate.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Education/2020/2020_survey_graph_data_Other.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Education/2020/2020_survey_graph_data_Second_Primary.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/MainBranch/2020/2020_survey_graph_data_other1.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/MainBranch/2020/2020_survey_graph_data_professional.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/MainBranch/2020/2020_survey_graph_data_student.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Year_of_code/2020/2020_survey_graph_data_1_5.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Year_of_code/2020/2020_survey_graph_data_6_10.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Year_of_code/2020/2020_survey_graph_data_11_15.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Year_of_code/2020/2020_survey_graph_data_16_20.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Year_of_code/2020/2020_survey_graph_data_21_30.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Year_of_code/2020/2020_survey_graph_data_31_up.csv'
    ]

    edge_file_lst_2022 = [
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Country/2022/2022_survey_graph_data_india.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Country/2022/2022_survey_graph_data_uk.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Country/2022/2022_survey_graph_data_us.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Education/2022/2022_survey_graph_data_Bachelor.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Education/2022/2022_survey_graph_data_Graduate.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Education/2022/2022_survey_graph_data_Other.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Education/2022/2022_survey_graph_data_Second_Primary.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/MainBranch/2022/2022_survey_graph_data_other1.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/MainBranch/2022/2022_survey_graph_data_professional.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/MainBranch/2022/2022_survey_graph_data_student.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Year_of_code/2022/2022_survey_graph_data_1_5.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Year_of_code/2022/2022_survey_graph_data_6_10.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Year_of_code/2022/2022_survey_graph_data_11_15.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Year_of_code/2022/2022_survey_graph_data_16_20.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Year_of_code/2022/2022_survey_graph_data_21_30.csv',
        '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/edges/Year_of_code/2022/2022_survey_graph_data_31_up.csv'
    ]

    file_name_lst = [
        'india',
        'uk',
        'us',
        'Bachelor',
        'Graduate',
        'Other',
        'Second_Primary',
        'other1',
        'professional',
        'student',
        '1_5',
        '6_10',
        '11_15',
        '16_20',
        '21_30',
        '31_up'
    ]

    gephi_name_lst = [
        'c_india',
        'c_uk',
        'c_us',
        'edu_Bachelor',
        'edu_Graduate',
        'edu_Other',
        'edu_Second_Primary',
        'mb_other1',
        'mb_professional',
        'mb_student',
        'yoc_1_5',
        'yoc_6_10',
        'yoc_11_15',
        'yoc_16_20',
        'yoc_21_30',
        'yoc_31_up'
    ]

    for i in range(16):
        node_f = '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/nodes/nodes2020.csv'
        edge_f = edge_file_lst_2020[i]
        # TODO: change 2020/2022
        gephi_name = '2020_' + gephi_name_lst[i] + '.gexf'
        file_name = file_name_lst[i]
        result_file = '/Users/vivanli/Desktop/preprocess_survey/networksFinalProject/2020_result_all.xlsx'
        analyze(node_f, edge_f, gephi_name, file_name, result_file)
