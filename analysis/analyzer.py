import csv
from operator import itemgetter
from statistics import mean

import networkx as nx
from collections import Counter
from scipy.stats import kendalltau

def prepList(node_f1, edge_f1):
    with open(node_f1, 'r') as node_csv:  # Open the file
        nodeReader = csv.reader(node_csv)  # Read the csv
        # Retrieve the data, will produce list within list, e.g., [['Bash/Shell/PowerShell'], ['C']]
        nodes = [n for n in nodeReader][1:]

    # Take nodes out of list, e.g., ['Bash/Shell/PowerShell', 'C']
    node_names = [n[0] for n in nodes]

    with open(edge_f1, 'r') as edge_csv:  # Open the file
        edgeReader = csv.reader(edge_csv)  # Read the csv
        edges = [tuple(e) for e in edgeReader][1:]  # Retrieve the data

    # create dummy graph
    Ggg = nx.MultiDiGraph()
    Ggg.add_nodes_from(node_names)
    Ggg.add_edges_from(edges)

    # Normalize
    width_dict = Counter(Ggg.edges())
    edge_width = [(u, v, value) for ((u, v), value) in width_dict.items()]
    n = 2  # N. . .
    nums = [x[n] for x in edge_width]
    average = mean(nums)
    # print(average)
    normalizedEdges = []
    for i in edge_width:
        if i[2] > average:
            tuple1 = (i[0], i[1], i[2] - average)
            for j in range(int(tuple1[2])):
                normalizedEdges.append((i[0], i[1]))

    # create real graph
    G = nx.MultiDiGraph()
    G.add_nodes_from(node_names)
    G.add_edges_from(normalizedEdges)

    degree_dict_in = dict(G.degree(G.nodes()))
    nx.set_node_attributes(G, degree_dict_in, 'degree_in')
    degree_dict_in_sorted = sorted(degree_dict_in.items(), key=itemgetter(1), reverse=True)

    return degree_dict_in_sorted
def prepStats(node_f1, edge_f1, node_f2, edge_f2):
    l1= prepList(node_f1, edge_f1)
    l2= prepList(node_f2, edge_f2)
    createSecondListAndTau(l1, l2)

def createDegreeList(degree_sorted):
    nodess=[]
    i = 1;
    for d in degree_sorted[:]:
        tuple1 = (i, d[0])
        i = i + 1
        nodess.append(tuple1)

    return nodess

def createSecondListAndTau(degree_sorted, degree_sorted_2):
    list1 = createDegreeList(degree_sorted)

    X = []
    for ll in list1:
        X.append(ll[0])

    Y = []


    for l in list1:
        i = 1;
        for m in degree_sorted_2:
            if (m[0] == l[1]):
                Y.append(i)
            i = i + 1
    print(X)
    print(Y)
    # corr, _ = kendalltau(X, Y)
    # print(corr);

def analyze(node_f, edge_f, results):
    #create new csv file
    f = open('../results/'+results, 'w')

    # create the csv writer
    writer = csv.writer(f)

    with open(node_f, 'r') as node_csv:  # Open the file
        nodeReader = csv.reader(node_csv)  # Read the csv
        # Retrieve the data, will produce list within list, e.g., [['Bash/Shell/PowerShell'], ['C']]
        nodes = [n for n in nodeReader][1:]

    # Take nodes out of list, e.g., ['Bash/Shell/PowerShell', 'C']
    node_names = [n[0] for n in nodes]

    with open(edge_f, 'r') as edge_csv:  # Open the file
        edgeReader = csv.reader(edge_csv)  # Read the csv
        edges = [tuple(e) for e in edgeReader][1:]  # Retrieve the data

    #create dummy graph
    Ggg = nx.MultiDiGraph()
    Ggg.add_nodes_from(node_names)
    Ggg.add_edges_from(edges)

    #Normalize
    width_dict = Counter(Ggg.edges())
    edge_width = [(u, v, value) for ((u, v), value) in width_dict.items()]
    n = 2  # N. . .
    nums = [x[n] for x in edge_width]
    average = mean(nums)
    # print(average)
    normalizedEdges = []
    for i in edge_width:
        if i[2] > average:
            tuple1 = (i[0], i[1], i[2]-average)
            for j in range(int(tuple1[2])):
                normalizedEdges.append((i[0], i[1]))

    #create real graph
    G = nx.MultiDiGraph()
    G.add_nodes_from(node_names)
    G.add_edges_from(normalizedEdges)

    degree_dict_in = dict(G.degree(G.nodes()))
    nx.set_node_attributes(G, degree_dict_in, 'degree_in')
    degree_dict_in_sorted = sorted(degree_dict_in.items(), key=itemgetter(1), reverse=True)

    # In degree
    #print("\nNodes by in degree:")
    writer.writerow("Nodes by in degree:")
    for d in degree_dict_in_sorted[:]:
        writer.writerow(d)
        #print(d)


    degree_dict_out = dict(G.out_degree(G.nodes()))
    nx.set_node_attributes(G, degree_dict_out, 'degree_out')
    degree_dict_out_sorted = sorted(degree_dict_out.items(), key=itemgetter(1), reverse=True)

    # Out degree
    #print("\nNodes by out degree: ")
    writer.writerow("Nodes by out degree:")
    for d in degree_dict_out_sorted[:]:
        writer.writerow(d)
        #print(d)

    # need to first convert to DiGraph
    G2 = nx.DiGraph(G)
    eigenvector_centrality = nx.eigenvector_centrality(G2, max_iter=1000)
    nx.set_node_attributes(G, eigenvector_centrality, 'degree_centrality')
    eigenvector_centrality_sorted = sorted(eigenvector_centrality.items(), key=itemgetter(1), reverse=True)

    #DiGraph density
    density = [nx.density(G2)]
    writer.writerow("Network density")
    writer.writerow(density)
    #print("Network density: ", density)
    # eigenvector centrality

    #Eigen centrality
    writer.writerow("Nodes by eigenvector centrality")
    writer.writerow(density)
    #print("\nNodes by eigenvector centrality:")
    for d in eigenvector_centrality_sorted[:]:
        writer.writerow(d)
        #print(d)

    #reciprocity
    reciprocity = [nx.reciprocity(G)]
    writer.writerow("Reciprocity")
    writer.writerow(reciprocity)
    #print("\nGraph reciprocity: ", reciprocity)

    #sorted edges
    width_dict = Counter(G.edges())
    edge_width = [(u, v, value) for ((u, v), value) in width_dict.items()]
    sorted_by_third = sorted(edge_width, key=lambda tup: tup[2], reverse=True)
    writer.writerow("Weighted edges")
    #print("weighted edges")
    for d in sorted_by_third:
        writer.writerow(d)
        #print(d)

    f.close()

