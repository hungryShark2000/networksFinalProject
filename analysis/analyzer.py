import csv
from operator import itemgetter
import networkx as nx

# This part of networkx, for community detection, needs to be imported separately.
from networkx.algorithms import community


def analyze(nodes, edges):
    with open(nodes, 'r') as nodecsv:  # Open the file
        nodereader = csv.reader(nodecsv)  # Read the csv
        # Retrieve the data (using Python list comprhension and list slicing to remove the header row, see footnote 3)
        nodes = [n for n in nodereader][1:]

    node_names = [n[0] for n in nodes]  # Get a list of only the node names

    with open(edges, 'r') as edgecsv:  # Open the file
        edgereader = csv.reader(edgecsv)  # Read the csv
        edges = [tuple(e) for e in edgereader][1:]  # Retrieve the data

    G = nx.MultiDiGraph()
    G.add_nodes_from(node_names)
    G.add_edges_from(edges)

    # Density
    density = nx.density(G)
    print("Network density:", density)

    # Total degree
    degree_dict = dict(G.degree(G.nodes()))
    nx.set_node_attributes(G, degree_dict, 'degree')
    sorted_degree = sorted(degree_dict.items(), key=itemgetter(1), reverse=True)

    print("\nNodes by degree:")
    for d in sorted_degree[:]:
        print(d)

    degree_dict_in = dict(G.in_degree(G.nodes()))
    nx.set_node_attributes(G, degree_dict_in, 'degree_in')
    sorted_degree = sorted(degree_dict_in.items(), key=itemgetter(1), reverse=True)

    # In degree
    print("\nNodes by in degree:")
    for d in sorted_degree[:]:
        print(d)

    degree_dict_out = dict(G.out_degree(G.nodes()))
    nx.set_node_attributes(G, degree_dict_out, 'degree_in')
    sorted_degree = sorted(degree_dict_out.items(), key=itemgetter(1), reverse=True)

    # In degree
    print("\nNodes by out degree:")
    for d in sorted_degree[:]:
        print(d)


if __name__ == '__main__':
    node_f = '../nodes/nodes2016.csv'
    edge_f = '../edges/byCountryUS.csv'
    analyze(node_f, edge_f)
