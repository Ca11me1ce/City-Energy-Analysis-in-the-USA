#######################
# Author: Dandan Wang
# NetID: dw862
# Function: analyze the relationship between energy consumption and greenhouse gas emission.
# ####################
import pandas as pd
import csv
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import community

def binData(myData, attr, newAttr, n_bin):
    # Create even spaced bins using min and max
    minNum = myData[attr].min() - 1
    maxNum = myData[attr].max() + 1
    step = (maxNum - minNum) / n_bin
    bins =  np.arange(minNum, maxNum + step, step)
    myData[newAttr] = np.digitize(myData[attr], bins)

def genNetwork():
    data = pd.read_csv("binned_residential.csv", sep=',', encoding='latin1')
    data['emission'] = data['gas_lb_ghg'] + data['elec_lb_ghg']
    binData(data, 'gas_mcf', 'consume_level', 50)
    binData(data, 'emission', 'emission_level', 50)
    newData = pd.DataFrame(data, columns = ['consume_level', 'emission_level'])
    gp = newData.groupby(['consume_level', 'emission_level'])
    newdf=gp.size()
    print(newdf[:10])
    newdf.to_csv("network.csv")

def buildGraph():
    # Build the graph
    G = nx.DiGraph()
    with open('network.csv', 'r') as f:
        for line in f:
            data = line.strip().split(',')
            source = int(data[0])
            target = int(data[1])
            weight = int(data[2])
            G.add_edge(source, target, weight=weight)
    return G

def netStats(G):
    # Prints summary information about the graph
    print(nx.info(G))

    # Print the degree of each node
    print("Node, Degree")
    for v in list(G):
        print('{}, {}'.format(v, G.degree[v]))

    # Compute and print stats of the full network
    nbr_nodes = len(G.nodes())
    nbr_edges = len(G.edges())
    print("Number of nodes in full network: ", nbr_nodes)
    print("Number of edges in full network: ", nbr_edges)

    # Change G to an undirected graph and find the numbers of CCs
    undirected_G = G.to_undirected()
    nbr_components = nx.number_connected_components(undirected_G)
    print("Number of connected components:", nbr_components)

    # Print the density of graph
    print("The density of nodes is: ", nx.density(G))
    # Print the number of triangles.
    dict_triangles = nx.triangles(undirected_G)
    sums = 0
    for i in dict_triangles:
        sums += dict_triangles[i]
    print("The number of triangles in graph is: ", sums / 3)

    # Compute degree centralities and then store the value with each node in the networkx graph
    centralities = nx.degree_centrality(G)
    values = [centralities[node] for node in list(G.nodes())]
#    nx.draw_spring(undirected_G, cmap = plt.get_cmap('jet'), node_color = values, node_size = 10, with_labels = False)
#    plt.show()
#    plt.savefig("degree.png")
    print("The averages for the centralities is: ", np.mean(values))

    # Print the length of largest connected component in the graph.
    print("The length of largest connected component in the graph: ", len(sorted(nx.connected_components(undirected_G), key = len, reverse = True)[0]))

def clustering(G):
    # Change subgraph to an undirected graph
#    undirected_G = G.to_undirected()
    # Conduct modularity clustering
    # Create an unweighted version of G because modularity works only on graphs with non-negative edge weights
#    unweighted_G = nx.Graph()
#    for u, v in undirected_G.edges():
#        unweighted_G.add_edge(u, v)
#    partition = community.best_partition(G)

    # Compute the clustering coefficient
    clus_coeff = nx.clustering(G)
    print("The clustering coefficient is: ", clus_coeff)

    # Print clusters (You will get a list of each node with the cluster you are in)
    print()
    print("Clusters")
#    print(partition)

    # Get the values for the clusters and select the node color based on the cluster value
    values = [clus_coeff.get(node) for node in G.nodes()]
    nx.draw_spring(G, cmap = plt.get_cmap('jet'), node_color = values, node_size=10, with_labels=False)
    #plt.show()
    plt.savefig("cluster.png")

    # Determine the final modularity value of the network
    # Change subgraph to an undirected graph
    undirected_G = G.to_undirected()
    # Conduct modularity clustering
    # Create an unweighted version of G because modularity works only on graphs with non-negative edge weights
    unweighted_G = nx.Graph()
    for u, v in undirected_G.edges():
        unweighted_G.add_edge(u, v)
    partition = community.best_partition(unweighted_G)

    modValue = community.modularity(partition, unweighted_G)
    print("modularity: {}".format(modValue))

if __name__ == "__main__":
    genNetwork()
    G = buildGraph()
    netStats(G)
    clustering(G)
