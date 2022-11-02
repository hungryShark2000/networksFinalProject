import csv
from operator import itemgetter
import networkx as nx

# This part of networkx, for community detection, needs to be imported separately.
from networkx.algorithms import community


def analyze(node_f, edge_f):
    with open(node_f, 'r') as node_csv:  # Open the file
        nodeReader = csv.reader(node_csv)  # Read the csv
        # Retrieve the data, will produce list within list, e.g., [['Bash/Shell/PowerShell'], ['C']]
        nodes = [n for n in nodeReader][1:]

    # Take nodes out of list, e.g., ['Bash/Shell/PowerShell', 'C']
    node_names = [n[0] for n in nodes]

    with open(edge_f, 'r') as edge_csv:  # Open the file
        edgeReader = csv.reader(edge_csv)  # Read the csv
        edges = [tuple(e) for e in edgeReader][1:]  # Retrieve the data

    G = nx.MultiDiGraph()
    G.add_nodes_from(node_names)
    G.add_edges_from(edges)

    # Uncomment this to download for Gephi
    # nx.write_gexf(G, "2022_uk.gexf")

    # Density
    density = nx.density(G)
    print("Network density: ", density)

    # # Total degree
    # degree_dict = dict(G.degree(G.nodes()))
    # nx.set_node_attributes(G, degree_dict, 'degree')
    # sorted_degree = sorted(degree_dict.items(), key=itemgetter(1), reverse=True)
    #
    # print("Nodes by degree: ")
    # for d in sorted_degree[:]:
    #     print(d)

    degree_dict_in = dict(G.degree(G.nodes()))
    nx.set_node_attributes(G, degree_dict_in, 'degree_in')
    degree_dict_in_sorted = sorted(degree_dict_in.items(), key=itemgetter(1), reverse=True)

    # In degree
    print("\nNodes by in degree:")
    for d in degree_dict_in_sorted[:]:
        print(d)

    degree_dict_out = dict(G.out_degree(G.nodes()))
    nx.set_node_attributes(G, degree_dict_out, 'degree_out')
    degree_dict_out_sorted = sorted(degree_dict_out.items(), key=itemgetter(1), reverse=True)

    # Out degree
    print("\nNodes by out degree: ")
    for d in degree_dict_out_sorted[:]:
        print(d)

    # need to first convert to DiGraph
    G2 = nx.DiGraph(G)
    eigenvector_centrality = nx.eigenvector_centrality(G2, max_iter=1000)
    nx.set_node_attributes(G, eigenvector_centrality, 'degree_centrality')
    eigenvector_centrality_sorted = sorted(eigenvector_centrality.items(), key=itemgetter(1), reverse=True)

    # eigenvector centrality
    print("\nNodes by eigenvector centrality:")
    for d in eigenvector_centrality_sorted[:]:
        print(d)

    reciprocity = nx.reciprocity(G)
    print("\nGraph reciprocity: ", reciprocity)


if __name__ == '__main__':
    node_f = '../nodes/nodes2022.csv'
    edge_f = '../edges/2022/2022_survey_graph_data_uk.csv'
    analyze(node_f, edge_f)
