import networkx as nx
import matplotlib.pyplot as plt
import random

def generating_graphs(n_vertices, k):
    """
    Return the a graph with n_vertices vertices and a minimal 
    FVS of cardinality lesser or equal than k.

    Parameters:
    n_vertics (int): Number of vertices.
    k (int): Upper bound on the minimal FVS.

    Returns:
    list: A graph and an FVS of cardinality k.
    """
    if n_vertices <= k + 2:
        print("The input is not feasible")
        return []
    else:
        G = nx.erdos_renyi_graph(n = n_vertices, p = 0, directed = False)
        FVS = []
        nodes = list(G.nodes())

        while len(FVS) < k: 
            random_edge = random.sample(nodes, 2)
            if G.has_edge(random_edge[0], random_edge[1]) == False:
                G.add_edge(random_edge[0], random_edge[1])
            else:
                continue

            if nx.is_forest(G.subgraph([v for v in list(G.nodes) if v not in FVS])) == False:  
                FVS.append(random_edge[0])

        return [G, FVS]