if __name__ == '__main__':
    node_16 = '../nodes/nodes2016.csv'
    node_18 = '../nodes/nodes2018.csv'
    edge_f = '../edges/2018/education/byEducationSomeCollege.csv'
    #prepStats(node_16, node_16, '../edges/2016/country/byCountryUS.csv', '../edges/2016/country/byCountryUS.csv')
    #analyze(node_16, "../edges/2016.csv", '2016.csv')
    analyze(node_18, "../edges/2018.csv", '2018.csv')
    prepList(node_18, "../edges/2018.csv")
    prepStats(node_18, "../edges/2018/country/byCountryIndia.csv", node_18, '../edges/2018/country/byCountryUS.csv')
    #2016
    # analyze(node_16, '../edges/2016/country/byCountryIndia.csv', '2016/countryIndia.csv')
    # analyze(node_16, '../edges/2016/country/byCountryUS.csv', '2016/countryUS.csv')
    # analyze(node_16, '../edges/2016/country/byCountryUK.csv', '2016/countryUK.csv')
    # analyze(node_16, '../edges/2016/education/byEducationOther.csv', '2016/educationOther.csv')
    # analyze(node_16, '../edges/2016/education/byEducationCollege.csv', '2016/educationCollege.csv')
    # analyze(node_16, '../edges/2016/education/byEducationGraduate.csv', '2016/educationGraduate.csv')
    # analyze(node_16, '../edges/2016/profession/byProfOther.csv', '2016/profOther.csv')
    # analyze(node_16, '../edges/2016/profession/byProfStudent.csv', '2016/profStudent.csv')
    # analyze(node_16, '../edges/2016/profession/byProfFull.csv', '2016/profFull.csv')
    # analyze(node_16, '../edges/2016/time/byTime0-5.csv', '2016/time0-5.csv')
    # analyze(node_16, '../edges/2016/time/byTime6-10.csv', '2016/time6-10.csv')
    # analyze(node_16, '../edges/2016/time/byTime11-15.csv', '2016/time11-15.csv')
    #
    # #2018
    # analyze(node_18, '../edges/2018/country/byCountryIndia.csv', '2018/countryIndia.csv')
    # analyze(node_18, '../edges/2018/country/byCountryUS.csv', '2018/countryUS.csv')
    # analyze(node_18, '../edges/2018/country/byCountryUK.csv', '2018/countryUK.csv')
    # analyze(node_18, '../edges/2018/education/byEducationOther.csv', '2018/educationOther.csv')
    # analyze(node_18, '../edges/2018/education/byEducationCollege.csv', '2018/educationCollege.csv')
    # analyze(node_18, '../edges/2018/education/byEducationGraduate.csv', '2018/educationGraduate.csv')
    # analyze(node_18, '../edges/2018/profession/byProfPart.csv', '2018/profPart.csv')
    # analyze(node_18, '../edges/2018/profession/byProfStudent.csv', '2018/profStudent.csv')
    # analyze(node_18, '../edges/2018/profession/byProfFull.csv', '2018/profFull.csv')
    # analyze(node_18, '../edges/2018/time/byTime0-5.csv', '2018/time0-5.csv')
    # analyze(node_18, '../edges/2018/time/byTime6-10.csv', '2018/time6-10-5.csv')
    # analyze(node_18, '../edges/2018/time/byTime10-15.csv', '2018/time11-15.csv')
    # analyze(node_18, '../edges/2018/time/byTime15-20.csv', '2018/time15-20.csv')
    # analyze(node_18, '../edges/2018/time/byTime20-30.csv', '2018/time20-30.csv')
    # analyze(node_18, '../edges/2018/time/byTime30+.csv', '2018/time30+.csv')

